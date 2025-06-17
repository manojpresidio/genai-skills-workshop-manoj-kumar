
from google import genai
from google.genai import types

from typing import Optional, List, Dict, Any, Union

PROJECT_ID = "qwiklabs-gcp-02-682b5eee4362"
MODEL = "gemini-2.0-flash-001"
client = None

def get_gemini_client():
    """
    Get or create a singleton instance of the Gemini client.
    
    This function implements the singleton pattern to ensure that only one
    instance of the Gemini client is created and reused throughout the application.
    This is more efficient than creating a new client for each request.
    
    Returns:
        genai.Client: A configured Google GenAI client instance
    """
    global client
    if client is not None:
        return client
    
    # Initialize the Google GenAI client
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location="global",
    )
    
    return client

def call_llm(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.2,
    max_output_tokens: int = 1024,
    top_p: float = 0.8,
    history: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Generic function for making calls to the Gemini LLM.
    
    Args:
        prompt: The user prompt to send to the model
        system_prompt: Optional system prompt to set context for the model
        temperature: Controls randomness in the model (0.0 to 1.0)
        max_output_tokens: Maximum number of tokens in the response
        top_p: Nucleus sampling parameter (0.0 to 1.0)
        history: Optional conversation history as a list of message dictionaries
        
    Returns:
        The text response from the model
    """
    # Get the Gemini client
    gemini_client = get_gemini_client()
    
    # Handle conversation history if provided
    if history:
        # Incorporate history into the prompt
        conversation_context = ""
        for message in history:
            role = message.get("role", "user")
            content_text = message.get("content", "")
            if role == "user":
                conversation_context += f"User: {content_text}\n"
            elif role == "model":
                conversation_context += f"AI: {content_text}\n"
        
        # Add the conversation context to the prompt
        if conversation_context:
            prompt = f"{conversation_context}\nUser: {prompt}"
    
    # Prepare generation config with system instruction
    generation_config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        top_p=top_p,
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
            )
        ],
        system_instruction=[types.Part.from_text(text=system_prompt or '')]
    )
    
    try:
        # Generate response
        response = gemini_client.models.generate_content(
            model=MODEL,
            contents=[prompt],
            config=generation_config
        )
        print(f"Prompt: {prompt}")
        print(f"\nResponse: {response.text}\n\n")
        # Return the text response
        return response.text
    except Exception as e:
        print(f"Error generating content: {e}")
        return f"An error occurred while generating a response: {str(e)}"
