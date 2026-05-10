from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import stego
import huffman 
import base64
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/encode")
async def encode_endpoint(image: UploadFile = File(...), message: str = Form(...)):
    # 1. Comprimir con Huffman
    encoded_bits, dictionary = huffman.encode(message)

    # 2. Leer imagen y ocultar bits
    img_bytes = await image.read()
    stego_img = stego.encode_message(img_bytes, encoded_bits)
    
    # Convertimos los bytes de la imagen a una cadena Base64
    img_b64 = base64.b64encode(stego_img).decode('utf-8')

    # En un proyecto real, deberías devolver la imagen Y el diccionario.
    # Por ahora, devolvemos un JSON con el diccionario para que el front lo vea.
    return {
        "message": "Mensaje oculto con éxito",
        "bits": encoded_bits,
        "dictionary": dictionary,
        "image_b64": img_b64
    }