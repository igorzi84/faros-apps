import json
from graphqlclient import GraphQLClient


def lambda_handler(event, context):
    client = GraphQLClient("https://api.faros.ai/v0/graphql")
    client.inject_token("Bearer {}".format(event["farosToken"]))

    query = '''{
              ec2_volume {
                data {
                  volumeId
                  instance {
                    instanceId
                    state {
                      name
                    }
                  }
                  farosAccountId
                  farosRegionId 
                }
              }
            }'''

    response = client.execute(query)
    response_json = json.loads(response)
    volumes = response_json["data"]["ec2_volume"]["data"]
    return [i for i in volumes if i["instance"]["state"]["name"] == "stopped"]
