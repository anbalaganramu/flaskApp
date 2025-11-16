from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/<username>')
def get_user_gists(username):
    try:
        res = requests.get(f'https://api.github.com/users/{username}/gists')
        if res.status_code == 404:
            return jsonify({'error': 'User not found'}), 404
        res.raise_for_status()
        gists = res.json()
        # Return simplified info per assignment
        result = [
            {
                "id": g["id"],
                "description": g.get("description") or "",
                "html_url": g["html_url"]
            }
            for g in gists
        ]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)