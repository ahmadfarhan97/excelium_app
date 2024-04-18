from werkzeug.middleware.proxy_fix import ProxyFix
from flask import render_template, session, request, redirect, url_for
import msal
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from pandas.io.json import build_table_schema

from hello_app.src.blob_uploader import BlobUploader

from . import app_config
from . import app
from .src.excel_reader import ReadFile
from .src.msal_login import _build_auth_code_flow, _build_msal_app, _get_token_from_cache, _load_cache, _save_cache

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


app.jinja_env.globals.update(
    _build_auth_code_flow=_build_auth_code_flow
)  # Used in template

token_credential = DefaultAzureCredential()

blob_service_client = BlobServiceClient(
    account_url=f"https://exceliumtest.blob.core.windows.net",
    credential=token_credential
)

type_list = ['integer', 'number', 'boolean',
             'datetime', 'duration', 'string', 'any']


@app.route("/login")
def login():
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
    return render_template(
        "login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__
    )


# Its absolute URL must match your app's redirect_uri set in AAD
@app.route(app_config.REDIRECT_PATH)
def authorized():
    try:
        cache_msal = _load_cache()
        result = _build_msal_app(cache_msal=cache_msal).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args
        )
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache_msal)
    except ValueError:  # Usually caused by CSRF
        pass  # Simply ignore them
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY
        + "/oauth2/v2.0/logout"
        + "?post_logout_redirect_uri="
        + url_for("home", _external=True)
    )


@app.route("/")
def home():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("home.html")


@app.route("/about/")
def about():
    if not session.get("user"):
        return redirect(url_for("login"))
    if session.get("user"):
        # print(session.get("user"))
        aud = session.get("user")["aud"]
        print(aud)
        return render_template("about.html")


@app.route("/contact/")
def contact():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("contact.html")


@app.route("/upload/")
def upload():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("upload.html")


@app.route("/filetabslist", methods=["GET", "POST"])
def filetabslist():
    if not session.get("user"):
        return redirect(url_for("login"))
    if request.method == "POST":
        file = request.files["file"]
        file_name = file.name
        session['file_name'] = file_name
        data = file.read()
        session['data'] = data
        read_file = ReadFile(data)
        tabs_list = read_file.tabs_list()
        container_name = session.get("user")["aud"]
        if request.form.get('save_file'):
            upload_blob = BlobUploader(
                file_name, container_name, app_config.STORAGE_SAS_URL, data)
            upload_blob.post_request()
        return render_template("file_tabs_list.html", tabs=tabs_list)


@app.route("/dropdown/", methods=("POST", "GET"))
def dropdown():
    if not session.get("user"):
        return redirect(url_for("login"))
    if request.method == "POST":
        data = session['data']
        tab = request.form.get("tab")
        session['tab'] = tab
        read_file = ReadFile(data)
        tabs_list = read_file.tabs_list()
        columns_list = read_file.tab_column_list(tab)
        return render_template("dropdown_menu.html", columns_list=columns_list, tabs=tabs_list)


@app.route("/schema/", methods=("POST", "GET"))
def schema():
    if not session.get("user"):
        return redirect(url_for("login"))
    if request.method == "POST":
        column_from = request.form.get("column_from")
        column_to = request.form.get("column_to")
        session['column_from'] = column_from
        session['column_to'] = column_to
        data = session['data']
        if request.form.get('all_schema'):
            tab = session['tab']
            read_file = ReadFile(data)
            read_xls = read_file.read_tabs_xlsx(tab)
            read_xls = read_xls.loc[:, column_from:column_to]
            session['columns_selected']  = read_xls.columns.values.tolist()
            df_schema = build_table_schema(read_xls, index=False)
            file_name = session['file_name']
            container_name = session.get("user")["aud"]
            upload_blob = BlobUploader(
                file_name, container_name, app_config.STORAGE_SAS_URL, data)
            upload_blob.post_request()
            return render_template('schema.html', title="page", jsonfile=df_schema, type_list=type_list)
        else:
            return redirect(url_for('html_table'))
            # df_schema = df_schema['fields']
            # print(df_schema)
            # df_schema = json.dumps(df_schema, indent=4)
            # print(type(df_schema))


@app.route("/check_schema/", methods=("POST", "GET"))
def check_schema():
    if not session.get("user"):
        return redirect(url_for("login"))
    if request.method == "POST":
        columns_selected = session['columns_selected']
        schema = request.form.to_dict(flat=False)
        schema_types = schema['column_type']
        # columns_sel_dict = []
        # for value in columns_selected:
        #     dict_name = {}
        #     dict_name['columns_name'] = (value)
        #     columns_sel_dict.append(dict_name)
        # print(columns_sel_dict)
        # columns_type_dict = []
        # for value in schema_types:
        #     dict_name = {}
        #     dict_name['columns_type'] = (value)
        #     columns_type_dict.append(dict_name)
        # print(columns_type_dict)
        columns_dict = {}
        for value in columns_selected:
            for key in schema_types:
                columns_dict[value] = key
                schema_types.remove(key)
                break
        return redirect(url_for("html_table"))

@app.route("/htmltable/", methods=("POST", "GET"))
def html_table():
    if not session.get("user"):
        return redirect(url_for("login"))
    else:
        data = session['data']
        tab = session['tab']
        column_from = session['column_from']
        column_to = session['column_to']
        read_file = ReadFile(data)
        read_xls = read_file.read_tabs_xlsx(tab)
        read_xls = read_xls.loc[:, column_from:column_to]
        return render_template(
            "html_table.html",
            tables=[read_xls.to_html(classes="data")],
            titles=read_xls.columns.values,
        )
