from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from .controllers import ImportController
# from .controllers import ServerActionController
from .schemas import ImportRequest
from .dependencies import get_infra_creator, get_queue_creator, common_query_params
from app.config import logger

router = APIRouter()
CommonQueryParams = Annotated[dict, Depends(common_query_params)]
infra_creator = get_infra_creator()
q = get_queue_creator().create_queue()

@router.post("/import/network")
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
        logger.error(f"Import network failed: {e}")
        raise HTTPException(status_code=500, detail="Import network failed!")
    
@router.post("/import/subnet")
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
        logger.error(f"Import subnet failed: {e}")
        raise HTTPException(status_code=500, detail="Import subnet failed!")
    
@router.post("/import/router")
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
        logger.error(f"Import router failed: {e}")
        raise HTTPException(status_code=500, detail="Import router failed!")
    
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
        logger.error(f"Import router interface failed: {e}")
        raise HTTPException(status_code=500, detail="Import router interface failed!")
    
@router.post("/import/port")
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
        logger.error(f"Import port failed: {e}")
        raise HTTPException(status_code=500, detail="Import port failed!")
    
@router.post("/import/floatingip")
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
        logger.error(f"Import floating ip failed: {e}")
        raise HTTPException(status_code=500, detail="Import floating ip failed!")
    
@router.post("/import/block")
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
        logger.error(f"Import block volume failed: {e}")
        raise HTTPException(status_code=500, detail="Import block volume failed!")
    
@router.post("/import/server")
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
        logger.error(f"Import server failed: {e}")
        raise HTTPException(status_code=500, detail="Import server failed!")