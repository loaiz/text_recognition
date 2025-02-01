from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import easyocr
import io 
import re

app = FastAPI()

reader = easyocr.Reader(['es','en'], gpu=False)

PLATE_REGEX = r"^[A-Z]{3}-\d{2}[A-Z]$|^[A-Z]{3}\d{3}$|^[A-Z]{3}\d{2}[A-Z]$"


@app.post("/upload/")
async def detect_plate(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        image = Image.open(io.BytesIO(contents))

        image = image.convert("RGB")

        result = reader.readtext(contents, detail=0)

        plates = [text for text in result if re.match(PLATE_REGEX, re.sub(r"[^a-zA-Z0-9]", "", text))]
        
        
        print(result)

        if plates:
            return {"plates": plates}
        else:
            return {"message":"Moto robada"}


    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
def hello_world():
    return {"message":"Hola Mundo"}