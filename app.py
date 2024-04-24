# Importing necessary libraries
import streamlit as st
from dotenv import load_dotenv
from utils import * # Importing utility functions
import uuid
import os

#Creating session variables
if 'unique_id' not in st.session_state:
    st.session_state['unique_id'] =''

def main():
    load_dotenv()

    st.set_page_config(page_title="Invoice Extractor")
    st.subheader("I can help you in Invoices Extraction process")
    pdf = st.file_uploader("Upload invoices here, only PDF files allowed", type=["pdf"],accept_multiple_files=True)

    submit=st.button("Publish")

    PINECONE_API_KEY=os.environ['PINECONE_API_KEY']
    # invoice_description = st.text_area("Please enter the 'INVOICE DETAILS' here...",key="1")
    # document_count = st.text_input("No.of 'INVOICES' to return",key="2")

    extracted_data = ""

    #Create embeddings instance
    embeddings=create_embeddings_load_data()
    if submit:
        with st.spinner('Wait for it...'):

            # Creating a unique ID, so that we can use to query and get only the user uploaded documents from PINECONE vector store
            st.session_state['unique_id']=uuid.uuid4().hex

            # Creating a list of documents from user uploaded PDF files
            final_docs_list=create_docs(pdf,st.session_state['unique_id'])

            # Displaying the count of resumes that have been uploaded
            st.write("*Documents uploaded* :"+str(len(final_docs_list)))

            # Pushing data to PINECONE
            push_to_pinecone(PINECONE_API_KEY,"us-east-1","text-to-csv",embeddings,final_docs_list)

    extract=st.button("Extract")

    if extract:
        # Retrieving relevant documents from Pinecone
        relavant_docs=similar_docs(PINECONE_API_KEY,"us-east-1","text-to-csv",embeddings)

        combined_df = pd.DataFrame()

        # Displaying a separator
        st.write(":heavy_minus_sign:" * 30)

        # Iterating through relevant documents
        for item in range(len(relavant_docs)):
            # Extracting content from pages
            result = relavant_docs[item][0].page_content
            extracted_data = extract_data(result)
            df = to_df(extracted_data)
            combined_df = combined_df._append(df, ignore_index=True)

        st.write(combined_df)

        st.success("Hope I was able to save your time❤️")
        
#Invoking main function
if __name__ == '__main__':
    main()
