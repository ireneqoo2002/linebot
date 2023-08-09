from line_bot_api import *
from events.basic import *
from events.oil import *
from events.Msg_Template import *
from model.mongodb import *
import re
import twstock
import datetime

app=Flask(__name__)


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
#處理訊息
@handler.add(MessageEvent,message=TextMessage)
def handle_messahe(event):
     profile = line_bot_api.get_profile(event.source.user_id)
     uid = profile.user_id
     message_text = str(event.message.text).lower()
     msg = str(event.message.text).upper().strip()#使用者輸入的內容
     emsg = event.message.text
     user_name = profile.display_name#使用者名稱

     #使用說明############################################

     if message_text =='@使用說明':
         about_us_event(event)

    #油價################################################
     if event.message.text =="油價查詢":
         content = oil_price()
         line_bot_api.reply_message(
             event.reply_token,
             TextSendMessage(text=content)
         )
    #股價################################################
     if event.message.text=="股價查詢":
        line_bot_api.push_message(uid,TextSendMessage("請輸入#加股票代號......"))
    #股價查詢
     if re.match("想知道股價[0-9]:", msg):
        stockNumber = msg[2:6]
        btn_msg = stock_reply_other(stockNumber)
        line_bot_api.push_message(uid, btn_msg)
        return 0
    #新增使用者關注的股票到mongodb  
     if re.match("關注[0-9]{4}[<>][0-9]", msg):
        stockNumber = msg[2:6]
        content = write_my_stock(uid, user_name,stockNumber,msg[6:7],msg[7:])
        line_bot_api.push_message(uid, TextSendMessage(content)) 
        return 0
     if (emsg.startswith('#')):
        text = emsg[1:]
        content =''

        stock_rt = twstock.realtime.get(text)
        my_datetime = datetime.datetime.fromtimestamp(stock_rt['timestamp']+8*60*60)
        my_time = my_datetime.strftime('%H:%M:%S')

        content +='%s (%s) %s\n' % (
            stock_rt['info']['name'],
            stock_rt['info']['code'],
            my_time)
        
        content += '現價: %s / 開盤: %s\n'%(
            stock_rt['realtime']['latest_trade_price'],
            stock_rt['realtime']['open'])
        content += '最高: %s / 最低:%s\n'%(
            stock_rt['realtime']['high'],
            stock_rt['realtime']['low'])
        
        content += '量: %s\n'%(stock_rt['realtime']['accumulate_trade_volume'])

        stock = twstock.Stock(text)
        content += '-----\n'
        content += '最近五日價格: \n'
        price5 = stock.price[-5:][::-1]
        date5 = stock.date[-5:][::-1]
        for i in range(len(price5)):
            content += '[%s] %s\n' % (date5[i].strftime("%Y-%m-%d"), price5[i])
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text=content)
        )
    #匯率################################################
     if re.match('幣別種類',emsg):
         message=show_Button()
         line_bot_api.reply_message(event.reply_token,message)
    #股價################################################
     if message_text =='@小幫手':
         Usage(event)
     if event.message.text =="@小幫手":
        buttons_template =TemplateSendMessage(
            alt_text='小幫手 template',
            template=ButtonsTemplate(
                title='選擇服務',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/QCi6YUM.png',
                actions=[
                    MessageTemplateAction(
                        label='油價查詢',
                        text='油價查詢'
                    ),
                    MessageTemplateAction(
                        label='匯率查詢',
                        text='匯率查詢'
                    ),
                    MessageTemplateAction(
                        label='股價查詢',
                        text='股價查詢'
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            [buttons_template])
#封鎖################################################

@handler.add(FollowEvent)
def handle_unfollow(event):
    welcome_msg = """HEllO,歡迎您成為分析趨勢的好友!
-我這裡有股票、匯率的資訊
-直接點選下方選單功能使用"""

    line_bot_api.replay_message(
        event.reply_token,
        TextSendMessage(text=welcome_msg))
    

@handler.add(FollowEvent)
def handle_unfollow(event):
    print(event)

if __name__=="__main__":
    app.run()