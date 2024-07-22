from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModel
import pinecone
import re
import config

def embed_text(text):
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    hf_embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return hf_embeddings.embed_documents([text])

if __name__ == '__main__':
    # Connect to Pinecone
    pinecone_api = config.pinecone_api
    pc = pinecone.Pinecone(api_key=pinecone_api)
    index = pc.Index("datawarehouse-schema")

    # load the data
    with open('examples.txt', "r") as file:
        content = file.read()
        examples = re.findall(r'{.*?}', content, re.DOTALL)
        examples = [example.replace('\n', '') for example in examples]

    # Embed the data
    for i, example in enumerate(examples):
        embeding = embed_text(example)
        example = example.replace('{', '').replace('}', '').strip()
        index.upsert(
            vectors=[{
                "id":str(i+1),
                "values":embeding[0],
                "metadata":{"Text" : example}
            }],
            namespace="namespace1"
        )
        
    print("Data uploaded successfully")