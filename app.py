#Definin the app to run the front End
import streamlit as st
import datetime as dt
import pandas as pd
import plotly.express as px
import requests
from src.components.pdf_parser import pdf_parser,pdf_decrypt
from src.components.code_generator import get_in_context_reponse,get_generated_results_explantion,get_example_qns
from PIL import Image
#Session States
def initialize_session_state():
    #dataframes
    if 'dataframe' not in st.session_state:
        st.session_state.dataframe = ''
    #sesion state for example questions
    if "example_questions" not in st.session_state:
        st.session_state.example_questions = []
    #sesion state for example questions alrady selected
    if "selected_examples" not in st.session_state:
        st.session_state.selected_examples = []

initialize_session_state()

#Defining the main function:
def main():
    #Getting the favicon
    im = Image.open('assets/logo.png')
    st.logo('assets/logo.png')
    st.set_page_config("ChatPesa",page_icon=im)
    st.title("💬 Chat with Your Mpesa Statements:📊")

    #Decrpyt variable
    #Side Menu Bar
    with st.sidebar:
        st.title("🛠️ Configuration:⚙️")
        #Activating Demo Data
        st.text("Turn on to use demo data")
        demo_on = st.toggle("Use demo data: 📈")

    if demo_on:
        #impprting the demo data:
        df = pd.read_csv("Demo_Data/mpesa_demo_data.csv")
        #adding to session state
        st.session_state.dataframe = df
        st.text("Here are your transactions!💵")
        st.dataframe(df)
        
        chat_window(df)
    
    #Other option
    else:
        #Sidebar
        #Side Menu Bar
        with st.sidebar:
            st.text("Use your Mpesa Statement: 📝")
            pdf_file = st.file_uploader("Upload your Mpesa Statement",accept_multiple_files=False)
            pdf_password = st.text_input("Enter File password",type='password')
            #pdf_path = "\mpesa_statement_v2.pdf"
            if st.button("Submit & Process"):
                with st.spinner("Processing..."):
                    try:
                        pdf_decrypt(pdf_file=pdf_file,pdf_password=pdf_password)
            
                        st.success("Done")
        
                    except Exception as e:
                        st.error("Failed to decrypt the PDF. Please check you've uploaded your statement and entered the correct password.")
  
    #Loading the dataframe
    try:
        if pdf_file and pdf_password:
            df = pdf_parser(pdf_file=pdf_file,pdf_password=pdf_password)
            #adding to session state
            st.session_state.dataframe = df
            st.text("Here are your transactions!💵")
            st.dataframe(df)
            chat_window(df)
        else:
            st.code("Get Started by uploading your Mpesa Statement!")
    except Exception as e:
        print("Failed to decrypt the PDF. Please check you've uploaded your statement and entered the correct password.")

#Defining the function to Initialise the Chat Window
def chat_window(df):
    
    #Chat Window
    with st.chat_message("assistant"):
        st.write("What do you want to find out about your transactions today?🧐")

    #Initilizing message history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    #Displaying the message history on re-reun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            #priting the questions
            if 'question' in message:
                st.markdown(message["question"])
            #printing the code generated and the evaluated code
            elif 'code' in message:
                st.code(message['code'])
                exec(message['code'])
                #st.write(locals())
                st.write(locals()["results"])
            #retrieving results explanation
            elif 'explain' in message:
                st.markdown(message["explain"])
            #retrieving error messages
            elif 'error' in message:
                st.write(message['error'])
            
            
    #Getting the questions from the users
    user_question = st.chat_input("What would you like to find out about your Mpesa Transactions? ")

    #Getting the sample questions the user can use to prompt: can run only once:Can check if the list is None
    if len(st.session_state.example_questions) == 0:
        with st.spinner("Generating sample questions..."):
            get_sample_qns()
    
    #Display the sample question: Stop displaying when len of asked questions == len of example questions
    qn = display_sample_qns()
    #st.write(qn)

    if qn is not None:
        user_question = qn
      
   
    if user_question:
        #Displaying the user question in the chat message
        with st.chat_message("user"):
            st.markdown(user_question)
        #Adding user question to chat history
        st.session_state.messages.append({"role":"user","question":user_question})
        
        try:
            with st.spinner("Analyzing..."):
                get_analyst(user_question,attempt=2)
        
        except Exception as e:
            st.write(e)
            error_message = "⚠️Sorry, Couldn't generate the answer! Please try rephrasing your question!"
            #Displaying the error message
            with st.chat_message("assistant"):  
                st.error(error_message)

            #Appending the error messaage to the session
            st.session_state.messages.append({"role":"assistant","error":error_message})
        finally:
            st.rerun()

    #Function to clear history
    def clear_chat_history():
        st.session_state.messages = []
    #Button for clearing history
    st.sidebar.text("Click to Clear Chat history")
    st.sidebar.button("CLEAR 🗑️",on_click=clear_chat_history)
    #st.sidebar.image("Documents\mpesa_img.png")

def get_analyst(user_question,attempt=2):
    global results 
    try:     
        #Getting response from the API end-point
        code = get_in_context_reponse(user_question)
        st.code(code)
        #Running the generated code
        exec(code)

        #Getting the answer generated
        answer = locals()['results']

        #st.write(answer)
        explain = get_generated_results_explantion(question=user_question,code=code,results=answer)
        
        ##Print the generated code, results & Explanation
        st.code(code)
        st.write(locals()["results"])
        st.markdown(explain)
        
        #Appending the code and explanation  to message hisotry
        st.session_state.messages.append({"role":"assistant","code":code})
        st.session_state.messages.append({"role":"assistant","explain":explain})
    
    except Exception as e:
        st.write(e)
        if attempt >3:
        #st.error("Maximum retries reached for generating analyst insights.")
            raise Exception("Maximum retries reached")
        error_raised = ''
        error_raised = (f"The previously generated code: {code} raised this error : {type(e).__name__}: {str(e)}")

        #st.write(error_raised)
        #st.write(f"Retrying...{attempt}")
        
        # Recursive call with updated attempt count
        return get_analyst(error_raised, attempt + 1)

def get_sample_qns():
    """
    Can run the function only once to get the list of questions about 10 questions
    Based on the questions; if there are still questions display as long as they have not been selected previously
    """

    try:
        number=20
        qns = get_example_qns(number)

        #Adding to the session state
        st.session_state.example_questions = qns
        #st.write(qns)
       
    except Exception as e:
        return None

#Displaying the sample questions:
def display_sample_qns():
    """
    Display the quuestions generated by the LLM
    Once a user selects a question, DO NOT display in subsquent
    
    """
    try:
        # Create a horizontal container for side-by-side layout
        col1, col2 = st.columns(2)

        example_qns = st.session_state.example_questions
        selected_qns = st.session_state.selected_examples

        # Convert lists to sets for faster membership checking
        set1 = set(example_qns)
        set2 = set(selected_qns)

        # Find elements in list1 that are not in list2
        qns = list(set1.difference(set2))

        # Display buttons in separate columns only if remaining is greater or equals to 2:
        if len(qns) >=2:
            with col1:
                clicked1 = st.button(f':green[{qns[0]}]')
            with col2:
                clicked2 = st.button(f':blue[{qns[1]}]')

            if clicked1:
                st.session_state.selected_examples.append(qns[0])
                return qns[0]
            
            elif clicked2:
                st.session_state.selected_examples.append(qns[1])
                return qns[1]
    except Exception as e:
        pass


if __name__ == "__main__":
    main()

