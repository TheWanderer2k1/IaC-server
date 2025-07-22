from fastapi import FastAPI
from app.middlewares.auth import AuthMiddleware
from app.routes.identity.router import router as IdentityRouter
from app.routes.compute.router import router as ComputeRouter
from app.routes.block.router import router as BlockRouter

app = FastAPI()
app.add_middleware(AuthMiddleware)
app.include_router(IdentityRouter)
app.include_router(ComputeRouter)
app.include_router(BlockRouter)