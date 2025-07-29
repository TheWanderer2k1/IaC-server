import json
import pydot
from pathlib import Path
from app.config import settings
from app.core.IaC.lib.graph import DirectedAcyclicGraph
from .openstack_resource import RESOURCES
from app.core.IaC.interfaces.cloud_infra_interface import ICloudInfrastructure
from app.core.IaC.lib.Terraform.tf import Terraform # chỗ này nên dùng DI và interface để có thể mở rộng sang tool khác (OpenTofu)
from app.utils.utils import Utils

class OpenStackCloudInfrastructure(ICloudInfrastructure):
    def __init__(self, path_to_tf_workspace, 
                    provider_version, 
                    auth_url, 
                    region,
                    token,  # Use token for authentication
                    tenant_name,
                    endpoint_overrides):
        self.path_to_tf_workspace = path_to_tf_workspace
        self.tf = Terraform(self.path_to_tf_workspace)  # Đang bị gán cứng dùng Terraform
        # initialize the infrastructure dictionary with required providers and resources
        self.infra_dict = {
            "terraform": {
                "required_providers": {
                    "openstack": {
                        "source": "terraform-provider-openstack/openstack",
                        "version": provider_version
                    }
                }
            },
            "provider": {
                "openstack": {
                    "auth_url": auth_url,
                    "region": region,
                    "token": token,  # Use token for authentication
                    "tenant_name": tenant_name
                }
            },
            "resource": {}
        }
        # endpoint overrides
        if endpoint_overrides:
            self.infra_dict["provider"]["openstack"]["endpoint_overrides"] = endpoint_overrides
        # init the user environment if not exists
        dir_path = Path(self.path_to_tf_workspace)
        dir_path.mkdir(parents=True, exist_ok=True)
        # # check if IaC config file is exist
        # file = Path(f"{self.path_to_tf_workspace}/main.tf.json")
        # if not file.is_file():
        self.output_infrastructure()
        self.tf.init()
        self._refresh_infrastructure()
        self.infra_graph = DirectedAcyclicGraph()
        self._construct_infrastructure_dict()
        # self._construct_infrastructure_graph_in_reverse()
    
    def _refresh_infrastructure(self):
        try:
            result = self.tf.refresh()
            # print(result)
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

    def _construct_infrastructure_dict(self):
        try:
            json_output = self.tf.show_json()
            state_data = json.loads(json_output)
            for tf_resource in state_data.get('values', {}).get('root_module', {}).get('resources', []):
                resource_type = tf_resource['type']
                resource_name = tf_resource['name']
                resource_values = self._filter_attributes(resource_type, tf_resource['values'])
                if tf_resource.get('depends_on'):
                    resource_values['depends_on'] = tf_resource['depends_on']
                if resource_type not in self.infra_dict['resource']:
                    self.infra_dict['resource'][resource_type] = {}
                self.infra_dict['resource'][resource_type][resource_name] = resource_values
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

    def _construct_infrastructure_graph(self):
        try:
            result = self.tf.graph()
            graph = pydot.graph_from_dot_data(result)[0]
            for vertex in graph.get_nodes():
                if vertex.get_name() not in ('node', 'edge', 'graph'):
                    vertex_name = vertex.get_name().replace('"', '')
                    self.infra_graph.add_vertex(vertex_name)
            for edge in graph.get_edges():
                from_vertex = edge.get_source().replace('"', '')
                to_vertex = edge.get_destination().replace('"', '')
                self.infra_graph.add_edge(from_vertex, to_vertex)
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")
    
    # Reverse the graph so that when deleting cascade, it will save computation cost
    def _construct_infrastructure_graph_in_reverse(self):
        try:
            result = self.tf.graph()
            graph = pydot.graph_from_dot_data(result)[0]
            for vertex in graph.get_nodes():
                if vertex.get_name() not in ('node', 'edge', 'graph'):
                    vertex_name = vertex.get_name().replace('"', '')
                    self.infra_graph.add_vertex(vertex_name)
            for edge in graph.get_edges():
                from_vertex = edge.get_destination().replace('"', '')
                to_vertex = edge.get_source().replace('"', '')
                self.infra_graph.add_edge(from_vertex, to_vertex)
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")
    
    # need review
    # need to filter out null, empty, "" values (falsy values)
    # need avoid conflic between attributes and nested attributes
    def _filter_attributes(self, type, attributes_dict):
        for key in attributes_dict.copy():
            if key not in RESOURCES[type]: # remove attributes not in the resource type
                del attributes_dict[key]
            elif not attributes_dict[key]:  # remove falsy values
                del attributes_dict[key]
            elif isinstance(attributes_dict[key], dict) and attributes_dict[key]: # remove nested attributes not in the resource type
                for nested_key in attributes_dict[key].copy():
                    if nested_key not in RESOURCES[type][key]:
                        del attributes_dict[key][nested_key]
            elif isinstance(attributes_dict[key], list) and attributes_dict[key]: # remove nested attributes not in the resource type
                for nested_element in attributes_dict[key]:
                    if isinstance(nested_element, dict):
                        for nested_key in nested_element.copy():
                            if (not RESOURCES[type][key][0]) or (nested_key not in RESOURCES[type][key][0]):
                                del nested_element[nested_key]
        return attributes_dict

    def add_resource(self, resource_type, resource_name, resource_values, depends_on=None):
        if depends_on:
            resource_values['depends_on'] = depends_on
        if resource_type not in self.infra_dict['resource']:
            self.infra_dict['resource'][resource_type] = {}
        self.infra_dict['resource'][resource_type][resource_name] = resource_values

    def modify_resource(self, resource_type, resource_name, resource_values, depends_on=None):
        if resource_type not in self.infra_dict['resource'] or resource_name not in self.infra_dict['resource'][resource_type]:
            raise Exception(f"Resource {resource_name} of type {resource_type} does not exist.")
        if depends_on:
            resource_values['depends_on'] = depends_on
        self.infra_dict['resource'][resource_type][resource_name].update(resource_values)

    def delete_resource(self, resource_type, resource_name):
        if resource_type not in self.infra_dict['resource'] or resource_name not in self.infra_dict['resource'][resource_type]:
            raise Exception(f"Resource {resource_name} of type {resource_type} does not exist.")
        # construct infrastructure graph for deletion
        self._construct_infrastructure_graph_in_reverse()
        try:
            nodes_to_remove = self.infra_graph.remove_vertext_cascade_reverse(f"{resource_type}.{resource_name}")
            for node in nodes_to_remove:
                type, name = node.split('.')
                del self.infra_dict['resource'][type][name]
        except Exception as e:
            raise Exception(f"An error occurred while deleting resource {resource_name} of type {resource_type}: {e}")

    def output_infrastructure(self):
        try:
            # remove all null key-value
            final_infra_dict = Utils.remove_null_values(self.infra_dict)
            # generate config file
            with open(f"{self.path_to_tf_workspace}/main.tf.json", "w") as f:
                json.dump(final_infra_dict, f, indent=2)
            # # debug
            # print(json.dumps(self.infra_dict, indent=2))
        except Exception as e:
            raise Exception(f"An error occurred while saving the infrastructure: {e}")
    
    def apply_infrastructure(self):
        try:
            # tf apply
            result = self.tf.apply()
            print(result)
        except Exception as e:
            raise Exception(f"An unexpected error occurred when apply: {e}")
    
    def destroy_infrastructure(self):
        try:
            result = self.tf.destroy()
            print(result)
        except Exception as e:
            raise Exception(f"An unexpected error occurred when destroy: {e}")
        
    def import_resource(self, resource_type, resource_name, resource_id):
        try:
            # add resource placeholder in config file
            if resource_type not in self.infra_dict['resource']:
                self.infra_dict['resource'][resource_type] = {}
            self.infra_dict['resource'][resource_type][resource_name] = {}
            # generate config file
            with open(f"{self.path_to_tf_workspace}/main.tf.json", "w") as f:
                json.dump(self.infra_dict, f, indent=2)
            result = self.tf.import_resource(f"{resource_type}.{resource_name}", resource_id)
            print(result)
        except Exception as e:
            raise Exception(f"An unexpected error occurred when import: {e}")
