import os
from pathlib import Path

import slack
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

# loading environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

todo_list = []
important_links = {
                    'SWAG': 'https://swagup.typeform.com/to/FK4IFawL',
                   'ONBOARD': 'https://confluence.lblw.cloud/'
                              'display/EX/Onboarding+plan',
                   'OFFICE': 'https://apps.powerapps.com/play/'
                             '3111bc06-74c2-4981-ab52-881d4461a0e3?tenant'
                             'Id=eaa6cb52-58d7-45cd-8bd6-b1d2a8e61312'
                }

connecting_data = {
    "HR": [
            {
                "name": "Human Resource1",
                "email": "humanresource1@loblaw.ca",
                "title": "Human resource manager"
            },
            {
                "name": "Human Resource2",
                "email": "humanresource2@loblaw.ca",
                "title": "Human resource manager"
            },
            {
                "name": "Human Resource3",
                "email": "humanresource3@loblaw.ca",
                "title": "Human resource manager"
            }
        ],
    "IT": [
            {
                "name": "Developer1",
                "email": "developer1@loblaw.ca",
                "title": "Developer I"
            },
            {
                "name": "Developer2",
                "email": "developer2@loblaw.ca",
                "title": "Developer manager"
            }
        ],
    "PRODUCT": [
            {
                "name": "PM1",
                "email": "pm1@loblaw.ca",
                "title": "Product manager"
            },
            {
                "name": "PM2",
                "email": "pm2@loblaw.ca",
                "title": "Product manager"
            }
        ],
}
definitions = {
    'CONFLUENCE': 'Our content collaboration tool used to help teams '
                  'to collaborate and share knowledge efficiently',
    'CLV': 'Customer Lifetime Value',
    'DEI': 'Diversity Equity and Inclusion',
    'EDW': "An enterprise data warehouse (EDW) is a relational data warehouse "
           "containing a companys business data, including information "
           "about its customers.",
    'WELLD': 'A “welcoming” slack companion that enables new employees to get '
             'onboarded and connected with ease'
}

default_text_acronyms = definitions.keys()
default_text_resouces = important_links.keys()
default_text_connecting = connecting_data.keys()


@slack_event_adapter.on('message')
def repeats_message(payload):
    # looking for the key event
    event = payload.get('event', {})

    # get the channel id from the channel
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    default_text_a = ''
    for term in default_text_acronyms:
        default_text_a += ' ' + term

    default_text_r = ''
    for term in default_text_resouces:
        default_text_r += ' ' + term

    default_text_c = ''
    for term in default_text_connecting:
        default_text_c += ' ' + term

    # greetings
    if text in ['hi', 'Hi', 'morning', 'hello', 'hi there']:
      if user_id != BOT_ID:
           client.chat_postMessage(channel=channel_id,
                                    text='Welcome to LD, I\'m WelLD, I will be your onboarding companion '
                                         'for all of your questions and concerns. \n\n'
                                         'For: \n'
                                         'Acronyms: /acronym '
                                         '({})\n'
                                         'Resources: /resources '
                                         '({})\n'
                                         'Connections: /connecting '
                                         '({})\n'
                                         'End Conversation: /end \n'
                                         'Create todo list: /todo '
                                         '(task1, task2, task3)'.format(
                                             default_text_a,
                                             default_text_r,
                                             default_text_c))


@app.route('/acronyms', methods=['POST'])
def acronyms():
    data = request.form
    # user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    word = data.get('text').upper()
    input_text = word

    default_text = ''
    for term in default_text_acronyms:
        default_text += '\n\t' + term
    
    if word in definitions:
        word = definitions.get(word, "Sorry! Definition not found")
        client.chat_postMessage(channel=channel_id, text=f'{input_text}: {word}')
    else:
        word = "Sorry! Definition not found"

    client.chat_postMessage(channel=channel_id,
                          text="Please see a list of acronyms commonly used in our department after '/acronyms':"
                                 "{}\ni.e. /acronyms WELLD".format(default_text))

    return Response(), 200


@app.route('/resources', methods=['POST'])
def resources():
    data = request.form
    # user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    link = data.get('text').upper()
    input_text = link

    default_text = ''
    for term in default_text_resouces:
       default_text += '\n\t' + term

    if link in important_links:
        link = important_links.get(
            link, f"Sorry! Resource not found, please try another word:{default_text}")
        client.chat_postMessage(
            channel=channel_id, text=f'Here, we found these links: \n {input_text}: {link}')
    else:
      link = "Sorry! Resource not found, please try another word:{}".format(default_text)

    client.chat_postMessage(channel=channel_id, xtext="Please use terms in this list after '/resources':"
                                 "{}\ni.e. /resources swag".format(default_text))

    return Response(), 200


@app.route('/connecting', methods=['POST'])
def connecting():
    data = request.form
    channel_id = data.get('channel_id')
    text = data.get('text')
    department = connecting_data.get(text.upper(), None)
    default_text = ''
    for term in default_text_connecting:
        default_text += '\n\t' + term
    
    print(text, department)
    info = ""
    if department == None:
        info = "Please use terms in this list after '/connecting': \n {}" \
               "\ni.e. /connecting HR".format(default_text)
    else:
        for p in department:
            info += "Name: " + p.get("name") + ", email: " + p.get("email") + ", title: " + p.get("title") + "\n"

    client.chat_postMessage(channel=channel_id, text=info)

    return Response(), 200


@slack_event_adapter.on('member_joined_channel')
def onboard_tasks(payload):
    event = payload.get('event', {})
    user_id = event.get('user')
    if BOT_ID != user_id:
        client.chat_postMessage(channel=user_id,
                                text="WELCOME ABOARD!", blocks=[
                                    {
                                        "type": "section",
                                        "text": {
                                            "type": "mrkdwn",
                                            "text": "TO-DO"
                                        },
                                        "accessory": {
                                            "type": "checkboxes",
                                            "options": [
                                                            {
                                                                "text": {
                                                                    "type": "mrkdwn",
                                                                    "text": todo_list[0]
                                                                },
                                                                "description": {
                                                                    "type": "mrkdwn",
                                                                    "text": "*this is mrkdwn text*"
                                                                },
                                                                "value": "value-0"
                                                            },
                                                            {
                                                                "text": {
                                                                    "type": "mrkdwn",
                                                                    "text": todo_list[1]
                                                                },
                                                                "description": {
                                                                    "type": "mrkdwn",
                                                                    "text": "*this is mrkdwn text*"
                                                                },
                                                                "value": "value-1"
                                                            },
                                                            {
                                                                "text": {
                                                                    "type": "mrkdwn",
                                                                    "text": todo_list[2]
                                                                },
                                                                "description": {
                                                                    "type": "mrkdwn",
                                                                    "text": "*this is mrkdwn text*"
                                                                },
                                                                "value": "value-2"
                                                            }
                                                        ],
                                                    "action_id": "checkboxes-action"
                                            }
                                        }
                                    ])


@app.route('/todo', methods=['POST'])
def todo():
    data = request.form
    text = data.get('text')
    channel_id = data.get('channel_id')
    
    global todo_list
    todo_list = text.split(",")
    print(todo_list)
    
    print_list = ''
    for t in todo_list:
        print_list = print_list + '\n' + t

    client.chat_postMessage(channel=channel_id, text=f'You have created a todo list: {print_list}')
    
    return Response(), 200


@app.route('/end', methods=['POST'])
def end():
    data = request.form
    channel_id = data.get('channel_id')

    client.chat_postMessage(channel=channel_id, text='bye, have a nice day')
    return Response(), 200


if __name__ == '__main__':
    app.run(debug=True)  # port 5000
