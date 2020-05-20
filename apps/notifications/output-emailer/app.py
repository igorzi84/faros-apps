from graphqlclient import GraphQLClient
from jinja2 import Environment, FileSystemLoader
import os
import json


def lambda_handler(event, context):
    client = GraphQLClient("https://api.faros.ai/v0/graphql")
    client.inject_token("Bearer " + event["farosToken"])
    params = event['params']
    report_name = params['report_name']
    recipient = params['recipient']
    records = event.get('data')

    if records:
      header = list(records[0].keys())
      data = [[record[k] for k in header] for record in records]
    else:
      header = None
      data = []

    file_loader = FileSystemLoader(os.path.dirname(__file__))
    env = Environment(loader=file_loader)
    template = env.get_template('email.html')
    html = template.render(report_name=report_name, header=header, data=data)

    sender = 'no-reply@faros.ai'
    subject = 'Faros AI notification'

    query = '''mutation($to: [String!]!, $subject: String!, $htmlBody: String!) {
        faros_send_email(
            to: $to
            subject: $subject
            textBody: "This report can only be seen in HTML enabled email clients"
            htmlBody: $htmlBody
        )
    }'''
    variables = {
        "to": [recipient],
        "subject": subject,
        "htmlBody": html
    }

    response = client.execute(query, variables)
    response_json = json.loads(response)

    return { "data" : response_json }
