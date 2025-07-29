from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from .controllers import BlockVolumeController
from .schemas import BlockVolumeCreateRequest, VolumeUpdateRequest
from .dependencies import get_infra_creator, get_queue_creator, common_query_params
from app.config import logger

router = APIRouter()
CommonQueryParams = Annotated[dict, Depends(common_query_params)]
infra_creator = get_infra_creator()
q = get_queue_creator().create_queue()

@router.post("/v3/{project_id}/volumes")
async def handle_create_volume(request: Request,
                               project_id: str,
                               block_volume_create_request: BlockVolumeCreateRequest,
                               params: CommonQueryParams):
    try:
        controller = BlockVolumeController(request,
                                           infra_creator,
                                           params)
        # q.add_job(controller.create_volume, block_volume_create_request=block_volume_create_request)
        controller.create_volume(block_volume_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        logger.error(f"Create volume failed: {e}")
        raise HTTPException(status_code=500, detail="Create volume failed!")
    
@router.put("/v3/{project_id}/volumes/{volume_id}")
async def handle_update_volume(request: Request,
                               project_id: str,
                               volume_id: str,
                               volume_update_request: VolumeUpdateRequest,
                               params: CommonQueryParams):
    try:
        controller = BlockVolumeController(request, infra_creator, params)
        # q.add_job(controller.update_volume, project_id=project_id,
        #                                     volume_id=volume_id, 
        #                                     volume_update_request=volume_update_request)
        controller.update_volume(project_id, volume_id, volume_update_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        logger.error(f"Update volume failed: {e}")
        raise HTTPException(status_code=500, detail="Update volume failed!")
    
@router.delete("/v3/{project_id}/volumes/{volume_id}")
async def handle_delete_volume(request: Request,
                               project_id: str,
                               volume_id: str,
                               params: CommonQueryParams):
    try:
        controller = BlockVolumeController(request,
                                           infra_creator,
                                           params)
        # q.add_job(controller.delete_volume, project_id=project_id, volume_id=volume_id)
        controller.delete_volume(project_id, volume_id)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        logger.error(f"Delete volume failed: {e}")
        raise HTTPException(status_code=500, detail="Delete volume failed!")