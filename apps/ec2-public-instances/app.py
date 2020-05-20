import json
from graphqlclient import GraphQLClient


def lambda_handler(event, context):
    client = GraphQLClient("https://api.faros.ai/v0/graphql")
    client.inject_token("Bearer {}".format(event["farosToken"]))

    query = '''{
              ec2_instance {
                data {
                  instanceId
                  publicIpAddress
                  farosAccountId
                  farosRegionId                  
                }
              }
            }'''

    response = client.execute(query)
    response_json = json.loads(response)
    instances = response_json["data"]["ec2_instance"]["data"]
    return [i for i in instances if i["publicIpAddress"] is not None]
