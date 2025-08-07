from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from .controllers import NetworkController
# from .controllers import ServerActionController
from .schemas import NetworkCreateRequest, SubnetCreateRequest, RouterCreateRequest, AddInterfaceRouterRequest, PortCreateRequest, NetworkUpdateRequest, SubnetUpdateRequest, FloatingIpCreateRequest
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
        # controller.create_network(network_create_request)
        q.add_infra_job(request.client.host, controller, "create_network", network_create_request=network_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Create network failed!")
    
@router.put("/v2.0/networks/{network_id}")
async def handle_update_network(request: Request,
                                network_id: str,
                                network_update_request: NetworkUpdateRequest,
                                params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        # controller.update_network(network_id, network_update_request)
        q.add_infra_job(request.client.host, controller, "update_network", network_id=network_id,
                                                                            network_update_request=network_update_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Update network failed!")
    
@router.delete("/v2.0/networks/{network_id}")
async def handle_delete_network(request: Request,
                               network_id: str,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        # result = controller.delete_network(network_id)
        q.add_infra_job(request.client.host, controller, "delete_network", network_id=network_id)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Delete network failed!")
    
@router.post("/v2.0/subnets")
async def handle_create_subnet(request: Request,
                               subnet_create_request: SubnetCreateRequest,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        # controller.create_subnet(subnet_create_request)
        q.add_infra_job(request.client.host, controller, "create_subnet", subnet_create_request=subnet_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Create subnet failed!")

@router.put("/v2.0/subnets/{subnet_id}")
async def handle_update_subnet(request: Request,
                               subnet_id: str,
                               subnet_update_request: SubnetUpdateRequest,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        # controller.update_subnet(subnet_id, subnet_update_request)
        q.add_infra_job(request.client.host, controller, "update_subnet", subnet_update_request=subnet_update_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Update subnet failed!")

@router.delete("/v2.0/subnets/{subnet_id}")
async def handle_delete_subnet(request: Request,
                               subnet_id: str,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        # controller.delete_subnet(subnet_id)
        q.add_infra_job(request.client.host, controller, "delete_subnet", subnet_id=subnet_id)
        return JSONResponse(content={
                "message": "ok"
            },status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Delete subnet failed!")
    
@router.post("/v2.0/routers")
async def handle_create_router(request: Request,
                               router_create_request: RouterCreateRequest,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        # controller.create_router(router_create_request)
        q.add_infra_job(request.client.host, controller, "create_router", router_create_request=router_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Create router failed!")
    
@router.delete("/v2.0/routers/{router_id}")
async def handle_delete_router(request: Request,
                               router_id: str,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        # controller.delete_router(router_id)
        q.add_infra_job(request.client.host, controller, "delete_router", router_id=router_id)
        return JSONResponse(content={
                "message": "ok"
            },status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Delete router failed!")
    
@router.put("/v2.0/routers/{router_id}/add_router_interface")
async def handle_add_router_interface(request: Request,
                               router_id: str,
                               add_interface_to_router: AddInterfaceRouterRequest,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        # controller.add_interface_to_router(router_id, add_interface_to_router)
        q.add_infra_job(request.client.host, controller, "add_interface_to_router", router_id=router_id, 
                                                                                    add_interface_to_router=add_interface_to_router)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Add interface to router failed!")
    
@router.put("/v2.0/routers/{router_id}/remove_router_interface")
async def handle_remove_router_interface(request: Request,
                               router_id: str,
                               add_interface_to_router: AddInterfaceRouterRequest,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        # controller.remove_interface_from_router(router_id, add_interface_to_router)
        q.add_infra_job(request.client.host, controller, "remove_interface_from_router", router_id=router_id, 
                                                                                        add_interface_to_router=add_interface_to_router)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Remove router interface failed!")
    
@router.post("/v2.0/ports")
async def handle_create_port(request: Request,
                               port_create_request: PortCreateRequest,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        # controller.create_port(port_create_request)
        q.add_infra_job(request.client.host, controller, "create_port", port_create_request=port_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Create port failed!")
    
@router.delete("/v2.0/ports/{port_id}")
async def handle_delete_port(request: Request,
                               port_id: str,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        # controller.delete_port(port_id)
        q.add_infra_job(request.client.host, controller, "delete_port", port_id=port_id)
        return JSONResponse(content={
                "message": "ok"
            },status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Delete port failed!")
    

@router.post("/v2.0/floatingips")
async def handle_create_floatingip(request: Request,
                                    floating_ip_create_request: FloatingIpCreateRequest,
                                    params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        # controller.create_floating_ip(floating_ip_create_request)
        q.add_infra_job(request.client.host, controller, "create_floating_ip", floating_ip_create_request=floating_ip_create_request)
        return JSONResponse(content={
            "message": "ok"
        },status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Create floating ip failed!")    
    
@router.delete("/v2.0/floatingips/{floating_ip_id}")
async def handle_delete_floatingip(request: Request,
                               floating_ip_id: str,
                               params: CommonQueryParams):
    try:
        controller = NetworkController(request, infra_creator, params)
        # controller.delete_floating_ip(floating_ip_id)
        q.add_infra_job(request.client.host, controller, "delete_floating_ip", floating_ip_id=floating_ip_id)
        return JSONResponse(content={
                "message": "ok"
            },status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Delete floating ip failed!")
