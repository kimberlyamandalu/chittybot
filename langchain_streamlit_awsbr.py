import dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import BedrockChat
from langchain.schema import HumanMessage, AIMessage
import streamlit as st
    
# Load environment variables from .env file
## DO NOT COMMIT .env --> ADD to .gitignore
dotenv.load_dotenv()

# Setup Streamlit Chat Interface
st.header("ChittyBot: AWS Bedrock 🌩️ + LangChain 🦜️🔗 + Streamlit 👑")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    print("--- Chat history initialized ---")

if "llm" not in st.session_state:
    st.session_state.llm = BedrockChat(
        model_id="anthropic.claude-v2", # AWS Bedrock Model ID
        model_kwargs={"temperature": 0.7, "max_tokens_to_sample": 1024}, # AWS Bedrock Model arguments
        streaming=True, # enable response streaming
        callbacks=[StreamingStdOutCallbackHandler()], # response streaming handler
        verbose=False
    )
    print("--- LLM initialized ---")

# Reuse LLM object stored in Streamlit session
llm = st.session_state.llm

# Loop through messages list (chat history) and display in streamlit chat message container
for message in st.session_state.messages:
    # The "role" key in the additional_kwargs dict is used to determine the role icon (user or assistant) to use
    with st.chat_message(message.additional_kwargs['role']):
        st.markdown(message.content)

# st.chat_input creates a chat input box in the Streamlit app. The user can enter a message and it will be displayed in the chat message container.
# The string "Hello!" is used as a placeholder for the user's message.
if prompt := st.chat_input("Hello!"):
    print(f"\nHuman: {prompt}")
    print("AI: ")

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to session chat history
    human_input = HumanMessage(content=prompt, additional_kwargs={"role": "user"})
    st.session_state.messages.append(human_input)
    
    # Stream response from LLM and display in chat message container
    # Notice we send the list of messages so the bot remembers previous dialogues within the chat session
    stream_iterator = llm.stream(st.session_state.messages)
    with st.chat_message("assistant"):
        # Start with an empty message container for the assistant
        message_placeholder = st.empty()
        
        # Stream response from LLM in chunks and display in chat message container for real time chat experience
        full_response = ""
        for chunk in stream_iterator:
            full_response += chunk.content + " "    
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        
        # Add the final response to the chat history 
        ai_response = AIMessage(content=full_response, additional_kwargs={"role": "assistant"})
        st.session_state.messages.append(ai_response)
        
        # display in chat message container
        message_placeholder.markdown(full_response)