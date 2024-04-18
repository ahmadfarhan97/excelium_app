from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential


class CheckContainers:

    token_credential = DefaultAzureCredential()

    def __init__(self, account_url, name) -> None:
        self.account_url = account_url
        self.name = name
        self.connection = BlobServiceClient(account_url=self.account_url, credential=self.token_credential)

    def _list_containers(self):
        list_conts = self.connection.list_containers()
        cont_names = []
        for container in list_conts:
            cont_names.append(container.name)
        # print(cont_names)
        return cont_names

    def _create_container(self):
        new_container_name = self.name
        new_container = self.connection.create_container(new_container_name)
        return new_container

    def check_cont_in_list(self):
        name = self.name
        conts_list = self._list_containers()
        print(conts_list)
        if name in conts_list:
            return f'container named {name} already exist'
        else:
            self._create_container()
            return f'container named {name} created'
