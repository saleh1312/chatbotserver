from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://admin:KLTy7uctc62N89pL@cluster0.oj9e8wg.mongodb.net/chatbot?retryWrites=true&w=majority')


# mongodb+srv://admin:<password>@cluster0.oj9e8wg.mongodb.net/?retryWrites=true&w=majority


class ChatbotDatabase():
    def __init__(self) -> None:
        self.db = client.chatbot
        self.flows_doc = self.db.flows
        self.arrows_doc = self.db.arrows
        self.users_doc = self.db.users
        self.admins_doc = self.db.admins

    def getAllFlows(self):
        arr = []
        for document in self.flows_doc.find({}):
            document["_id"] = str(document["_id"])
            arr.append(document)

        return arr

    def getAllArrows(self):
        arr = []
        for document in self.arrows_doc.find({}):
            document["_id"] = str(document["_id"])
            arr.append(document)

        return arr

    def getAllUsers(self):
        arr = []
        for document in self.users_doc.find({}):
            document["_id"] = str(document["_id"])
            arr.append(document)

        return arr

    def getAllAdmins(self):
        arr = []
        for document in self.admins_doc.find({}):
            document["_id"] = str(document["_id"])
            arr.append(document)

        return arr

    def createFlow(self, arr):
        if (len(list(self.flows_doc.find())) > 0):
            self.flows_doc.delete_many({})  # will be changed
        self.flows_doc.insert_many(arr)
        print('FLOWS ADDED SUCCESSFULLY')

    def addUser(self, user):
        # if (len(list(self.users_doc.find())) > 0):
        #     self.users_doc.delete_many({}) ## will be changed
        self.users_doc.insert_one(user)
        print('USER ADDED SUCCESSFULLY')
        
    def nothing(self,dats):
        print(dats)
    
    def addAdmin(self, admin):
        # if (len(list(self.users_doc.find())) > 0):
        #     self.users_doc.delete_many({}) ## will be changed
        self.admins_doc.insert_one(admin)
        print('ADMIN ADDED SUCCESSFULLY')

    def updateAdmin(self, admin):
        self.admins_doc.update_one(
            {"userID": admin['userID']},
            {'$set':{
                'pageAccessToken': admin['pageAccessToken'],
                'pageInfo':admin['pageInfo'],
                'myPageId': admin['myPageId'],
                'botName': admin['botName'],
                'myInstagramId': admin['myInstagramId'],
                'instagramInfo': admin['instagramInfo'],
                'phoneNumber': admin['phoneNumber'],
                'emailInfo': admin['emailInfo'],
                'myWebsiteId': admin['myWebsiteId'],
                'websiteInfo': admin['websiteInfo'],
                }
            })
        print('UPDATED SUCCESSFULLY')   

    def updateAdminFlow(self, admin):
        self.admins_doc.update_one({"userID": admin['userID']}, {'$set': {'myFlow': admin['myFlow'], 'myArrows':admin['myArrows']}})
        print('UPDATED SUCCESSFULLY')
    

    def updateAdminUsers(self, users, id):
        self.admins_doc.update_one({"userID": id}, {'$set': {'myUsers': users}})
        print('UPDATED SUCCESSFULLY')

        
    def updateUsers(self, users):
        if (len(list(self.users_doc.find())) > 0):
            self.users_doc.delete_many({})  # will be changed
        self.users_doc.insert_many(users)
        print('USER UPDATED SUCCESSFULLY')

    def addArrows(self, arrows):
        if (len(list(self.arrows_doc.find())) > 0):
            self.arrows_doc.delete_many({})  # will be changed
        self.arrows_doc.insert_many(arrows)
        print('ARROWS ADDED SUCCESSFULLY')

    def flows_preparation(self, flows):
        final_map = {}
        for card in flows:
            final_map[card['id']] = {}
            keys_ = (list(card.keys()))
            content_list = []
            node_type = ""
            button_list = [[], [], [], [], [], ]
            for key_ in keys_:
                if (key_.find("nodeType") != -1):
                    node_type = card[key_]
                if (key_.find('textarea') != -1):
                    content_list.append({
                        'content_id': key_,
                        'content_text': card[key_]['text'],
                        'content_type': card[key_]['text_type'],
                    })
                if (key_.find('button') != -1):
                    idx = int(key_[-2])
                    button_list[idx].append({
                        'button_id': key_,
                        'button_text': card[key_]['text'],
                        'content_type': card[key_]['text_type'],
                    })

            final_map[card['id']] = {
                'title': card['title']['text'],
                'content': content_list,
                'button': button_list,
                'nodeType': node_type,
            }
            content_list = []
            button_list = []

        for key in (final_map):
            for idx, _ in enumerate(final_map[key]['content']):
                final_map[key]['content'][idx]['buttons'] = final_map[key]['button'][idx]
            for d in (final_map[key]):
                if (d == 'button'):
                    map(final_map[key].pop, ['button'])

        return final_map
