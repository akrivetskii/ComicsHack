from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import Response
import base64
import mimetypes
import os
from google import genai
from google.genai import types

def generate():
    client = genai.Client(api_key="AIzaSyD8pTi_OfJwLPK6F_fg_ePoMqfVjvu4QuM")

    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="Привет! Расскажи, что такое задача трёх тел."),
            ],
        ),
    ]

    response = client.models.generate_content(
        model=model, contents=contents
    )

    return response.text


app = FastAPI()
client = genai.Client()
model = "gemini-2.5-flash"

@app.get("/chat")
def chat_endpoint(prompt: str = Query(..., description="Текст запроса к модели")):
    try:

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            ),
        ]
        response = client.models.generate_content(model=model, contents=contents)
        return {"response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации: {str(e)}")

@app.get("/")
def read_root():
    res = generate()
    return {"message": "ComicsHack API работает! Используй /chat или /image"}
