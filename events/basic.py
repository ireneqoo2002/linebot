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
            "index":16,
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
    
def push_msg(event,msg):
    try:
        user_id=event.source.user_id
        line_bot_api.push_message(user_id,TextSendMessage(text=msg))
    except:
        room_id=event.source.room_id
        line_bot_api.push_message(room_id,TextSendMessage(text=msg))

def Usage(event):
    push_msg(event,"     查詢方法     \
                    \n\
                    \n小幫手可以查詢油價、匯率、股價\
                    \n\
                    \n 油價通知→→→輸入查詢油價\
                    \n 匯率通知→→→書入查詢匯率\
                    \n 匯率兌換→→→換匯USD/TWD\
                    \n 股價查詢→→→輸入#股票代號")