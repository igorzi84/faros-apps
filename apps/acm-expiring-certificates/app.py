import json
from graphqlclient import GraphQLClient
from datetime import datetime


def days_diff(date_string):
    return (datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ") - datetime.utcnow()).days


def lambda_handler(event, context):
    client = GraphQLClient("https://api.faros.ai/v0/graphql")
    client.inject_token("Bearer {}".format(event["farosToken"]))

    query = '''{
              acm_certificateDetail {
                data {
                  certificateArn
                  notAfter
                  farosAccountId
                  farosRegionId
                }
              }
            }'''

    response = client.execute(query)
    response_json = json.loads(response)
    certificates = response_json["data"]["acm_certificateDetail"]["data"]
    cutoff = int(event["params"]["days_left"])
    return [c for c in certificates if days_diff(c["notAfter"]) < cutoff]
