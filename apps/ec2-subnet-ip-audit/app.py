import json
from graphqlclient import GraphQLClient


def check_subnets(subnets, count):
    return [s for s in subnets if s["availableIpAddressCount"] < count]


def lambda_handler(event, context):
    client = GraphQLClient("https://api.faros.ai/v0/graphql")
    client.inject_token("Bearer {}".format(event["farosToken"]))

    query = '''{
              ec2_subnet {
                data {
                  subnetId
                  availableIpAddressCount
                  farosAccountId
                  farosRegionId                  
                }
              }
            }'''

    response = client.execute(query)
    response_json = json.loads(response)
    subnets = response_json["data"]["ec2_subnet"]["data"]
    count = int(event["params"]["ip_count"])
    return [
      subnet for subnet in subnets
      if subnet["availableIpAddressCount"] < count
    ]
