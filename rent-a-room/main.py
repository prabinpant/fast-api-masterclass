from fastapi import FastAPI

app = FastAPI(
    title="Rent a room",
    description="This is for booking stay at rooms",
    version="1.0.0",
    contact={"name": "Prabin Pant Sir", "email": "prabin20panta@gmail.com"},
)

apartment = {
    "id": 1,
    "name": "Sunny 2-room apartment",
    "price_per_room": 200,
    "bedrooms": 9,
    "bathrooms": 2,
}
house = {
    "id": 5,
    "name": "Sunny 2-room apartment",
    "price_per_room": 150,
    "bedrooms": 3,
    "bathrooms": 4,
}
studio = {
    "id": 10,
    "name": "Sunny 2-room apartment",
    "price_per_room": 400,
    "bedrooms": 1,
    "bathrooms": 2.5,
}


@app.get("/health", status_code=200)
def root():
    return {"message": "OK"}


@app.get("/rooms", status_code=200)
def get_rooms():

    return [apartment, house, studio]


@app.get("/rooms/{room_id}", status_code=200)
def get_room_by_id(room_id: int):
    for room in [apartment, house, studio]:
        if room["id"] == room_id:
            return room
