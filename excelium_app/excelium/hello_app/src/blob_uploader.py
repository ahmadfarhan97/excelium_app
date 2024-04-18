import requests


class BlobUploader():
    def __init__(self, file_name : str, container : str, storage_sas_url : str, blob : object) -> None:
        self.container = container
        self.file_name = file_name
        self.storage_sas_url = storage_sas_url
        self.blob = blob

    def _pass_var_url(self):
        storage_sas_url = self.storage_sas_url
        storage_sas_url = storage_sas_url.format(self.container, self.file_name)
        print(storage_sas_url)
        return storage_sas_url

    def post_request(self):
        blob = self.blob
        sas_url = self._pass_var_url()
        headers = { 'x-ms-blob-type' : 'BlockBlob' }
        requests.put(sas_url, headers=headers, files={'file': blob})
