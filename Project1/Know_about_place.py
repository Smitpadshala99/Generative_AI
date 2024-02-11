# Import the required modules
from langchain_google_genai import GoogleGenerativeAI  # Use to access the Google Generative AI
from langchain import PromptTemplate  # Use to create a prompt template
from langchain.chains import LLMChain  # Use to create a chain of LLMs
from langchain.chains import SequentialChain  # Use to create a chain (Sequential) of LLMs
import streamlit as st  # Use to create the web app
import os
import dotenv

dotenv.load_dotenv()

# the icon and the title of the web app
st.set_page_config(page_title="Know about the place...", page_icon="🏰")

# streamlit framework
st.title('Know about the place...')
input_text = st.text_input("Name a famous place")

# Gemini LLMS
google_api_key = os.getenv("Google_Gemini_AI_API")  # Google API Key
llm = GoogleGenerativeAI(temperature=0.8, google_api_key=google_api_key, model="gemini-pro")  # Initialize the Gemini LLM

# First Prompt Templates
first_input_prompt = PromptTemplate(
    input_variables=['place'],
    template="Tell me about the place called {place}"
)

# Chain of LLMs
chain = LLMChain(
    llm=llm,
    prompt=first_input_prompt,
    verbose=True,
    output_key='about_place'
)

# Second Prompt Templates
second_input_prompt = PromptTemplate(
    input_variables=['about_place'],
    template="Why is {place} famous?"
)

# Chain of LLMs
chain2 = LLMChain(
    llm=llm, prompt=second_input_prompt, verbose=True, output_key='famous_reason'
)

# Third Prompt Templates
third_input_prompt = PromptTemplate(
    input_variables=['famous_reason'],
    template="What are some of the nearest famous places to {place}?"
)

chain3 = LLMChain(llm=llm, prompt=third_input_prompt, verbose=True, output_key='nearest_places')

# Fourth Prompt Templates
fourth_input_prompt = PromptTemplate(
    input_variables=['nearest_places'],
    template="Tell me about the history of {place}"
)

# Chain of LLMs
chain4 = LLMChain(
    llm=llm, prompt=fourth_input_prompt, verbose=True, output_key='history'
)

# Fifth Prompt Templates
fifth_input_prompt = PromptTemplate(
    input_variables=['history'],
    template="Can you provide a summary of {place}?"
)

# Chain of LLMs
chain5 = LLMChain(
    llm=llm, prompt=fifth_input_prompt, verbose=True, output_key='summary'
)

# Sixth Prompt Templates
sixth_input_prompt = PromptTemplate(
    input_variables=['summary'],
    template="Imagine you are a tour guide. Write a compelling description to attract visitors to {place}"
)

# Chain of LLMs
chain6 = LLMChain(
    llm=llm, prompt=sixth_input_prompt, verbose=True, output_key='tour_description'
)

# Seventh Prompt Templates
seventh_input_prompt = PromptTemplate(
    input_variables=['tour_description'],
    template="Create a short story or a piece of prose inspired by the beauty of {place}"
)

# Chain of LLMs
chain7 = LLMChain(
    llm=llm, prompt=seventh_input_prompt, verbose=True, output_key='story'
)

# Update parent chain to include all chains
parent_chain = SequentialChain(
    chains=[chain, chain2, chain3, chain4, chain5, chain6, chain7],
    input_variables=['place'],
    output_variables=['about_place', 'famous_reason', 'nearest_places', 'history', 'summary', 'tour_description', 'story'],
    verbose=True
)

if input_text:
    result = parent_chain({'place': input_text})

    with st.expander("About the Place"):
        st.write(result['about_place'])

    with st.expander("Why is it Famous?"):
        st.write(result['famous_reason'])

    with st.expander("Nearest Famous Places"):
        st.write(result['nearest_places'])

    with st.expander("History"):
        st.write(result['history'])

    with st.expander("Summary"):
        st.write(result['summary'])

    with st.expander("Tour Description"):
        st.write(result['tour_description'])

    with st.expander("story or Prose"):
        st.write(result['story'])

    st.write('Data Fetched Successfully')
