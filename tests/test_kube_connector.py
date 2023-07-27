import json
import multiprocessing
import os
import shutil
import time

import requests

import kube_connector.database.db as database
from kube_connector.main import main
from tests.constants import *


def api_is_up():
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(ROO_URL)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        retries += 1
        time.sleep(0.1)
    return False


def check_string_in_file(file_path, search_string):
    with open(file_path, "r") as file:
        content = file.read()
    if search_string in content:
        return True
    else:
        return False


def add_mock_cloud(mock_body):
    # create the add_cloud json body
    body = json.dumps(mock_body)
    # send the add_cloud request
    response = requests.post(f"{ROO_URL}/add_cloud", data=body)
    return response


def test_home_page():
    process = multiprocessing.Process(target=main)
    process.start()
    assert api_is_up(), f"the servere {ROO_URL} was not up after {MAX_RETRIES} retries!"
    response = requests.get(ROO_URL)
    process.terminate()
    assert "text/html" in response.headers.get("content-type")
    assert response.status_code == 200
    assert "Running like  charm!" and "Kube-connector Status" in response.text


def test_favicon():
    process = multiprocessing.Process(target=main)
    process.start()
    assert api_is_up(), f"the servere {ROO_URL} was not up after {MAX_RETRIES} retries!"
    response = requests.get(f"{ROO_URL}/favicon.ico")
    process.terminate()
    assert int(response.headers.get("content-length")) == 5748
    assert response.status_code == 200


def test_add_cloud_aws():
    # start the server in a seperate process
    process = multiprocessing.Process(target=main)
    process.start()
    # Delete the aws dir to check if the code can create it
    if os.path.exists(AWS_DIR):
        shutil.rmtree(AWS_DIR)
    assert not os.path.exists(AWS_DIR), f"unable to remove the aws dir: {AWS_DIR}"

    # Make sure the server is up and ready to receive new tasks
    assert api_is_up(), f"the servere {ROO_URL} was not up after {MAX_RETRIES} retries!"

    # request the creationg of mock aws cloud
    response = add_mock_cloud(AWS_CLOUD_MOCK)

    # terminate the server after receiving the response
    process.terminate()

    # assert the dir was created
    assert os.path.exists(AWS_DIR), f"unable to create the aws dir: {AWS_DIR}"

    # assert  all the files were created
    for file in AWS_FILES:
        file_path = os.path.join(AWS_DIR, file)
        assert os.path.exists(file_path), f"the file {file_path} does not exist!"

    # assert that the parameters were added corectly in the configuration files
    assert check_string_in_file(
        os.path.join(AWS_DIR, AWS_FILES[0]), AWS_REGION
    ), f"The config file is not set with correct region"
    assert check_string_in_file(
        os.path.join(AWS_DIR, AWS_FILES[1]), AWS_ID
    ), f"The credentials file is not set with correct id"

    # assert the response was ok
    assert response.status_code == 200

    # assert that the content of the response is correct
    assert "status" and "SUCCESS!" in str(response.content)

    # Delete the aws dir for it not to interfere the next tests
    if os.path.exists(AWS_DIR):
        shutil.rmtree(AWS_DIR)

    # TODO: Add a test to check if the database contains the cloud added


def test_add_cloud_os():
    # start the server in a seperate process
    process = multiprocessing.Process(target=main)
    process.start()
    # Delete the openstack file to check if the code can create it
    if os.path.exists(OS_FILE):
        os.remove(OS_FILE)
    assert not os.path.exists(OS_FILE), f"unable to remove the openstack file: {OS_FILE}"

    # Make sure the server is up and ready to receive new tasks
    assert api_is_up(), f"the servere {ROO_URL} was not up after {MAX_RETRIES} retries!"

    # request the creationg of mock openstack cloud
    response = add_mock_cloud(OS_CLOUD_MOCK)

    # terminate the server after receiving the response
    process.terminate()

    # assert the file was created
    assert os.path.exists(OS_FILE), f"unable to create the openstack file: {OS_FILE}"

    # assert that the parameters were added corectly in the configuration file
    assert check_string_in_file(
        OS_FILE, OS_REGION
    ), f"The config file is not set with correct region"
    assert check_string_in_file(
        OS_FILE, OS_USER
    ), f"The config file is not set with correct user name"

    # assert the response was ok
    assert response.status_code == 200

    # assert that the content of the response is correct
    assert "status" and "SUCCESS!" in str(response.content)

    # finally, remove the openstack file for it not to interfere the next tests
    if os.path.exists(OS_FILE):
        os.remove(OS_FILE)

    # TODO: Add a test to check if the database contains the cloud added


