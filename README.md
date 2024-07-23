# Smart Schema Suggestion
### Overview
Smart Schema Suggestion is a Streamlit application that leverages a Llama 03 language model to recommend the best database schema for your data warehouse based on database and datawarehouse requirements and insights from similar projects retrieved using vector database. The application integrates with Pinecone for vector search and uses the LlamaCpp model for generating schema recommendations.

### Features
- Recommends most efficient schema after detailed assesing about of data warehouse and its databases.
- Utilizes Pinecone as vector database for retrieving insights from similar projects.
- Employs HuggingFace endpoint for loading Llama 3 model from huggingface.
- Provides User-friendly interface built with Streamlit.
- Supports various schema types: Hierarchical, Flat, Relational, Star, Snowflake, and Network.
### Requirements
- Python 3.8 or higher
- Streamlit
- Pinecone
- HuggingFace Embeddings
- LlamaCpp (Optional)
- Transformers
- Sentence Transformers
### Installation
#### Clone the repository
```bash
git clone https://github.com/yourusername/smart-schema-suggestion.git
cd smart-schema-suggestion
```
#### Create a virtual environment
```bash
python -m venv env
source env/bin/activate
# On Windows: `env\Scripts\activate`
```
#### Install dependencies
```bash
pip install -r requirements.txt
```
#### Setting up API's
- Set up your Pinecone and hugging face Api's as environment variables
  <br>OR
- Assign them to variables in config.py

#### Populate vector database
```bash
python embedding.py
```
More examples can be added to examples.txt

#### Run Streamlit
```bash
streamlit run app.py
```

## Project Structure
```graphql
smart-schema-suggestion/
│
├── app.py                # Main Streamlit application
├── upload_data.py        # Script to upload data to Pinecone
├── requirements.txt      # Project dependencies
├── Config.py             # For API backup
└── examples.txt          # Real-world examples for embedding and uploading
```
### Real-World Examples
The examples.txt file contains various real-world examples used to populate the vector database. Here are some examples included in the project:

Retail Data Warehouse
```json
{
    "Data Warehouse": "RetailDW",
    "Databases": ["SalesDB", "InventoryDB", "CustomerDB"],
    "Data Volume": "50 TB",
    "Query Patterns": "OLAP, real-time sales analysis, inventory forecasting",
    "Growth Rate": "10% per month",
    "Performance Requirements": "Sub-second query response times",
    "Data Integration": "ETL from POS systems, ERP, and CRM",
    "User Load": "1000 concurrent users",
    "Security Requirements": "PCI DSS compliance",
    "Budget Constraints": "Medium budget"
}
```
Healthcare Data Warehouse
```json
{
    "Data Warehouse": "HealthDW",
    "Databases": ["PatientDB", "TreatmentDB", "BillingDB"],
    "Data Volume": "200 TB",
    "Query Patterns": "OLAP, patient treatment history, billing analysis",
    "Growth Rate": "5% per month",
    "Performance Requirements": "High-speed access for critical patient data",
    "Data Integration": "HL7, FHIR standards from various EHR systems",
    "User Load": "500 concurrent users",
    "Security Requirements": "HIPAA compliance",
    "Budget Constraints": "High budget"
}
```
## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
- Streamlit
- Pinecone
- HuggingFace
- Langchain
