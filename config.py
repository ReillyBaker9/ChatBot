#This files holds the main variables, the tokens and the URLs, 
#along with specific URL formats to proceed to HTTP requests 

TOKEN = '1184647758:AAHqSNCXENyuEDRbcdWrs874waAr0Cy9hPg'
NGROK_URL = 'https://84ffd6a5f44b.ngrok.io'
BASE_TELEGRAM_URL = 'https://api.telegram.org/bot{}'.format(TOKEN)
LOCAL_WEBHOOK_ENDPOINT = '{}/webhook'.format(NGROK_URL)
TELEGRAM_INIT_WEBHOOK_URL = '{}/setWebhook?url={}'.format(BASE_TELEGRAM_URL, LOCAL_WEBHOOK_ENDPOINT)
TELEGRAM_SEND_MESSAGE_URL = BASE_TELEGRAM_URL + '/sendMessage?chat_id={}&text={}'
TELEGRAM_SEND_POLL_URL = BASE_TELEGRAM_URL + '/sendMessage?chat_id={}&text={}&reply_markup=InlineKeyboardMarkup'
TELEGRAM_ANSWER_CALLBACK_URL = BASE_TELEGRAM_URL + '/answerCallbackQuery?id={}&text={}'




#Previous variables 
#TOKEN = '1184647758:AAHqSNCXENyuEDRbcdWrs874waAr0Cy9hPg'
#NGROK_URL = 'https://43a155df.ngrok.io'
#BASE_TELEGRAM_URL = 'https://api.telegram.org/bot{}'.format(TOKEN)
#LOCAL_WEBHOOK_ENDPOINT = '{}/webhook'.format(NGROK_URL)
#TELEGRAM_INIT_WEBHOOK_URL = '{}/setWebhook?url={}'.format(BASE_TELEGRAM_URL, LOCAL_WEBHOOK_ENDPOINT)
#TELEGRAM_SEND_MESSAGE_URL = BASE_TELEGRAM_URL + '/sendMessage?chat_id={}&text={}'