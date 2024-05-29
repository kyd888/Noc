from flask import Flask, request, jsonify
from instagrapi import Client
import json

app = Flask(__name__)

def get_engaged_users(instagram_username, instagram_password, target_username):
    cl = Client()
    cl.login(instagram_username, instagram_password)

    # Get the user's media
    user_id = cl.user_id_from_username(target_username)
    medias = cl.user_medias(user_id, amount=10)  # Adjust the amount as needed

    engaged_users = {}

    for media in medias:
        likers = cl.media_likers(media.pk)
        commenters = cl.media_comments(media.pk)

        for liker in likers:
            engaged_users[liker.username] = engaged_users.get(liker.username, 0) + 1
        
        for comment in commenters:
            engaged_users[comment.user.username] = engaged_users.get(comment.user.username, 0) + 1

    # Sort users by engagement
    sorted_users = sorted(engaged_users.items(), key=lambda x: x[1], reverse=True)
    return sorted_users

@app.route('/api/engaged_users', methods=['POST'])
def api_engaged_users():
    data = request.json
    instagram_username = data.get('instagram_username')
    instagram_password = data.get('instagram_password')
    target_username = data.get('target_username')

    if not instagram_username or not instagram_password or not target_username:
        return jsonify({'error': 'Instagram username, password, and target username are required'}), 400

    try:
        engaged_users = get_engaged_users(instagram_username, instagram_password, target_username)
        return jsonify(engaged_users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
