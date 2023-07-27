import logging

import kube_connector.database.db as database
from kube_connector.api.message import Message


def add_cloud(req):
    m = Message()
    if "payload" not in req.keys() or "iden" not in req.keys():
        m.status = "Failed"
        m.reply = (
            "The request must contain a payload"
            if "payload" not in req.keys()
            else "The request must contain an iden"
        )
        logging.error("addCloud request Failed: " + m.reply)
        return m.cast_dict()

    cloudItem = req["payload"]
    logging.info("payload extracted: " + str(cloudItem))
    iden = req["iden"]
    logging.info("iden extracted: " + str(iden))

    try:
        database.add_cloud_item(cloudItem)
    except Exception as e:
        m.status = "Failed"
        m.reply = "The cloud item was not added to the DB"
        logging.error('addCloud request Failed with the following error: "' + str(e) + '"')
        return m.cast_dict()

    m.status = "SUCCESS!"
    m.reply = "Cloud added with ID: " + str(iden)
    m.data = cloudItem
    print(m.reply)
    logging.info("addCloud request SUCCESS: " + m.reply)
    return m.cast_dict()


def create_database():
    m = Message()
    m.from_dict(clear_database())
    if m.status == "Failed":
        return m
    try:
        database.create_database()
        m.status = "SUCCESS!"
    except Exception as e:
        m.status = "Failed"
        m.reply = "DB was not created!"
        logging.error('DB was not created with the following error: "' + str(e) + '"')
    return m.cast_dict()


def clear_database():
    m = Message()
    try:
        database.clear_database()
        m.status = "SUCCESS!"
    except Exception as e:
        m.status = "Failed"
        m.reply = "DB was not cleared!"
        logging.error('DB was not cleared with the following error: "' + str(e) + '"')
    return m.cast_dict()


def clear_sg_db():
    m = Message()
    try:
        database.clear_sg_db()
        m.status = "SUCCESS!"
    except Exception as e:
        m.status = "Failed"
        m.reply = "DB was not cleared!"
        logging.error('DB was not cleared with the following error: "' + str(e) + '"')
    return m.cast_dict()


def get_security_group(req):
    m = Message()
    try:
        sg = database.get_security_group(req["sg_name"])
        if sg:
            m.status = "SUCCESS!"
            m.data = sg[0]
        else:
            m.status = "Failed"
            m.reply = "The requested security group %s was not found!" % req["sg_name"]
    except Exception as e:
        m.status = "Failed"
        m.reply = (
            "Error encountered when trying to reterieve the security group %s." % req["sg_name"]
        )
        logging.exception(e)
    return m.cast_dict()


def add_kuberentes_token(req):
    m = Message()

    try:
        token_id = database.add_kubernetes_token(req["token"])
    except Exception as e:
        m.status = "Failed"
        m.reply = "Error encountered when adding the token %s." % req["token"]
        logging.exception(e)

    if m.reply == "":
        m.status = "SUCCESS!"
        m.reply = "The kubentes token is added with id %s" % token_id

    return m.cast_dict()


def get_kuberentes_token(req):
    m = Message()

    try:
        token = database.get_kubernetes_token(req["token_id"])
    except Exception as e:
        m.status = "Failed"
        m.reply = "Error encountered when getting the token with id %s." % req["token_id"]
        logging.exception(e)

    if m.reply == "" and not token == None:
        m.status = "SUCCESS!"
        m.data = token
    elif token == None:
        m.reply = "The Token with id %s was not found" % req["token_id"]

    return m.cast_dict()
