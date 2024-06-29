from fastapi import FastAPI, HTTPException
from fastapi import  File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import io


from pydantic import BaseModel
from typing import List
import requests

app = FastAPI()

class Pokemon(BaseModel):
    name: str
    height: float
    weight: float
    types: List[str]

class Trainer(BaseModel):
    name: str
    town: str

CRUD_SERVICE_URL = "http://localhost:8001"
IMAGE_SERVICE_URL = "http://localhost:8002"

@app.get("/pokemons/")
def get_pokemons_by_type(pokemon_type: str):
    print(CRUD_SERVICE_URL)
    response = requests.get(f"{CRUD_SERVICE_URL}/pokemons/", params={"pokemon_type": pokemon_type})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@app.post("/pokemons/")
def add_pokemon(pokemon: Pokemon):
    response = requests.post(f"{CRUD_SERVICE_URL}/pokemons/", json=pokemon.dict())
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@app.get("/pokemons/{pokemon_name}/owners/")
def get_trainers_of_pokemon(pokemon_name: str):
    response = requests.get(f"{CRUD_SERVICE_URL}/pokemons/{pokemon_name}/owners/")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@app.get("/trainers/{trainer_name}/pokemons/")
def get_pokemons_by_trainer(trainer_name: str):
    response = requests.get(f"{CRUD_SERVICE_URL}/trainers/{trainer_name}/pokemons/")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@app.post("/trainers/")
def add_trainer(trainer: Trainer):
    response = requests.post(f"{CRUD_SERVICE_URL}/trainers/", json=trainer.dict())
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@app.post("/trainers/{trainer_name}/pokemons/{pokemon_name}")
def add_pokemon_to_trainer(trainer_name: str, pokemon_name: str):
    response = requests.post(f"{CRUD_SERVICE_URL}/trainers/{trainer_name}/pokemons/{pokemon_name}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@app.delete("/trainers/{trainer_name}/pokemons/{pokemon_name}")
def delete_pokemon_from_trainer(trainer_name: str, pokemon_name: str):
    response = requests.delete(f"{CRUD_SERVICE_URL}/trainers/{trainer_name}/pokemons/{pokemon_name}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@app.post("/trainers/{trainer_name}/pokemons/{pokemon_name}/evolve")
def evolve_pokemon(trainer_name: str, pokemon_name: str):
    response = requests.post(f"{CRUD_SERVICE_URL}/trainers/{trainer_name}/pokemons/{pokemon_name}/evolve")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@app.get("/images/")
def list_images():
    response = requests.get(f"{IMAGE_SERVICE_URL}/images")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()
    
@app.post("/images/")
def upload_image(file: UploadFile = File(...)):
    response = requests.post(f"{IMAGE_SERVICE_URL}/images")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@app.get("/images/{pokemon_name}")
def get_image(pokemon_name: str):
    response = requests.get(f"{IMAGE_SERVICE_URL}/images/{pokemon_name}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return StreamingResponse(io.BytesIO(response.content), media_type=response.headers["content-type"])
       
