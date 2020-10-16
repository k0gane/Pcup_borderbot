from PIL import Image, ImageDraw, ImageFont
import os
import sys
import datetime
import json
import tweepy
import time
import requests

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

def make_json(idol_id):#json整形部
    s1 = scraping_json(idol_id, 1, 10)
    s2 = scraping_json(idol_id, 91, 100)
    s3 = scraping_json(idol_id, 991, 1000)
    s4 = scraping_json(idol_id, 2991, 3000)
    p1 = s1[-4]['entries']
    p2 = s2[-4]['entries']
    p3 = s3[-4]['entries']
    p4 = s4[-4]['entries']
    pp1 = s1[-30]['entries']
    pp2 = s2[-30]['entries']
    pp3 = s3[-30]['entries']
    pp4 = s4[-30]['entries']
    s1 = s1[-1]['entries']
    s2 = s2[-1]['entries']
    s3 = s3[-1]['entries']
    s4 = s4[-1]['entries']
    return {"1位":{'name':s1[0]["nickname"], 'fan_num':s1[0]["score"], 'dif_60':culc_diff(s1[0]["score"], p1[0]["score"]), 'dif_24':culc_diff(s1[0]["score"], pp1[0]["score"])}, 
                   "2位":{'name':s1[1]["nickname"], 'fan_num':s1[1]["score"], 'dif_60':culc_diff(s1[1]["score"], p1[1]["score"]), 'dif_24':culc_diff(s1[1]["score"], pp1[1]["score"])},
                   "3位":{'name':s1[2]["nickname"], 'fan_num':s1[2]["score"], 'dif_60':culc_diff(s1[2]["score"], p1[2]["score"]), 'dif_24':culc_diff(s1[2]["score"], pp1[2]["score"])},
                   "10位":{'name':s1[9]["nickname"], 'fan_num':s1[9]["score"], 'dif_60':culc_diff(s1[9]["score"], p1[9]["score"]), 'dif_24':culc_diff(s1[9]["score"], pp1[9]["score"])},
                   "100位":{'name':s2[9]["nickname"], 'fan_num':s2[9]["score"], 'dif_60':culc_diff(s2[9]["score"], p2[9]["score"]), 'dif_24':culc_diff(s2[9]["score"], pp2[9]["score"])},
                   "1000位":{'name':s3[9]["nickname"], 'fan_num':s3[9]["score"], 'dif_60':culc_diff(s3[9]["score"], p3[9]["score"]), 'dif_24':culc_diff(s3[9]["score"], pp3[9]["score"])},
                   "3000位":{'name':s4[9]["nickname"], 'fan_num':s4[9]["score"], 'dif_60':culc_diff(s4[9]["score"], p4[9]["score"]), 'dif_24':culc_diff(s4[9]["score"], pp4[9]["score"])}
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
    
    text = str(datetime.datetime.now())[:-7]
    font_size = 40
    height = 360
    width = 440
    img = add_text_to_image(base_img, text, font_path, font_size, font_color, height, width) # dummy for get text_size

    past_time = (datetime.datetime.now().day-12)*24+datetime.datetime.now().hour-15
    text = "開始から"+str(past_time)+"時間経過(残り"+str(189-past_time)+"時間)"
    font_size = 40
    height = 500
    width = 230
    img = add_text_to_image(base_img, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    

    #kogane_data = get_data()

    mano_data = make_json("1")
    img_mano = make_rank('mano', mano_data, font_path)
    hiori_data = make_json('2')
    img_hiori = make_rank('hiori', hiori_data, font_path)
    meguru_data = make_json('3')
    img_meguru = make_rank('meguru', meguru_data, font_path)
    kogane_data = make_json('4')
    img_kogane = make_rank('kogane', kogane_data, font_path)
    mamimi_data = make_json('5')
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
    time.sleep(60)
    
    sakuya_data = make_json('6')
    img_sakuya = make_rank('sakuya', sakuya_data, font_path)
    yuika_data = make_json('7')
    img_yuika = make_rank('yuika', yuika_data, font_path)
    kiriko_data = make_json('8')
    img_kiriko = make_rank('kiriko', kiriko_data, font_path)
    amana_data = make_json('14')
    img_amana = make_rank('amana', amana_data, font_path)
    tenka_data = make_json('15')
    img_tenka = make_rank('tenka', tenka_data, font_path)
    chiyuki_data = make_json('16')
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
    time.sleep(60)
    
    kaho_data = make_json('9')
    img_kaho = make_rank('kaho', kaho_data, font_path)
    chiyoko_data = make_json('10')
    img_chiyoko = make_rank('chiyoko', chiyoko_data, font_path)
    juri_data = make_json('11')
    img_juri = make_rank('juri', juri_data, font_path)    
    rinze_data = make_json('12')
    img_rinze = make_rank('rinze', rinze_data, font_path)
    natsuha_data = make_json('13')
    img_natsuha = make_rank('natsuha', natsuha_data, font_path)

    asahi_data = make_json('17')
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
    time.sleep(60)

    fuyuko_data = make_json('18')
    img_fuyuko = make_rank('fuyuko', fuyuko_data, font_path)
    mei_data = make_json('19')
    img_mei = make_rank('mei', mei_data, font_path)
    tooru_data = make_json('20')
    img_tooru = make_rank('tooru', tooru_data, font_path)
    madoka_data = make_json('21')
    img_madoka = make_rank('madoka', madoka_data, font_path)
    koito_data = make_json('22')
    img_koito = make_rank('koito', koito_data, font_path)
    hinana_data = make_json('23')
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

def tweet_picture(now_time):#メイン
    nowtime = datetime.datetime.now()
    past_time = (nowtime.day-12)*24+nowtime.hour-15
    top_player = make_image(now_time)
    text = str(nowtime.month) + "/" +  str(nowtime.day) + " " + str(nowtime.hour) + ":00 現在\nPカップボーダー\n"
    if(now_time % 100 == 24):
        text += "最高日速\n"
    else:
        text += "最高時速\n"
    text += no1 + no2 + no3
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

def scraping_json(idol_id, rank_begin, rank_end):
    url = "https://kl8xmr7hlb.execute-api.ap-northeast-1.amazonaws.com/dev/v1/40005/getHistoryByRank/{}/{}/{}".format(idol_id, rank_begin, rank_end)
    r = requests.get(url)
    data = r.json()
    return data

make_image(101609)
    