from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import bookings, labs, import_excel
from app.ws.routes import router as ws_router

app = FastAPI(title="ELDAR API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(labs.router)
app.include_router(bookings.router)
app.include_router(import_excel.router)
app.include_router(ws_router)

@app.get("/health")
def health(): return {"status": "ok"}
