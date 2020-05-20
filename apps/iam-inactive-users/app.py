import json
from graphqlclient import GraphQLClient
from datetime import datetime


def days_diff(date_string):
    return (datetime.utcnow() - datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")).days


def lambda_handler(event, context):
    client = GraphQLClient("https://api.faros.ai/v0/graphql")
    client.inject_token("Bearer {}".format(event["farosToken"]))

    query = '''{
              iam_user {
                data {
                  userId
                  userName
                  passwordLastUsed
                  farosAccountId
                  farosRegionId
                }
              }
            }'''

    response = client.execute(query)
    response_json = json.loads(response)
    users = response_json["data"]["iam_user"]["data"]
    cutoff = int(event["params"]["max_days"])
    return [
      u for u in users
      if u["passwordLastUsed"] is None or days_diff(u["passwordLastUsed"]) > cutoff
    ]
