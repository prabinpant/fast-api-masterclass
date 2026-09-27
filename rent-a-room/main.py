from enum import Enum
from typing import Annotated, Literal

from fastapi import Cookie, FastAPI, Header, HTTPException, Query, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, StringConstraints, field_validator

openapi_tags = [{"name": "rooms", "description": "The **routes** for rooms"}]

app = FastAPI(
    title="Rent a room",
    description="This is for booking stay at rooms",
    version="1.0.0",
    contact={"name": "Prabin Pant Sir", "email": "prabin20panta@gmail.com"},
    openapi_tags=openapi_tags,
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


class AppCookies(BaseModel):
    theme: Literal["light", "dark"] = "dark"
    language: Literal["en", "np"] = "np"

    @field_validator("theme", mode="before")
    @classmethod
    def check_valid_language(cls, theme: str) -> str:
        return theme if theme in ["light", "dark"] else "dark"


class AppHeaders(BaseModel):
    user_agent: str | None = None


class RoomQueryParams(BaseModel):
    max_price: int | None = Field(ge=10, le=10_000, default=None)
    search: Annotated[str | None, StringConstraints(to_lower=True)] = Field(
        max_length=10,
        min_length=3,
        title="Search keyword",
        description="Type in the keyword that you want to search from",
        default=None,
        examples=["haribahadur"],
    )

    @field_validator("search")
    @classmethod
    def fail_if_funny(cls, search: str) -> str:
        if "lol" in search:
            raise ValueError("Being too funny?")
        return search


@app.get("/health", status_code=200)
def root(
    cookies: Annotated[AppCookies, Cookie()], headers: Annotated[AppHeaders, Header()]
):

    print(headers.user_agent)

    greetings = {"en": "Health is okay", "np": "Thik cha hajur"}

    message = greetings.get(cookies.language)

    return {"message": message}


@app.get(
    "/rooms",
    status_code=200,
    tags=["rooms"],
    summary="List all available rooms",
    description="Veryy detailed info bro",
    response_description="Khai k ho",
)
def get_rooms(params: Annotated[RoomQueryParams, Query()]):
    collection = [apartment, house, studio]
    search = params.search
    max_price = params.max_price
    return [
        room
        for room in collection
        if (search == None or search in room["name"].lower())
        and (max_price == None or room["price_per_room"] <= max_price)
    ]


@app.get("/rooms/mansions", status_code=200, tags=["rooms"], deprecated=True)
def get_mansions(params: Annotated[RoomQueryParams, Query()]):
    collection = [house]
    search = params.search
    max_price = params.max_price
    return [
        room
        for room in collection
        if (search == None or search in room["name"].lower())
        and (max_price == None or room["price_per_room"] <= max_price)
    ]


@app.get("/rooms/{room_id}", status_code=200, tags=["rooms"])
def get_room_by_id(room_id: int):
    for room in [apartment, house, studio]:
        if room["id"] == room_id:
            return room

    raise HTTPException(404)


@app.get("/preferences", status_code=200, tags=["preferences"])
def set_preferences(response: Response):

    app_cookies = AppCookies()

    response.set_cookie(key="theme", value=app_cookies.theme)
    response.set_cookie(key="language", value=app_cookies.language)

    return {"message": "Preferences updated"}
