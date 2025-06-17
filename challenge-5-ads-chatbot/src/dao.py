
from google.cloud import bigquery
from src.prompts import searchable_query_prompt
from src.gemini_client import call_llm

def make_searchable_query(user_input):
    """
    Transform the user input into a concise query suitable for vector search.
    
    Args:
        user_input: The original user query
        
    Returns:
        A transformed query optimized for vector search
    """
    # Get the searchable query prompt
    prompt = searchable_query_prompt()
    
    # Call LLM to transform the user input
    transformed_query = call_llm(
        prompt=user_input,
        system_prompt=prompt,
        temperature=0.1  # Lower temperature for more deterministic results
    )
    
    # Return the transformed query, stripped of any whitespace
    return transformed_query.strip()

# Run the Vector search on Bigquery
def bq_vector_search(user_query):
    """
    Perform vector search on BigQuery to retrieve relevant context for the user query.
    
    This function:
    1. Transforms the user query into a more searchable format
    2. Executes a vector similarity search in BigQuery using the transformed query
    3. Retrieves the most relevant Q&A pairs from the knowledge base
    4. Formats the results into a context string for the LLM
    
    Args:
        user_query (str): The original query provided by the user
        
    Returns:
        str: Formatted context containing relevant Q&A pairs from the knowledge base,
             or an error message if the search fails
    """
    # Create a BigQuery client
    client = bigquery.Client()
    
    # Transform the user query to make it more searchable
    searchable_query = make_searchable_query(user_query)
    
    # Prepare the query with proper escaping to prevent SQL injection
    query = f"""
    SELECT
        query.query,
        base.content as content,
        base.answer,
        base.question
    FROM
        VECTOR_SEARCH(
            TABLE `ADS.faq_embedded`,
            'ml_generate_embedding_result',
            (
                SELECT
                    ml_generate_embedding_result,
                    content AS query
                FROM
                    ML.GENERATE_EMBEDDING(
                        MODEL `ADS.Embeddings`,
                        (SELECT ? AS content)
                    )
            ),
            top_k => 5,
            options => '{{"fraction_lists_to_search": 0.01}}'
        );
    """
    
    # Use query parameters to prevent SQL injection
    query_params = [bigquery.ScalarQueryParameter(None, "STRING", searchable_query.strip())]
    job_config = bigquery.QueryJobConfig(query_parameters=query_params)
    
    try:
        # Execute the query
        query_job = client.query(query, job_config=job_config)
        
        # Get the results
        results = query_job.result()
        
        # Format the results into a context string
        context = ""
        for row in results:
            context += f"Question: {row.question}\nAnswer: {row.answer}\n\n"
        
        return context
    except Exception as e:
        print(f"Error executing BigQuery: {e}")
        return "No relevant information found in the knowledge base."
