from PIL import Image, ImageDraw, ImageFont
import os
import sys
import datetime
import json
import tweepy

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
    
def make_json(chara_id, border, border_b60, border_b24):#json整形部
    s = str(chara_id)
    return {"1位":{'name':border[s][0]["nickname"], 'fan_num':border[s][0]["score"], 'dif_60':culc_diff(border[s][0]["score"], border_b60[s][0]["score"]), 'dif_24':culc_diff(border[s][0]["score"], border_b24[s][0]["score"])}, 
                   "2位":{'name':border[s][1]["nickname"], 'fan_num':border[s][1]["score"], 'dif_60':culc_diff(border[s][1]["score"], border_b60[s][1]["score"]), 'dif_24':culc_diff(border[s][1]["score"], border_b24[s][1]["score"])},
                   "3位":{'name':border[s][2]["nickname"], 'fan_num':border[s][2]["score"], 'dif_60':culc_diff(border[s][2]["score"], border_b60[s][2]["score"]), 'dif_24':culc_diff(border[s][2]["score"], border_b24[s][2]["score"])},
                   "10位":{'name':border[s][9]["nickname"], 'fan_num':border[s][9]["score"], 'dif_60':culc_diff(border[s][9]["score"], border_b60[s][9]["score"]), 'dif_24':culc_diff(border[s][9]["score"], border_b24[s][9]["score"])},
                   "100位":{'name':border[s][99]["nickname"], 'fan_num':border[s][99]["score"], 'dif_60':culc_diff(border[s][99]["score"], border_b60[s][99]["score"]), 'dif_24':culc_diff(border[s][99]["score"], border_b24[s][99]["score"])},
                   "1000位":{'name':border[s][999]["nickname"], 'fan_num':border[s][999]["score"], 'dif_60':culc_diff(border[s][999]["score"], border_b60[s][999]["score"]), 'dif_24':culc_diff(border[s][999]["score"], border_b24[s][999]["score"])},
                   "3000位":{'name':border[s][2999]["nickname"], 'fan_num':border[s][2999]["score"], 'dif_60':culc_diff(border[s][2999]["score"], border_b60[s][2999]["score"]), 'dif_24':culc_diff(border[s][2999]["score"], border_b24[s][2999]["score"])}
                   }

def ranking(now, past):#時速ランキング
    now_data = {}
    past_data = {}
    rank = []
    for i in range(1, 24):
        for j in range(len(now[str(i)])):
            try:
                now_data[now[str(i)][j]["earthUserId"]] = {'score':(now_data[now[str(i)][j]["earthUserId"]]['score']+now[str(i)][j]["score"]), 'nickname':now[str(i)][j]["nickname"]}
            except:
                now_data[now[str(i)][j]["earthUserId"]] = {'score':now[str(i)][j]["score"], 'nickname':now[str(i)][j]["nickname"]}
        for j in range(len(past[str(i)])):        
            try:
                past_data[past[str(i)][j]["earthUserId"]] = {'score':(past_data[past[str(i)][j]["earthUserId"]]['score']+past[str(i)][j]["score"]), 'nickname':past[str(i)][j]["nickname"]}
            except:
                past_data[past[str(i)][j]["earthUserId"]] = {'score':past[str(i)][j]["score"], 'nickname':past[str(i)][j]["nickname"]}
                
    for name in now_data.keys():
        try:
            rank.append([now_data[name]['nickname'], now_data[name]['score']-past_data[name]['score']])
        except:
            continue
    rank = sorted(rank, reverse=True, key=lambda x: x[1])

    return [rank[0], rank[1], rank[2]]
            
