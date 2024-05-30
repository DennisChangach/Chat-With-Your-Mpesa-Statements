from langchain.prompts import PromptTemplate
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_openai import OpenAI
#from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from src.components.few_shots import few_shots
from src.components.prompts import in_context_prompt,generate_feedback_prompt,generate_exmp_qns_prompt
from dotenv import load_dotenv
import streamlit as st
import os
import uvicorn

# Load environment variables
load_dotenv()

#Configuring Langsmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Load the LLM - Gemini Pro
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0,convert_system_message_to_human=True)

#Loading openai models: GPT 3.5
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
#gpt3_5_llm = ChatOpenAI(temperature=0, openai_api_key= OPENAI_API_KEY,model_name = "gpt-3.5-turbo-0125")

#Initilializing the output parser
output_parser = StrOutputParser()

llm = gemini_llm
#Function for using in prompt context
def get_in_context_reponse(input_question):
    #getting the few shot examples
    examples = str(few_shots)
    
    my_prompt = in_context_prompt
  
    #Defining the prompt template
    prompt = PromptTemplate(input_variables=['question','examples'],template=my_prompt)

    #Defining the prompt template
    prompt = PromptTemplate(input_variables=['question','examples'],
                            template=my_prompt,
                            )
    #Defining the LLM Chain
    chain=prompt|llm

    response = chain.invoke({'question':input_question,'examples':examples})

    #st.markdown(response)
    
    return response.content


#Function to get feedback based on the results
def get_generated_results_explantion(question,results,code):
    #Selecting the llm
  
    my_prompt = generate_feedback_prompt

    #Defining the prompt template
    prompt = PromptTemplate(input_variables=['question','results','code'],template=my_prompt)

    
    #Defining chain with new format
    chain=prompt|llm

    response = chain.invoke({'question':question,
                         'results':results,
                         'code':code,
                            })
                       
    #st.write(response)

    return response.content

#Function to get example questions
def get_example_qns(number):

    qns = []
    my_prompt = generate_exmp_qns_prompt

    #Defining the prompt template
    prompt = PromptTemplate(input_variables=['number'],template=my_prompt)

    #Defining chain with new format
    chain=prompt|llm

    response = chain.invoke({'number':number})

    #st.write(response.content)

    for qn in response.content.split('\n'):
        if len(qn.strip()) !=0:
            qns.append(qn)

    return qns