from fastapi import FastAPI
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
                types.Part.from_text(text="Привет! Ты говоришь по-русски?"),
            ],
        ),
    ]

    response = client.models.generate_content(
        model=model, contents=contents
    )

    return response.text

    # generate_content_config = types.GenerateContentConfig(
    #     response_modalities=[
    #         "IMAGE",
    #         "TEXT",
    #     ],
    # )

    # file_index = 0
    # for chunk in client.models.generate_content_stream(
    #     model=model,
    #     contents=contents,
    #     config=generate_content_config,
    # ):
    #     if (
    #         chunk.candidates is None
    #         or chunk.candidates[0].content is None
    #         or chunk.candidates[0].content.parts is None
    #     ):
    #         continue
    #     if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
    #         file_name = f"first.txt_{file_index}"
    #         file_index += 1
    #         inline_data = chunk.candidates[0].content.parts[0].inline_data
    #         data_buffer = inline_data.data
    #         file_extension = mimetypes.guess_extension(inline_data.mime_type)
    #         save_binary_file(f"{file_name}{file_extension}", data_buffer)
    #     else:
    #         print(chunk.text)


app = FastAPI()

@app.get("/")
def read_root():
    res = generate()
    return {"message": res}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}