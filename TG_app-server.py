from flask import Flask, request, jsonify
from config import TELEGRAM_INIT_WEBHOOK_URL
from config import TELEGRAM_SEND_MESSAGE_URL
from config import TELEGRAM_SEND_POLL_URL
from config import TELEGRAM_ANSWER_CALLBACK_URL
from telegram_bot import TelegramBot
import sys
#This file runs the Flask app, routes the HTTP resquests and calls methods in other files 


app = Flask(__name__)

#Initialize the Webhook with TG with a static function
TelegramBot.init_webhook(TELEGRAM_INIT_WEBHOOK_URL)

#Initalize the bot class instant -> TO DO this will have to threaded after 
bot = TelegramBot()

#From JSON Body, assess if the req is a message or a callback in the TG semantic 
#TO DO, move and wrap to the "engine" file 
def is_message(req):
    print('Entering is_message' , file=sys.stderr)

    try:
        message = req['message']
        print('Is_message returns TRUE' , file=sys.stderr)
        return True
    except:
        print('Is_message returns FALSE' , file=sys.stderr)
        return False
    
def is_callback(req):
    print('Entering is_callback' , file=sys.stderr)
    try:
        
        callback_query = req['callback_query']
        print('is_callback returns TRUE' , file=sys.stderr)
        return True
    except:
        print('is_callback returns FALSE' , file=sys.stderr)
        return False

@app.route('/webhook', methods=['GET','POST'])
def index():
    req = request.get_json()
    print('/webhook with request: '+ str(req) , file=sys.stderr)

    
    if is_message(req) == True :
       
        bot.parse_webhook_data_message(req)
        success = bot.post_message()
        
        return "100"
    elif is_callback(req) == True :
        
        
        bot.parse_webhook_data_callbackQuey(req)
        ret_code = bot.post_callbackQuery()
        
        
        return ret_code
    else :
        return "300"
    return req # TODO: Success should reflect the success of the reply

@app.route('/InlineKB', methods=['GET','POST'])
def inline_keyboard():
    req = request.get_json()
    print('/InlineKB with request: '+ str(req) , file=sys.stderr)

    bot.parse_webhook_data_inlineKeyboard(req)
    bot.post_inlineKB()
    
    return req

@app.route('/', methods=['GET','POST'])
def reroute():
    print('/ with request: '+ str(request.get_json()), file=sys.stderr)


    return "Please try to add /InlineKB to your URL"
    

if __name__ == '__main__':
    app.run(port=5000)


# https://telegram.me

# check bot initialization: https://api.telegram.org/bot<822448732:AAGUNRBnPPHjVhOqySQZk_QzP_VaZhgx9i0>/getme
# check webhook url: https://api.telegram.org/bot822448732:AAGUNRBnPPHjVhOqySQZk_QzP_VaZhgx9i0/getWebhookInfo




