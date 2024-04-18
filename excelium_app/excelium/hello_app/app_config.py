import os

b2c_tenant = "exceliumltd"
signupsignin_user_flow = "B2C_1_signupsignin"
editprofile_user_flow = "B2C_1_profileediting"

# resetpassword_user_flow = "B2C_1_passwordreset1"  # Note: Legacy setting.
    # If you are using the new
    # "Recommended user flow" (https://docs.microsoft.com/en-us/azure/active-directory-b2c/user-flow-versions),
    # you can remove the resetpassword_user_flow and the B2C_RESET_PASSWORD_AUTHORITY settings from this file.

authority_template = "https://{tenant}.b2clogin.com/{tenant}.onmicrosoft.com/{user_flow}"

CLIENT_ID = "<CLIENT ID>" # Application (client) ID of app registration

CLIENT_SECRET = "<CLIENT SECRET>" # Placeholder - for use ONLY during testing.
# In a production app, we recommend you use a more secure method of storing your secret,
# like Azure Key Vault. Or, use an environment variable as described in Flask's documentation:
# https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# if not CLIENT_SECRET:
#     raise ValueError("Need to define CLIENT_SECRET environment variable")

AUTHORITY = authority_template.format(
    tenant=b2c_tenant, user_flow=signupsignin_user_flow)
B2C_PROFILE_AUTHORITY = authority_template.format(
    tenant=b2c_tenant, user_flow=editprofile_user_flow)

# B2C_RESET_PASSWORD_AUTHORITY = authority_template.format(
#     tenant=b2c_tenant, user_flow=resetpassword_user_flow)
    # If you are using the new
    # "Recommended user flow" (https://docs.microsoft.com/en-us/azure/active-directory-b2c/user-flow-versions),
    # you can remove the resetpassword_user_flow and the B2C_RESET_PASSWORD_AUTHORITY settings from this file.

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
                              # The absolute URL must match the redirect URI you set
                              # in the app's registration in the Azure portal.

# This is the API resource endpoint
ENDPOINT = '' # Application ID URI of app registration in Azure portal

# These are the scopes you've exposed in the web API app registration in the Azure portal
SCOPE = ["https://exceliumltd.onmicrosoft.com/check-container/tasks.read", "https://exceliumltd.onmicrosoft.com/check-container/tasks.write"]  # Example with two exposed scopes: ["demo.read", "demo.write"]

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session

# import os

# CLIENT_ID = "" # Application (client) ID of app registration

# CLIENT_SECRET = "" # Placeholder - for use ONLY during testing.
# # In a production app, we recommend you use a more secure method of storing your secret,
# # like Azure Key Vault. Or, use an environment variable as described in Flask's documentation:
# # https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
# # CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# # if not CLIENT_SECRET:
# #     raise ValueError("Need to define CLIENT_SECRET environment variable")

# AUTHORITY = "https://login.microsoftonline.com/excelest.onmicrosoft.com"  # For multi-tenant app
# # AUTHORITY = "https://login.microsoftonline.com/excelest.onmicrosoft.com"

# REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
#                               # The absolute URL must match the redirect URI you set
#                               # in the app's registration in the Azure portal.

# # You can find more Microsoft Graph API endpoints from Graph Explorer
# # https://developer.microsoft.com/en-us/graph/graph-explorer
# ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent


# # You can find the proper permission names from this document
# # https://docs.microsoft.com/en-us/graph/permissions-reference
# SCOPE = ["User.ReadBasic.All"]

# SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session

STORAGE_SAS_URL = 'SAS URL STRING'

# # ### YOUR APP CONFIGS ###
# # # write to filesystem:
# # SESSION_TYPE = 'filesystem'



# # # sample title in navbar
# # SAMPLE_DESCRIPTION = 'Authentication: Use MSAL Python to sign users in to your own Azure Active Directory tenant'
# # SCOPE = ["User.ReadBasic.All"]

# # AUTHORITY = "https://login.microsoftonline.com/Excelest"
# # REDIRECT_PATH = "/getAToken"
# # ENDPOINT = 'https://graph.microsoft.com/v1.0/users'
