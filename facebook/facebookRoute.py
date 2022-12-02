from flask import Blueprint, request
import requests
import random
from config import PAGE_ACCESS_TOKEN, MODEL_URI, VERIFY_TOKEN
from utils.utils import handlemessage, get_current_user, chatbot_db, email_checker
from facebook.facebookApi import FacebookAPI
import sys

fbRoute = Blueprint("fbRoute", __name__, template_folder="templates")


# initialize chatbot database

# This is API key for facebook messenger.
API = "https://graph.facebook.com/v14.0/me/messages?access_token="+PAGE_ACCESS_TOKEN
facebook_chatbot = FacebookAPI(API)
#
savedDestID = None
savedIndx = None

my_flows = chatbot_db.getAllFlows()
my_arrows = chatbot_db.getAllArrows()
my_users = chatbot_db.getAllUsers()
history_ids = my_users

# Prepare all flows
final_map = chatbot_db.flows_preparation(my_flows)

# Welcome Messages
welcome_messages = ["start", "hi", "hello",
                    "السلام عليكم", "ازيك", "ايه الاخبار", "welcome"]




@fbRoute.route("/facebook_verfied", methods=['GET'])
def fbverify():

    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token missmatch", 403
        return request.args['hub.challenge'], 200
    
    return "Hello Facebook", 200


