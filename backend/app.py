from flask import Flask, jsonify, request
from flask_cors import CORS

import requests

# Slack APIのBotトークン
SLACK_TOKEN1 = 'xoxp-7198233806352-'
SLACK_TOKEN2 = '7175441389970-7182903419191-'
SLACK_TOKEN3 = '7e54c0d85954ca33cca5d344c4b5ff44'
SLACK_TOKEN = SLACK_TOKEN1 + SLACK_TOKEN2 + SLACK_TOKEN3
CHANNEL_ID = 'C07VATEAM4M'

app = Flask(__name__)
CORS(app, origins="http://localhost:4200")  # CORSを有効にする

data = {"message": "Hello from Flask!"}  # 初期メッセージ
@app.route('/')
def hello_world():
    # 意図的にエラーを発生
    return 1 / 0  # ゼロ除算エラー
# GETリクエストを受け取るエンドポイント
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)

# POSTリクエストを受け取るエンドポイント
@app.route('/api/data', methods=['POST'])
def post_data():
    content = request.json  # リクエストのJSONデータを受け取る
    data["message"] = content.get("message", "No message")
    return jsonify({"status": "success", "data": data}), 200

# GETリクエストを受け取るエンドポイント
@app.route('/api/tallyData', methods=['GET'])
def post_tallyData():
    data = fetch_channel_reactions(CHANNEL_ID)
    print(data)
    # display_reactions(data)
    return jsonify(data)


# メッセージ履歴を取得する関数
def get_messages(channel_id, cursor=None):
    url = 'https://slack.com/api/conversations.history'
    headers = {
        'Authorization': f'Bearer {SLACK_TOKEN}',
    }
    params = {
        'channel': channel_id,
        'cursor': cursor,
        'limit': 10000 # 一度に取得するメッセージ数
    }
    
    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()

    if not response_data.get('ok'):
        print(f"Error: {response_data.get('error')}")
        return [], None

    return response_data['messages'], response_data.get('response_metadata', {}).get('next_cursor')

# リアクション情報を取得する関数
def get_reactions(channel_id, timestamp):
    url = 'https://slack.com/api/reactions.get'
    headers = {
        'Authorization': f'Bearer {SLACK_TOKEN}',
    }
    params = {
        'channel': channel_id,
        'timestamp': timestamp
    }
    
    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()

    if not response_data.get('ok'):
        print(f"Error: {response_data.get('error')}")
        return None

    return response_data.get('message', {}).get('reactions', [])

# チャンネル内のリアクション情報を取得して表示
def fetch_channel_reactions(channel_id):
    cursor = None
    all_reactions = []

    # メッセージ履歴を取得
    while True:
        messages, cursor = get_messages(channel_id, cursor)

        if not messages:
            break
        
        for message in messages:
            print(message)
            timestamp = message['ts']
            text = message['text']

            # メッセージにリアクションがあれば取得
            reactions = get_reactions(channel_id, timestamp)
            # if reactions:
            for reaction in reactions:
                emoji = reaction['name']
                count = reaction['count']
                users = reaction['users']
                all_reactions.append({
                    'message': text,
                    'timestamp': timestamp,
                    'emoji': emoji,
                    'count': count,
                    'users': users
                })

        if not cursor:
            break

    return all_reactions

# リアクションの結果を表示
def display_reactions(reactions):
    if not reactions:
        print("No reactions found.")
        return

    for reaction in reactions:
        print(f"Message: {reaction['message']}")
        print(f"Timestamp: {reaction['timestamp']}")
        print(f"Emoji: {reaction['emoji']} (Count: {reaction['count']})")
        print(f"Users: {', '.join(reaction['users'])}")
        print("=" * 40)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)
