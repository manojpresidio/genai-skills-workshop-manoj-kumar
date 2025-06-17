import sys
import os
import pytest

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.chatbot_service import call_agent
from src.gemini_client import call_llm
from src.utils import extract_json

# Sample snow-related queries that should be answered
test_queries = [
    "What is the mission of Alaska Department of Snow?",
    "How do I report an unplowed road?",
    "What are the snow removal priorities after a storm?",
    "When will my residential street be plowed?"
]

# Test system prompt for evaluating responses
test_evaluation_system_prompt = """
You are an evaluator for the Alaska Department of Snow chatbot. Your task is to determine if the chatbot's response is:
1. Relevant to snow management, road conditions, or Alaska Department of Snow services
2. Professional and helpful
3. Factual and informative

Respond with a JSON object in the following format:
{
    "result": "Yes" or "No",
    "reason": "Brief explanation of your evaluation"
}

Only respond with the JSON object, no additional text.
"""

def test_call_agent():
    """
    Test the call_agent function with various snow-related queries.
    
    This test:
    1. Sends predefined snow-related queries to the chatbot
    2. Gets responses from the call_agent function
    3. Evaluates each response using the LLM with a specialized evaluation prompt
    4. Verifies that each response is relevant, professional, and informative
    
    The test passes if all responses receive a "Yes" evaluation from the LLM,
    indicating they meet the quality criteria for the Alaska Department of Snow chatbot.
    
    Raises:
        AssertionError: If any response fails the evaluation
    """
    print("\nTesting call_agent function...")
    
    for query in test_queries:
        # Get response from the chatbot
        response = call_agent(query)
        print(f"\nQuery: {query}")
        print(f"Response: {response}")
        
        # Evaluate the response using the LLM
        evaluation_prompt = f"Query: {query}\nResponse: {response}"
        
        # Use the call_llm function for evaluation
        eval_response = call_llm(
            prompt=evaluation_prompt,
            system_prompt=test_evaluation_system_prompt,
            temperature=0
        )
        
        # Extract the JSON from the response
        eval_json = extract_json(eval_response)
        print(f"Evaluation: {eval_json}")
        
        # Assert that the evaluation is positive
        assert eval_json["result"] == "Yes", f"Failed for query: {query} because {eval_json.get('reason', 'unknown reason')}"

if __name__ == "__main__":
    pytest.main(["-v"])
