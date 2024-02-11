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
st.set_page_config(page_title="Know about person...", page_icon="🚹")

# streamlit framework
st.title('Know about person...')
input_text = st.text_input("Name a famous person")

# Gemini LLMS
google_api_key = os.getenv("Google_Gemini_AI_API")  # Google API Key
llm = GoogleGenerativeAI(temperature=0.8, google_api_key=google_api_key, model="gemini-pro")  # Initialize the Gemini LLM

# First Prompt Templates
first_input_prompt = PromptTemplate(
    input_variables=['name'],
    template="Tell me about the life and achievements of {name}"
)

# Chain of LLMs
chain = LLMChain(
    llm=llm,
    prompt=first_input_prompt,
    verbose=True,
    output_key='person'
)

# Second Prompt Templates
second_input_prompt = PromptTemplate(
    input_variables=['person'],
    template="when and where was {person} born? give only date and place"
)

# Chain of LLMs
chain2 = LLMChain(
    llm=llm, prompt=second_input_prompt, verbose=True, output_key='dob'
)

# Third Prompt Templates
third_input_prompt = PromptTemplate(
    input_variables=['person'],
    template="Describe the early life and upbringing of the person born on {person}"
)

chain3 = LLMChain(llm=llm, prompt=third_input_prompt, verbose=True, output_key='early_life')

# Fourth Prompt Templates
fourth_input_prompt = PromptTemplate(
    input_variables=['early_life'],
    template="Share interesting anecdotes or lesser-known facts about the person's early life: {early_life}"
)

# Chain of LLMs
chain4 = LLMChain(
    llm=llm, prompt=fourth_input_prompt, verbose=True, output_key='interesting_facts'
)

# Fifth Prompt Templates
fifth_input_prompt = PromptTemplate(
    input_variables=['person'],
    template="Write a fictional interview with {person}. What questions would you ask? How would they respond?"
)

# Chain of LLMs
chain5 = LLMChain(
    llm=llm, prompt=fifth_input_prompt, verbose=True, output_key='interview'
)


# Sixth Prompt Templates
sixth_input_prompt = PromptTemplate(
    input_variables=['interview'],
    template="Write a fictional newspaper headline about an event involving {name}"
)

# Chain of LLMs
chain6 = LLMChain(
    llm=llm, prompt=sixth_input_prompt, verbose=True, output_key='headline'
)

# Seventh Prompt Templates
seventh_input_prompt = PromptTemplate(
    input_variables=['headline'],
    template="Create a short poem or song lyrics inspired by the life and legacy of {name}"
)

# Chain of LLMs
chain7 = LLMChain(
    llm=llm, prompt=seventh_input_prompt, verbose=True, output_key='poem'
)

# Update parent chain to include chain4 and chain5
parent_chain = SequentialChain(
    chains=[chain, chain2, chain3, chain4, chain5, chain6, chain7],
    input_variables=['name'],
    output_variables=['person', 'dob', 'early_life', 'interesting_facts', 'interview', 'headline', 'poem'],
    verbose=True
)

if input_text:
    result = parent_chain({'name': input_text})

    with st.expander("Name"):
        st.write(result['name'])

    with st.expander("Life and Achievements"):
        st.write(result['person'])

    with st.expander("Birth Details"):
        st.write(result['dob'])

    with st.expander("Early Life"):
        st.write(result['early_life'])

    with st.expander("Interesting Facts"):
        st.write(result['interesting_facts'])

    with st.expander("Imagined Interview"):
        st.write(result['interview'])

    with st.expander("Fictional Headline"):
        st.write(result['headline'])

    with st.expander("Poem or Lyrics"):
        st.write(result['poem'])

    st.write('Data Fetched Successfully')
