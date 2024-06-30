from fastapi import FastAPI, HTTPException
import requests
from fastapi.responses import StreamingResponse
import io
import random
from typing import List, Tuple, Dict, Any

app = FastAPI()

# CRUD service URL
CRUD_SERVICE_URL = "http://localhost:8001"
# Image service URL
IMAGE_SERVICE_URL = "http://localhost:8002"

@app.post("/breed/{parent1_id}/{parent2_id}")
async def breed_pokemon(parent1_id: int, parent2_id: int):
    try:
        # Fetch parent 1 data
        parent1_response = requests.get(f"{CRUD_SERVICE_URL}/pokemon_id/{parent1_id}")
        if parent1_response.status_code != 200:
            raise HTTPException(status_code=parent1_response.status_code, detail="Parent 1 not found")
        parent1_data = parent1_response.json()
        print(parent1_data)
        # Fetch parent 2 data
        parent2_response = requests.get(f"{CRUD_SERVICE_URL}/pokemon_id/{parent2_id}")
        if parent2_response.status_code != 200:
            raise HTTPException(status_code=parent2_response.status_code, detail="Parent 2 not found")
        parent2_data = parent2_response.json()
        
        print(f"{IMAGE_SERVICE_URL}/images/{str(parent1_data)}")
        # Fetch parent 1 image
        parent1_image_response = requests.get(f"{IMAGE_SERVICE_URL}/images/{parent1_data[0]}")
        print(parent1_image_response)
        print(f"{IMAGE_SERVICE_URL}/images/{parent1_data[0]}")
        if parent1_image_response.status_code != 200:
            raise HTTPException(status_code=parent1_image_response.status_code, detail="Parent 1 image not found")
        parent1_image = StreamingResponse(io.BytesIO(parent1_response.content), media_type=parent1_response.headers["content-type"])

        # Fetch parent 2 image
        parent2_image_response = requests.get(f"{IMAGE_SERVICE_URL}/images/{parent2_data[0]}")
        print(parent2_image_response)
        if parent2_image_response.status_code != 200:
            raise HTTPException(status_code=parent2_image_response.status_code, detail="Parent 2 image not found")
        parent2_image = StreamingResponse(io.BytesIO(parent2_response.content), media_type=parent2_response.headers["content-type"])


        parent1_type_response = requests.get(f"{CRUD_SERVICE_URL}/pokemon_type_id/{parent1_id}")
        if parent2_response.status_code != 200:
            raise HTTPException(status_code=parent2_response.status_code, detail="Parent 2 not found")
        parent1_type = parent1_type_response.json()
        print(parent1_type)


        parent2_type_response = requests.get(f"{CRUD_SERVICE_URL}/pokemon_type_id/{parent2_id}")
        if parent2_response.status_code != 200:
            raise HTTPException(status_code=parent2_response.status_code, detail="Parent 2 not found")
        parent2_type = parent2_type_response.json()
        print(parent2_type)


        new_pokemon_name = f"{parent1_data[0]}-{parent2_data[0]}"
        new_pokemon_type = [parent1_type[0],parent2_type[0]]
        new_pokemon_height = random.randint(1,10)
        new_pokemon_wieght = random.randint(1,10)
        new_pokemon_data = {
        "name": new_pokemon_name,
        "height": new_pokemon_height,
        "weight": new_pokemon_wieght,  
        "types": new_pokemon_type   
}
        print(type(new_pokemon_data))
        print(new_pokemon_data)

        response = requests.post(f"{CRUD_SERVICE_URL}/pokemons/", json=new_pokemon_data)
        print(response.status_code)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        try:
            parent1_response = requests.get(f"{IMAGE_SERVICE_URL}/images/{parent1_data[0]}")
            parent1_response.raise_for_status()
            parent1_image = io.BytesIO(parent1_response.content)
            files = {"file": ("parent1_image.png", parent1_image, "image/png")}
            response1 = requests.post(f"{IMAGE_SERVICE_URL}/images/", files=files)
            response1.raise_for_status()
            parent1_image_id = response1.json()["file_id"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload parent1 image: {str(e)}")






        return {
            "parent1": {
                "id": parent1_id,

            },
            "parent2": {
                "id": parent2_id,

            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
