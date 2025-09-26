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


API_KEY = "AIzaSyD8pTi_OfJwLPK6F_fg_ePoMqfVjvu4QuM"

app = FastAPI()
client = genai.Client(api_key=API_KEY)
model_chat = "gemini-2.5-flash"
model_image = "models/imagen-4.0-generate-001"

@app.get("/chat")
def chat_endpoint(prompt: str = Query(..., description="Текст запроса к модели")):
    try:

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            ),
        ]
        response = client.models.generate_content(model=model_chat, contents=contents)
        return {"response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации: {str(e)}")


@app.get("/image")
def image_endpoint(prompt: str = Query(..., description="Описание изображения")):
    result = client.models.generate_images(
        model=model_image,
        prompt=prompt,
        config=dict(
            number_of_images=1,
            output_mime_type="image/jpeg",
            person_generation="ALLOW_ALL",
            aspect_ratio="1:1",
            image_size="1K",
        ),
    )

    if not result.generated_images:
        print("No images generated.")
        return

    if len(result.generated_images) != 1:
        print("Number of images generated does not match the requested number.")

    image_bytes = result.generated_images[0].image
    return Response(content=image_bytes, media_type="image/jpeg")


@app.get("/")
def read_root():
    res = generate()
    return {"message": res}
