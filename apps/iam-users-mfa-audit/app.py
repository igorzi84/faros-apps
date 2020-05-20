import json
from graphqlclient import GraphQLClient


def lambda_handler(event, context):
    client = GraphQLClient("https://api.faros.ai/v0/graphql")
    client.inject_token("Bearer {}".format(event["farosToken"]))

    query = '''{
              iam_userDetail {
                data {
                  userId
                  userName
                  mfaDevices {
                    data {
                      serialNumber
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
    return [
        {
            "name": u["userName"],
            "id": u["userId"],
            "farosAccountId": u["farosAccountId"],
            "farosRegionId": u["farosRegionId"]
        }
        for u in users if not u["mfaDevices"]["data"]
    ]