def make_image(now_time, font_color="black"):#画像生成部
    base_image_path = "haikei.jpg"
    base_img = Image.open(base_image_path).copy()
    with open('border/' + str(now_time) + '.json', 'r', encoding="utf-8") as f:
        border = json.load(f)
    
    if(now_time%100 == 10):
        with open('border/' + str(now_time-10) + '.json', 'r', encoding="utf-8") as f:
            border_b60 = json.load(f)
    else:
        with open('border/' + str(now_time-1) + '.json', 'r', encoding="utf-8") as f:
            border_b60 = json.load(f)
        
    with open('border/' + str(now_time-100) + '.json', 'r', encoding="utf-8") as f:
        border_b24 = json.load(f)    
    
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
    text = "開始から"+str(past_time)+"時間経過(残り"+str(213-past_time)+"時間)"
    font_size = 40
    height = 500
    width = 230
    img = add_text_to_image(base_img, text, font_path, font_size, font_color, height, width) # dummy for get text_size
    

    #kogane_data = get_data()

    mano_data = make_json("1", border, border_b60, border_b24)
    img_mano = make_rank('mano', mano_data, font_path)
    hiori_data = make_json('2', border, border_b60, border_b24)
    img_hiori = make_rank('hiori', hiori_data, font_path)
    meguru_data = make_json('3', border, border_b60, border_b24)
    img_meguru = make_rank('meguru', meguru_data, font_path)
    kogane_data = make_json('4', border, border_b60, border_b24)
    img_kogane = make_rank('kogane', kogane_data, font_path)
    mamimi_data = make_json('5', border, border_b60, border_b24)
    img_mamimi = make_rank('mamimi', mamimi_data, font_path)
    sakuya_data = make_json('6', border, border_b60, border_b24)
    img_sakuya = make_rank('sakuya', sakuya_data, font_path)
    yuika_data = make_json('7', border, border_b60, border_b24)
    img_yuika = make_rank('yuika', yuika_data, font_path)
    kiriko_data = make_json('8', border, border_b60, border_b24)
    img_kiriko = make_rank('kiriko', kiriko_data, font_path)
    kaho_data = make_json('9', border, border_b60, border_b24)
    img_kaho = make_rank('kaho', kaho_data, font_path)
    chiyoko_data = make_json('10', border, border_b60, border_b24)
    img_chiyoko = make_rank('chiyoko', chiyoko_data, font_path)
    juri_data = make_json('11', border, border_b60, border_b24)
    img_juri = make_rank('juri', juri_data, font_path)
    rinze_data = make_json('12', border, border_b60, border_b24)
    img_rinze = make_rank('rinze', rinze_data, font_path)
    natsuha_data = make_json('13', border, border_b60, border_b24)
    img_natsuha = make_rank('natsuha', natsuha_data, font_path)
    amana_data = make_json('14', border, border_b60, border_b24)
    img_amana = make_rank('amana', amana_data, font_path)
    tenka_data = make_json('15', border, border_b60, border_b24)
    img_tenka = make_rank('tenka', tenka_data, font_path)
    chiyuki_data = make_json('16', border, border_b60, border_b24)
    img_chiyuki = make_rank('chiyuki', chiyuki_data, font_path)
    asahi_data = make_json('17', border, border_b60, border_b24)
    img_asahi = make_rank('asahi', asahi_data, font_path)
    fuyuko_data = make_json('18', border, border_b60, border_b24)
    img_fuyuko = make_rank('fuyuko', fuyuko_data, font_path)
    mei_data = make_json('19', border, border_b60, border_b24)
    img_mei = make_rank('mei', mei_data, font_path)
    tooru_data = make_json('20', border, border_b60, border_b24)
    img_tooru = make_rank('tooru', tooru_data, font_path)
    madoka_data = make_json('21', border, border_b60, border_b24)
    img_madoka = make_rank('madoka', madoka_data, font_path)
    koito_data = make_json('22', border, border_b60, border_b24)
    img_koito = make_rank('koito', koito_data, font_path)
    hinana_data = make_json('23', border, border_b60, border_b24)
    img_hinana = make_rank('hinana', hinana_data, font_path)
    
    dst11 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst12 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst13 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    
    dst21 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst22 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst23 = Image.new('RGB', (img_mano.width*2, img_mano.height))

    dst31 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst32 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst33 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    
    dst41 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst42 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst43 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    
    dst1 = Image.new('RGB', (img_mano.width*2, img_mano.height*3))
    dst2 = Image.new('RGB', (img_mano.width*2, img_mano.height*3))
    dst3 = Image.new('RGB', (img_mano.width*2, img_mano.height*3))
    dst4 = Image.new('RGB', (img_mano.width*2, img_mano.height*3))
    
    dst11.paste(img, (0, 0))
    dst11.paste(img_mano, (img_mano.width, 0))
    
    dst12.paste(img_hiori, (0, 0))
    dst12.paste(img_meguru, (img_mano.width, 0))
    
    dst13.paste(img_kogane, (0, 0))
    dst13.paste(img_mamimi, (img_mano.width, 0))
    
    dst21.paste(img_sakuya, (0, 0))
    dst21.paste(img_yuika, (img_mano.width, 0))
    
    dst22.paste(img_kiriko, (0, 0))
    dst22.paste(img_amana, (img_mano.width, 0))
    
    dst23.paste(img_tenka, (0, 0))
    dst23.paste(img_chiyuki, (img_mano.width, 0))
    
    dst31.paste(img_kaho, (0, 0))
    dst31.paste(img_chiyoko, (img_mano.width, 0))
    
    dst32.paste(img_juri, (0, 0))
    dst32.paste(img_rinze, (img_mano.width, 0))
    
    dst33.paste(img_natsuha, (0, 0))
    dst33.paste(img_asahi, (img_mano.width, 0))
    
    dst41.paste(img_fuyuko, (0, 0))
    dst41.paste(img_mei, (img_mano.width, 0))
    
    dst42.paste(img_tooru, (0, 0))
    dst42.paste(img_madoka, (img_mano.width, 0))
    
    dst43.paste(img_hinana, (0, 0))
    dst43.paste(img_koito, (img_mano.width, 0))
    
    dst1.paste(dst11, (0, 0))
    dst1.paste(dst12, (0, img_mano.height))
    dst1.paste(dst13, (0, img_mano.height*2))    
    
    dst2.paste(dst21, (0, 0))
    dst2.paste(dst22, (0, img_mano.height))
    dst2.paste(dst23, (0, img_mano.height*2))

    dst3.paste(dst31, (0, 0))
    dst3.paste(dst32, (0, img_mano.height))
    dst3.paste(dst33, (0, img_mano.height*2))
    
    dst4.paste(dst41, (0, 0))
    dst4.paste(dst42, (0, img_mano.height))
    dst4.paste(dst43, (0, img_mano.height*2))
    
    dst1.save("img1.png")
    dst2.save("img2.png")
    dst3.save("img3.png")
    dst4.save("img4.png")
    if(now_time%100 == 24):
        top_player = ranking(border, border_b24)
    else:
        top_player = ranking(border, border_b60)
    
    return top_player

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
    no1 = top_player[0]
    no2 = top_player[1]
    no3 = top_player[2]
    no1 = "1位 "+no1[0]+" "+str(no1[1])+"人\n"
    no2 = "2位 "+no2[0]+" "+str(no2[1])+"人\n"
    no3 = "3位 "+no3[0]+" "+str(no3[1])+"人\n"
    text = str(nowtime.month) + "/" +  str(nowtime.day) + " " + str(nowtime.hour) + ":00 現在\nPカップボーダー\n"
    if(now_time % 100 == 24):
        text += "最高日速\n"
    elif(now_time%100 == 1):
        text += "10時間速\n"
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

tweet_picture(101616)