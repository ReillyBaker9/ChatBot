import requests
import sys

from config import TELEGRAM_INIT_WEBHOOK_URL
from config import TELEGRAM_SEND_MESSAGE_URL
from config import TELEGRAM_SEND_POLL_URL
from config import TELEGRAM_ANSWER_CALLBACK_URL



class TelegramBot:

    def __init__(self):
        """"
        Initializes an instance of the TelegramBot class.
        Attributes:
            chat_id:str: Chat ID of Telegram chat, used to identify which conversation outgoing messages should be send to.
            text:str: Text of Telegram chat
            first_name:str: First name of the user who sent the message
            last_name:str: Last name of the user who sent the message
        """
        #Attribute for answering the chat
        
        self.chat_id = None
        self.text = None
        self.first_name = None
        self.last_name = None
        self.data = None

        #Attribute for posting to the chat
        
        self.chat_ext_id = None
        self.text_ext = None
        self.data_ext = None
        
        #Attribute for callback functions 
        
        self.callback_id = None
        self.callback_from = None
        self.callback_message_id = None
        self.callback_chatinstance = None
        self.callback_data = None
        
        #Attributes for inline keyboard with 2 options 
        self.chat_id = None
        self.text_inlinekb = None
        self.inline_keyboard = None
        self.ikb_opt_1_callback_data = None
        self.ikb_opt_1_text = None
        self.ikb_opt_2_callback_data = None
        self.ikb_opt_2_text = None

     
    def parse_webhook_data_message(self, data):
        """
        Parses Telegram JSON request from webhook and sets fields for conditional actions
        Args:
            data:str: JSON string of data
        """
        #Example of data -> What Telegram sends to the Ngrok server when I write something in the bot 
        #{'update_id': 960162050, 'message': {'message_id': 27, 'from': {'id': 924179441, 'is_bot': False, 'first_name': 'Bruno', 'last_name': 'Sivanandan', 'language_code': 'en'}, 'chat': {'id': 924179441, 'first_name': 'Bruno', 'last_name': 'Sivanandan', 'type': 'private'}, 'date': 1587271715, 'text': 'Test'}}
        
        message = data['message']
        
        self.data = data 
        self.chat_id = message['chat']['id']
        self.incoming_message_text = message['text'].lower()
        self.first_name = message['from']['first_name']
        self.last_name = message['from']['last_name']

    def post_message(self):

        success = None
        
        # should be handled in parse_webhook_data_message
        #self.chat_id = 924179441
        self.outgoing_message_text = self.data
        #self.outgoing_message_text = "Something else"
        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self.chat_id, self.outgoing_message_text))

        return True if res.status_code == 200 else False

    def parse_webhook_data_inlineKeyboard(self,data):
        url = "https://api.telegram.org/bot1184647758:AAHqSNCXENyuEDRbcdWrs874waAr0Cy9hPg/sendMessage"

        print('ENTERING parse_webhook_data_inlineKeyboard', file=sys.stderr)

        self.chat_id = data["chat_id"]
        self.text_inlinekb = data["text"]
        self.inline_keyboard = data["reply_markup"]["inline_keyboard"]
        self.ikb_opt_1_callback_data = self.inline_keyboard[0][0]["callback_data"]
        self.ikb_opt_1_text = self.inline_keyboard[0][0]["text"]
        self.ikb_opt_2_callback_data = self.inline_keyboard[0][1]["callback_data"]
        self.ikb_opt_2_text = self.inline_keyboard[0][1]["text"]

        #Need to put this in another function post

    #After parsing, posts formats the data for an HTTP request to the TG server 
    def post_inlineKB(self):
        #TO DO -> Render this URL dynamic in the CONFIG files 
        url = "https://api.telegram.org/bot1184647758:AAHqSNCXENyuEDRbcdWrs874waAr0Cy9hPg/sendMessage"

        payload = "{\r\n        \"chat_id\": \"" + self.chat_id + "\",\r\n        \"text\": \"" + self.text_inlinekb + "\",\r\n        \"reply_markup\": {\r\n            \"inline_keyboard\": [[\r\n                {\r\n                    \"text\": \""+ self.ikb_opt_1_text + "\",\r\n                    \"callback_data\": \"" + self.ikb_opt_1_callback_data  + "\"            \r\n                }, \r\n                {\r\n                    \"text\": \""+self.ikb_opt_2_text+"\",\r\n                    \"callback_data\": \"" +self.ikb_opt_2_callback_data+ "\"            \r\n                }]\r\n            ]\r\n        }\r\n    }"

        headers = {
              'Content-Type': 'application/json'
            }

        response = requests.request("GET", url, headers=headers, data = payload)

        return response  

    def parse_webhook_data_callbackQuey(self, data):
        
        callback_query = data['callback_query']
        
        self.callback_id = callback_query['id']
        self.callback_data = callback_query['data']
    #Answers the callbackQuery with the callback ID and the text
    def post_callbackQuery(self):

        success = None
        #Shoud be dynamic
        #self.chat_id = 924179441
        #temp = self.callback_id
        
        success = requests.post(TELEGRAM_ANSWER_CALLBACK_URL.format(self.callback_id, "Test"))

        
        if self.callback_data == self.ikb_opt_1_callback_data:
            res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self.chat_id, self.ikb_opt_1_callback_data))
            
        elif self.callback_data == self.ikb_opt_2_callback_data:
            res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self.chat_id, self.ikb_opt_2_callback_data))
        
        return "200"  

    @staticmethod
    def init_webhook(url):
        """
        Initializes the webhook
        Args:
            url:str: Provides the telegram server with a endpoint for webhook data
        """

        requests.get(url, verify=True)