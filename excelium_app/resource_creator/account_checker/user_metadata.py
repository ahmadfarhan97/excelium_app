import logging
import uuid
from azure.data.tables import TableServiceClient
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureNamedKeyCredential


class UserMetaData:

    token_credential = DefaultAzureCredential()

    def __init__(self, account_url, entity) -> None:
        self.account_url = account_url
        self.entity = entity
        self.table_name = "UserMetadata"
        my_access_key = '<ACCESS KEY>'
        credential = AzureNamedKeyCredential("exceliumtest", my_access_key)
        self.connection = TableServiceClient(
            endpoint=self.account_url, credential=credential)
        self.table_client = self.connection.get_table_client(
            table_name=self.table_name)

    def dict_entity(self):
        entity['PartitionKey']  = entity['aud']
        entity['RowKey']        = uuid.uuid4()
        entity['EntityType']    = 'created'
        keys_values = entity.items()
        new_dict = {str(key): str(value) for key, value in keys_values}
        print(new_dict)
        return new_dict

    def _create_entity(self):
        edited_entity = self.dict_entity()
        self.table_client.create_entity(edited_entity)

    def query_entity(self):
        entity = self.entity
        aud = entity['aud']
        # aud = 'test3'

        query_filter = f"PartitionKey eq '{aud}'"

        filtered_entity = self.table_client.query_entities(
            query_filter=query_filter)

        list_of_entities = []
        for entity in filtered_entity:
            list_of_entities.append(entity)
        return list_of_entities

    def check_entity(self):
        list_of_entities = self.query_entity()
        if not list_of_entities:
            print(list_of_entities)
            self._create_entity()
            print('inserted')
        else:
            print(list_of_entities)
            return logging.info('User already exist in User Metadata Table')