@fbRoute.route("/facebook_verfied", methods=['POST'])
def fbwebhook():
    global facebook_chatbot
    global final_map
    global savedIndx
    global savedDestID
    global chatbot_db
    data = request.get_json()
    pageId = data['entry'][0]['messaging'][0]['recipient']['id']
    my_flows, my_arrows, my_users, userID, pageAccessToken = get_current_flow(pageId)
    api = "https://graph.facebook.com/v14.0/me/messages?access_token=" + pageAccessToken
    facebook_chatbot = FacebookAPI(api)
    final_map = chatbot_db.flows_preparation(my_flows)

    try:
        # Read messages from facebook messanger.
        message = data['entry'][0]['messaging'][0]['message'] if data['entry'][0]['messaging'][0].get(
            'message') else None
        sender_id = data['entry'][0]['messaging'][0]['sender']['id']
        postback_button = data['entry'][0]['messaging'][0]['postback'] if data['entry'][0]['messaging'][0].get(
            'postback') else None
        # read = data['entry'][0]['messaging'][0]['read'] if data['entry'][0]['messaging'][0].get(
        #     'read') else None
        current_user, entered_cards, user_index = get_current_user(sender_id, my_users)

        if postback_button != None:
            if postback_button['title'] == 'Get Started' or postback_button['title'] == "Start" or postback_button['title'] == 'start':
                entered_cards.append(final_map['box_1']['title'])
                current_user['cards'] = entered_cards
                current_user['id'] = sender_id
                if current_user['isNew']:
                    my_users.append(current_user)
                else:
                    my_users[user_index] = current_user
                chatbot_db.updateAdminUsers(my_users, userID)

                replies = []
                for btn in final_map['box_1']['content'][0]['buttons']:
                    replies.append({
                        "type": "postback",
                        "title": btn['button_text'],
                        "payload": "DEVELOPER_DEFINED_PAYLOAD",
                    })

                facebook_chatbot.send_type_action(sender_id)
                response = facebook_chatbot.message_with_buttons(
                    sender_id, final_map['box_1']['content'][0]['content_text'], replies)
                handlemessage(
                    sender_id, {'text': postback_button['title'], 'type': 'text'}, False,pageId)
                handlemessage(sender_id, {
                    'text':{'title': final_map['box_1']['content'][0]['content_text'], 'buttons': replies}, 'type': 'card'}, True,pageId)

                return response

        if message != None:
            if message['text'].lower() in welcome_messages:
                entered_cards.append(my_flows[0]['title']['text'])
                current_user['cards'] = entered_cards
                current_user['id'] = sender_id
                if current_user['isNew']:
                    my_users.append(current_user)
                else:
                    my_users[user_index] = current_user
                chatbot_db.updateAdminUsers(my_users, userID)

                replies = []
                for btn in final_map['box_1']['content'][0]['buttons']:
                    replies.append({
                        "type": "postback",
                        "payload": "<POSTBACK_PAYLOAD>",
                        "title": btn['button_text']
                    })

                if (len(replies) != 0):
                    facebook_chatbot.send_type_action(sender_id)
                    response = facebook_chatbot.message_with_buttons(
                        sender_id, final_map['box_1']['content'][0]['content_text'], replies)
                    print(response)

                    handlemessage(
                        sender_id, {'text': message['text'], 'type': 'button'}, False,pageId)
                    handlemessage(sender_id, {'text': {
                                  'title': final_map['box_1']['content'][0]['content_text'], 'buttons': replies}, 'type': 'card'}, True,pageId)

                else:
                    facebook_chatbot.send_type_action(sender_id)
                    response = facebook_chatbot.message_with_buttons(
                        sender_id, final_map['box_1']['content'][0]['content_text'], [])
                    handlemessage(
                        sender_id, {'text': message['text'], 'type': 'button'}, False,pageId)
                    handlemessage(sender_id, {
                                  'text': final_map['box_1']['content'][0]['content_text'], 'type': 'text'}, True,pageId)
                return response

        if message != None:
            if message['text'] == "انهاء":
                current_user['isAIActivated'] = False
                current_user['isFChatActivated'] = False
                current_user['isCollectMailActivated'] = False

                if current_user['isNew']:
                    my_users.append(current_user)
                else:
                    my_users[user_index] = current_user
                chatbot_db.updateAdminUsers(my_users, userID)

                replies = []
                for btn in final_map['box_1']['content'][0]['buttons']:
                    replies.append({
                        "type": "postback",
                        "title": btn['button_text'],
                        "payload": "DEVELOPER_DEFINED_PAYLOAD",
                    })

                facebook_chatbot.send_type_action(sender_id)
                response = facebook_chatbot.message_with_buttons(
                    sender_id, final_map['box_1']['content'][0]['content_text'], replies)
                handlemessage(
                    sender_id, {'text': message['text'], 'type': 'text'}, False,pageId)
                handlemessage(sender_id, {
                    'text': final_map['box_1']['content'][0]['content_text'], 'type': 'text'}, True,pageId)

                return response

            if current_user['isAIActivated']:
                all_context = []
                for content in final_map[savedDestID]['content']:
                    all_context.append(content['content_text'])
                all_context = ', '.join(all_context)
                model_resp = requests.post(f"{MODEL_URI}/qa", json={
                    "quest": message['text'],
                    "context": final_map[savedDestID]['content'][savedIndx]['content_text']
                }).json()

                facebook_chatbot.send_type_action(sender_id)
                response = facebook_chatbot.message_with_quick_replies(sender_id, model_resp['Res'], [
                    {
                        "content_type": "text",
                        "title": "انهاء",
                        "payload": "endAIChat",
                    },
                ])
                entered_cards.append(final_map[savedDestID]['title'])
                current_user['cards'] = entered_cards
                current_user['id'] = sender_id
                if current_user['isNew']:
                    my_users.append(current_user)
                else:
                    my_users[user_index] = current_user
                chatbot_db.updateAdminUsers(my_users, userID)

                return response

            if current_user['isFChatActivated']:
                response = requests.post(f"{MODEL_URI}/freechat", json={
                    "quest": message['text']
                }).json()

                facebook_chatbot.send_type_action(sender_id)
                response = facebook_chatbot.message_with_quick_replies(sender_id, response['Res'], [
                    {
                        "content_type": "text",
                        "title": "انهاء",
                        "payload": "endAIChat",
                    },
                ])
                entered_cards.append(final_map[savedDestID]['title'])
                current_user['cards'] = entered_cards
                current_user['id'] = sender_id
                if current_user['isNew']:
                    my_users.append(current_user)
                else:
                    my_users[user_index] = current_user
                return response

            if current_user['isCollectMailActivated']:
                check_msg = email_checker(message['text'])
                facebook_chatbot.send_type_action(sender_id)
                response = facebook_chatbot.text_message(sender_id, check_msg)
                if check_msg == "Sorry this mail is invalid. please re-enter your email.":
                    current_user['isCollectMailActivated'] = True
                else:
                    current_user['isCollectMailActivated'] = False
                # response = facebook_chatbot.message_with_quick_replies(sender_id, check_msg, [
                #     {
                #         "content_type": "text",
                #         "title": "انهاء",
                #         "payload": "endCollectMail",
                #     },
                # ])
                entered_cards.append(final_map[savedDestID]['title'])
                current_user['cards'] = entered_cards
                current_user['id'] = sender_id
                if current_user['isNew']:
                    my_users.append(current_user)
                else:
                    my_users[user_index] = current_user
                return response

            else:
                handlemessage(
                    sender_id, {'text': message['text'], 'type': 'text'}, False,pageId)
                handlemessage(sender_id, {'text': postback_button['title'], 'type':'button'}, False,pageId)
                handlemessage(sender_id, {'text': {'title': 'welcome', 'buttons': [{
                    "type": "web_url",
                    "url": "https://electro-pi.com/",
                    "title": "View Website"
                }, {
                    "type": "web_url",
                    "url": "https://www.facebook.com/ElectroPi.A.I/",
                    "title": "View FB Page"
                },
                    {
                    "type": "postback",
                    "title": "Start",
                    "payload": "start"
                }]}, 'type': 'card'}, True,pageId)

            facebook_chatbot.send_type_action(sender_id)
            response = facebook_chatbot.static_error_message(sender_id)
            return response

        else:
            buttonID = None
            contentID = None
            boxKey = None
            for key in (final_map):
                for idx, cnt in enumerate(final_map[key]['content']):
                    for btn in cnt['buttons']:
                        if postback_button['title'] == btn["button_text"]:
                            buttonID = btn["button_id"]

            for key in (final_map):
                for idx, cnt in enumerate(final_map[key]['content']):
                    if postback_button['title'] == cnt["content_text"]:
                        contentID = cnt["content_id"]
                        boxKey = key

            destination_id = None
            
            
            
            if buttonID != None:
                for arrow in my_arrows:
                    if arrow['start'] == buttonID:
                        destination_id = arrow['end']

                contentList = (final_map[destination_id]['content'])

                entered_cards.append(final_map[destination_id]['title'])
                current_user['cards'] = entered_cards
                current_user['id'] = sender_id
                if current_user['isNew']:
                    my_users.append(current_user)
                else:
                    my_users[user_index] = current_user
                chatbot_db.updateAdminUsers(my_users, userID)

                if (len(contentList) > 1):
                    replies = []
                    for cont in contentList:
                        replies.append({
                            "type": "postback",
                            "title": cont['content_text'],
                            "payload": "<POSTBACK_PAYLOAD>",
                        })

                    facebook_chatbot.send_type_action(sender_id)
                    response = facebook_chatbot.message_with_buttons(
                        sender_id, final_map[destination_id]['title'], replies)

                    handlemessage(
                        sender_id, {'text': postback_button['title'], 'type': 'text'}, False,pageId)
                    handlemessage(sender_id, {'text': {
                                  'title': final_map[destination_id]['title'], 'buttons': replies}, 'type': 'card'}, True,pageId)

                    return response

                else:
                    random_content = (random.choice(
                        final_map[destination_id]['content']))
                    random_content_index = final_map[destination_id]['content'].index(
                        random_content)
                    
                   

                    replies = []
                    for btn in final_map[destination_id]['content'][random_content_index]['buttons']:
                        replies.append({
                            "type": "postback",
                            "title": btn['button_text'],
                            "payload": "<POSTBACK_PAYLOAD>",
                        })

                    if (len(replies) != 0):
                        content_type = final_map[destination_id]['content'][random_content_index]['content_type']
                       
                        if content_type == "Image":
                            facebook_chatbot.send_type_action(sender_id)
                            response = facebook_chatbot.message_with_image_buttons(sender_id, final_map[destination_id]["title"], final_map[destination_id]['content'][random_content_index]['content_text'],
                                                                                   replies)
                            
                            handlemessage(
                                sender_id, {'text': postback_button['title'], 'type': 'text'}, False,pageId)
                            handlemessage(sender_id, {'text': {
                                          'title': final_map[destination_id]['content'][random_content_index]['content_text'], 'buttons': replies}, 'type': 'cardImg'}, True,pageId)

                        if content_type == "Text":
                            facebook_chatbot.send_type_action(sender_id)
                            response = facebook_chatbot.message_with_buttons(
                                sender_id, final_map[destination_id]['content'][random_content_index]['content_text'], replies)
                            
                            handlemessage(
                                sender_id, {'text': postback_button['title'], 'type': 'text'}, False,pageId)
                            handlemessage(sender_id, {'text': {
                                          'title': final_map[destination_id]['content'][random_content_index]['content_text'], 'buttons': replies}, 'type': 'card'}, True,pageId)

                        return response

                    else:
                        content_type = final_map[destination_id]['content'][random_content_index]['content_type']

                        if content_type == "Image":
                            facebook_chatbot.send_type_action(sender_id)
                            response = facebook_chatbot.message_with_image(
                                sender_id, final_map[destination_id]['content'][random_content_index]['content_text'])
                            
                            handlemessage(
                                sender_id, {'text': postback_button['title'], 'type': 'text'}, False,pageId)
                            handlemessage(sender_id, {
                                          'text': final_map[destination_id]['content'][random_content_index]['content_text'], 'type': 'img'}, True,pageId)
                            return response

                        if content_type == "Video":
                            facebook_chatbot.send_type_action(sender_id)

                            response = facebook_chatbot.message_with_video(
                                sender_id, final_map[destination_id]['content'][random_content_index]['content_text'])

                            handlemessage(
                                sender_id, {'text': postback_button['title'], 'type': 'text'}, False,pageId)
                            handlemessage(sender_id, {
                                          'text': final_map[destination_id]['content'][random_content_index]['content_text'], 'type': 'video'}, True,pageId)
                            return response

                        if content_type == "URL":
                            facebook_chatbot.send_type_action(sender_id)

                            facebook_chatbot.send_type_action(sender_id)
                            response = facebook_chatbot.message_with_url(
                                sender_id,
                                final_map[destination_id]['title'],
                                final_map[destination_id]['content'][random_content_index]['content_text']
                                )

                            handlemessage(
                                sender_id, {'text': postback_button['title'], 'type': 'text'}, False,pageId)
                            handlemessage(sender_id, {
                                          'text': final_map[destination_id]['content'][random_content_index]['content_text'], 'type': 'url'}, True,pageId)
                            return response

                        else:
                            nType = final_map[destination_id]['nodeType']
                            if nType == "AIChat":
                                current_user['isAIActivated'] = True
                                savedDestID = destination_id
                                savedIndx = random_content_index

                                if current_user['isNew']:
                                    my_users.append(current_user)
                                else:
                                    my_users[user_index] = current_user
                                chatbot_db.updateAdminUsers(my_users, userID)

                                facebook_chatbot.send_type_action(sender_id)
                                response = facebook_chatbot.text_message(
                                    sender_id, "عايز تعرف ايه؟")

                                handlemessage(
                                    sender_id, {'text': postback_button['title'], 'type': 'text'}, False,pageId)
                                handlemessage(
                                    sender_id, {'text': "عايز تعرف ايه؟", 'type': 'text'}, True,pageId)
                                return response

                            if nType == "FreeChat":
                                current_user['isFChatActivated'] = True
                                savedDestID = destination_id
                                savedIndx = random_content_index

                                if current_user['isNew']:
                                    my_users.append(current_user)
                                else:
                                    my_users[user_index] = current_user
                                chatbot_db.updateAdminUsers(my_users, userID)

                                facebook_chatbot.send_type_action(sender_id)
                                response = facebook_chatbot.text_message(
                                    sender_id, "عايز تعرف ايه؟")

                                handlemessage(
                                    sender_id, {'text': postback_button['title'], 'type': 'text'}, False,pageId)
                                handlemessage(
                                    sender_id, {'text': "عايز تعرف ايه؟", 'type': 'text'}, True,pageId)
                                return response

                            if nType == "CollectMails":
                                current_user['isCollectMailActivated'] = True
                                savedDestID = destination_id
                                savedIndx = random_content_index

                                if current_user['isNew']:
                                    my_users.append(current_user)
                                else:
                                    my_users[user_index] = current_user
                                chatbot_db.updateAdminUsers(my_users, userID)

                                facebook_chatbot.send_type_action(sender_id)
                                response = facebook_chatbot.text_message(
                                    sender_id, final_map[destination_id]['content'][random_content_index]['content_text'])

                                handlemessage(
                                    sender_id, {'text': postback_button['title'], 'type': 'text'}, False, pageId)
                                handlemessage(
                                    sender_id, {'text': final_map[destination_id]['content'][random_content_index]['content_text'], 'type': 'text'}, True, pageId)
                                return response


                            facebook_chatbot.send_type_action(sender_id)
                            response = facebook_chatbot.text_message(
                                sender_id, final_map[destination_id]['content'][random_content_index]['content_text'])

                            handlemessage(
                                sender_id, {'text': postback_button['title'], 'type': 'text'}, False,pageId)
                            handlemessage(sender_id, {
                                          'text': final_map[destination_id]['content'][random_content_index]['content_text'], 'type': 'text'}, True,pageId)
                            return response

            if contentID != None:
                entered_cards.append(final_map[boxKey]['title'])
                current_user['cards'] = entered_cards
                current_user['id'] = sender_id
                if current_user['isNew']:
                    my_users.append(current_user)
                else:
                    my_users[user_index] = current_user
                chatbot_db.updateAdminUsers(my_users, userID)
                dest_content = final_map[boxKey]['content'][0]
                if (len(dest_content['buttons']) > 0):
                    replies = []
                    for btn in dest_content['buttons']:
                        replies.append({
                            "type": "postback",
                            "title": btn['button_text'],
                            "payload": "<POSTBACK_PAYLOAD>",
                        })
                    facebook_chatbot.send_type_action(sender_id)
                    response = facebook_chatbot.message_with_buttons(
                        sender_id, dest_content['content_text'], replies)

                    handlemessage(
                        sender_id, {'text': postback_button['title'], 'type': 'text'}, False,pageId)
                    handlemessage(sender_id, {'text': {
                                  "title": dest_content['content_text'], 'buttons': replies}, 'type': 'card'}, True,pageId)
                    return response

                else:
                    facebook_chatbot.send_type_action(sender_id)
                    response = facebook_chatbot.text_message(
                        sender_id, dest_content['content_text'])
                        
                    handlemessage(
                        sender_id, {'text': postback_button['title'], 'type': 'text'}, False,pageId)
                    handlemessage(
                        sender_id, {'text': dest_content['content_text'], 'type': 'text'}, True,pageId)
                    return response

            else:
                handlemessage(
                    sender_id, {'text': message['text'], 'type': 'text'}, False,pageId)
                handlemessage(sender_id, {'text': {'title': 'welcome', 'buttons': [{
                    "type": "web_url",
                    "url": "https://electro-pi.com/",
                    "title": "View Website"
                }, {
                    "type": "web_url",
                    "url": "https://www.facebook.com/ElectroPi.A.I/",
                    "title": "View FB Page"
                },
                    {
                    "type": "postback",
                    "title": "Start",
                    "payload": "start"
                }]}, 'type': 'text'}, True,pageId)

            facebook_chatbot.send_type_action(sender_id)
            response = facebook_chatbot.static_error_message(
                senderId=sender_id)
            return response

    except:
        return "NOT WORKING!"



def get_current_flow(recip_id):
    my_admins = chatbot_db.getAllAdmins()
    for admin in my_admins:
        if admin['myPageId'] == recip_id:
            return admin['myFlow'], admin['myArrows'], admin['myUsers'], admin['userID'], admin['pageAccessToken']
