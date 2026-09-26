from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from pydantic import AfterValidator

app = FastAPI(
    title="Rent a room",
    description="This is for booking stay at rooms",
    version="1.0.0",
    contact={"name": "Prabin Pant Sir", "email": "prabin20panta@gmail.com"},
)

app.mount("/files", StaticFiles(directory="assets"), name="assets")

apartment = {
    "id": 1,
    "name": "Sunny 2-room apartment",
    "price_per_room": 200,
    "bedrooms": 9,
    "bathrooms": 2,
}
house = {
    "id": 5,
    "name": "Dwarikas",
    "price_per_room": 150,
    "bedrooms": 3,
    "bathrooms": 4,
}
studio = {
    "id": 10,
    "name": "Lakeside",
    "price_per_room": 400,
    "bedrooms": 1,
    "bathrooms": 2.5,
}


def fail_if_funny(search: str):
    if "lol" in search:
        raise ValueError("Being too funny?")
    return search


search_query_validation = Query(
    min_length=3,
    max_length=10,
    title="Search term",
    description="This is a description",
)

search_Humor_ban = AfterValidator(fail_if_funny)

SearchQuery = Annotated[str | None, search_query_validation, search_Humor_ban]


@app.get("/health", status_code=200)
def root():
    return {"message": "OK"}


@app.get("/rooms", status_code=200)
def get_rooms(
    max_price: Annotated[int | None, Query(lt=10_000, gt=90)] = None,
    search: SearchQuery = None,
):
    collection = [apartment, house, studio]
    return [
        room
        for room in collection
        if (search == None or search.lower() in room["name"].lower())
        and (max_price == None or room["price_per_room"] <= max_price)
    ]


@app.get("/rooms/mansions", status_code=200)
def get_mansions(
    max_price: Annotated[int | None, Query(lt=10_000, gt=90)] = None,
    search: SearchQuery = None,
):
    collection = [house]
    return [
        room
        for room in collection
        if (search == None or search.lower() in room["name"].lower())
        and (max_price == None or room["price_per_room"] <= max_price)
    ]


@app.get("/rooms/{room_id}", status_code=200)
def get_room_by_id(room_id: int):
    for room in [apartment, house, studio]:
        if room["id"] == room_id:
            return room

    raise HTTPException(404)
