import streamlit as st
from langchain_community.llms import LlamaCpp
import pinecone
from embedding import embed_text
import json
import config
from langchain_community.llms import HuggingFaceEndpoint,HuggingFaceHub
import os 

def vectorDatabase(text):
    if 'PINECONE_API_KEY' not in os.environ:
        print("Using config file for pinecone api")
        apikey = config.pinecone_api
    else:
        print("Using env for pinecone api")
        apikey = os.getenv['PINECONE_API']

    pc = pinecone.Pinecone(api_key=apikey)
    index = pc.Index("datawarehouse-schema")

    vect = embed_text(text)
    results = index.query(
        namespace="namespace1",
        vector=vect[0],
        include_metadata=True,
        top_k=4,
    )
    return results

def getLlmResponse(datawarehouse, databases, data_volume, query_patterns, growth_rate, performance_requirements, user_load, security_requirements):
    schemas = ['Hierarchical', 'Flat', 'Relational', 'Star', 'Snowflake', 'Network']
    # Use for local LLM
    # llm = LlamaCpp(
    #     model_path='D:\LLMMyDatabase\models\mistral-7b-instruct-v0.1.Q5_K_M.gguf',
    #     max_tokens=2000,
    #     n_ctx=1024,
    #     temperature=0.5
    # )

    # Use for HuggingFace LLM
    if 'HUGGING_API' not in os.environ:
        print("Using config file for hugging face api")
        Hugging_api = config.hugghing_api
    else:
        print("Using env for hugging api")
        Hugging_api = os.getenv['HUGGING_API']
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
        top_k=2,
        temperature=0.1,
        repetition_penalty=1.03,
        huggingfacehub_api_token=Hugging_api
    )

    vector_res = vectorDatabase('Data Warehouse: ' + datawarehouse + ', Databases: ' + databases + ', Data Volume: ' + str(data_volume) + ', Query Patterns: ' + query_patterns + ', Growth Rate: ' + str(growth_rate) + ', Performance Requirements: ' + performance_requirements + ', User Load: ' + user_load + ', Security Requirements: ' + security_requirements)
    
    if vector_res:
        matches = vector_res['matches']
        metadata_values = [match['metadata']['Text'] for match in matches]
        vector_context = "\n\n".join([json.dumps(metadata) for metadata in metadata_values])
        vector_context.replace('"', '')
        print(vector_context)
    else:
        metadata_values = []
        vector_context = "No additional insights found from the vector database."

    prompt_template = """
    Youu are an architect designing a new data warehouse. You have the following requirements:
    1. The target data warehouse is named: {datawarehouse}.
    2. It will include the following databases: {databases}.
    3. Estimated data volume: {data_volume} TB.
    4. Common query patterns: {query_patterns}.
    5. Expected growth rate: {growth_rate} % per month.
    6. Specific performance requirements: {performance_requirements}.
    7. Number of concurrent users expected: {user_load}.
    8. Specific security or compliance requirements: {security_requirements}.
    These are some related examples. You must answer using this examples: 
    <context>
    {vector_context}
    </context>
    Suggest the most suitable schema for this data warehouse.
    """

    input_variables = {
        "datawarehouse": datawarehouse,
        "databases": databases,
        "data_volume": data_volume,
        "query_patterns": query_patterns,
        "growth_rate": growth_rate,
        "performance_requirements": performance_requirements,
        "user_load": user_load,
        "security_requirements": security_requirements,
        "schemas": ', '.join(schemas),
        "vector_context": vector_context,
        }
    
    prompt = prompt_template.format(**input_variables)
    response = llm(prompt)
    return response


# Streamlit application
if __name__ == '__main__':

    st.set_page_config(
        page_title="Smart Schema Suggestions ", 
        layout="centered", 
        initial_sidebar_state="expanded"
    )
    st.markdown("<h1 style='text-align: center;'>Smart Schema Suggestion</h1>", unsafe_allow_html=True)

    datawarehouse_name = st.text_area("Enter your target data warehouse name", height=25, key="datawarehouse_name")
    databases = st.text_area("Enter your target databases", height=25, key="databases")
    col1, col2 = st.columns(2)

    with col1:
        query_patterns = st.selectbox("Describe your common operational query patterns",
                                    ("OLAP", "OLTP", "Mixed"), index=0,
                                    key="query_patterns")
        growth_rate = st.number_input("Expected growth rate/Scaling (% per month)", min_value=0.0, step=0.1, format="%.1f", key="growth_rate")
        security_requirements = st.selectbox("Describe any specific security or compliance requirements", 
                                            ("Highly sensitive data", "Standard security", "No specific requirements"), index=1,
                                            key="security_requirements")

    with col2:
        data_volume = st.number_input("Estimated data volume (in TB)", min_value=0.0, step=0.1, format="%.1f", key="data_volume")
        performance_requirements = st.selectbox("Describe performance requirements",
                                                ("High-speed", "Medium-speed", "No-speed requirement"), index=2, key="performance_requirements")
        user_load = st.selectbox("Number of concurrent users expected", 
                                ("Very High", "High", "Medium", "Low"), index=3,
                                key="user_load")
    submit = st.button("Recommend Schema")

    # Response from llm 
    if submit:
        response = getLlmResponse(
            datawarehouse_name,
            databases,
            data_volume,
            query_patterns,
            growth_rate,
            performance_requirements,
            user_load,
            security_requirements,
        )
        st.write(response)
