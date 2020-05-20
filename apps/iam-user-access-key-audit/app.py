import json
from graphqlclient import GraphQLClient
from datetime import datetime


def days_diff(date_string):
    return (datetime.utcnow() - datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")).days


def has_old_access_keys(access_keys, max_days):
    return [key for key in access_keys if key["status"] == "Active" and days_diff(key["createDate"]) > max_days]


def lambda_handler(event, context):
    client = GraphQLClient("https://api.faros.ai/v0/graphql")
    client.inject_token("Bearer {}".format(event["farosToken"]))

    query = '''{
              iam_userDetail {
                data {
                  userId
                  userName
                  accessKeys {
                    data {
                      status
                      createDate
                      accessKeyId
                    }
                  }
                  farosAccountId
                  farosRegionId
                }
              }
            }'''

    response = client.execute(query)
    response_json = json.loads(response)
    users = response_json["data"]["iam_userDetail"]["data"]
    old_access_keys = []
    cutoff = int(event["params"]["max_days"])
    for user in users:
        old_keys = [key for key in user["accessKeys"]["data"]
                    if key["status"] == "Active" and days_diff(key["createDate"]) > cutoff]
        if old_keys:
            old_access_keys.append({
                "userId": user["userId"],
                "userName": user["userName"],
                "accessKeys": old_keys,
                "farosAccountId": user["farosAccountId"],
                "farosRegionId": user["farosRegionId"]
            })

    return old_access_keys
