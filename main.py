from dotenv import load_dotenv
import streamlit as st
from constants import *
from utils import timeit
from chatbot import PDFHandler, TextChunkHandler, VectorStoreHandler, ConversationChainHandler, UserInputHandler
from htmlTemplates import css

@timeit
def main():
    load_dotenv()
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)
    st.markdown(css, unsafe_allow_html=True)

    # Initialize session state variables if they don't exist
    st.session_state.setdefault("conversation", None)
    st.session_state.setdefault("chat_history", None)

    st.header(HEADER_TEXT)
    user_question = st.text_input(TEXT_INPUT_PROMPT)
    if user_question:
        UserInputHandler.handle_userinput(user_question)

    with st.sidebar:
        st.subheader(SUB_HEADER_TEXT)
        pdf_docs = st.file_uploader(PDF_UPLOAD_MSG, accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner(PROCESSING_MSG):
                # get pdf text
                raw_text = PDFHandler.get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = TextChunkHandler.get_text_chunks(raw_text)

                # create vector store
                vectorstore = VectorStoreHandler.get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = ConversationChainHandler.get_conversation_chain(vectorstore)

        # Add a help section in the sidebar
        st.subheader("Need Help?")
        st.write("If you need any help, please refer to the FAQ section or contact us at amin.mba@iuj.ac.jp")

if __name__ == '__main__':
    main()
