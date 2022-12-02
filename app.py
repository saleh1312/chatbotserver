from flask import Flask, request, jsonify
from flask_socketio import join_room, leave_room
from flask_socketio import SocketIO
from flask_cors import CORS
import utils.utils as utils
import time
from database.database import ChatbotDatabase
from datetime import datetime
import pytz


app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "testtest123"

utils.socketio = SocketIO(app, logger=True, engineio_logger=True,
                             cors_allowed_origins="*")
                          
# initialize chatbot database
utils.chatbot_db = ChatbotDatabase()

from facebook.facebookRoute import fbRoute
from instagram.instagramRoute import instaRoute
from website.websiteRoute import webRoute
from website.websiteApi import WebsiteAPI
from facebook.facebookApi import FacebookAPI
from instagram.instagramApi import InstagramAPI
from config import PAGE_ACCESS_TOKEN



app.register_blueprint(fbRoute)
app.register_blueprint(instaRoute)
app.register_blueprint(webRoute)


# This is API key for facebook messenger.
API = "https://graph.facebook.com/v14.0/me/messages?access_token="+PAGE_ACCESS_TOKEN
facebook_chatbot = FacebookAPI(API)
instagram_chatbot = InstagramAPI(API)
web_chatbot = WebsiteAPI()
#
savedDestID = None
savedIndx = None

my_flows = utils.chatbot_db.getAllFlows()
my_arrows = utils.chatbot_db.getAllArrows()
my_users = utils.chatbot_db.getAllUsers()
my_admins = utils.chatbot_db.getAllAdmins()
history_ids = my_users

# Prepare all flows
final_map = utils.chatbot_db.flows_preparation(my_flows)

# Welcome Messages
welcome_messages = ["start", "hi", "hello",
                    "السلام عليكم", "ازيك",
                    "ايه الاخبار", "welcome",
                    "get started", "get start"
                    ]


# @app.route("/", methods=['GET'])
# def fbverify():
#     return "Facebook", 200


@app.route("/instagram", methods=['GET'])
def instagramVerify():
    return "Hello Instagram", 200

@app.route("/instagram", methods=['GET'])
def instaWebhook():
    return "Instagram", 200


@app.route("/website", methods=['POST'])
def websiteWebhook():
    return "website", 200


@app.route('/add_flows', methods=['POST'])
def add_flows():
    global my_flows
    global my_arrows
    flows = request.get_json(force=True)['flows']
    arrows = request.get_json(force=True)['arrows']
    my_flows = flows
    my_arrows = arrows
    utils.chatbot_db.createFlow(flows)
    utils.chatbot_db.addArrows(arrows)
    resp = jsonify({"Res": "you added " + str(len(flows)) +
                   " flows successfuly connected with " + str(len(arrows)) + " arrows."})
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


@app.route('/get_flows', methods=['GET'])
def get_flows():
    my_flows = utils.chatbot_db.getAllFlows()
    my_arrows = utils.chatbot_db.getAllArrows()
    resp = jsonify({"flows": my_flows, "arrows": my_arrows})
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


@app.route('/get_users', methods=['GET'])
def get_users():
    global my_users
    resp = jsonify({"users": my_users, })
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


@app.route('/get_admins', methods=['GET'])
def get_admins():
    my_admins = utils.chatbot_db.getAllAdmins()
    resp = jsonify({"admins": my_admins, })
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp

@app.route('/add_admins', methods=['POST'])
def add_admins():
    admin = request.get_json(force=True)['admin']
    utils.chatbot_db.addAdmin(admin)
    resp = jsonify({"Res": "User added successfuly"})
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp

@app.route('/update_admins', methods=['POST'])
def update_admins():
    admin = request.get_json(force=True)['admin']
    utils.chatbot_db.updateAdmin(admin)
    utils.chatbot_db.updateAdminFlow(admin)
    resp = jsonify({"Res": "User updated successfuly"})
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp

@app.route('/update_admin_flow', methods=['POST'])
def update_admin_flow():
    admin = request.get_json(force=True)['admin']
    utils.chatbot_db.updateAdminFlow(admin)
    resp = jsonify({"Res": "User updated successfuly"})
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


@utils.socketio.on('connect')
def test_connect(client):
    foo = request.args.get('foo')

    join_room(foo)
    utils.socketio.emit('testing',
                  "hello from server", broadcast=True,room=foo)
    
    print("client connected")


@utils.socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@utils.socketio.on('testing')
def sending(data):
    utils.socketio.emit('testing', data, broadcast=True)


@utils.socketio.on('sending_data_to_facebook')
def sending_to_facebook(data):
    ide = data["id_user"]
    text = data["text"]
    me = data["me"]
    typee = data["type"]

    print(ide, text, me)
    utils.msg_types[typee](ide, text)
    utils.socketio.emit('recived_message_from_facebook', {
        "text": text, "id": ide, "me": me, "type": typee, "from_facebook": False}, broadcast=True)




def async_sending_message_broadcast(data):
    """
    datetime_object = datetime.strptime(data["timer"], '%Y-%m-%dT%H:%M:%S.%fZ')
    now = datetime.now(tz=pytz.utc).replace(tzinfo=None)
   
    margin = datetime_object-now
    total_secs_to_sleep=int(margin.total_seconds()) 
    print("total secs to sleep")
    total_secs_to_sleep
    """
    if data["state"]=="Schedule":
        time.sleep(data["timer"])
    
    print("//////////////")
    print(data)
    print("//////////////")
    content = data["content"]
    filterList = data["filterList"]
    myUsers = data["myUsers"]
    page_data = data["page_data"]


    for user in myUsers:
        filter_status=True
        if not any(x in filterList["Cards"] for x in user["cards"]):
            filter_status=False


        if filter_status:

            for key,message in content.items():
                print(message)
                utils.msg_types[message["type"].lower()](user["id"], message["content"],page_data["pageAccessToken"])
                utils.socketio.emit('recived_message_from_facebook', {
                    "text": message["content"], "id": user["id"], "me": True, "type": message["type"].lower()}, broadcast=True,
                    room=page_data["pageInfo"]["pageId"])

@utils.socketio.on('broadcasting_filtered')
def sending_to_multi_facebook_filtered(data):
    utils.socketio.start_background_task(async_sending_message_broadcast,data)
                


def test(ff):
    time.sleep(10)
    print("ahahahahahh")
    print(ff)

@app.route("/free", methods=['GET'])
def instagramVerifyfre():
    utils.socketio.start_background_task(test,"fff")
    return "Hello Instagram", 200
    
    

if __name__ == "__main__":
    app.run(port=3030, debug=True, threaded=True)
    # utils.socketio.run(app, port=5004)
    #utils.socketio.run(app, port=8080, allow_unsafe_werkzeug=True,debug=True)
    # app.run()
