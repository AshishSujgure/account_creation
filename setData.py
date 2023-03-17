import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

class getDynamoDB:

    def __init__(self,eventName:str,request_status:str,account_id:str,non_prod_environment_name:str,project_key:str,parent_ou_id:str,working_directory:str,customer_name:str,
                record_id:str,customer_id:str,app_id:str,non_prod_env_id:str,create_1pass_vault:str,billing_id:str,builder:str,create_cloudcraft_integration:str,enterprise_support:str,
                skip_tekton:str,category:str,owner:str,budget_daily:str,permission_sets:str) -> None:
        self.eventName = eventName
        self.request_status = request_status
        self.account_id = account_id
        self.non_prod_environment_name = non_prod_environment_name
        self.project_key = project_key
        self.parent_ou_id = parent_ou_id
        self.working_directory = working_directory
        self.customer_name = customer_name
        self.record_id = record_id
        self.customer_id = customer_id
        self.app_id = app_id
        self.non_prod_env_id = non_prod_env_id
        self.create_1pass_vault = create_1pass_vault
        self.billing_id = billing_id
        self.builder = builder
        self.create_cloudcraft_integration = create_cloudcraft_integration
        self.enterprise_support = enterprise_support
        self.skip_tekton = skip_tekton
        self.category = category
        self.owner = owner
        self.budget_daily = budget_daily
        self.permission_sets = permission_sets

    
    def sendEmail(self):
        SENDER = "platform-engineering@pivotree.com"
        RECIPIENT = self.builder
        AWS_REGION = "us-east-1"
        SUBJECT = "AWS account creation request"
        BODY_HTML = f"""
        Below is the required data for customer "{self.customer_name}" AWS Account creation request: <br><br>
              <html>
              <head>
              <style>
              #customers {{
                font-family: Arial, Helvetica, sans-serif;
                border-collapse: collapse;
                width: 100%;
              }}
              
              #customers td, #customers th {{
                border: 1px solid #ddd;
                padding: 8px;
              }}
              
              #customers tr:nth-child(even){{background-color: #f2f2f2;}}
              
              #customers tr:hover {{background-color: #ddd;}}
              
              #customers th {{
                padding-top: 12px;
                padding-bottom: 12px;
                text-align: left;
                background-color: #3366CC;
                color: white;
              }}
              </style>
              </head>
              <body>
              
              <table id="customers">
                <tr>
                  <th>Required Data</th>
                  <th>Data Provided</th>
                </tr>
                <tr>
                  <td>ACCOUNT ID</td>
                  <td>{self.account_id}</td>
                </tr>
                 <tr>
                  <td>APP ID</td>
                  <td>{self.app_id}</td>
                </tr>
                <tr>
                  <td>CUSTOMER ID</td>
                  <td>{self.customer_id}</td>
                </tr>
                <tr>
                <td>BILLING ID</td>
                <td>{self.billing_id}</td>
              </tr>
                <tr>
                  <td>CUSTOMER NAME</td>
                  <td>{self.customer_name}</td>
                </tr>
                <tr>
                  <td>NON PROD ENV ID</td>
                  <td>{self.non_prod_env_id}</td>
                </tr>
                <tr>
                  <td>NON PROD ENV NAME</td>
                  <td>{self.non_prod_environment_name}</td>
                </tr>
                <tr>
                  <td>OWNER</td>
                  <td>{self.owner}</td>
                </tr>
                 <tr>
                  <td>DAILY BUDGET</td>
                  <td>{self.budget_daily}</td>
                </tr>
                <tr>
                  <td>PARENT OU ID</td>
                  <td>{self.parent_ou_id}</td>
                </tr>
                <tr>
                  <td>PROJECT KEY</td>
                  <td>{self.project_key}</td>
                </tr>
                <tr>
                <td>CREATE 1PASSWORD VAULT</td>
                <td>{self.create_1pass_vault}</td>
               </tr>
               <tr>
               <td>CREATE CLOUDCRAFT INTEGRATION</td>
               <td>{self.create_cloudcraft_integration}</td>
               </tr>
               <tr>
               <td>ENABLE ENTERPRISE SUPPORT</td>
               <td>{self.enterprise_support}</td>
               </tr>
               <tr>
               <td>SKIP TEKTON</td>
               <td>{self.skip_tekton}</td>
               </tr>
               <tr>
               <td>CATEGORY</td>
               <td>{self.category}</td>
               </tr>
                <tr>
                  <td>WORKING DIRECTORY</td>
                  <td>{self.working_directory}</td>
                </tr>
                  <tr>
                  <td>PERMISSION SETS</td>
                  <td>{self.permission_sets}</td>
                </tr>
                  <tr>
                  <td>REQUEST STATUS</td>
                  <td>{self.request_status}</td>
                </tr>
                <tr>
                <td>REQUESTER</td>
                <td>{self.builder}</td>
              </tr>
              </table>
              
              </body>
              </html>
              <br><br> Cheers, <br> -- Self Service Tool`
            """
        CHARSET = "UTF-8"
        client = boto3.client("ses", region_name=AWS_REGION)

        try:
            response = client.send_email(
                Destination={
                    "ToAddresses": [
                    RECIPIENT,
                    ],
                },
                Message={
                    "Body": {
                        "Html": {
                            "Charset": CHARSET,
                            "Data": BODY_HTML,
                        },
                    },
                    "Subject": {
                        "Charset": CHARSET,
                        "Data": SUBJECT,
                    },
                },
                Source=SENDER,
            )

        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            print("Email sent! Message ID:"),
            print(response["MessageId"])

    def add_group_permissions(self):
    # Defines group permissions for new account creation using self service tool
        list_user_group=[]
        group_permissions = ""

        for json_elements  in self.permission_sets:
            for values in json_elements:
                if(values == "value"):
                    list_user_group.append(json_elements[values])

        for user_group in range(len(list_user_group)):
            if(list_user_group[user_group] == "operations"):
                operations_permissions = "\""+"operations"+"\""+" = "+"["+"\""+"Operations"+"\""+" , "+"\""+"ReadOnlyAccess"+"\""+"]"
                group_permissions = group_permissions + operations_permissions + " , "

            if(list_user_group[user_group] == "dba"):
                dba_permission = "\""+"dba"+"\""+" "+"="+" "+"["+"\""+"PivotreeDba"+"\""+"]"
                group_permissions = group_permissions + dba_permission + " , "

            if(list_user_group[user_group] == "solutions"):
                solutions_permission = "\""+"solutions"+"\""+" "+"="+" "+"["+"\""+"ReadOnlyAccess"+"\""+"]"
                group_permissions = group_permissions + solutions_permission + " , "

            if(list_user_group[user_group] == "read"):
                read_permission = "\""+"read"+"\""+" "+"="+" "+"["+"\""+"ReadOnlyAccess"+"\""+"]"
                group_permissions = group_permissions + read_permission + " , " 

            if(list_user_group[user_group] == "sa-presales"):
                presales_permissions = "\""+"sa-presales"+"\""+" "+"="+" "+"["+"\""+"ReadOnlyAccess"+"\""+"]"
                group_permissions = group_permissions + presales_permissions + " , " 
    
            if(list_user_group[user_group] == "security"):
                security_permission = "\""+"security"+"\""+" "+"="+" "+"["+"\""+"ReadOnlyAccess"+"\""+"]"
                group_permissions = group_permissions + security_permission + " , "    
    
            if(list_user_group[user_group] == "triage"):
                triage_permission = "\""+"triage"+"\""+" "+"="+" "+"["+"\""+"PivotreeTriage"+"\""+"]"
                group_permissions = group_permissions + triage_permission + " , "  

            if(list_user_group[user_group] == "tam"):
                tam_permission = "\""+"tam"+"\""+" "+"="+" "+"["+"\""+"ReadOnlyAccess"+"\""+"]"
                group_permissions = group_permissions + tam_permission + " , "  
        
        platform_permission = "\""+"platform"+"\""+" "+"="+" "+"["+"\""+"ReadOnlyAccess"+"\""+"]"
        group_permissions = group_permissions + platform_permission + " , "  
        group_permissions = group_permissions[:-2]
        group_permissions = " { "+group_permissions+" } "
        print("Group Permissions mapped successfully: ", group_permissions)
        return group_permissions


