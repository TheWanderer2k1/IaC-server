from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from .controllers import InfraController
from .schemas import InfraPreset1Request
from .dependencies import get_infra_creator, get_queue_creator, common_query_params
from app.config import logger

router = APIRouter()
CommonQueryParams = Annotated[dict, Depends(common_query_params)]
infra_creator = get_infra_creator()
q = get_queue_creator().create_queue()

@router.post("/infra")
async def handle_provision_infra(request: Request,
                                 infra_preset1_request: InfraPreset1Request,
                                 params: CommonQueryParams):
    try:
        controller = InfraController(request, infra_creator, params)
        state = controller.provision_infra_preset1(infra_preset1_request)
        # q.add_job(controller.create_server, server_create_request=server_create_request)
        return JSONResponse(content=state,status_code=200)
    except Exception as e:
        logger.error(f"Provision infra failed: {e}")
        raise HTTPException(status_code=500, detail="Provision infra failed!")