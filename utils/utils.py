import requests
from config import PAGE_ACCESS_TOKEN
import json
socketio = None
chatbot_db = None

# sending text or url message to facebbok
def callsendapi1(sender, response,page_access_token):
  
    payload = {
        "recipient": {"id": sender},
        "message": {"text": response},
        "message_type": "RESPONSE"
    }
    headers = {"content-type": "application/json"}
    url = "https://graph.facebook.com/v15.0/me/messages?access_token={}".format(
        page_access_token)
    send_resp = requests.post(url, json=payload, headers=headers)

# sending  image , video message to facebbok


def callsendapi2(sender, response,page_access_token):

    payload = {
        "recipient": {"id": sender},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": response
                }
            }
        },
        "message_type": "RESPONSE"
    }
    headers = {"content-type": "application/json"}
    url = "https://graph.facebook.com/v15.0/me/messages?access_token={}".format(
        page_access_token)
    send_resp = requests.post(url, json=payload, headers=headers)
    
    str_data=json.dumps(send_resp.json())
    with open("fafa.txt","w") as f:
        f.write(str_data)


def callsendapi3(sender, response,page_access_token):

    payload = {
        "recipient": {"id": sender},
        "message": {
            "attachment": {
                "type": "video",
                "payload": {
                    "url": response
                }
            }
        },
        "message_type": "RESPONSE"
    }
    headers = {"content-type": "application/json"}
    url = "https://graph.facebook.com/v15.0/me/messages?access_token={}".format(
        page_access_token)
    send_resp = requests.post(url, json=payload, headers=headers)
    
    str_data=json.dumps(send_resp.json())
    with open("fafa.txt","w") as f:
        f.write(str_data)


msg_types = {
    "text": callsendapi1,
    "url": callsendapi1,
    "image": callsendapi2,
    "video": callsendapi3
}


def handlemessage(sender, message_body, me,pageId):
    if "text" in message_body:
        meesage_from_facebook = message_body["text"]

        response = {"text": meesage_from_facebook,
                    "type": message_body['type'], "id": sender, "me": me}
        
        print("rec----------------------------------------------------------------------------------------------")

        socketio.emit('recived_message_from_facebook',
                      response, broadcast=True,room=pageId)

    else:
        response = {"text": "من فضلك ادخل نص فقط"}
        callsendapi1(sender, response)


def get_current_user(sender_id, users):
    isFound = False
    if (len(users) > 0):
        for idx, user in enumerate(users):
            if sender_id == user['id']:
                isFound = True
                current_user = user
                entered_cards = user['cards']
                user_index = idx
                is_new = False
                current_user['isNew'] = False
                current_user['isAIActivated'] = False if user['isAIActivated'] == None else user['isAIActivated']
                current_user['isFChatActivated'] = False if user['isFChatActivated'] == None else user['isFChatActivated']
                current_user['isCollectMailActivated'] = False if user['isCollectMailActivated'] == None else user['isCollectMailActivated']
                current_user['cards'] = entered_cards
                return current_user, entered_cards, user_index
        if not isFound:
            entered_cards = []
            current_user = {}
            is_new = True
            decativate = False
            current_user['id'] = sender_id
            current_user['isNew'] = is_new
            current_user['isAIActivated'] = decativate
            current_user['isFChatActivated'] = decativate
            current_user['isCollectMailActivated'] = decativate
            return current_user, entered_cards, -1
    else:
        entered_cards = []
        current_user = {}
        is_new = True
        decativate = False
        current_user['id'] = sender_id
        current_user['isNew'] = is_new
        current_user['isAIActivated'] = decativate
        current_user['isFChatActivated'] = decativate
        current_user['isCollectMailActivated'] = decativate
        return current_user, entered_cards, -1




import re
 
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
def email_checker(email):
    if(re.fullmatch(regex, email)):
        return "Thanks, I recived your mail"
    else:
        return "Sorry this mail is invalid. please re-enter your email."