from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import router as chat_router

app = FastAPI(title="Cosmetic IA API")

# ✅ 1. LE CORS (Indispensable)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 2. LES ROUTES (Sans conflit de préfixe)
# On inclut le chat_router. 
# Si dans chat.py tu as @router.post("/chat"), l'URL sera /api/chat
app.include_router(chat_router, prefix="/api")

# ✅ 3. ROUTE DE TEST (À la racine pour être sûr)
@app.get("/")
def health():
    return {"status": "ok", "message": "Serveur opérationnel ✅"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)