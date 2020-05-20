import json
from graphqlclient import GraphQLClient


def get_policy_arns(user):
    policy_arns = [p["policyArn"] for p in user["attachedManagedPolicies"]]
    group_policy_arns = [p["policyArn"] for g in user["groups"]["data"] for p in g["attachedManagedPolicies"]]
    policy_arns.extend(group_policy_arns)
    return policy_arns


def get_missing_policies(required, attached):
    return list(frozenset(required).difference(attached))


def lambda_handler(event, context):
    client = GraphQLClient("https://api.faros.ai/v0/graphql")
    client.inject_token("Bearer {}".format(event["farosToken"]))

    query = """{
              iam_userDetail {
                data {
                  userId
                  userName
                  attachedManagedPolicies {
                    policyName
                    policyArn
                  }
                  groups {
                    data {
                      groupId
                      groupName
                      attachedManagedPolicies {
                        policyName
                        policyArn
                      }
                    }
                  }
                  farosAccountId
                  farosRegionId
                }
              }
            }"""

    response = client.execute(query)
    response_json = json.loads(response)
    users = response_json["data"]["iam_userDetail"]["data"]
    users_without_policies = []
    required_policy_arns = event["params"]["required_policy_arns"].split(",")

    for user in users:
        policies = get_policy_arns(user)
        missing_policies = get_missing_policies(required_policy_arns, policies)
        if missing_policies:
            users_without_policies.append({
                "userId": user["userId"],
                "userName": user["userName"],
                "farosAccountId": user["farosAccountId"],
                "farosRegionId": user["farosRegionId"],
                "missing_policies": missing_policies}
            )

    return users_without_policies
