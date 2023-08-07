from flask import Flask,request,abort
from linebot import (LineBotApi,WebhookHandler,exceptions)
from linebot.exceptions import(InvalidSignatureError)
from linebot.models import *

app=Flask(__name__)

line_bot_api=LineBotApi('EeXOCO6/WX7grCTxTs4HWUuH9Jg/MeTseMMgTr/kCEO8aZx75aht4YdgGsJ5QMThuTqlC5RFKYH8Rn4gt/CB6TPKADJwio4YaQOyGI3F1BoRgKTsecZ6NAgu1kNACcqGk87h1OGrKJlY9b4Vr2vPmAdB 04t89/1O/w1cDnyilFU=')

handler=WebhookHandler('8ee37bacd5d2c37ddfaeffb96b622619')