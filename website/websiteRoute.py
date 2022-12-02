
from flask import Blueprint, request, jsonify
from utils.utils import handlemessage, get_current_user, chatbot_db
from website.websiteApi import WebsiteAPI

webRoute = Blueprint("webRoute", __name__, template_folder="templates")


# initialize chatbot database

# This is API key for facebook messenger.
web_chatbot = WebsiteAPI()
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



@webRoute.route("/website", methods=['POST'])
def websiteWebhook():
    global web_chatbot
    global final_map
    global savedIndx
    global savedDestID
    global chatbot_db
    data = request.get_json()
    print(data['message'])
    print('*****************')
    my_flows, my_arrows, my_users, userID = get_current_flow("123abc123")
    final_map = chatbot_db.flows_preparation(my_flows)

    try:
        # Read messages from facebook messanger.
        message = data['message']
        sender_id = "user123456"

        # current_user, entered_cards, user_index = get_current_user(sender_id)

        if message != None:
            if message.lower() in welcome_messages:
                # entered_cards.append(my_flows[0]['title']['text'])
                # current_user['cards'] = entered_cards
                # current_user['id'] = sender_id
                # if current_user['isNew']:
                #     my_users.append(current_user)
                # else:
                #     my_users[user_index] = current_user
                # chatbot_db.updateUsers(my_users)
                replies = []
                for btn in final_map['box_1']['content'][0]['buttons']:
                    replies.append({
                        "content_type": "text",
                        "title": btn['button_text'],
                        "payload": "<POSTBACK_PAYLOAD>",
                    })
                
                if (len(replies) != 0):
                    response = web_chatbot.message_with_buttons(
                        sender_id, final_map['box_1']['content'][0]['content_text'], replies)
                    
                    # response.headers.add('Access-Control-Allow-Origin', '*')
                    # handlemessage(
                    #     sender_id, {'text': message['text'], 'type': 'button'}, False)
                    # handlemessage(sender_id, {'text': {
                    #               'title': final_map['box_1']['content'][0]['content_text'], 'buttons': replies}, 'type': 'card'}, True)

                else:
                    response = web_chatbot.message_with_buttons(
                        sender_id, final_map['box_1']['content'][0]['content_text'], [])
                    # handlemessage(
                    #     sender_id, {'text': message['text'], 'type': 'button'}, False)
                    # handlemessage(sender_id, {
                    #               'text': final_map['box_1']['content'][0]['content_text'], 'type': 'text'}, True)
                message_ = {"answer": response, "type": "text_buttons"}
                return jsonify(message_)
        
        if message != None:
            if message == "انهاء":
                # current_user['isAIActivated'] = False
                # current_user['isFChatActivated'] = False

                # if current_user['isNew']:
                #     my_users.append(current_user)
                # else:
                #     my_users[user_index] = current_user
                # chatbot_db.updateUsers(my_users)

                replies = []
                for btn in final_map['box_1']['content'][0]['buttons']:
                    replies.append({
                        "type": "postback",
                        "title": btn['button_text'],
                        "payload": "DEVELOPER_DEFINED_PAYLOAD",
                    })

                # instagram_chatbot.send_type_action(sender_id)
                response = web_chatbot.message_with_buttons(
                    sender_id, final_map['box_1']['content'][0]['content_text'], replies)

                # handlemessage(
                #     sender_id, {'text': message['text'], 'type': 'text'}, False)
                # handlemessage(sender_id, {
                #     'text': final_map['box_1']['content'][0]['content_text'], 'type': 'text'}, True)

                return response

        #     if current_user['isAIActivated']:
        #         all_context = []
        #         for content in final_map[savedDestID]['content']:
        #             all_context.append(content['content_text'])
        #         all_context = ', '.join(all_context)
        #         model_resp = requests.post(f"{config.MODEL_URI}/qa", json={
        #             "quest": message['text'],
        #             "context": final_map[savedDestID]['content'][savedIndx]['content_text']
        #         }).json()

        #         instagram_chatbot.send_type_action(sender_id)
        #         response = instagram_chatbot.message_with_quick_replies(sender_id, model_resp['Res'], [
        #             {
        #                 "content_type": "text",
        #                 "title": "انهاء",
        #                 "payload": "endAIChat",
        #             },
        #         ])
        #         entered_cards.append(final_map[savedDestID]['title'])
        #         current_user['cards'] = entered_cards
        #         current_user['id'] = sender_id
        #         if current_user['isNew']:
        #             my_users.append(current_user)
        #         else:
        #             my_users[user_index] = current_user
        #         chatbot_db.updateUsers(my_users)

        #         return response

        #     if current_user['isFChatActivated']:
        #         response = requests.post(f"{config.MODEL_URI}/freechat", json={
        #             "quest": message['text']
        #         }).json()

        #         instagram_chatbot.send_type_action(sender_id)
        #         response = instagram_chatbot.message_with_quick_replies(sender_id, response['Res'], [
        #             {
        #                 "content_type": "text",
        #                 "title": "انهاء",
        #                 "payload": "endAIChat",
        #             },
        #         ])
        #         entered_cards.append(final_map[savedDestID]['title'])
        #         current_user['cards'] = entered_cards
        #         current_user['id'] = sender_id
        #         if current_user['isNew']:
        #             my_users.append(current_user)
        #         else:
        #             my_users[user_index] = current_user
        #         return response

        
        if message != None:
            buttonID = None
            contentID = None
            boxKey = None
            for key in (final_map):
                for idx, cnt in enumerate(final_map[key]['content']):
                    for btn in cnt['buttons']:
                        if message == btn["button_text"]:
                            buttonID = btn["button_id"]

            for key in (final_map):
                for idx, cnt in enumerate(final_map[key]['content']):
                    if message == cnt["content_text"]:
                        contentID = cnt["content_id"]
                        boxKey = key

            destination_id = None
            
           
            if buttonID != None:
                for arrow in my_arrows:
                    if arrow['start'] == buttonID:
                        destination_id = arrow['end']

                contentList = (final_map[destination_id]['content'])

                # entered_cards.append(final_map[destination_id]['title'])
                # current_user['cards'] = entered_cards
                # current_user['id'] = sender_id
                # if current_user['isNew']:
                #     my_users.append(current_user)
                # else:
                #     my_users[user_index] = current_user
                # chatbot_db.updateUsers(my_users)

                if (len(contentList) > 1):
                    replies = []
                    for cont in contentList:
                        replies.append({
                            "content_type": "text",
                            "title": cont['content_text'],
                            "payload": "<POSTBACK_PAYLOAD>",
                        })

                    # instagram_chatbot.send_type_action(sender_id)
                    response = web_chatbot.message_with_buttons(
                        sender_id, final_map[destination_id]['title'], replies)

                    # handlemessage(
                    #     sender_id, {'text': message['text'], 'type': 'text'}, False)
                    # handlemessage(sender_id, {'text': {
                    #               'title': final_map[destination_id]['title'], 'buttons': replies}, 'type': 'card'}, True)

                    print(response)
                    message_ = {"answer": response, "type": "text_buttons"}
                    return jsonify(message_)

                else:
                    random_content = final_map[destination_id]['content'][0]
                    random_content_index = final_map[destination_id]['content'].index(
                        random_content)

                    
                    replies = []
                    for btn in final_map[destination_id]['content'][random_content_index]['buttons']:
                        replies.append({
                            "content_type": "text",
                            "title": btn['button_text'],
                            "payload": "<POSTBACK_PAYLOAD>",
                        })

                    if (len(replies) != 0):
                        content_type = final_map[destination_id]['content'][random_content_index]['content_type']
                        if content_type == "Image":
                            # instagram_chatbot.send_type_action(sender_id)
                            response = web_chatbot.message_with_image_buttons(sender_id, final_map[destination_id]["title"], final_map[destination_id]['content'][random_content_index]['content_text'],
                                                                                    replies)
                            # handlemessage(
                            #     sender_id, {'text': message['text'], 'type': 'text'}, False)
                            # handlemessage(sender_id, {'text': {
                            #               'title': final_map[destination_id]['content'][random_content_index]['content_text'], 'buttons': replies}, 'type': 'cardImg'}, True)

                        if content_type == "Text":
                            # handlemessage(
                            #     sender_id, {'text': message['text'], 'type': 'text'}, False)
                            # handlemessage(sender_id, {'text': {
                            #               'title': final_map[destination_id]['content'][random_content_index]['content_text'], 'buttons': replies}, 'type': 'card'}, True)

                            # instagram_chatbot.send_type_action(sender_id)
                            response = web_chatbot.message_with_buttons(
                                sender_id, final_map[destination_id]['content'][random_content_index]['content_text'], replies)

                        print(response)
                        message_ = {"answer": response, "type": "text_buttons"}
                        return jsonify(message_)

                    else:
                        content_type = final_map[destination_id]['content'][random_content_index]['content_type']

                        if content_type == "Image":
                            # handlemessage(
                            #     sender_id, {'text': message['text'], 'type': 'text'}, False)
                            # handlemessage(sender_id, {
                            #               'text': final_map[destination_id]['content'][random_content_index]['content_text'], 'type': 'img'}, True)
                            # instagram_chatbot.send_type_action(sender_id)
                            response = web_chatbot.message_with_image(
                                sender_id, final_map[destination_id]['content'][random_content_index]['content_text'])
                            print(response)
                            message_ = {"answer": response, "type": "image"}
                            return jsonify(message_)

                        if content_type == "Video":
                            # handlemessage(
                            #     sender_id, {'text': message['text'], 'type': 'text'}, False)
                            # handlemessage(sender_id, {
                            #               'text': final_map[destination_id]['content'][random_content_index]['content_text'], 'type': 'video'}, True)
                            # instagram_chatbot.send_type_action(sender_id)

                            response = web_chatbot.message_with_video(
                                sender_id, final_map[destination_id]['content'][random_content_index]['content_text'])
                            print(response)
                            message_ = {"answer": response, "type": "video"}
                            return jsonify(message_)

                        if content_type == "URL":
                            # web_chatbot.send_type_action(sender_id)
                            # handlemessage(
                            #     sender_id, {'text': message['text'], 'type': 'text'}, False)
                            # handlemessage(sender_id, {
                            #               'text': final_map[destination_id]['content'][random_content_index]['content_text'], 'type': 'url'}, True)

                            # web_chatbot.send_type_action(sender_id)
                            response = web_chatbot.text_message(
                                sender_id, final_map[destination_id]['content'][random_content_index]['content_text'])
                            print(response)
                            message_ = {"answer": response, "type": "url"}
                            return jsonify(message_)

                        else:
                            nType = final_map[destination_id]['nodeType']
                            # handlemessage(sender_id, {'text':postback_button['title'], 'type':'text'})
                            if nType == "AIChat":
                                # current_user['isAIActivated'] = True
                                # savedDestID = destination_id
                                # savedIndx = random_content_index

                                # if current_user['isNew']:
                                #     my_users.append(current_user)
                                # else:
                                #     my_users[user_index] = current_user
                                # chatbot_db.updateUsers(my_users)

                                # handlemessage(
                                #     sender_id, {'text': message['text'], 'type': 'text'}, False)
                                # handlemessage(
                                #     sender_id, {'text': "عايز تعرف ايه؟", 'type': 'text'}, True)
                                # web_chatbot.send_type_action(sender_id)
                                response = web_chatbot.text_message(
                                    sender_id, "عايز تعرف ايه؟")
                                print(response)
                                message_ = {"answer": response,"type": "text"}
                                return jsonify(message_)

                            if nType == "FreeChat":
                                # current_user['isFChatActivated'] = True
                                # savedDestID = destination_id
                                # savedIndx = random_content_index

                                # if current_user['isNew']:
                                #     my_users.append(current_user)
                                # else:
                                #     my_users[user_index] = current_user
                                # chatbot_db.updateUsers(my_users)

                                # handlemessage(
                                #     sender_id, {'text': message['text'], 'type': 'text'}, False)
                                # handlemessage(
                                #     sender_id, {'text': "عايز تعرف ايه؟", 'type': 'text'}, True)
                                # instagram_chatbot.send_type_action(sender_id)
                                response = web_chatbot.text_message(
                                    sender_id, "عايز تعرف ايه؟")
                                print(response)
                                message_ = {"answer": response, "type": "text"}
                                return jsonify(message_)

                            # handlemessage(
                            #     sender_id, {'text': message['text'], 'type': 'text'}, False)
                            # handlemessage(sender_id, {
                            #               'text': final_map[destination_id]['content'][random_content_index]['content_text'], 'type': 'text'}, True)

                            # instagram_chatbot.send_type_action(sender_id)
                            response = web_chatbot.text_message(
                                sender_id, final_map[destination_id]['content'][random_content_index]['content_text'])
                            print(response)
                            message_ = {"answer": response, "type": "text"}
                            return jsonify(message_)

        #     if contentID != None:
        #         handlemessage(
        #             sender_id, {'text': message['text'], 'type': 'text'})
        #         entered_cards.append(final_map[boxKey]['title'])
        #         current_user['cards'] = entered_cards
        #         current_user['id'] = sender_id
        #         if current_user['isNew']:
        #             my_users.append(current_user)
        #         else:
        #             my_users[user_index] = current_user
        #         chatbot_db.updateUsers(my_users)
        #         dest_content = final_map[boxKey]['content'][0]
        #         if (len(dest_content['buttons']) > 0):
        #             replies = []
        #             for btn in dest_content['buttons']:
        #                 replies.append({
        #                     "type": "postback",
        #                     "title": btn['button_text'],
        #                     "payload": "<POSTBACK_PAYLOAD>",
        #                 })

        #             handlemessage(
        #                 sender_id, {'text': message['text'], 'type': 'text'}, False)
        #             handlemessage(sender_id, {'text': {
        #                           "title": dest_content['content_text'], 'buttons': replies}, 'type': 'card'}, True)
        #             instagram_chatbot.send_type_action(sender_id)
        #             response = instagram_chatbot.message_with_buttons(
        #                 sender_id, dest_content['content_text'], replies)
        #             return response

        #         else:
        #             handlemessage(
        #                 sender_id, {'text': message['text'], 'type': 'text'}, False)
        #             handlemessage(
        #                 sender_id, {'text': dest_content['content_text'], 'type': 'text'}, True)
        #             instagram_chatbot.send_type_action(sender_id)
        #             response = instagram_chatbot.text_message(
        #                 sender_id, dest_content['content_text'])
        #             return response

        #     else:
        #         handlemessage(
        #             sender_id, {'text': message['text'], 'type': 'text'}, False)
        #         # handlemessage(sender_id, {'text': message['text'], 'type':'button'}, False)
        #         handlemessage(sender_id, {'text': {'title': 'welcome', 'buttons': [{
        #             "type": "web_url",
        #             "url": "https://electro-pi.com/",
        #             "title": "View Website"
        #         }, {
        #             "type": "web_url",
        #             "url": "https://www.facebook.com/ElectroPi.A.I/",
        #             "title": "View FB Page"
        #         },
        #             {
        #             "type": "postback",
        #             "title": "Start",
        #             "payload": "start"
        #         }]}, 'type': 'text'}, True)

        #     instagram_chatbot.send_type_action(sender_id)
        #     response = instagram_chatbot.static_error_message(
        #         senderId=sender_id)
        #     return response

        # else:
        #     handlemessage(
        #         sender_id, {'text': message['text'], 'type': 'text'}, False)
        #     # handlemessage(sender_id, {'text': postback_button['title'], 'type':'button'}, False)
        #     handlemessage(sender_id, {'text': {'title': 'welcome', 'buttons': [{
        #         "type": "web_url",
        #         "url": "https://electro-pi.com/",
        #         "title": "View Website"
        #     }, {
        #         "type": "web_url",
        #         "url": "https://www.facebook.com/ElectroPi.A.I/",
        #         "title": "View FB Page"
        #     },
        #         {
        #         "type": "postback",
        #         "title": "Start",
        #         "payload": "start"
        #     }]}, 'type': 'card'}, True)
        #     instagram_chatbot.send_type_action(sender_id)
        #     response = instagram_chatbot.static_error_message(sender_id)
        #     return response

    except:
        return "NOT WORKING!"

def get_current_flow(recip_id):
    my_admins = chatbot_db.getAllAdmins()
    for admin in my_admins:
        if admin['myWebsiteId'] == recip_id:
            return admin['myFlow'], admin['myArrows'], admin['myUsers'], admin['userID']