from PIL import Image, ImageDraw, ImageFont
import os
import sys
import datetime
import json
import tweepy
import time
import requests
from retrying import retry


def add_text_to_image(img, text, font_path, font_size, font_color, height, width, max_length=50):#画像に文字を合成する部分
    position = (width, height)
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(img)
    draw.text(position, text, font_color, font=font)
    
    return img

def culc_diff(a, b):#差分計算
    try:
        return a-b
    except:
        return 0

def make_json(idol_id, now_time):#json整形部
    s = scraping_json(idol_id, now_time)
    p = scraping_json(idol_id, now_time-datetime.timedelta(hours=1))
    pp = scraping_json(idol_id, now_time-datetime.timedelta(days=1))

    return {"1位":{'name':s[0]["nickname"], 'fan_num':s[0]["score"], 'dif_60':culc_diff(s[0]["score"], p[0]["score"]), 'dif_24':culc_diff(s[0]["score"], pp[0]["score"])}, 
                   "2位":{'name':s[1]["nickname"], 'fan_num':s[1]["score"], 'dif_60':culc_diff(s[1]["score"], p[1]["score"]), 'dif_24':culc_diff(s[1]["score"], pp[1]["score"])},
                   "3位":{'name':s[2]["nickname"], 'fan_num':s[2]["score"], 'dif_60':culc_diff(s[2]["score"], p[2]["score"]), 'dif_24':culc_diff(s[2]["score"], pp[2]["score"])},
                   "10位":{'name':s[3]["nickname"], 'fan_num':s[3]["score"], 'dif_60':culc_diff(s[3]["score"], p[3]["score"]), 'dif_24':culc_diff(s[3]["score"], pp[3]["score"])},
                   "100位":{'name':s[4]["nickname"], 'fan_num':s[4]["score"], 'dif_60':culc_diff(s[4]["score"], p[4]["score"]), 'dif_24':culc_diff(s[4]["score"], pp[4]["score"])},
                   "1000位":{'name':s[5]["nickname"], 'fan_num':s[5]["score"], 'dif_60':culc_diff(s[5]["score"], p[5]["score"]), 'dif_24':culc_diff(s[5]["score"], pp[5]["score"])},
                   "3000位":{'name':s[6]["nickname"], 'fan_num':s[6]["score"], 'dif_60':culc_diff(s[6]["score"], p[6]["score"]), 'dif_24':culc_diff(s[6]["score"], pp[6]["score"])}
                   }
            
