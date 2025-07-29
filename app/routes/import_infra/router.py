from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from .controllers import ImportController
# from .controllers import ServerActionController
from .schemas import ImportRequest
from .dependencies import get_infra_creator, get_queue_creator, common_query_params

router = APIRouter()
CommonQueryParams = Annotated[dict, Depends(common_query_params)]
infra_creator = get_infra_creator()
q = get_queue_creator().create_queue()

@router.post("/import/networks")
async def handle_import_network(request: Request,
                               import_request: ImportRequest,
                               params: CommonQueryParams):
    try:
        controller = ImportController(request, infra_creator, params)
        controller.import_network(import_request)
        # q.add_job(controller.create_network, network_create_request=network_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/import/subnets")
async def handle_import_subnet(request: Request,
                               import_request: ImportRequest,
                               params: CommonQueryParams):
    try:
        controller = ImportController(request, infra_creator, params)
        controller.import_subnet(import_request)
        # q.add_job(controller.create_network, network_create_request=network_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/import/routers")
async def handle_import_router(request: Request,
                               import_request: ImportRequest,
                               params: CommonQueryParams):
    try:
        controller = ImportController(request, infra_creator, params)
        controller.import_router(import_request)
        # q.add_job(controller.create_network, network_create_request=network_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/import/router_interface")
async def handle_import_router_interface(request: Request,
                               import_request: ImportRequest,
                               params: CommonQueryParams):
    try:
        controller = ImportController(request, infra_creator, params)
        controller.import_router_interface(import_request)
        # q.add_job(controller.create_network, network_create_request=network_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/import/ports")
async def handle_import_port(request: Request,
                               import_request: ImportRequest,
                               params: CommonQueryParams):
    try:
        controller = ImportController(request, infra_creator, params)
        controller.import_port(import_request)
        # q.add_job(controller.create_network, network_create_request=network_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/import/floatingips")
async def handle_import_floatingip(request: Request,
                               import_request: ImportRequest,
                               params: CommonQueryParams):
    try:
        controller = ImportController(request, infra_creator, params)
        controller.import_floatingip(import_request)
        # q.add_job(controller.create_network, network_create_request=network_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/import/blocks")
async def handle_import_blockvol(request: Request,
                               import_request: ImportRequest,
                               params: CommonQueryParams):
    try:
        controller = ImportController(request, infra_creator, params)
        controller.import_blockvol(import_request)
        # q.add_job(controller.create_network, network_create_request=network_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/import/servers")
async def handle_import_server(request: Request,
                               import_request: ImportRequest,
                               params: CommonQueryParams):
    try:
        controller = ImportController(request, infra_creator, params)
        controller.import_server(import_request)
        # q.add_job(controller.create_network, network_create_request=network_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")