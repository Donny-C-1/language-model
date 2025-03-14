from flask import Flask, request, jsonify;

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({ "message": "Who am I, How did i get stuck behind this screen!" })

if __name__ == "__main__":
    app.run(debug=True) #Remove debug=True for production environment