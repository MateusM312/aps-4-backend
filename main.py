from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import eventos_router, participantes_routers, usuario_router, auth_router
from database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Gerenciamento de eventos acadêmicos - Santana & Mendes")

@app.get("/")
def raiz():
    return {"Alerta de Sucesso":"Hello World!"}

app.include_router(eventos_router.router)
app.include_router(participantes_routers.router)
app.include_router(usuario_router.router)
app.include_router(auth_router.router)