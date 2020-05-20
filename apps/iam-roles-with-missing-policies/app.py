import json
from graphqlclient import GraphQLClient


def get_missing_policies(required, attached):
    return list(frozenset(required).difference(attached))


def lambda_handler(event, context):
    client = GraphQLClient("https://api.faros.ai/v0/graphql")
    client.inject_token("Bearer {}".format(event["farosToken"]))

    query = """{
              iam_roleDetail {
                data {
                  roleId
                  roleName
                  attachedManagedPolicies {
                    policyName
                    policyArn
                  }
                  farosAccountId
                  farosRegionId                  
                }      
              }
            }"""

    response = client.execute(query)
    response_json = json.loads(response)
    roles = response_json["data"]["iam_roleDetail"]["data"]
    required_policy_arns = event["params"]["required_policy_arns"].split(",")
    roles_without_policies = []
    for role in roles:
        policies = [p["policyArn"] for p in role["attachedManagedPolicies"]]
        missing_policies = get_missing_policies(required_policy_arns, policies)
        if missing_policies:
            roles_without_policies.append({
                "roleId": role["roleId"],
                "roleName": role["roleName"],
                "farosAccountId": role["farosAccountId"],
                "farosRegionId": role["farosRegionId"],
                "missing_policies": missing_policies
            })

    return roles_without_policies
