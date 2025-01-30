import requests
import pandas as pd

def embed(text: str) -> list:
    """
    Generate an embedding vector for the given text using Ollama.

    :param text: The text to be embedded
    :return: A list representing the embedding vector
    """
    # URL for Ollama's embedding API, assuming it's running locally on default port
    url = "http://localhost:11434/api/embeddings"
    
    # Default model - adjust based on your needs or available models
    model = "nomic-embed-text:lastest"   

    # Prepare the payload
    payload = {
        "model": model,
        "prompt": text
    }

    try:
        # Send POST request to Ollama to get embeddings
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Parse the JSON response
        result = response.json()
        
        # Return the embeddings
        return result.get("embedding", [])

    except requests.RequestException as e:
        # Handle any network or API errors
        print(f"An error occurred while embedding the text: {e}")
        return []

# Example usage:
# vector = embed("This is a test sentence for embedding.")
# print(vector)

def chunk_and_embed(text: str, chunk_size: int = 1000) -> pd.DataFrame:
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