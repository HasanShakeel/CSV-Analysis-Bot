from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import logging
from services.file_conversion import convert_excel_to_csv

app = APIRouter()

UPLOAD_FOLDER = "uploads"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/uploadfile")
async def upload_file(file: UploadFile = File(...), extension: str = Form(...)):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    logger.info(f"Saving file to {file_path}")

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")

    try:
        if extension in ['xlsx', 'xls']:
            convert_excel_to_csv(file_path)
            logger.info(f"File {file.filename} converted successfully")
        else:
            logger.info(f"File {file.filename} is not an Excel file. No conversion needed.")
    except Exception as e:
        logger.error(f"Error converting Excel to CSV: {e}")
        raise HTTPException(status_code=500, detail=f"Error converting Excel to CSV: {e}")

    return JSONResponse(content={"filename": file.filename, "detail": "File uploaded and processed successfully"})
