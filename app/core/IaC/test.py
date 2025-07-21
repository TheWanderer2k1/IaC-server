import pydot

if __name__ == "__main__":
    tf_graph_string = """
    digraph G {
  rankdir = "RL";
  node [shape = rect, fontname = "sans-serif"];
  "openstack_identity_project_v3.vpc01" [label="openstack_identity_project_v3.vpc01"];
  "openstack_identity_project_v3.vpc01_default_project" [label="openstack_identity_project_v3.vpc01_default_project"];
  "openstack_identity_role_assignment_v3.vpc01_admin_role_assignment" [label="openstack_identity_role_assignment_v3.vpc01_admin_role_assignment"];
  "openstack_identity_user_v3.vpc01_admin" [label="openstack_identity_user_v3.vpc01_admin"];
  "openstack_networking_network_v2.shared_network_1" [label="openstack_networking_network_v2.shared_network_1"];
  "openstack_networking_router_interface_v2.shared_network_1_router_interface" [label="openstack_networking_router_interface_v2.shared_network_1_router_interface"];
  "openstack_networking_router_v2.shared_network_1_router" [label="openstack_networking_router_v2.shared_network_1_router"];
  "openstack_networking_subnet_v2.shared_network_1_subnet" [label="openstack_networking_subnet_v2.shared_network_1_subnet"];
  "openstack_identity_project_v3.vpc01_default_project" -> "openstack_identity_project_v3.vpc01";
  "openstack_identity_role_assignment_v3.vpc01_admin_role_assignment" -> "openstack_identity_user_v3.vpc01_admin";
  "openstack_identity_user_v3.vpc01_admin" -> "openstack_identity_project_v3.vpc01_default_project";
  "openstack_networking_network_v2.shared_network_1" -> "openstack_identity_user_v3.vpc01_admin";
  "openstack_networking_router_interface_v2.shared_network_1_router_interface" -> "openstack_networking_router_v2.shared_network_1_router";
  "openstack_networking_router_interface_v2.shared_network_1_router_interface" -> "openstack_networking_subnet_v2.shared_network_1_subnet";
  "openstack_networking_router_v2.shared_network_1_router" -> "openstack_identity_user_v3.vpc01_admin";
  "openstack_networking_subnet_v2.shared_network_1_subnet" -> "openstack_networking_network_v2.shared_network_1";
}
"""
    graph = pydot.graph_from_dot_data(tf_graph_string)[0]
    
    for vertex in graph.get_nodes():
        print(f"Vertex: {vertex.get_name()}")