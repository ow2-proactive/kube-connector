# main.py
import argparse
import logging

import uvicorn

import kube_connector.database.db as database


def parse_cli_options():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        nargs="?",
        type=int,
        default=5000,
        help="The port of the API",
    )
    parser.add_argument(
        "-k",
        "--key",
        dest="key",
        nargs="?",
        type=str,
        help="encryption key",
    )

    options = parser.parse_args()
    return options.__dict__


async def app(scope, receive, send):
    ...


def main():
    logging.basicConfig(
        filename="kube-connector.log",
        format="%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    logging.info("kube-connector started")
    options = parse_cli_options()
    port = options["port"]
    key = options["key"]
    database.create_database()
    uvicorn.run("kube_connector.api.api:app", port=port, log_level="info", host="0.0.0.0")


if __name__ == "__main__":
    main()
