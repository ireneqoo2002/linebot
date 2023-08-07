from flask import Flask,request,abort
from linebot import (LineBotApi,WebhookHandler,exceptions)
from linebot.exceptions import(InvalidSignatureError)
from linebot.models import *

app=Flask(__name__)

line_bot_api=LineBotApi('EeXOCO6/WX7grCTxTs4HWUuH9Jg/MeTseMMgTr/kCEO8aZx75aht4YdgGsJ5QMThuTqlC5RFKYH8Rn4gt/CB6TPKADJwio4YaQOyGI3F1BoRgKTsecZ6NAgu1kNACcqGk87h1OGrKJlY9b4Vr2vPmAdB 04t89/1O/w1cDnyilFU=')

handler=WebhookHandler('8ee37bacd5d2c37ddfaeffb96b622619')

@app.route("/callback",methods=['POST'])
def callback():
    signature=request.headers['X-Line-Signature']


    body=request.get_data(as_text=True)
    app.logger.info("Request body: "+body)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    #message=TextSendMessage(text=event.message.text)
    #line_bot_api.reply_message(event.reply_token,message)
    emoji = [
        {
            "index":0,
            "productId": "5ac1bfd5040ab15980c9b435",
            "emojiId": "009"
        },
        {
            "index":6,
            "productId": "5ac2211e031a6752fb806d61",
            "emojiId": "003"
        }
    ]

    text_message=TextSendMessage(text='''$Master Finance $
Hello! 您好，這是一個分析股票、油價的頻道！''',emojis=emoji)

    sticker_message = StickerMessage(
        package_id='8522',
        sticker_id='16581271'
    )
    line_bot_api.reply_message(
        event.reply_token,
        [text_message,sticker_message])
    
if __name__=="__main__":
    app.run()