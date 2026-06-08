from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_methods=["*"],
    allow_headers=["*"])

@app.get("/orders")
async def get_orders():
    return [
        {"id": 1, "product_id": 1, "quantity": 2, "total_price": 21.98},
        {"id": 2, "product_id": 2, "quantity": 1, "total_price": 19.99},
        {"id": 3, "product_id": 3, "quantity": 3, "total_price": 17.97},
    ]