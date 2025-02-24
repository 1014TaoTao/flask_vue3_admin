import os

from kubernetes import client, config
from kubernetes.client.api_client import ApiClient


class K8sApi:
    def __init__(self):
        config_path = os.path.join(r"../../../data/config")
        config.kube_config.load_kube_config(config_file=config_path)
        self.k8s_client = ApiClient()
        self.api_instance = client.CoreV1Api(api_client=self.k8s_client)

    def get_namespaces(self) -> list:
        """
        Get list of namespaces.
        """
        return self.api_instance.list_namespace(watch=False).items

    def get_services(self) -> list:
        """
        Get list of all services.
        """
        return self.api_instance.list_service_for_all_namespaces(watch=False).items

    def get_pods(self) -> list:
        """
        Get list of all pods.
        """
        return self.api_instance.list_pod_for_all_namespaces(watch=False).items
