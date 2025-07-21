from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from .controllers import ServerController
# from .controllers import ServerActionController
from .schemas import ServerCreateRequest
from .dependencies import get_infra_creator, get_queue_creator, common_query_params

router = APIRouter()
CommonQueryParams = Annotated[dict, Depends(common_query_params)]
infra_creator = get_infra_creator()
q = get_queue_creator().create_queue()

@router.post("/servers")
async def handle_create_server(request: Request,
                               server_create_request: ServerCreateRequest,
                               params: CommonQueryParams):
    try:
        controller = ServerController(request, 
                                      infra_creator,
                                      params)
        # result = controller.create_server(server_create_request)
        q.add_job(controller.create_server, server_create_request=server_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/servers/delete")
async def handle_delete_server(request: Request,
                               server_id: str,
                               params: CommonQueryParams):
    try:
        controller = ServerController(request, 
                                      infra_creator,
                                      params)
        # result = controller.delete_server(server_id)
        q.add_job(controller.delete_server, server_id=server_id)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")