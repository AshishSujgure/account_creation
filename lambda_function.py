import json
import ast
import requests
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from setData import getDynamoDB
from github import Github

def lambda_handler(event, context):
    """
    Assigning values to pipeline variables
    """
    print("##Below Event occured")
    eventName = event["Records"][0]["eventName"]
    request_status = event["Records"][0]["dynamodb"]["NewImage"]["request_status"]["S"]
    account_id = event["Records"][0]["dynamodb"]["NewImage"]["account_id"]["S"]
    non_prod_environment_name = event["Records"][0]["dynamodb"]["NewImage"][
        "non_prod_environment_name"
    ]["S"]
    project_key = event["Records"][0]["dynamodb"]["NewImage"]["project_key"]["S"]
    parent_ou_id = event["Records"][0]["dynamodb"]["NewImage"]["parent_ou_id"]["S"]
    working_directory = event["Records"][0]["dynamodb"]["NewImage"][
        "working_directory"
    ]["S"]
    customer_name = event["Records"][0]["dynamodb"]["NewImage"]["customer_name"]["S"]
    record_id = event["Records"][0]["dynamodb"]["NewImage"]["id"]["S"]
    customer_id = event["Records"][0]["dynamodb"]["NewImage"]["customer_id"]["S"]
    app_id = event["Records"][0]["dynamodb"]["NewImage"]["app_id"]["S"]
    non_prod_env_id = event["Records"][0]["dynamodb"]["NewImage"]["non_prod_env_id"][
        "S"
    ]
    create_1pass_vault = event["Records"][0]["dynamodb"]["NewImage"][
        "create_1pass_vault"
    ]["S"]
    billing_id = event["Records"][0]["dynamodb"]["NewImage"]["billing_id"]["S"]
    builder = event["Records"][0]["dynamodb"]["NewImage"]["builder"]["S"]
    create_cloudcraft_integration = event["Records"][0]["dynamodb"]["NewImage"][
        "create_cloudcraft_integration"
    ]["S"]
    enterprise_support = event["Records"][0]["dynamodb"]["NewImage"][
        "enterprise_support"
    ]["S"]
    request_status = event["Records"][0]["dynamodb"]["NewImage"]["request_status"]["S"]
    skip_tekton = event["Records"][0]["dynamodb"]["NewImage"]["skip_tekton"]["S"]
    category = event["Records"][0]["dynamodb"]["NewImage"]["category"]["S"]
    owner = event["Records"][0]["dynamodb"]["NewImage"]["owner"]["S"]
    budget_daily = event["Records"][0]["dynamodb"]["NewImage"]["budget_daily"]["S"]
    permission_sets = event["Records"][0]["dynamodb"]["NewImage"]["permission_sets"]["S"]
    permission_sets = ast.literal_eval(permission_sets)

    instance = getDynamoDB(eventName,request_status,account_id,non_prod_environment_name,project_key,parent_ou_id,working_directory,customer_name,
                record_id,customer_id,app_id,non_prod_env_id,create_1pass_vault,billing_id,builder,create_cloudcraft_integration,enterprise_support,
                skip_tekton,category,owner,budget_daily,permission_sets)
    permission_sets = instance.add_group_permissions()   
    instance.sendEmail()

    variables = [
        {"key": "account_id", "value": ""},
        {"key": "app_id", "value": ""},
        {"key": "customer_id", "value": ""},
        {"key": "customer_name", "value": ""},
        {"key": "non_prod_environment_name", "value": ""},
        {"key": "non_prod_env_id", "value": ""},
        {"key": "PROJECT_KEY", "value": ""},
        {"key": "parent_ou_id", "value": ""},
        {"key": "working_directory", "value": ""},
        {"key": "create_1pass_vault", "value": ""},
        {"key": "billing_id", "value": ""},
        {"key": "builder", "value": ""},
        {"key": "create_cloudcraft_integration", "value": ""},
        {"key": "enterprise_support", "value": ""},
        {"key": "skip_tekton", "value": ""},
        {"key": "category", "value": ""},
        {"key": "owner", "value": ""},
        {"key": "budget_daily", "value": ""},
        {"key": "permission_sets", "value": ""},
    ]
    if eventName == "MODIFY" and request_status == "Approved":
        print("Condition ran Successfully")
        callGitHubAPI()

def callGitHubAPI():
    json_object = json.loads(get_secret())
    for key in json_object:
        GITHUB_TOKEN_ID = json_object["GITHUB_TOKEN"]
        break
    # Define your GitHub credentials and repository information
    repository_name = "arche"
    repository_owner = "pvtrlabs"

    # Connect to the GitHub API using PyGithub library
    g = Github(GITHUB_TOKEN_ID)
    repo = g.get_user(repository_owner).get_repo(repository_name)

    # Retrieve the JSON file from the repository
    file_path = "account_details.json"
    file_contents = repo.get_contents(file_path)
    file_data = json.loads(file_contents.decoded_content)

    # Modify the JSON data as needed
    file_data['account_id'] = account_id
    file_data['app_id'] = app_id
    file_data['customer_id'] = customer_id
    file_data['customer_name'] = customer_name
    file_data['billing_id'] = billing_id
    file_data['non_prod_environment_name'] = non_prod_environment_name
    file_data['non_prod_env_id'] = non_prod_env_id
    file_data['PROJECT_KEY'] = project_key
    file_data['parent_ou_id'] = parent_ou_id
    file_data['working_directory'] = working_directory
    file_data['create_1pass_vault'] = create_1pass_vault
    file_data['cloudcraft'] = create_cloudcraft_integration
    file_data['enterprise_support'] = enterprise_support
    file_data['category'] = category
    file_data['builder'] = builder
    file_data['skip_tekton'] = skip_tekton
    file_data['owner'] = owner
    file_data['budget_daily'] = budget_daily

    # Commit the changes to the repository
    commit_message = "Updated account_details.json"
    repo.update_file(file_path, commit_message, json.dumps(file_data), file_contents.sha)
    return {
        'statusCode': 200,
        'body': json.dumps('File updated successfully!')
    }


def get_secret():
        """
        This Function will retrieve the "GITHUB_TOKEN" for Cloudcheckr from AWS Secrets Manager
        """

        secret_name = "arn:aws:secretsmanager:us-east-1:772846873375:secret:GitHubActions-dcp5As"
        region_name = "us-east-1"
        secret = ""

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        )

        try:
            get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
            )
        except Exception as e:
            print(e)

        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
        return secret

