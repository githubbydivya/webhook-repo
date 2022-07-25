import enum
from datetime import datetime, timezone

import certifi
import pymongo

from flask import request
from flask import json
from flask import Flask, render_template, make_response, jsonify

from app.extensions import MongoConnection

app = Flask(__name__)

# Fetch DB connections for Mongo
db = MongoConnection()
db = db.connect()

title = "Webhook Receiver application with Flask and MongoDB"
heading = "Webhook Receiver Data"


@app.route('/')
def api_root():
    return 'Welcome to Webhook Project'


class GithubActionEnum(enum.Enum):
    PUSH = 1
    PULL_REQUEST = 2
    MERGE = 3


def save_data_info_in_db(info):
    data = json.loads(info)
    # Section for Push Request
    if "commits" in data:
        request_id = data['after']
        action = GithubActionEnum.PUSH.name
        author = data['head_commit']['author']['name']
        timestamp = format_dates(data['head_commit']['timestamp'])
        from_branch = data['ref']
        to_branch = data['repository']['master_branch']
        db.mongoDB.webhookReceiver.insert_one(
            {'request_id': request_id, 'author': author, 'action': action, 'from_branch': from_branch,
             'to_branch': to_branch, 'timestamp': timestamp})
    elif "action" in data and data['action'] == 'opened':
        request_id = data['pull_request']['head']['sha']
        action = GithubActionEnum.PULL_REQUEST.name
        author = data['sender']['login']
        timestamp = format_dates(data['repository']['pushed_at'])
        from_branch = data['pull_request']['base']['ref']
        to_branch = data['pull_request']['head']['ref']
        db.mongoDB.webhookReceiver.insert_one(
            {'request_id': request_id, 'author': author, 'action': action, 'from_branch': from_branch,
             'to_branch': to_branch, 'timestamp': timestamp})
    elif "action" in data and data['action'] == 'closed':
        request_id = data['pull_request']['merge_commit_sha']
        action = GithubActionEnum.MERGE.name
        author = data['sender']['login']
        timestamp = format_dates(data['repository']['pushed_at'])
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']
        db.mongoDB.webhookReceiver.insert_one(
            {'request_id': request_id, 'author': author, 'action': action, 'from_branch': from_branch,
             'to_branch': to_branch, 'timestamp': timestamp})

    print("Data Inserted in Mongo DB")


@app.route('/webhook/receiver', methods=['POST'])
def gh_webhook_receiver():
    info = json.dumps(request.json)
    print("gh_webhook_receiver Data -> ", info)
    save_data_info_in_db(info)
    return info


@app.route('/webhook/data', methods=['GET'])
def gh_webhook_data():
    cursor = db.mongoDB.webhookReceiver.find({})
    return render_template('index.html', webhookData=cursor, t=title, h=heading)


def format_dates(date_string):
    dt_obj = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')
    dt_obj_utc = dt_obj.astimezone(timezone.utc)
    formatted_date = dt_obj_utc.strftime("%d  %B %Y %H:%M %p %Z")
    print(formatted_date)
    return special_nth_day(formatted_date)


def special_nth_day(formatted_date: str,
                    dic={'1': 'st', '2': 'nd', '3': 'rd'}):
    formatted_date_list = list(formatted_date)
    char_date_0 = formatted_date_list[0]
    char_date_1 = formatted_date_list[1]
    if char_date_0 == '1':
        formatted_date_list[2] = 'th'
    elif char_date_0 == '0' or char_date_0 == '2' or char_date_0 == '3':
        val_from_dic = None
        if char_date_1 in dic:
            val_from_dic = dic[char_date_1]
        if val_from_dic:
            formatted_date_list[2] = val_from_dic
        else:
            formatted_date_list[2] = 'th'

    formatted_date_list_new = ''.join(formatted_date_list)
    return formatted_date_list_new


if __name__ == '__main__':
    # flask run --port = 5002
    app.run(debug=True, port=5002)