def test_update_servers_with_no_cloud():
    # start the server in a seperate process
    process = multiprocessing.Process(target=main)
    process.start()

    # Make sure the server is up and ready to receive new tasks
    assert api_is_up(), f"the servere {ROO_URL} was not up after {MAX_RETRIES} retries!"

    body = json.dumps(UPDATE_SERVERS_BODY)
    response = requests.post(f"{ROO_URL}/update_servers", data=body)

    process.terminate()

    # assert the response was ok
    assert response.status_code == 200

    # assert that the content of the response contains a failed status
    assert "status" and "Failed" in str(response.content)

    # assert the reason for the failure is cloud not found
    assert CLOUD_NOT_FOUND in str(response.content)


def test_update_servers_with_cloud():
    # start the server in a seperate process
    process = multiprocessing.Process(target=main)
    process.start()

    # Make sure the server is up and ready to receive new tasks
    assert api_is_up(), f"the servere {ROO_URL} was not up after {MAX_RETRIES} retries!"

    # request the creationg of mock openstack cloud
    add_mock_cloud(OS_CLOUD_MOCK)

    # send a request to update the servers for the mock cloud
    body = json.dumps(UPDATE_SERVERS_BODY)
    response = requests.post(f"{ROO_URL}/update_servers", data=body)

    process.terminate()

    # assert the response was ok
    assert response.status_code == 200

    # assert that the content of the response contains a failed status
    assert "status" and "Failed" in str(response.content)

    # assert the reason for the failure is that the server is unreachable
    assert TEST_API_UNREACHABLE in str(response.content)

    # finally, remove the openstack file for it not to interfere the next tests
    if os.path.exists(OS_FILE):
        os.remove(OS_FILE)


def test_update_sg_with_no_cloud():
    # start the server in a seperate process
    process = multiprocessing.Process(target=main)
    process.start()

    # Make sure the server is up and ready to receive new tasks
    assert api_is_up(), f"the servere {ROO_URL} was not up after {MAX_RETRIES} retries!"

    body = json.dumps(UPDATE_SG_BODY)
    response = requests.post(f"{ROO_URL}/update_security_groups", data=body)

    process.terminate()

    # assert the response was ok
    assert response.status_code == 200

    # assert that the content of the response contains a failed status
    assert "status" and "Failed" in str(response.content)

    # assert the reason for the failure is cloud not found
    assert CLOUD_NOT_FOUND in str(response.content)


def test_update_sg_with_cloud():
    # start the server in a seperate process
    process = multiprocessing.Process(target=main)
    process.start()

    # Make sure the server is up and ready to receive new tasks
    assert api_is_up(), f"the servere {ROO_URL} was not up after {MAX_RETRIES} retries!"

    # request the creationg of mock openstack cloud
    add_mock_cloud(OS_CLOUD_MOCK)

    # send a request to update the servers for the mock cloud
    body = json.dumps(UPDATE_SG_BODY)
    response = requests.post(f"{ROO_URL}/update_servers", data=body)

    process.terminate()

    # assert the response was ok
    assert response.status_code == 200

    # assert that the content of the response contains a failed status
    assert "status" and "Failed" in str(response.content)

    # assert the reason for the failure is that the server is unreachable
    assert TEST_API_UNREACHABLE in str(response.content)

    # finally, remove the openstack file for it not to interfere the next tests
    if os.path.exists(OS_FILE):
        os.remove(OS_FILE)
