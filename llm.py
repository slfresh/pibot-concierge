import os
from openai import OpenAI

# LM Studio typically hosts its server on port 1234
# Allows setting via environment variable (e.g. for a remote PC running LM Studio)
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")

# api_key is required by the SDK but not used by local LM Studio
client = OpenAI(base_url=LM_STUDIO_URL, api_key="lm-studio")

def answer_question(query: str, context: str) -> str:
    system_prompt = f"""You are a helpful and polite hotel concierge AI assistant.
Use the following information about the hotel to answer the guest's question.
If the information provided does not contain the answer, politely tell them you don't know and they should contact the front desk.

Hotel Information:
{context}
"""

    try:
        response = client.chat.completions.create(
            # the model name doesn't matter much for LM Studio, it uses whatever is loaded
            model="local-model",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.3,
            max_tokens=256
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error communicating with the local AI model: {e}"
