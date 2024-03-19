#Definin the app to run the front End
import streamlit as st
import datetime as dt
import pandas as pd
import requests

#Defining the main function:
def main():
    st.set_page_config("Chatting with Mpesa")
    st.title("Chatting with my Mpesa Statements")

    #Reading the CSV file
    df = pd.read_csv('Documents\mpesa_data.csv')

    df['Completion Time'] = pd.to_datetime(df['Completion Time'])

    #Chat Window
    with st.chat_message("assistant"):
        st.write("What do you want to find out about your transactions today?")

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
                st.write(eval(message['code']))
            #retrieving error messages
            elif 'error' in message:
                st.text(message['error'])
            

    #Getting the questions from the users
    user_question = st.chat_input("What would you like to find out about your Mpesa Transactions? ")

    if user_question:
        #Displaying the user question in the chat message
        with st.chat_message("user"):
            st.markdown(user_question)
        #Adding user question to chat history
        st.session_state.messages.append({"role":"user","question":user_question})
        
        response = requests.post("http://localhost:8000/generate_response", json={"question": user_question})

        try:
            #checking if the response from the server is successful
            if response.status_code == 200:
                #extracting the code from the JSON response
                code = response.json()["code"]
                st.code(code)
                st.write(eval(code))
            #Adding the assistant response to chat history
            st.session_state.messages.append({"role":"assistant","code":code})
        
        except Exception as e:
            error_message = "⚠️Error occured while fetching response from the server!"
            #Displaying the error message
            with st.chat_message("assistant"):  
                st.error(error_message)

            #Appending the error messaage to the session
            st.session_state.messages.append({"role":"assistant","error":error_message})

        
    #Side Menu Bar
    with st.sidebar:
        st.title("Configuration:⚙️")
    
    
    #Function to clear history
    def clear_chat_history():
        st.session_state.messages = []
    #Button for clearing history
    st.sidebar.button("Clear Chat History",on_click=clear_chat_history)


if __name__ == "__main__":
    main()

