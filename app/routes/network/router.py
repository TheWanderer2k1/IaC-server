from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from .controllers import NetworkController
# from .controllers import ServerActionController
from .schemas import NetworkCreateRequest, SubnetCreateRequest, RouterCreateRequest, AddInterfaceRouterRequest, PortCreateRequest
from .dependencies import get_infra_creator, get_queue_creator, common_query_params

router = APIRouter()
CommonQueryParams = Annotated[dict, Depends(common_query_params)]
infra_creator = get_infra_creator()
q = get_queue_creator().create_queue()

@router.post("/v2.0/networks")
async def handle_create_network(request: Request,
                               network_create_request: NetworkCreateRequest,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        # result = controller.create_network(network_create_request)
        q.add_job(controller.create_network, network_create_request=network_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.delete("/v2.0/networks/{network_id}")
async def handle_delete_network(request: Request,
                               network_id: str,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        # result = controller.delete_server(server_id)
        q.add_job(controller.delete_network, network_id=network_id)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/v2.0/subnets")
async def handle_create_subnet(request: Request,
                               subnet_create_request: SubnetCreateRequest,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        q.add_job(controller.create_subnet, subnet_create_request=subnet_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@router.delete("/v2.0/subnets/{subnet_id}")
async def handle_delete_subnet(request: Request,
                               subnet_id: str,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        q.add_job(controller.detach_volume, subnet_id=subnet_id)
        return JSONResponse(content={
                "message": "ok"
            },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/v2.0/routers")
async def handle_create_router(request: Request,
                               router_create_request: RouterCreateRequest,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        q.add_job(controller.create_router, router_create_request=router_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.delete("/v2.0/routers/{router_id}")
async def handle_delete_router(request: Request,
                               router_id: str,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        q.add_job(controller.delete_router, router_id=router_id)
        return JSONResponse(content={
                "message": "ok"
            },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.put("/v2.0/routers/{router_id}/add_router_interface")
async def handle_create_router(request: Request,
                               router_id: str,
                               add_interface_to_router: AddInterfaceRouterRequest,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        q.add_job(controller.add_interface_to_router, router_id=router_id, add_interface_to_router=add_interface_to_router)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.put("/v2.0/routers/{router_id}/remove_router_interface")
async def handle_create_router(request: Request,
                               router_id: str,
                               add_interface_to_router: AddInterfaceRouterRequest,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        q.add_job(controller.remove_interface_from_router, router_id=router_id, add_interface_to_router=add_interface_to_router)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/v2.0/ports")
async def handle_create_port(request: Request,
                               port_create_request: PortCreateRequest,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        q.add_job(controller.create_port, port_create_request=port_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.delete("/v2.0/ports/{port_id}")
async def handle_delete_port(request: Request,
                               port_id: str,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        q.add_job(controller.delete_port, port_id=port_id)
        return JSONResponse(content={
                "message": "ok"
            },status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
