import os

def call_llm(prompt):
    import openai
    client = openai
    client.api_key = os.getenv("OPENAI_API_KEY", "")
    
    try:
        response = client.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    
    except Exception as e:
        print(f"LLM Error: {e}")
        return f"Error in LLM call: {e}"