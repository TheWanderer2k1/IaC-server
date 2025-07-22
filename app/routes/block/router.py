from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from .controllers import BlockVolumeController
from .schemas import BlockVolumeCreateRequest
from .dependencies import get_infra_creator, get_queue_creator, common_query_params

router = APIRouter()
CommonQueryParams = Annotated[dict, Depends(common_query_params)]
oc_creator = get_infra_creator()
q = get_queue_creator().create_queue()

@router.post("/v3/{project_id}/volumes")
async def handle_create_volume(request: Request,
                               project_id: str,
                               block_volume_create_request: BlockVolumeCreateRequest,
                               params: CommonQueryParams):
    try:
        controller = BlockVolumeController(request,
                                           oc_creator,
                                           params)
        q.add_job(controller.create_volume, block_volume_create_request=block_volume_create_request)
        # controller.create_volume(block_volume_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/v3/{project_id}/volumes/{volume_id}")
async def handle_delete_volume(request: Request,
                               project_id: str,
                               volume_id: str,
                               params: CommonQueryParams):
    try:
        controller = BlockVolumeController(request,
                                           oc_creator,
                                           params)
        # result = controller.delete_server(server_id)
        q.add_job(controller.delete_volume, project_id=project_id, volume_id=volume_id)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")