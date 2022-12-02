from flask import Flask, request, jsonify,request
from flask_cors import CORS
import sys
from config import PAGE_ACCESS_TOKEN, MODEL_URI, VERIFY_TOKEN
import requests
import random
import logging

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "testtest123"


@app.route("/facebook_verfied", methods=['GET'])
def fbverify():
    
    print("f1")
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token missmatch", 403
        return request.args['hub.challenge'], 200
    
    return "Hello Facebook", 200


@app.route("/facebook_verfied", methods=['POST'])
def fbverify2():
    
    data = request.get_json()
    print(data)
    print("************************************************")
    
    return "Hello Facebook", 200

if __name__ == "__main__":
    app.run(port=8080, debug=True)


