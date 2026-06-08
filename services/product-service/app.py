from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000", "http://localhost:3001"], allow_methods=["*"], allow_headers=["*"])

@app.get("/products")
async def get_products():
    return [
        {"id": 1, "name": "Product 1", "price": 10.99},
        {"id": 2, "name": "Product 2", "price": 19.99},
        {"id": 3, "name": "Product 3", "price": 5.99},
    ]