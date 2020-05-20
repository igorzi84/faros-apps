import json
from graphqlclient import GraphQLClient


def check_policies(policies):
    bad_policies = frozenset(["AmazonEC2FullAccess", "AutoScalingFullAccess",
                             "ElasticLoadBalancingFullAccess", "AutoScalingConsoleFullAccess"])

    for policy in policies:
        if policy["policyName"] in bad_policies:
            return True

    return False


def lambda_handler(event, context):
    client = GraphQLClient("https://api.faros.ai/v0/graphql")
    client.inject_token("Bearer {}".format(event["farosToken"]))

    query = '''{
              iam_roleDetail {
                data {
                  roleId
                  roleName
                  rolePolicyList {
                    policyName
                  }
                  farosAccountId
                  farosRegionId
                }
              }
            }'''

    response = client.execute(query)
    response_json = json.loads(response)
    policies = response_json["data"]["iam_roleDetail"]["data"]
    return [p for p in policies if check_policies(p["rolePolicyList"])]
