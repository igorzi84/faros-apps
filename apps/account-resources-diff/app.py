import json
from graphqlclient import GraphQLClient
from termcolor import colored

def filter_list(data, key, account):
    ret = [x for x in data if x["farosAccountId"] == account]
    ret = sorted(ret, key = lambda x: x[key])

    return ret

def diff_sorted_lists(list1, list2, key):
    pointer1 = 0
    pointer2 = 0
    diffs = []
    while pointer1 < len(list1) and pointer2 < len(list2):
        item1 = list1[pointer1]
        item2 = list2[pointer2]

        if item1[key] < item2[key]:
            diffs.append(colored("- " + json.dumps(item1, indent=4, sort_keys=True), "red"))
            pointer1 += 1
        elif item1[key] > item2[key]:
            diffs.append(colored("+ " + json.dumps(item2, indent=4, sort_keys=True), "green"))
            pointer2 += 1
        else:
            # diffs.append(json.dumps(item2, indent=4, sort_keys=True))
            pointer1 += 1
            pointer2 += 1

    return diffs

def lambda_handler(event, context):
    client = GraphQLClient("https://api.faros.ai/v0/graphql")
    client.inject_token("Bearer " + event["farosToken"])

    query = event["params"]["query"]
    key = event["params"]["key"]
    ref_account_id = event["params"]["ref_account_id"]
    new_account_id = event["params"]["new_account_id"]

    response = client.execute(query)
    response_json = json.loads(response)

    object_name = next(iter(response_json["data"]))
    data = response_json["data"][object_name]["data"]

    list1 = filter_list(data, key, ref_account_id)
    list2 = filter_list(data, key, new_account_id)

    return diff_sorted_lists(list1, list2, key)
