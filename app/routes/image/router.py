from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from .controllers import ImageController
from typing import Annotated
from .dependencies import get_infra_creator, common_query_params

router = APIRouter()
CommonQueryParams = Annotated[dict, Depends(common_query_params)]
infra_creator = get_infra_creator()

@router.get("/images")
async def handle_get_images(request: Request, params: CommonQueryParams):
    try:
        controller = ImageController(request, infra_creator, params)
        images = await controller.get_images()
        return JSONResponse(content=images, status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Get images failed!")