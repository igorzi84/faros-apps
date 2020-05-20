import json
from graphqlclient import GraphQLClient
from datetime import datetime


def days_diff(date_string):
   return (datetime.utcnow() - datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")).days


def lambda_handler(event, context):
    client = GraphQLClient("https://api.faros.ai/v0/graphql")
    client.inject_token("Bearer {}".format(event["farosToken"]))

    query = '''{
              ec2_instance {
                data {
                  instanceId
                  state {
                    name
                  }
                  launchTime
                  farosAccountId
                  farosRegionId
                }
              }
            }'''

    response = client.execute(query)
    response_json = json.loads(response)
    instances = response_json["data"]["ec2_instance"]["data"]
    cutoff = int(event["params"]["num_days"])
    return [
      i for i in instances
      if i["state"]["name"] == "running" and days_diff(i["launchTime"]) > cutoff
    ]
