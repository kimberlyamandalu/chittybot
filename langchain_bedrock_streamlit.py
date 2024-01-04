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

if "bedrock_chat_object" not in st.session_state:
    st.session_state.bedrock_chat_object = BedrockChat(
        model_id="anthropic.claude-v2", # AWS Bedrock Model ID
        model_kwargs={"temperature": 0.7, "max_tokens_to_sample": 1024}, # AWS Bedrock Model arguments
        streaming=True, # enable response streaming
        callbacks=[StreamingStdOutCallbackHandler()], # response streaming handler
        verbose=False
    )
    print("Bedrock Chat Object Initialized")

# Reuse Bedrock chat object stored in Streamlit session
bedrock_chat = st.session_state.bedrock_chat_object

# Loop through messages list (chat history) and display in streamlit chat message container
for message in st.session_state.messages:
    # The "role" key in the additional_kwargs dict is used to determine the role icon (user or assistant) to use
    with st.chat_message(message.additional_kwargs['role']):
        st.markdown(message.content)

# st.chat_input creates a chat input box in the Streamlit app. The user can enter a message and it will be displayed in the chat message container.
# The string "Hello!" is used as a placeholder for the user's message.
if prompt := st.chat_input("Hello!"):
    print(f"\nHuman: {prompt}")
    print("\nAI: ")
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    human_input = HumanMessage(content=prompt, additional_kwargs={"role": "user"})
    # Add user message to chat history
    st.session_state.messages.append(human_input)
    # chat_history.append(HumanMessage(content=prompt))
    
    stream_iterator = bedrock_chat.stream(st.session_state.messages)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in stream_iterator:
            full_response += chunk.content + " "
            
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        
        ai_response = AIMessage(content=full_response, additional_kwargs={"role": "assistant"})
        st.session_state.messages.append(ai_response)
        message_placeholder.markdown(full_response)
