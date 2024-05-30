#Main application for chatting with Mpesa Statement
import pandas as pd
import streamlit as st
import os
import matplotlib.pyplot as plt
from langchain.llms import GooglePalm
from langchain.prompts import PromptTemplate
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import SemanticSimilarityExampleSelector
from few_shots import few_shots
from dotenv import load_dotenv
load_dotenv()

#configuring the api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Loading the LLM - Gemini Pro
llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.3)
# Reading the structured csv
df = pd.read_csv('Documents\mpesa_data.csv')
#df.head()

#Function for generating the response based on fine tuning the LLM using few shot examples
def get_few_shot_response(input_question):
    #defining the prompt - example prompt
    example_prompt = PromptTemplate(
        input_variables=['Question','Answer'],
        template="\nQuestion: {Question}\nAnswer: {Answer}",
    )

    #Embedding the few shot examples
    embeddings=GoogleGenerativeAIEmbeddings(model='models/embedding-001')
    # creating a blob of all the sentences
    to_vectorize = [" ".join(example.values()) for example in few_shots]
    #generating a vector store: 
    vector_store=FAISS.from_texts(to_vectorize, embeddings, metadatas=few_shots)

    #Checking sematic similarity: # Helping to pull similar looking queries
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore = vector_store,
        k=2, #number of examples
    )

    example_selector.select_examples({"Question": "What is the total amount of money withdrawn?"})


    my_prompt = """
    You are a financial advisor with knowdlege analysing data using pandas. 
    You will be provided with the columns details of a pandas data frame and you
    should generate the result based on the user's question. The dataframe conisists of transactions
    made by a user on Mpesa platform, which is a mobile money platform. 

    Given input question, first create a syntatically correct pandas syntax and return the syntax
    as an executable python code. 

    The dataframe name is df and only use the columns in the dataframe.\n\n

    Pay attention to use current_date = datetime.date.today() to get the current date, if the question involves "today".


    The following are the column names and their descriptions:
    'Receipt No.': Unique identifier for each mpesa transaction done. 
    'Completion Time': The timestamp for when the transaction was completed
    'Details': The details of the transaction
    'Name': The Account Name for the transaction done
    'Transaction_Type': The type of transaction; These are the type of transactions:['Mpesa Charges', 'Pay Bill', 'Bank Payment', 'Till No',
        'Send Money', 'Airtime Purchase', 'Receive Money', 'Pochi',
        'Other', 'M-Shwari Loan', 'Mshwari Withdraw', 'Mshwari Deposit',
        'Cash Withdrawal', 'Customer Deposit']
    'Paid In': The amount that was received in their Mpesa Account. 
    'Withdrawn': the Amount that was withdrawn or sent from their account
    'Balance': the balance remaining after the transaction was made

    Here's the dataframe information: 
    Data columns (total 8 columns):
    #   Column            Non-Null Count  Dtype  
    ---  ------            --------------  -----  
    0   Receipt No.       3508 non-null   object 
    1   Completion Time   3508 non-null   object 
    2   Details           3508 non-null   object 
    3   Name              3508 non-null   object 
    4   Transaction_Type  3508 non-null   object 
    5   Paid In           3508 non-null   float64
    6   Withdrawn         3508 non-null   float64
    7   Balance           3508 non-null   float64

    Make sure the response follows this format: 
    'Answer': 'df["Withdrawn"].sum()'

    """

    PROMPT_SUFFIX = """

    Question: {input}\n

    """

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix= my_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=['input'],
    )

    #Defining the LLM Chain
    chain = LLMChain(llm=llm,prompt=few_shot_prompt,verbose=True)

    response = chain.run(input=input_question)
    #Printing the response
    #print(response)
    #Extracting the code bit
    python_code = response.split(": ")[1].strip("'")
    
    return python_code

#Function for using in prompt context
def get_in_cotext_reponse(input_question):
    #getting the few shot examples
    examples = str(few_shots)
    
    my_prompt = """
    You are a financial advisor with knowdlege analysing data using pandas. 
    You will be provided with the columns details of a pandas data frame and you
    should generate the result based on the user's question. The dataframe conisists of transactions
    made by a user on Mpesa platform, which is a mobile money platform. 

    Given input question, first create a syntatically correct pandas syntax and return the syntax
    as an executable python code. 

    The dataframe name is df and only use the columns in the dataframe.\n\n

    The following are the column names and their descriptions:
    'Receipt No.': Unique identifier for each mpesa transaction done. 
    'Completion Time': The timestamp for when the transaction was completed
    'Details': The details of the transaction
    'Name': The Account Name for the transaction done
    'Transaction_Type': The type of transaction; These are the type of transactions:['Mpesa Charges', 'Pay Bill', 'Bank Payment', 'Till No',
        'Send Money', 'Airtime Purchase', 'Receive Money', 'Pochi',
        'Other', 'M-Shwari Loan', 'Mshwari Withdraw', 'Mshwari Deposit',
        'Cash Withdrawal', 'Customer Deposit']
    'Paid In': The amount that was received in their Mpesa Account. 
    'Withdrawn': the Amount that was withdrawn or sent from their account
    'Balance': the balance remaining after the transaction was made


    Here's the dataframe information: 
        Data columns (total 8 columns):
        #   Column            Non-Null Count  Dtype  
        ---  ------            --------------  -----  
        0   Receipt No.       3508 non-null   object 
        1   Completion Time   3508 non-null   object 
        2   Details           3508 non-null   object 
        3   Name              3508 non-null   object 
        4   Transaction_Type  3508 non-null   object 
        5   Paid In           3508 non-null   float64
        6   Withdrawn         3508 non-null   float64
        7   Balance           3508 non-null   float64

    Make sure the response follows this format: 'Answer': 'df["Withdrawn"].sum()'

    You can use the following examples: {examples} to get a better context of the type of response to provide

    Question: {question}\n


    """
    #Defining the prompt template
    #Defining the prompt template
    prompt = PromptTemplate(input_variables=['question','examples'],template=my_prompt)

    #Defining the LLM Chain
    chain = LLMChain(llm=llm,prompt=prompt,verbose=True)

    response = chain.run(question=input_question,examples=examples)

    python_code = response.split(": ")[1].strip("'")

    return python_code

def main():
    st.set_page_config("Chatting with Mpesa")
    st.header("Chatting with my Mpesa Statements")

    #Getting the input question
    input_question = st.text_input("What would you like to find out about your Mpesa Transactions?")

    if input_question:
        code = get_in_cotext_reponse(input_question)
        st.code(code)
        st.write(eval(code))

if __name__ == '__main__':
    main()
    