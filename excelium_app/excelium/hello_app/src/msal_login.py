import msal
from flask import session, url_for

from hello_app import app_config
from hello_app import app


def _load_cache():
    cache_msal = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache_msal.deserialize(session["token_cache"])
    return cache_msal


def _save_cache(cache_msal):
    if cache_msal.has_state_changed:
        session["token_cache"] = cache_msal.serialize()


def _build_msal_app(cache_msal=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID,
        authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET,
        token_cache=cache_msal,
    )


def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [], redirect_uri=url_for("authorized", _external=True)
    )


def _get_token_from_cache(scope=None):
    cache_msal = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache_msal=cache_msal)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache_msal)
        return result


app.jinja_env.globals.update(
    _build_auth_code_flow=_build_auth_code_flow
)  # Used in template