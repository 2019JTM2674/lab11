import requests

def telegram_bot_sendtext(bot_message):
    
    bot_token = '1034111351:AAGKsm_SSiXEGOU87-h-YcVJ4kd3UQJQY7o'
    bot_chatID = '950802426'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
    

test = telegram_bot_sendtext("Testing Telegram bot")
print(test)