from flask import Flask
import requests
app = Flask(__name__)


class InstagramAPI():
    def __init__(self, api) -> None:
        self.API = api

    def text_message(self, senderId, message):
        request_body = {
            "recipient": {
                "id": senderId
            },
            "messaging_type": "RESPONSE",
            "message": {
                "text": message,
            }
        }
        resp = requests.post(self.API, json=request_body).json()
        return resp

    def message_with_buttons(self, senderId, message, buttons):
        request_body = {
            "recipient": {
                "id": senderId
            },
            "messaging_type": "RESPONSE",
            "message": {
                "text": message,
                "quick_replies": buttons
            }
        }
        print(buttons)

        resp = requests.post(self.API, json=request_body).json()
        return resp

    def message_with_quick_replies(self, senderId, message, replies):
        request_body = {
            "recipient": {
                "id": senderId
            },
            "messaging_type": "RESPONSE",
            "message": {
                "text": message,
                "quick_replies": replies
            }
        }

        resp = requests.post(self.API, json=request_body).json()
        return resp

    def message_with_image_buttons(self, senderId, message, image, buttons):
        request_body = {
            "recipient": {
                "id": senderId
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": message,
                                "image_url": image,
                                "buttons": buttons
                            },
                        ]
                    }
                }
            }
        }

        resp = requests.post(self.API, json=request_body).json()
        return resp

    def message_with_image(self, senderId, imageURL):
        request_body = {
            "recipient": {
                "id": senderId
            },
            "messaging_type": "RESPONSE",
            "message": {
                "attachment": {
                    "type": "image",
                    "payload": {
                        "url": imageURL,
                        "is_reusable": True
                    }
                }
            }
        }
        resp = requests.post(self.API, json=request_body).json()
        return resp

    def message_with_video(self, senderId, videoURL):
        request_body = {
            "recipient": {
                "id": senderId
            },
            "messaging_type": "RESPONSE",
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "media",
                        "elements": [
                            {
                                "media_type": "video",
                                "url": videoURL
                            }
                        ]
                    }
                }
            }
        }
        resp = requests.post(self.API, json=request_body).json()
        return resp

    def static_error_message(self, senderId):
        request_body = {
            "recipient": {
                "id": senderId
            },
            "message": {
                "attachment": {
                    "type": "template",
                            "payload": {
                                "template_type": "generic",
                                "elements": [
                                    {
                                        "title": "Welcome!",
                                        "image_url": "https://scontent.fcai19-7.fna.fbcdn.net/v/t1.6435-9/117038179_2805661699657873_5401116646475347922_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=t2vsx5Nm8boAX8TVuOm&_nc_ht=scontent.fcai19-7.fna&oh=00_AT-gxsN8Mywqyf8Ck6PL9TW7H8qBqKVdRf7TcSNvIPMlGQ&oe=635089ED",
                                        "subtitle": "We have the right hat for everyone.",
                                        "default_action": {
                                            "type": "web_url",
                                            "url": "https://electro-pi.com/",
                                            "webview_height_ratio": "tall",
                                        },
                                        "buttons": [
                                            {
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
                                            }
                                        ]
                                    },
                                ]
                            }
                }
            }
        }
        resp = requests.post(self.API, json=request_body).json()
        return resp

    def send_type_action(self, sender_id):
        request_body = {
            "recipient": {
                "id": sender_id
            },
            "sender_action": "typing_on"
        }

        response = requests.post(self.API, json=request_body).json()
        return response
