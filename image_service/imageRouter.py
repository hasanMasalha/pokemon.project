import requests
from fastapi import APIRouter, File, UploadFile, HTTPException, Response
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
import logging
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
image_router = APIRouter()
# Connect to MongoDB
try:
    logger.info("Attempting to connect to MongoDB at mongodb:27017")
    client = MongoClient("mongodb://localhost:27017/")
    db = client.pokemon_images
    fs = GridFS(db)
    logger.info("Connected to MongoDB successfully")
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    raise HTTPException(status_code=500, detail="Could not connect to MongoDB")
@image_router.post("/images/")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_id = fs.put(file.file, filename=file.filename)
        print(file.file)
        print(file.filename)
        logger.info(f"Uploaded image: {file.filename}, ID: {file_id}")
        return {"file_id": str(file_id)}
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")

@image_router.get("/images/{pokemon_name}")
async def get_image(pokemon_name: str):
    try:
        data = db.fs.files.find_one({"filename": pokemon_name + ".png"})
        if data is None:
            raise HTTPException(status_code=404, detail="Image not found")
        file_id = data['_id']
        output_data = fs.get(file_id).read()
        # Determine the file type and set the appropriate media type
        file_type = data.get("contentType", "image/png")  # Default to image/png if contentType is not set
        return Response(content=output_data, media_type=file_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
@image_router.get("/images/")
async def list_images():
    try:
        files = db.fs.files.find()
        image_list = [{"file_id": str(file["_id"]), "filename": file["filename"]} for file in files]
        return {"images": image_list}
    except Exception as e:
        logger.error(f"Error listing images: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing images: {str(e)}")







