from fastapi import APIRouter, Body, Response, HTTPException
from typing import Annotated
from .controller import AuthController
from .schemas import AuthRequest
from app.config import logger

router = APIRouter(
    prefix="/v3/auth"
)

@router.post("/tokens")
async def handle_authentication(auth: Annotated[AuthRequest, Body(embed=True)], response: Response):
    try:
        return await AuthController.authentication(auth, response)
    except Exception as e:
        logger.error(f"Error when authenticate user: {e}")
        raise HTTPException(status_code=500, detail="Error occured!")
