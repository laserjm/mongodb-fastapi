from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from model import Letter

from database import (
    fetch_one_letter,
    fetch_one_letter_by_id,
    fetch_all_letters,
    create_letter,
    update_letter,
    remove_letter
)

origins = ['https://lolcahost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello":"World2"}

@app.get("/api/letter", response_model=List[Letter])
async def get_letter():
    response = await fetch_all_letters()
    return response

@app.get("/api/letter/{id}", response_description="Get a single letter", response_model=Letter)
async def show_letter(id: str):
    response = await fetch_one_letter_by_id(id)
    if response:
        return response
    raise HTTPException(404, "das war nix")

# @app.get("/api/letter/{title}", response_model=Letter)
# async def get_letter(title):
#     response = await fetch_one_letter(title)
#     if response:
#         return response
#     raise HTTPException(404, "das war nix")

@app.post("/api/letter/", response_model=Letter)
async def post_letter(letter: Letter):
    response = await create_letter(letter.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@app.put("/api/letter/{title}/", response_description="Update a letter", response_model=Letter)
async def put_letter(title: str, desc: str):
    response = await update_letter(title, desc)
    if response:
        return response
    raise HTTPException(404, f"There is no letter with the title {title}")

@app.delete("/api/todo/{title}")
async def delete_todo(title):
    response = await remove_letter(title)
    if response:
        return "Successfully deleted letter"
    raise HTTPException(404, f"There is no todo with the title {title}")