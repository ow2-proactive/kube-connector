# /usr/bin/python3.10
import logging

import fastapi
from starlette.responses import FileResponse

import kube_connector.api.cloud_gateway as cloud_gateway
import kube_connector.api.db_gateway as db_gateway
import kube_connector.connectors.openstack_conector as openstack

app = fastapi.FastAPI()

favicon_path = "kube_connector/landing-page/AE.icon"
home_page = "kube_connector/landing-page/index.html"


@app.get("/", response_class=fastapi.responses.HTMLResponse)
async def root():
    """
    Get the home page of the api as an html file.

    Returns:
    - home page as an html file.
    """
    logging.info("/ is called")
    return FileResponse(home_page)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    Get the favicon of the api as an png file.

    Returns:
    - favicon as an png file.
    """
    return FileResponse(favicon_path)


@app.post("/add_cloud")
async def add_cloud(info: fastapi.Request):
    """
    Add a cloud definition to kube-connector to be used with the cloud sdks.

    Parameters:
    - A Json body of a cloud that includes provider_name, provider_type,
    and a payload that contains the necessary definition of the cloud based
    on the cloud type.

    Returns:
    - The request status and an error if any.
    """
    logging.info("/add_cloud is called")
    req = await info.json()
    logging.info("/add_cloud request body: " + str(req))
    m = cloud_gateway.add_cloud(req)
    return m


# deprecated
@app.get("/get_servers")
async def get_servers(info: fastapi.Request):
    logging.info("/get_servers is called")
    req = await info.json()
    m = cloud_gateway.get_servers(req)
    return m


@app.post("/update_servers")
async def get_servers(info: fastapi.Request):
    """
    Update the list of servers and save them in the data base, if this endpoint is called for the
    first time, it will collect all the new servers and add them, otherwise it will only
    add the newly added servers

    Parameters:
    - A Json body of a cloud that includes provider_name, provider_type

    Returns:
    - The request status and an error if any.
    """
    logging.info("/update_servers is called")
    req = await info.json()
    m = cloud_gateway.update_servers(req)
    return m


# deprecated
@app.get("/get_security_groups")
async def get_security_groups(info: fastapi.Request):
    logging.info("/get_security_groups is called")
    req = await info.json()
    m = cloud_gateway.get_security_groups(req)
    return m


@app.post("/update_security_groups")
async def update_security_groups(info: fastapi.Request):
    """
    Update the list of security groups and save them in the data base,
    if this endpoint is called for the first time, it will collect all
    the new security groups and add them, otherwise it will only add
    the newly added security groups

    Parameters:
    - A Json body of a cloud that includes provider_name, provider_type

    Returns:
    - The request status and an error if any.
    """
    logging.info("/update_security_groups is called")
    req = await info.json()
    m = cloud_gateway.update_security_groups(req)
    return m


@app.get("/get_security_group")
async def get_security_group(info: fastapi.Request):
    logging.info("/get_security_group is called")
    req = await info.json()
    m = db_gateway.get_security_group(req)
    return m


@app.post("/create_security_group")
async def create_security_group(info: fastapi.Request):
    logging.info("/create_security_group is called")
    req = await info.json()
    m = cloud_gateway.create_security_group(req)
    return m


@app.post("/add_sg_rule")
async def add_sg_rule(info: fastapi.Request):
    logging.info("/add_sg_rule is called")
    req = await info.json()
    m = cloud_gateway.add_security_group_rule(req)
    return m


@app.post("/open_ip")
async def open_ip(info: fastapi.Request):
    logging.info("/open_ip is called")
    req = await info.json()
    m = cloud_gateway.open_ip(req)
    return m


@app.post("/add_kuberentes_token")
async def add_kuberentes_token(info: fastapi.Request):
    logging.info("/add_kuberentes_token is called")
    req = await info.json()
    m = db_gateway.add_kuberentes_token(req)
    return m


@app.get("/get_kuberentes_token")
async def get_kuberentes_token(info: fastapi.Request):
    logging.info("/get_kuberentes_token is called")
    req = await info.json()
    m = db_gateway.get_kuberentes_token(req)
    return m


@app.post("/create_db")
async def create_db(info: fastapi.Request):
    logging.info("/create DB is called")
    m = db_gateway.create_database()
    return m


@app.post("/add_to_cluster")
async def create_db(info: fastapi.Request):
    logging.info("/add_to_cluster is called")
    req = await info.json()
    m = cloud_gateway.add_to_cluster(req)
    return m


@app.delete("/clear_db")
async def clear_db(info: fastapi.Request):
    logging.info("/clear DB is called")
    m = db_gateway.clear_database()
    return m


@app.delete("/clear_sg_db")
async def clear_db(info: fastapi.Request):
    logging.info("/clear_sg_db is called")
    m = db_gateway.clear_sg_db()
    return m
