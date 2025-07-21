from app.core.IaC.factories.openstack_cloud_infra_creator import OpenStackCloudInfrastructureCreator

if __name__ == "__main__":
    try:
        oc_creator = OpenStackCloudInfrastructureCreator()
        oc_infra = oc_creator.create_infrastructure(
            path_to_tf_workspace="D:\Terraform\openstack-init",
            provider_version="3.0.0",
            auth_url="http://controller:5000/v3",
            region="RegionOne",
            # user_name="user01",
            # password="hoanganh",
            token=r"gAAAAABoZdmS7r1sY2YhWG8gwhXkHLkmz773HDn3vJ88xFFliO955MX86OzYkY7Iombs_NIfZWNgivxm6zeePUDscS-98O7KtBJbP6XsaDFFjQ54jOoMjlW1sniqLTCwzELSO4VvuA1Tf6SLlfdjrj9FMY1iGsecyRb3rYcoGO9ZNUvio0hVxCQ",  # Use token for authentication
            tenant_name="normal-project-01"
        )

        # oc_infra.add_resource(
        #     tf_resource_type="openstack_compute_instance_v2",       # resource type, get from config 
        #     tf_resource_name="test_instance_firsttime_init",        # unique name, auto genrated
        #     tf_resource_values={                                    # resource attributes, get from api that user call
        #         "name": "test_instance_firsttime_init",
        #         "image_id": "c186f1c5-eaaa-4c4f-9915-aec7a6ef5184",
        #         "flavor_name": "m1.nano",
        #         "network": [
        #             {
        #                 "name": "shared_network_1",
        #             }
        #         ],
        #         "security_groups": ["default"]
        #     }
        # )
        # oc_infra.modify_resource(
        #     resource_type="openstack_compute_instance_v2",
        #     resource_name="test_instance_2",
        #     resource_values={
        #         "name": "test_instance_2_updated",
        #         "image_id": "c186f1c5-eaaa-4c4f-9915-aec7a6ef5184",
        #         "flavor_name": "m1.nano",
        #         "network": [
        #             {
        #             "uuid": "${openstack_networking_network_v2.shared_network_2.id}"
        #             }
        #         ],
        #         "security_groups": ["default"]
        #     }
        # )
        oc_infra.delete_resource(
            tf_resource_type="openstack_compute_instance_v2",
            tf_resource_name="test_instance_firsttime_init"
        )

        oc_infra.output_infrastructure()
        oc_infra.apply_infrastructure()
    except Exception as e:
        print(f"An error occurred: {e}")