from line_bot_api import *

def about_us_event(event):
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
    
