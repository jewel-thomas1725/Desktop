from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Bloom data model
class BloomData(BaseModel):
    species: str
    color: str
    bloom_intensity: float  # 0-1 scale

# Mock bloom data (lat, lon -> flower info)
flower_map = {
    (10.5, 76.2): [
        {"species": "Marigold", "color": "orange", "bloom_intensity": 0.8},
        {"species": "Jasmine", "color": "white", "bloom_intensity": 0.5},
    ],
    (28.6, 77.2): [
        {"species": "Sunflower", "color": "yellow", "bloom_intensity": 0.9}
    ]
}

@app.get("/api/bloom", response_model=List[BloomData])
def get_bloom(lat: float, lon: float, date: str):
    key = (round(lat, 1), round(lon, 1))
    return flower_map.get(key, [])
