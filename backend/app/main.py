from fastapi import FastAPI
from app.api.routes import bookings
app = FastAPI(title="ELDAR API")
app.include_router(bookings.router)
@app.get("/health")
def health(): return {"status": "ok"}