def make_image(now_time, font_color="black"):#画像生成部
    base_image_path = "haikei.jpg"
    base_img = Image.open(base_image_path).copy()
    
    font_path = "rn3lo-1vsc6.ttf"
    
    # get fontsize
    text = "Pカップボーダー"
    font_size = 128
    height = 180
    width = 70
    img = add_text_to_image(base_img, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    text = "現在時刻:"
    font_size = 60
    height = 350
    width = 180
    img = add_text_to_image(base_img, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    text = str(now)[:-7]
    font_size = 40
    height = 360
    width = 440
    img = add_text_to_image(base_img, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    past_time = (now.day-12)*24+now.hour-15
    text = "開始から"+str(past_time)+"時間経過(残り"+str(213-past_time)+"時間)"
    font_size = 40
    height = 500
    width = 230
    img = add_text_to_image(base_img, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    mano_data = make_json("1", now_time)
    img_mano = make_rank('mano', mano_data, font_path)
    hiori_data = make_json('2', now_time)
    img_hiori = make_rank('hiori', hiori_data, font_path)
    meguru_data = make_json('3', now_time)
    img_meguru = make_rank('meguru', meguru_data, font_path)
    kogane_data = make_json('4', now_time)
    img_kogane = make_rank('kogane', kogane_data, font_path)
    mamimi_data = make_json('5', now_time)
    img_mamimi = make_rank('mamimi', mamimi_data, font_path)
    
    dst11 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst12 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst13 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    
    dst1 = Image.new('RGB', (img_mano.width*2, img_mano.height*3))
    
    dst11.paste(img, (0, 0))
    dst11.paste(img_mano, (img_mano.width, 0))
    
    dst12.paste(img_hiori, (0, 0))
    dst12.paste(img_meguru, (img_mano.width, 0))
    
    dst13.paste(img_kogane, (0, 0))
    dst13.paste(img_mamimi, (img_mano.width, 0))
    
    dst1.paste(dst11, (0, 0))
    dst1.paste(dst12, (0, img_mano.height))
    dst1.paste(dst13, (0, img_mano.height*2))
    
    dst1.save("img1.png")
    
    sakuya_data = make_json('6', now_time)
    img_sakuya = make_rank('sakuya', sakuya_data, font_path)
    yuika_data = make_json('7', now_time)
    img_yuika = make_rank('yuika', yuika_data, font_path)
    kiriko_data = make_json('8', now_time)
    img_kiriko = make_rank('kiriko', kiriko_data, font_path)
    amana_data = make_json('14', now_time)
    img_amana = make_rank('amana', amana_data, font_path)
    tenka_data = make_json('15', now_time)
    img_tenka = make_rank('tenka', tenka_data, font_path)
    chiyuki_data = make_json('16', now_time)
    img_chiyuki = make_rank('chiyuki', chiyuki_data, font_path)


    dst21 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst22 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst23 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    
    dst2 = Image.new('RGB', (img_mano.width*2, img_mano.height*3))
    
    dst21.paste(img_sakuya, (0, 0))
    dst21.paste(img_yuika, (img_mano.width, 0))
    
    dst22.paste(img_kiriko, (0, 0))
    dst22.paste(img_amana, (img_mano.width, 0))
    
    dst23.paste(img_tenka, (0, 0))
    dst23.paste(img_chiyuki, (img_mano.width, 0))
    
    dst2.paste(dst21, (0, 0))
    dst2.paste(dst22, (0, img_mano.height))
    dst2.paste(dst23, (0, img_mano.height*2))
    
    dst2.save("img2.png")
    
    kaho_data = make_json('9', now_time)
    img_kaho = make_rank('kaho', kaho_data, font_path)
    chiyoko_data = make_json('10', now_time)
    img_chiyoko = make_rank('chiyoko', chiyoko_data, font_path)
    juri_data = make_json('11', now_time)
    img_juri = make_rank('juri', juri_data, font_path)    
    rinze_data = make_json('12', now_time)
    img_rinze = make_rank('rinze', rinze_data, font_path)
    natsuha_data = make_json('13', now_time)
    img_natsuha = make_rank('natsuha', natsuha_data, font_path)

    asahi_data = make_json('17', now_time)
    img_asahi = make_rank('asahi', asahi_data, font_path)
    
    dst31 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst32 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst33 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    
    dst3 = Image.new('RGB', (img_mano.width*2, img_mano.height*3))
    
    dst31.paste(img_kaho, (0, 0))
    dst31.paste(img_chiyoko, (img_mano.width, 0))
    
    dst32.paste(img_juri, (0, 0))
    dst32.paste(img_rinze, (img_mano.width, 0))
    
    dst33.paste(img_natsuha, (0, 0))
    dst33.paste(img_asahi, (img_mano.width, 0))
    
    dst3.paste(dst31, (0, 0))
    dst3.paste(dst32, (0, img_mano.height))
    dst3.paste(dst33, (0, img_mano.height*2))
    
    dst3.save("img3.png")

    fuyuko_data = make_json('18', now_time)
    img_fuyuko = make_rank('fuyuko', fuyuko_data, font_path)
    mei_data = make_json('19', now_time)
    img_mei = make_rank('mei', mei_data, font_path)
    tooru_data = make_json('20', now_time)
    img_tooru = make_rank('tooru', tooru_data, font_path)
    madoka_data = make_json('21', now_time)
    img_madoka = make_rank('madoka', madoka_data, font_path)
    koito_data = make_json('22', now_time)
    img_koito = make_rank('koito', koito_data, font_path)
    hinana_data = make_json('23', now_time)
    img_hinana = make_rank('hinana', hinana_data, font_path)

    dst41 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst42 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst43 = Image.new('RGB', (img_mano.width*2, img_mano.height))

    dst4 = Image.new('RGB', (img_mano.width*2, img_mano.height*3))
    
    dst41.paste(img_fuyuko, (0, 0))
    dst41.paste(img_mei, (img_mano.width, 0))
    
    dst42.paste(img_tooru, (0, 0))
    dst42.paste(img_madoka, (img_mano.width, 0))
    
    dst43.paste(img_hinana, (0, 0))
    dst43.paste(img_koito, (img_mano.width, 0))
    
    dst4.paste(dst41, (0, 0))
    dst4.paste(dst42, (0, img_mano.height))
    dst4.paste(dst43, (0, img_mano.height*2))
    
    dst4.save("img4.png")

def make_rank(idol_name, kogane_data, font_path, font_color="black"):#順位部分生成部
    base_image_path_2 = "background.jpg"
    base_img_2 = Image.open(base_image_path_2).copy()  
    
    kogane_pic_dir = "idol_fig/" + idol_name + ".png"
    kogane_pic = Image.open(kogane_pic_dir).convert("RGBA") .resize((330, 418))
    base_img_2.paste(kogane_pic, (-50, 207), kogane_pic)
    text = "                     名前          ファン数   +60m    +24h"
    font_size = 30
    height = 60
    width = 260
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width)
    
    # get fontsize
    text = "1位"
    font_size = 40
    height = 150
    width = 260
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    text = kogane_data['1位']['name'].ljust(10)
    font_size = 20
    height = 162
    width = 430
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['1位']['fan_num']).rjust(10)
    font_size = 20
    height = 162
    width = 650
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['1位']['dif_60']).rjust(8)
    font_size = 20
    height = 162
    width = 810
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['1位']['dif_24']).rjust(9)
    font_size = 20
    height = 162
    width = 950
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    text = "2位"
    font_size = 40
    height = 220
    width = 260
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    text = kogane_data['2位']['name'].ljust(10)
    font_size = 20
    height = 232
    width = 430
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['2位']['fan_num']).rjust(10)
    font_size = 20
    height = 232
    width = 650
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['2位']['dif_60']).rjust(8)
    font_size = 20
    height = 232
    width = 810
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['2位']['dif_24']).rjust(9)
    font_size = 20
    height = 232
    width = 950
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    text = "3位"
    font_size = 40
    height = 290
    width = 260
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    text = kogane_data['3位']['name'].ljust(10)
    font_size = 20
    height = 302
    width = 430
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['3位']['fan_num']).rjust(10)
    font_size = 20
    height = 302
    width = 650
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['3位']['dif_60']).rjust(8)
    font_size = 20
    height = 302
    width = 810
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['3位']['dif_24']).rjust(9)
    font_size = 20
    height = 302
    width = 950
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    text = "10位"
    font_size = 40
    height = 360
    width = 260
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    text = kogane_data['10位']['name'].ljust(10)
    font_size = 20
    height = 372
    width = 430
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['10位']['fan_num']).rjust(10)
    font_size = 20
    height = 372
    width = 650
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['10位']['dif_60']).rjust(8)
    font_size = 20
    height = 372
    width = 810
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['10位']['dif_24']).rjust(9)
    font_size = 20
    height = 372
    width = 950
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    text = "100位"
    font_size = 40
    height = 430
    width = 260
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    text = kogane_data['100位']['name'].ljust(10)
    font_size = 20
    height = 442
    width = 430
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['100位']['fan_num']).rjust(10)
    font_size = 20
    height = 442
    width = 650
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['100位']['dif_60']).rjust(8)
    font_size = 20
    height = 442
    width = 810
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['100位']['dif_24']).rjust(9)
    font_size = 20
    height = 442
    width = 950
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    text = "1000位"
    font_size = 40
    height = 500
    width = 260
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    text = kogane_data['1000位']['name'].ljust(10)
    font_size = 20
    height = 512
    width = 430
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['1000位']['fan_num']).rjust(10)
    font_size = 20
    height = 512
    width = 650
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['1000位']['dif_60']).rjust(8)
    font_size = 20
    height = 512
    width = 810
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['1000位']['dif_24']).rjust(9)
    font_size = 20
    height = 512
    width = 950
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    text = "3000位"
    font_size = 40
    height = 570
    width = 260
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    text = kogane_data['3000位']['name'].ljust(10)
    font_size = 20
    height = 582
    width = 430
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['3000位']['fan_num']).rjust(10)
    font_size = 20
    height = 582
    width = 650
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['3000位']['dif_60']).rjust(8)
    font_size = 20
    height = 582
    width = 810
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    text = str(kogane_data['3000位']['dif_24']).rjust(9)
    font_size = 20
    height = 582
    width = 950
    img = add_text_to_image(base_img_2, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    
    return img
    
def tweet_with_imgs(tweet, files):#ツイート実行部
    api = twitter_api()
    media_ids = []
    for ii in range(len(files)):
        img = api.media_upload(files[ii])
        media_ids.append(img.media_id_string)

    api.update_status(status=tweet, media_ids=media_ids)

def tweet_picture(nowtime):#メイン
    past_time = (nowtime.day-12)*24+nowtime.hour-15
    make_image(nowtime)
    text = str(nowtime.month) + "/" +  str(nowtime.day) + " " + str(nowtime.hour) + ":00 現在\nPカップボーダー\n"
    text += "\n#Pカップボーダー"
    print(text)
    tweet_with_imgs(text, ["img1.png", "img2.png", "img3.png", "img4.png"])

def twitter_api():#API叩き部
    consumer_key = 'UY1EOoVXLGYTggXySxNdbsZDs'
    consumer_secret = '17hLJxmUda2JN3iVabGKRS9XGhQhT89i9dsBo84QuVsDny5dPP'
    access_token = '360917569-LpZ64jwezvgwv0b2AQE0hygLX4vVoywig5vG3UGy'
    access_secret = '4qpJy4C0mRHsJBYDu59RXllRK0ZEPUKEpRvdVoZ4QT4E8'
    auth            = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api             = tweepy.API(auth)

    return api

@retry(wait_fixed=10000)
def scraping_json(idol_id, now_time):
    unix_time = int(now_time.timestamp()*1000)
    rank = "https://kl8xmr7hlb.execute-api.ap-northeast-1.amazonaws.com/dev/v1/40005/getLatestRetrieve/{}?asOf={}".format(idol_id, unix_time)
    r = requests.get(rank).json()
    rank_id = r["body"]["id"]
    url = "https://kl8xmr7hlb.execute-api.ap-northeast-1.amazonaws.com/dev/v1/getStandings/{}/1-3,10,100,1000,3000".format(rank_id)
    r = requests.get(url)
    data = r.json()
    time.sleep(3)
    return data["body"]

now = datetime.datetime.now()
tweet_picture(now)
    