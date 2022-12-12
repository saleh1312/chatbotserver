# from flask import Flask, request, jsonify, render_template
# from flask_pymongo import PyMongo
# from pymongo import MongoClient


# app = Flask(__name__) 
# client = MongoClient('localhost', 27017)
# db = client.chatbot
# flows_doc = db.flows
# arrows_doc = db.arrows
# users_doc = db.users
# print('------------------------')

# my_flows = [
#     {
#         'id': 'box_1',
#         'nodeType': 'Button+Text',
#         'title': {'text': 'Welcome', 'text_type': 'title'},
#         'box_1_textarea0': {'text': 'ازيك عامل ايه الاخبار عايزنى اساعدك؟', 'text_type': 'Text'},
#         'box_1_button00': {'text': 'اه ياريت', 'text_type': 'box_1_button00'},
#         'box_1_button01': {'text': 'لا شكرا', 'text_type': 'box_1_button01'},
#         'box_1_button02': {'text': 'free chat', 'text_type': 'box_1_button02'}
#     },
#     {
#         'id': 'box_2',
#         'nodeType': 'Button+Text',
#         'title': {'text': 'Help', 'text_type': 'title'},
#         'box_2_textarea0': {'text': 'مهتم تعرف ايه؟', 'text_type': 'Text'},
#         'box_2_button00': {'text': 'Projects', 'text_type': 'box_2_button00'},
#         'box_2_button01': {'text': 'Consultation', 'text_type': 'box_2_button01'},
#         'box_2_button02': {'text': 'Courses', 'text_type': 'box_2_button02'}
#     },
#     {
#         'id': 'box_7',
#         'nodeType': 'AIChat',
#         'title': {'text': 'AIChat', 'text_type': 'title'},
#         'box_7_textarea0': {'text': 'كورس الETE مهم لاى حد عايز يببدا فى مجال الذكاء الاصطناعى وسعر الكورس 7000', 'text_type': 'Text'}
#     },
#     {
#         'id': 'box_5', 
#         'nodeType': 'Button+Text', 
#         'title': {'text': 'Courses', 'text_type': 'title'}, 
#         'box_5_textarea0': {'text': 'عايز تعرف عن ايه فيهم؟', 'text_type': 'Text'}, 
#         'box_5_button00': {'text': 'CV', 'text_type': 'box_5_button00'},
#         'box_5_button01': {'text': 'ETE', 'text_type': 'box_5_button01'}
#     },
#     {
#         'id': 'box_6',
#         'nodeType': 'AIChat', 
#         'title': {'text': 'CV', 'text_type': 'title'}, 
#         'box_6_textarea0': {'text': 'كورس الcv هيساعدك بشكل كبير تبقى بروفيشنال ، سعر الكورس 5000', 'text_type': 'Text'}
#     },
#     {
#         'id': 'box_8', 
#         'nodeType': 'FreeChat', 
#         'title': {'text': 'FreeChat', 'text_type': 'title'}, 
#         'box_8_textarea0': {'text': 'اى حاجة تيجى من ريحة الحبايب', 'text_type': 'Text'}
#     },
#     {
#         'id': 'box_3',
#         'nodeType': 'Button+Text',
#         'title': {'text': 'Projects', 'text_type': 'title'},
#         'box_3_textarea0': {'text': 'احنا عندنا بروجكتس كتيرة منها شات بوت', 'text_type': 'Text'}
#     },
#     {
#         'id': 'box_4', 
#         'nodeType': 'Button+Text', 
#         'title': {'text': 'Consultation', 'text_type': 'title'}, 
#         'box_4_textarea0': {'text': 'احنا نقدؤ نساعدك سواء كنت بتحضر ماجستير او دكتوراه', 'text_type': 'Text'}
#     },
#     {
#         'id': 'box_9', 
#         'nodeType': 'Button+Text', 
#         'title': {'text': 'Button+Text', 'text_type': 'title'}, 
#         'box_9_textarea0': {'text': 'https://www.facebook.com/plugins/video.php?height=322&href=https%3A%2F%2Fwww.facebook.com%2Fafshat.aflam%2Fvideos%2F3141402806096776%2F&show_text=false&width=560&t=0',
#         'text_type': 'Video'}
#     }
#     ]

# my_arrows = [
#     {
#         'start': 'box_1_button00', 
#         'end': 'box_2'
#     },
#     {
#         'start': 'box_2_button00',
#         'end': 'box_3'
#     },
#     {
#         'start': 'box_2_button01',
#         'end': 'box_4'
#     },
#     {
#         'start': 'box_2_button02',
#         'end': 'box_5'
#     },
#     {
#         'start': 'box_5_button00',
#         'end': 'box_6'
#     },
#     {
#         'start': 'box_5_button01',
#         'end': 'box_7'
#     },
#     {
#         'start': 'box_1_button02',
#         'end': 'box_8'
#     },
#     {
#         'start': 'box_1_button01',
#         'end': 'box_9'
#     }
#     ]

# my_users = {
    
# }

# flows_doc.insert_many(my_flows)
# arrows_doc.insert_many(my_arrows)
# users_doc.insert_one(my_users)


# print('Data inserted successfuly')