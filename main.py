
from fastapi import FastAPI,Request, UploadFile, File, HTTPException,Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import Optional

# import os


import base64
from io import BytesIO
from rembg import remove
from PIL import Image
import uvicorn
import numpy as np

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

template = Jinja2Templates( directory= "templates" )
@app.get("/", response_class=HTMLResponse)
async def great(request: Request):
    return template.TemplateResponse('index.html' ,{"request": request, "title": "FastAP with"})


def base64_to_image(base64_string: str) -> Image.Image:
    """Convert base64 string to PIL Image"""
    try:
        image_data = base64.b64decode(base64_string.split(",")[1] if "," in base64_string else base64_string)
        return Image.open(BytesIO(image_data))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64 image: {str(e)}")

def image_to_base64(image: Image.Image, format: str = "PNG") -> str:
    """Convert PIL Image to base64 string"""
    buffered = BytesIO()
    image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

@app.post("/remove-background")
async def remove_background(
    file: UploadFile = File(None),
    base64_str: Optional[str] = Body(None)
):
# async def remove_background(file: UploadFile = File(None), base64_str: str = None):
    """
    Remove background from either uploaded file or base64 string
    """
    try:
        if file:
            # Process uploaded file
            image = Image.open(BytesIO(await file.read()))
        elif base64_str:
            # Process base64 string
            image = base64_to_image(base64_str)
        else:
            raise HTTPException(status_code=400, detail="Either file or base64_str must be provided")
        
        # Remove background
        output_image = remove(image)
        
        # If output_image is bytes, convert to PIL Image
        if isinstance(output_image, bytes):
            output_image = Image.open(BytesIO(output_image))
        elif isinstance(output_image, np.ndarray):
            output_image = Image.fromarray(output_image)

        # Convert to base64 for response
        output_base64 = image_to_base64(output_image)
        
        return {
            "status": "success",
            "image": f"data:image/png;base64,{output_base64}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


