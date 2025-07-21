from app.core.IaC.factories.openstack_cloud_infra_creator import oc_creator
from app.core.queue.factories.rq_queue_creator import rq_creator
from app.core.queue.factories.huey_queue_creator import huey_creator

# get openstack infra creator
def get_infra_creator():
    return oc_creator

# get queue
def get_queue_creator():
    return huey_creator

def common_query_params(region: str, domain: str, project: str, username: str):
    return {
        "region": region,
        "domain": domain,
        "project": project,
        "username": username
    }