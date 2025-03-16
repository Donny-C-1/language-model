from flask import Flask, request, jsonify, abort
import subprocess
import os
import hmac
import hashlib
import json

app = Flask(__name__)

GITHUB_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")

def verify_signature(payload, signature):
    # Verify that the request came from github
    if not GITHUB_SECRET:
        print("GITHUB_WEBHOOK_SECRET is missing!")
        return False
    
    computer_hash = "sha256=" + hmac.new(GITHUB_SECRET.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computer_hash, signature)

@app.route("/")
def home():
    return jsonify({ "message": "Who am I, How did i get stuck behind this screen!" })

@app.route("/deploy", methods=["POST"])
def deploy():
    # Verify GitHub signature
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature or not verify_signature(request.data, signature):
        abort(403, "Invalid signature")

    if request.headers.get("X-Github-Event") == "push":
        payload = request.get_json()
        branch = payload.get("ref") # Example: "refs/heads/production"

        if branch != "refs/heads/production":
            return "Push was not to production branch, ignoring.", 200 # Ignore other branches
        
        
        try:
            # Change to my repo directory
            os.chdir("/home/DonnyC/languagemodel")

            # Pull the latest changes from the production branch
            subprocess.run(['git', 'pull', 'origin', 'production'], check=True)

            # Install dependencies
            subprocess.run(['/home/DonnyC/languagemodel/venv/bin/pip', 'install', '-r', 'requirements.txt'], check=True)

            # Reload the web app
            subprocess.run(['/usr/bin/python3.8', '/home/DonnyC/.virtualenvs/DonnyC/bin/pythonanywhere-web-app-reload.py', 'donnyc.pythonanywhere.com'], check=True)

            return 'Deployment successful', 200
        except subprocess.CalledProcessError as e:
            return f'Deployment failed: {e}', 500
        except Exception as e:
            return f'Deployment failed: {e}', 500
    else:
        return 'Not a push event', 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) #Remove debug=True for production environment