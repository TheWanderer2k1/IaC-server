from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from .controllers import InfraController
from .schemas import InfraPreset1Request
from .dependencies import get_infra_creator, get_queue_creator, common_query_params
import pickle

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
        q.add_infra_job(request.client.host, controller, "provision_infra_vdi", infra_preset1_request=infra_preset1_request)
        return JSONResponse(content={"message": "Infra is being provisioned"}, status_code=202)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Provision infra failed!: {e}")
    
@router.get("/infra/test")
async def test_route(request: Request):
    try:
        q.add_job(request.client.host, InfraController.delayed_response)
        return JSONResponse(content={"message": f"Test route is working: {request.client.host}"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test route failed: {str(e)}")
