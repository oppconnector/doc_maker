import requests
import pandas as pd
from config import openweb_ui_api_key
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

def embed(text: str) -> list:
    """
    Generate an embedding vector for the given text using Ollama.

    :param text: The text to be embedded
    :return: A list representing the embedding vector
    """
    # URL for Ollama's embedding API, assuming it's running locally on default port
    url = "http://localhost:11434/api/embed"
    
    # Default model - adjust based on your needs or available models
    model = "nomic-embed-text"   

    # Prepare the payload
    payload = {
        "model": model,
        "input": text
    }

    try:
        # Send POST request to Ollama to get embeddings
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Parse the JSON response
        result = response.json()
        print("it worked")
        
        # Return the embeddings
        return result.get("embeddings", "None")

    except requests.RequestException as e:
        # Handle any network or API errors
        print(f"An error occurred while embedding the text: {e}")
        return []

# Example usage:
# vector = embed("This is a test sentence for embedding.")
# print(vector)

def chunk_embed_df(text: str, chunk_size: int = 1000) -> pd.DataFrame:
    """
    Chunk a long string of text, embed each chunk, and save into a pandas DataFrame.

    :param text: The long string of text to be chunked and embedded
    :param chunk_size: The size of each chunk in characters
    :return: DataFrame with 'chunk' and 'embedding' columns
    """
    # Chunk the text
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    # Embed each chunk
    embeddings = []
    for chunk in chunks:
        embedding = embed(chunk)
        embeddings.append(embedding)
    
    # Create DataFrame
    df = pd.DataFrame({
        'chunk': chunks,
        'embedding': embeddings
    })
    
    return df

# Example usage:
# long_text = "Your very long text here..."
# df = chunk_and_embed(long_text)
# print(df)

def ollama_llm(prompt):
    # Simple text generation
    model =  "phi3.5:latest"
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            "model": model ,
            "prompt": prompt,
            "stream": False
        }
    )
        # Check if the request was successful
    if response.status_code == 200:
        # Assuming the response is JSON, parse it
        #result = response.text # ['choices'][0]['message']['content']
        # Parse the JSON string into a Python dictionary
        # Directly parse the JSON from the response
        parsed_response = response.json()
        
        # Extract the 'response' message
        message = parsed_response.get('response', '')
        #print(result)
        return message
    else:
        print(f"Request failed with status code: {response.status_code}")
        #print(response.text)
        return None

    
def openweb_ui_llm(prompt):
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = openweb_ui_api_key
    model =  "phi3.5:latest"

    # URL for the API endpoint
    url = 'http://192.168.77.201:8080/api/chat/completions'

    # Headers for the request
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Body of the request
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Assuming the response is JSON, parse it
        result = response.json()['choices'][0]['message']['content']
        #print(result)
        return result
    else:
        print(f"Request failed with status code: {response.status_code}")
        #print(response.text)
        return None
    


def RAG_LLM(prompt, df):
    # Step 1: Vectorize the prompt
    prompt_embedding = embed(prompt)
    
    # Step 2: Perform RAG (Retrieval-Augmented Generation)
    # Convert DataFrame embeddings to a numpy array for computation
    embeddings_array = np.array(df['embedding'].tolist())
    
    # Compute similarity scores between prompt and each chunk's embedding
    similarities = cosine_similarity([prompt_embedding], embeddings_array)[0]
    
    # Find the index of the most similar chunk
    most_similar_idx = np.argmax(similarities)
    
    # Retrieve the most relevant chunk based on similarity
    relevant_chunk = df.loc[most_similar_idx, 'chunk']
    
    # Step 3: Combine prompt with relevant information
    augmented_prompt = f"{prompt}\n\nRelevant Information: {relevant_chunk}"
    
    # Step 4: Use the LLM to generate an answer based on the augmented prompt
    answer = ollama_llm(augmented_prompt)
    
    return answer