from fastapi import FastAPI
from openai import OpenAI 
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI()

client = OpenAI(api_key="sk-xxxxxx")  # Replace with your OpenAI API key

async def get_response(prompt: str):
    response = client.chat.completions.create(
        model="gpt-4",  # Change model if needed
        messages=[{"role": "user", "content": prompt}],
        stream=True  
    )
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield json.dumps({"response": chunk.choices[0].delta.content}) + "\n"
        await asyncio.sleep(0)  

@app.post("/chat/")
async def chat_stream(data: dict):
    prompt = data.get("question", "Hello!")
    return StreamingResponse(get_response(prompt), media_type="application/json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


