RESOURCES = {
    "openstack_compute_instance_v2": {
        "region": {}, 
        "name": {}, 
        "image_id": {}, 
        "flavor_id": {},
        "flavor_name": {},
        "user_data": {},
        "security_groups": {},
        "availability_zone_hints": {},
        "availability_zone": {},
        "network": [
            {
                "uuid": {},
                "name": {},
                "port": {},
                "fixed_ip_v4": {},
                "access_network": {},
            }
        ],
        "network_mode": {},
        "metadata": {},
        "config_drive": {},
        "admin_pass": {},
        "key_pair": {},
        "block_device": [
            {
                "uuid": {},
                "source_type": {},
                "volume_size": {},
                "guest_format": {},
                "boot_index": {},
                "destination_type": {},
                "delete_on_termination": {},
                "volume_type": {},
                "device_type": {},
                "disk_bus": {},
                "multiattach": {},
            }
        ],
        "scheduler_hints": {
            "group": {},
            "different_host": {},
            "same_host": {},
            "query": {},
            "target_cell": {},
            "different_cell": {},
            "build_near_host_ip": {},
            "additional_properties": {},
        },
        "personality": {
            "file": {},
            "content": {},
        },
        "stop_before_destroy": {},
        "force_delete": {},
        "power_state": {},
        "tags": {},
        "vendor_options": {
            "ignore_resize_confirmation": {},
            "detach_ports_before_destroy": {},
        },
        "hypervisor_hostname": {},
    },
    "openstack_compute_volume_attach_v2": {
        "region": {}, 
        "instance_id": {},
        "volume_id": {},
        "device": {},
        "multiattach": {},
        "tag": {},
        "vendor_options": {
            "ignore_volume_confirmation": {},
        },
    },
    "openstack_blockstorage_volume_v3": {
        "region": {},
        "size": {},
        "enable_online_resize": {},
        "availability_zone": {},
        "consistency_group_id": {},
        "description": {},
        "metadata": {},
        "name": {},
        "source_replica": {},
        "snapshot_id": {},
        "source_vol_id": {},
        "image_id": {},
        "backup_id": {},
        "volume_type": {},
        "volume_retype_policy": {},
        "scheduler_hints": {
            "different_host": {},
            "same_host": {},
            "local_to_instance": {},
            "query": {},
            "additional_properties": {},
        },
    },
    "openstack_networking_network_v2": {
        "region": {},
        "name": {},
        "description": {},
        "shared": {},
        "external": {},
        "tenant_id": {},
        "admin_state_up": {},
        "segments": [
            {
                "physical_network": {},
                "segmentation_id": {},
                "network_type": {},
            }
        ],
        "value_specs": {},
        "availability_zone_hints": {},
        "tags": {},
        "transparent_vlan": {},
        "port_security_enabled": {},
        "mtu": {},
        "dns_domain": {},
        "qos_policy_id": {},
    },
    "openstack_networking_subnet_v2": {
        "region": {},
        "network_id": {},
        "cidr": {},
        "prefix_length": {},
        "ip_version": {},
        "ipv6_ra_mode": {},
        "name": {},
        "description": {},
        "tenant_id": {},
        "allocation_pools": {
            "start": {},
            "end": {},
        },
        "gateway_ip": {},
        "no_gateway": {},
        "enable_dhcp": {},
        "dns_nameservers": {},
        "dns_publish_fixed_ip": {},
        "service_types": {},
        "segment_id": {},
        "subnetpool_id": {},
        "value_specs": {},
        "tags": {},
    },
    "openstack_networking_router_v2": {
        "region": {},
        "name": {},
        "description": {},
        "admin_state_up": {},
        "distributed": {},
        "external_network_id": {},
        "external_qos_policy_id": {},
        "enable_snat": {},
        "external_fixed_ip": [
            {
                "subnet_id": {},
                "ip_address": {}
            }
        ],
        "external_subnet_ids": [],
        "tenant_id": {},
        "value_specs": {},
        "tags": {},
        "vendor_options": {
            "set_router_gateway_after_create": {}
        },
        "availability_zone_hints": {}
    },
    "openstack_networking_router_interface_v2": {
        "region": {},
        "router_id": {},
        "subnet_id": {},
        "port_id": {},
        "force_destroy": {}
    },
    "openstack_networking_port_v2": {
        "region": {},
        "name": {},
        "description": {},
        "network_id": {},
        "admin_state_up": {},
        "mac_address": {},
        "tenant_id": {},
        "device_owner": {},
        "security_group_ids": [],
        "no_security_groups": {},
        "device_id": {},
        "fixed_ip": [
            {
                "subnet_id": {},
                "ip_address": {}
            }
        ],
        "no_fixed_ip": {},
        "allowed_address_pairs": {
            "ip_address": {},
            "mac_address": {}
        },
        "extra_dhcp_option": {
            "name": {},
            "value": {},
            "ip_version": {}
        },
        "port_security_enabled": {},
        "value_specs": {},
        "tags": {},
        # "binding": {
        #     "host_id": {},
        #     "profile": {},
        #     "vnic_type": {},
        #     "vif_details": {},
        #     "vif_type": {}
        # },
        "dns_name": {},
        "qos_policy_id": {}
    },
    "openstack_networking_floatingip_v2": {
        "region": {},
        "description": {},
        "pool": {},
        "port_id": {},
        "tenant_id": {},
        "address": {},
        "fixed_ip": {},
        "subnet_id": {},
        "subnet_ids": [],
        "value_specs": {},
        "tags": {},
        "dns_name": {},
        "dns_domain": {}
    }
}