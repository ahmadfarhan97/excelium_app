import logging
import json
import azure.functions as func
import os
import base64


from .list_containers import CheckContainers

def main(req: func.HttpRequest) -> func.HttpResponse:
    API_VERSION = "0.0.1"

    logging.info(
        f"Python HTTP trigger function processed a request, API version: {API_VERSION}")


    # Check HTTP basic authorization
    if not authorize(req):
        logging.info("HTTP basic authentication validation failed.")
        return func.HttpResponse(status_code=401)

    # Get the request body
    try:
        req_body = req.get_json()
    except:
        return func.HttpResponse(
            json.dumps({"version": API_VERSION, "action": "ShowBlockPage", "userMessage": "There was a problem with your request."}),
            status_code=200,
            mimetype="application/json"
        )

    # Print out the request body
    logging.info(f"Request body: {req_body}")


    # domain = req_body.get('email').split('@')[1]
    domain = req_body.get('client_id')

    account_url = 'https://exceliumtest.blob.core.windows.net'

    container_connect = CheckContainers(account_url, domain)
    check_container = container_connect.check_cont_in_list()
    logging.info(f'container status {check_container}')

    # Input validation passed successfully, return `Allow` response.
    return func.HttpResponse(
        json.dumps({"version": API_VERSION, "action": "Continue"}),
        status_code=200,
        mimetype="application/json"
    )


def authorize(req: func.HttpRequest):

    # Get the environment's credentials 
    username = os.environ["BASIC_AUTH_USERNAME"]
    password = os.environ["BASIC_AUTH_PASSWORD"]

    # Returns authorized if the username is empty or not exists.
    if not username:
        logging.info("HTTP basic authentication is not set.")
        return True

    # Check if the HTTP Authorization header exist
    if not req.headers.get("Authorization"):
        logging.info("Missing HTTP basic authentication header.")
        return False 

    # Read the authorization header
    auth = req.headers.get("Authorization")

    # Ensure the type of the authorization header id `Basic`
    if  "Basic " not in auth:
        logging.info("HTTP basic authentication header must start with 'Basic '.")
        return False  

    # Get the HTTP basic authorization credentials
    auth = auth[6:]
    authBytes = base64.b64decode(auth)
    auth  = authBytes.decode("utf-8")
    cred = auth.split(':')

    # Evaluate the credentials and return the result
    return (cred[0] == username and cred[1] == password)

