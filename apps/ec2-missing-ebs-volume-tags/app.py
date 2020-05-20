import json
from graphqlclient import GraphQLClient


def missing_tags(instance_tags, volume_tags):
    return list(instance_tags - volume_tags)


def lambda_handler(event, context):
    client = GraphQLClient("https://api.faros.ai/v0/graphql")
    client.inject_token("Bearer {}".format(event["farosToken"]))

    query = '''{
              ec2_volume {
                data {
                  volumeId
                  tags {
                    key
                    value
                  }
                  state
                  instance {
                    tags {
                      key
                      value
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
    volumes_with_missing_tags = []
    for v in volumes:
        if v["state"] == "in-use":
            instance_tags = frozenset([t["key"] for t in v["instance"]["tags"]])
            volume_tags = frozenset([t["key"] for t in v["tags"]])
            delta = missing_tags(instance_tags, volume_tags)
            if delta:
                volumes_with_missing_tags.append({"volume": v, "missingKeys": delta})

    return volumes_with_missing_tags
