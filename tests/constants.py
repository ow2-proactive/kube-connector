import os

ROO_URL = "http://localhost:5000"
MAX_RETRIES = 20
HOME_DIR = os.path.expanduser("~")
CURRENT_DIR = os.getcwd()

# AWS CONSTANTS
AWS_CLOUD_MOCK = {
    "provider_name": "test",
    "provider_type": "aws",
    "payload": {
        "region_name": "test-region",
        "aws_access_key_id": "test",
        "aws_secret_access_key": "test",
    },
}
AWS_REGION = "region = test-region"
AWS_ID = "aws_access_key_id = test"
AWS_DIR = f"{HOME_DIR}/.aws"
AWS_FILES = ["config", "credentials"]

# OpenStack CONSTANTS
OS_CLOUD_MOCK = {
    "provider_type": "openstack",
    "provider_name": "test_cloud",
    "payload": {
        "region_name": "test-region",
        "auth": {
            "username": "test-user",
            "password": "test-pass",
            "auth_url": "https://test-test:5000/v3",
            "project_name": "test-project",
            "user_domain_name": "test",
            "project_domain_name": "test",
        },
    },
}
OS_FILE = f"{CURRENT_DIR}/clouds.yaml"
OS_REGION = "    region_name: test-region"
OS_USER = "      username: test-user"


# SERVERS CONSTANTS
UPDATE_SERVERS_BODY = {
    "provider_type": "openstack",
    "provider_name": "test_cloud",
}
CLOUD_NOT_FOUND = "Cloud test_cloud was not found."
TEST_API_UNREACHABLE = "Unable to establish connection to https://test-test:5000/v3/auth/tokens"


# SGS CONSTANTS
UPDATE_SG_BODY = {
    "provider_type": "openstack",
    "provider_name": "test_cloud",
}
