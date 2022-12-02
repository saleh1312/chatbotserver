from website.websiteApi import WebsiteAPI
from facebook.facebookApi import FacebookAPI
from instagram.instagramApi import InstagramAPI

class User:
    def __init__(self, pageId, pageAccessToken):
        API = f"https://graph.facebook.com/v15.0/{pageId}/messages?access_token="+pageAccessToken
        self.pageId = pageId
        self.facebook_chatbot = FacebookAPI(API)
        self.instagram_chatbot = InstagramAPI(API)
        self.web_chatbot = WebsiteAPI()
    
