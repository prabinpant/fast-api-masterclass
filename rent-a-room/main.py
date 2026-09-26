from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

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


class RoomQueryParams(BaseModel):
    max_price: int | None = Field(ge=10, le=10_000, default=None)
    search: str | None = Field(
        max_length=10,
        min_length=3,
        title="Search keyword",
        description="Type in the keyword that you want to search from",
        default=None,
    )

    @field_validator("search")
    @classmethod
    def fail_if_funny(cls, search: str) -> str:
        if "lol" in search:
            raise ValueError("Being too funny?")
        return search


search_query_validation = Query(
    min_length=3,
    max_length=10,
    title="Search term",
    description="This is a description",
)


@app.get("/health", status_code=200)
def root():
    return {"message": "OK"}


@app.get("/rooms", status_code=200)
def get_rooms(params: Annotated[RoomQueryParams, Query()]):
    collection = [apartment, house, studio]
    search = params.search
    max_price = params.max_price
    return [
        room
        for room in collection
        if (search == None or search.lower() in room["name"].lower())
        and (max_price == None or room["price_per_room"] <= max_price)
    ]


@app.get("/rooms/mansions", status_code=200)
def get_mansions(params: Annotated[RoomQueryParams, Query()]):
    collection = [house]
    search = params.search
    max_price = params.max_price
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
