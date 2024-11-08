import requests

# Slack APIのBotトークン
SLACK_TOKEN = 'xoxp-7198233806352-7175441389970-7182903419191-'\
'7e54c0d85954ca33cca5d344c4b5ff44'
CHANNEL_ID = 'C07VATEAM4M'

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

# メイン処理
if __name__ == "__main__":
    reactions = fetch_channel_reactions(CHANNEL_ID)
    display_reactions(reactions)