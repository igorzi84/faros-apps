import json
from graphqlclient import GraphQLClient


def lambda_handler(event, context):
    client = GraphQLClient("https://api.faros.ai/v0/graphql")
    client.inject_token("Bearer {}".format(event["farosToken"]))

    query = '''{
              ec2_securityGroup {
                data {
                  groupId
                  instances {
                    data {
                      instanceId
                    }
                  }
                  farosAccountId
                  farosRegionId
                }
              }
            }'''

    response = client.execute(query)
    response_json = json.loads(response)
    groups = response_json["data"]["ec2_securityGroup"]["data"]
    return [g for g in groups if not g["instances"]["data"]]
