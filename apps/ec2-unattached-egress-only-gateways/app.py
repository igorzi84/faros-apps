import json
from graphqlclient import GraphQLClient


def lambda_handler(event, context):
    client = GraphQLClient("https://api.faros.ai/v0/graphql")
    client.inject_token("Bearer {}".format(event["farosToken"]))

    query = '''{
              ec2_egressOnlyInternetGateway {
                data {
                  egressOnlyInternetGatewayId
                  attachments {
                    vpcId
                  }
                  farosAccountId
                  farosRegionId
                }
              }
            }'''

    response = client.execute(query)
    response_json = json.loads(response)
    gateways = response_json["data"]["ec2_egressOnlyInternetGateway"]["data"]
    return [g for g in gateways if not g["attachments"]]
