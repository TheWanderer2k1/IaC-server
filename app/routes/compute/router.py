from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from .controllers import ServerController
# from .controllers import ServerActionController
from .schemas import ServerCreateRequest, VolumeAttachmentRequest, ServerUpdateRequest
from .dependencies import get_infra_creator, get_queue_creator, common_query_params
from app.config import logger

router = APIRouter()
CommonQueryParams = Annotated[dict, Depends(common_query_params)]
infra_creator = get_infra_creator()
q = get_queue_creator().create_queue()

@router.post("/servers")
async def handle_create_server(request: Request,
                               server_create_request: ServerCreateRequest,
                               params: CommonQueryParams):
    try:
        controller = ServerController(request, infra_creator, params)
        controller.create_server(server_create_request)
        # q.add_job(controller.create_server, server_create_request=server_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        logger.error(f"Create server failed: {e}")
        raise HTTPException(status_code=500, detail="Create server failed!")
    
@router.put("/servers/{server_id}")
async def handle_update_server(request: Request,
                               server_id: str,
                               server_update_request: ServerUpdateRequest,
                               params: CommonQueryParams):
    try:
        controller = ServerController(request, infra_creator, params)
        # q.add_job(controller.update_server, server_id=server_id, 
        #                                     server_update_request=server_update_request)
        controller.update_server(server_id, server_update_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        logger.error(f"Update server failed: {e}")
        raise HTTPException(status_code=500, detail="Update server failed!")
    
@router.delete("/servers/{server_id}")
async def handle_delete_server(request: Request,
                               server_id: str,
                               params: CommonQueryParams):
    try:
        controller = ServerController(request, infra_creator, params)
        result = controller.delete_server(server_id)
        # q.add_job(controller.delete_server, server_id=server_id)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        logger.error(f"Delete server failed: {e}")
        raise HTTPException(status_code=500, detail="Delete server failed!")
    
@router.post("/servers/{server_id}/os-volume_attachments")
async def handle_attach_volume(request: Request,
                               server_id: str,
                               volume_attachment_request: VolumeAttachmentRequest,
                               params: CommonQueryParams):
    try:
        controller = ServerController(request, infra_creator, params)
        # q.add_job(controller.attach_volume, server_id=server_id, volume_attachment_request=volume_attachment_request)
        controller.attach_volume(server_id, volume_attachment_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        logger.error(f"Attach volume failed: {e}")
        raise HTTPException(status_code=500, detail="Attach volume failed!")

@router.delete("/servers/{server_id}/os-volume_attachments/{volume_id}")
async def handle_detach_volume(request: Request,
                               server_id: str,
                               volume_id: str,
                               params: CommonQueryParams):
    try:
        controller = ServerController(request, infra_creator, params)
        # q.add_job(controller.detach_volume, server_id, volume_id)
        controller.detach_volume(server_id, volume_id)
        return JSONResponse(content={
                "message": "ok"
            },status_code=200)
    except Exception as e:
        logger.error(f"Detach volume failed: {e}")
        raise HTTPException(status_code=500, detail="Detach volume failed!")