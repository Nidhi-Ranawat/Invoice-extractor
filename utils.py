# Importing necessary libraries
from langchain.vectorstores import Pinecone
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Pinecone as PineconeStore
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
import pinecone
from pypdf import PdfReader
from langchain.llms.openai import OpenAI
import time
from pinecone import Pinecone

import pandas as pd
import json

# Function to extract text from PDF files
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to convert user uploaded PDF files to Langchain Documents
def create_docs(user_pdf_list, unique_id):
    docs=[]
    for filename in user_pdf_list:
        pdf_data=get_pdf_text(filename)
        docs.append(Document(
            page_content=pdf_data,
            metadata={"name": filename.name,"type=":filename.type,"size":filename.size,"unique_id":unique_id},
        ))
    return docs

#Create embeddings instance
def create_embeddings_load_data():
    embeddings = OpenAIEmbeddings()
    return embeddings

# Function to push embedded data to Vector Store - Pinecone
def push_to_pinecone(pinecone_apikey,pinecone_environment,pinecone_index_name,embeddings,docs):
    pinecone = Pinecone(
        api_key=pinecone_apikey,environment=pinecone_environment
        )
    index=PineconeStore.from_documents(docs,embeddings,index_name=pinecone_index_name)

# Function to pull data from Pinecone
def pull_from_pinecone(pinecone_apikey,pinecone_environment,pinecone_index_name,embeddings):
    print("10secs delay...")
    time.sleep(10)
    pinecone = Pinecone(
        api_key=pinecone_apikey,environment=pinecone_environment
    )
    index_name = pinecone_index_name
    index = PineconeStore.from_existing_index(index_name, embeddings)
    return index

# Function to find similar documents in Pinecone
def similar_docs(pinecone_apikey,pinecone_environment,pinecone_index_name,embeddings,k=6):
    query=""
    pinecone = Pinecone(
        api_key=pinecone_apikey,environment=pinecone_environment
    )
    index_name = pinecone_index_name
    index = pull_from_pinecone(pinecone_apikey,pinecone_environment,index_name,embeddings)
    
    index_stat = pinecone.Index(pinecone_index_name) 
    vector_count = index_stat.describe_index_stats() 
    k = vector_count["total_vector_count"]
    
    similar_docs = index.similarity_search_with_score(query, int(k))

    return similar_docs
    
# Function to extract relevant information from PDF pages
def extract_data(pages_data):
    template = """Extract ONLY the following values if found: 
    Customer Name,Address,City,State,Country,Pin,MobileNo,DOB,Email,PAN No,Insurance Company name,PolicyType,Product Name,Vehicle Registration Status,Vehicle No,Make,Model,Variant,Date of Registration,Year of Manufacturing,Type of Vehicle/OwnershipType,Vehicle Class,Vehicle Sub Class,ChasisNo,EngineNo,CC,Fuel,RTO,Zone,NCB,ODD,PCV/GCV/Misc/TW,Passenger/GVW,Bus Proposal Date,Policy Start Date,Policy Expiry Date,Policy No,Policy Issue Date,Business Type (New/Renwal/Rollover),Sum Insured,OD Net Premium,OwnerDriver(LPD),Roadside Assistance(WithoutBrokerage),GST/TaxAmount,Stamp Duty,Gross Premium,Payment Mode,Tran No,Tran Dated,BankName,Premium Receipt No,Prev Policy_no,Insured/Proposer Name and Without NilDep from this data: {pages}

    Format the extracted output as JSON with the following keys only: 
    Customer Name,Address,City,State,Country,Pin,MobileNo,DOB,Email,PAN No,Insurance Company name,PolicyType,Product Name,Vehicle Registration Status,Vehicle No,Make,Model,Variant,Date of Registration,Year of Manufacturing,Type of Vehicle/OwnershipType,Vehicle Class,Vehicle Sub Class,ChasisNo,EngineNo,CC,Fuel,RTO,Zone,NCB,ODD,PCV/GCV/Misc/TW,Passenger/GVW,Bus Proposal Date,Policy Start Date,Policy Expiry Date,Policy No,Policy Issue Date,Business Type (New/Renwal/Rollover),Sum Insured,OD Net Premium,OwnerDriver(LPD),Roadside Assistance(WithoutBrokerage),GST/TaxAmount,Stamp Duty,Gross Premium,Payment Mode,Tran No,Tran Dated,BankName,Premium Receipt No,Prev Policy_no,Insured/Proposer Name,Without NilDep
    """

    prompt_template = PromptTemplate(input_variables=["pages"], template=template)

    llm = OpenAI(temperature=0,max_tokens=1000)

    # Split the input data into smaller pdf_data
    chunk_size = 4000
    pdf_data = [pages_data[i:i+chunk_size] for i in range(0, len(pages_data), chunk_size)]
    
    dicts = []
    for chunk in pdf_data:
        str_dict = llm(prompt_template.format(pages=chunk))
        # print(llm(prompt_template.format(pages=chunk)))
        dictionary = json.loads(str_dict)
        dicts.append(dictionary)

    combined_dict = {}

    for d in dicts:
        for key, value in d.items():
            if key in combined_dict and combined_dict[key] == "NA":
                combined_dict[key] = value
            elif key not in combined_dict:
                combined_dict[key] = value

    return combined_dict

def to_df(data):
    # Add missing keys with 'NA' as value
    headers = [
    "Customer Name",
    "Address",
    "City",
    "State",
    "Country",
    "Pin",
    "MobileNo",
    "DOB",
    "Email",
    "PAN No",
    "Insurance Company name",
    "PolicyType",
    "Product Name",
    "Vehicle Registration Status",
    "Vehicle No",
    "Make",
    "Model",
    "Variant",
    "Date of Registration",
    "Year of Manufacturing",
    "Type of Vehicle/OwnershipType",
    "Vehicle Class",
    "Vehicle Sub Class",
    "ChasisNo",
    "EngineNo",
    "CC",
    "Fuel",
    "RTO",
    "Zone",
    "NCB",
    "ODD",
    "PCV/GCV/Misc/TW",
    "Passenger/GVW",
    "Bus Proposal Date",
    "Policy Start Date",
    "Policy Expiry Date",
    "Policy No",
    "Policy Issue Date",
    "Business Type (New/Renwal/Rollover)",
    "Sum Insured",
    "OD Net Premium",
    "OwnerDriver(LPD)",
    "Roadside Assistance(WithoutBrokerage)",
    "GST/TaxAmount",
    "Stamp Duty",
    "Gross Premium",
    "Payment Mode",
    "Tran No",
    "Tran Dated",
    "BankName",
    "Premium Receipt No",
    "Prev Policy_no",
    "Insured/Proposer Name",
    "Without NilDep"
]

    for header in headers:
        if header not in data:
            data[header] = 'NA'

    df = pd.DataFrame(data, index=[0])
    df = df[headers]
    return df
