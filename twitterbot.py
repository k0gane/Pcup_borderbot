########################################################
#               Pcup borderbot                         #
#               by using matsurihi.me                  #
#               made by @23k_h                         #
########################################################
from PIL import Image, ImageDraw, ImageFont
import os
import sys
import datetime
import json
import tweepy
import time
import requests
from retrying import retry
from datetime import timedelta

#prepartion
pcup_start_day, pcup_start_hour = 12, 16
pcup_end_day, pcup_end_hour = 18, 12
pcup_whole_time = (pcup_end_day - pcup_start_day) * 12 + (pcup_end_hour - pcup_start_hour)
api_domain = "1zkgz3dum2"
event_id = 40007

def add_text_to_image(img, text, font_size, font_color, height, width, max_length=50):#画像に文字を合成する部分
    font_path = "rn3lo-1vsc6.ttf"
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
    data = scraping_json(idol_id, now_time)
    print(data)
    try:#あっち
        # print(data)
        s = data[0]["body"]
        try:
            p = data[1]["body"]
            pp = data[2]["body"]
            return {"1位":{'name':s[0]["nickname"], 'fan_num':s[0]["score"], 'dif_60':culc_diff(s[0]["score"], p[0]["score"]), 'dif_24':culc_diff(s[0]["score"], pp[0]["score"])}, 
                    "2位":{'name':s[1]["nickname"], 'fan_num':s[1]["score"], 'dif_60':culc_diff(s[1]["score"], p[1]["score"]), 'dif_24':culc_diff(s[1]["score"], pp[1]["score"])},
                    "3位":{'name':s[2]["nickname"], 'fan_num':s[2]["score"], 'dif_60':culc_diff(s[2]["score"], p[2]["score"]), 'dif_24':culc_diff(s[2]["score"], pp[2]["score"])},
                    "10位":{'name':s[3]["nickname"], 'fan_num':s[3]["score"], 'dif_60':culc_diff(s[3]["score"], p[3]["score"]), 'dif_24':culc_diff(s[3]["score"], pp[3]["score"])},
                    "100位":{'name':s[4]["nickname"], 'fan_num':s[4]["score"], 'dif_60':culc_diff(s[4]["score"], p[4]["score"]), 'dif_24':culc_diff(s[4]["score"], pp[4]["score"])},
                    "1000位":{'name':s[5]["nickname"], 'fan_num':s[5]["score"], 'dif_60':culc_diff(s[5]["score"], p[5]["score"]), 'dif_24':culc_diff(s[5]["score"], pp[5]["score"])},
                    "3000位":{'name':s[6]["nickname"], 'fan_num':s[6]["score"], 'dif_60':culc_diff(s[6]["score"], p[6]["score"]), 'dif_24':culc_diff(s[6]["score"], pp[6]["score"])}
                    }
        except Exception as e:
            try:#2～23時間目
                p = data[1]["body"]
                return {"1位":{'name':s[0]["nickname"], 'fan_num':s[0]["score"], 'dif_60':culc_diff(s[0]["score"], p[0]["score"]), 'dif_24':s[0]["score"]}, 
                        "2位":{'name':s[1]["nickname"], 'fan_num':s[1]["score"], 'dif_60':culc_diff(s[1]["score"], p[1]["score"]), 'dif_24':s[1]["score"]},
                        "3位":{'name':s[2]["nickname"], 'fan_num':s[2]["score"], 'dif_60':culc_diff(s[2]["score"], p[2]["score"]), 'dif_24':s[2]["score"]},
                        "10位":{'name':s[3]["nickname"], 'fan_num':s[3]["score"], 'dif_60':culc_diff(s[3]["score"], p[3]["score"]), 'dif_24':s[3]["score"]},
                        "100位":{'name':s[4]["nickname"], 'fan_num':s[4]["score"], 'dif_60':culc_diff(s[4]["score"], p[4]["score"]), 'dif_24':s[4]["score"]},
                        "1000位":{'name':s[5]["nickname"], 'fan_num':s[5]["score"], 'dif_60':culc_diff(s[5]["score"], p[5]["score"]), 'dif_24':s[5]["score"]},
                        "3000位":{'name':s[6]["nickname"], 'fan_num':s[6]["score"], 'dif_60':culc_diff(s[6]["score"], p[6]["score"]), 'dif_24':s[6]["score"]}
                        }
            except:
                try:
                    return {"1位":{'name':s[0]["nickname"], 'fan_num':s[0]["score"], 'dif_60':s[0]["score"], 'dif_24':s[0]["score"]}, 
                            "2位":{'name':s[1]["nickname"], 'fan_num':s[1]["score"], 'dif_60':s[1]["score"], 'dif_24':s[1]["score"]},
                            "3位":{'name':s[2]["nickname"], 'fan_num':s[2]["score"], 'dif_60':s[2]["score"], 'dif_24':s[2]["score"]},
                            "10位":{'name':s[3]["nickname"], 'fan_num':s[3]["score"], 'dif_60':s[3]["score"], 'dif_24':s[3]["score"]},
                            "100位":{'name':s[4]["nickname"], 'fan_num':s[4]["score"], 'dif_60':s[4]["score"], 'dif_24':s[4]["score"]},
                            "1000位":{'name':s[5]["nickname"], 'fan_num':s[5]["score"], 'dif_60':s[5]["score"], 'dif_24':s[5]["score"]},
                            "3000位":{'name':s[6]["nickname"], 'fan_num':s[6]["score"], 'dif_60':s[6]["score"], 'dif_24':s[6]["score"]}
                            }
                except:#3000位おらん
                    return {"1位":{'name':s[0]["nickname"], 'fan_num':s[0]["score"], 'dif_60':s[0]["score"], 'dif_24':s[0]["score"]}, 
                            "2位":{'name':s[1]["nickname"], 'fan_num':s[1]["score"], 'dif_60':s[1]["score"], 'dif_24':s[1]["score"]},
                            "3位":{'name':s[2]["nickname"], 'fan_num':s[2]["score"], 'dif_60':s[2]["score"], 'dif_24':s[2]["score"]},
                            "10位":{'name':s[3]["nickname"], 'fan_num':s[3]["score"], 'dif_60':s[3]["score"], 'dif_24':s[3]["score"]},
                            "100位":{'name':s[4]["nickname"], 'fan_num':s[4]["score"], 'dif_60':s[4]["score"], 'dif_24':s[4]["score"]},
                            "1000位":{'name':s[5]["nickname"], 'fan_num':s[5]["score"], 'dif_60':s[5]["score"], 'dif_24':s[5]["score"]},
                            "3000位":{'name':"-", 'fan_num':"0", 'dif_60':"0", 'dif_24':"0"}
                            }                    
    except Exception as e:#matsurihi.me
        try:
            return {"1位":{'fan_num':data[0]["data"][-1]["score"], 'dif_60':culc_diff(data[0]["data"][-1]["score"], data[0]["data"][-3]["score"]), 'dif_24':culc_diff(data[0]["data"][-1]["score"], data[0]["data"][-25]["score"])}, 
                        "2位":{'fan_num':data[1]["data"][-1]["score"], 'dif_60':culc_diff(data[1]["data"][-1]["score"], data[1]["data"][-3]["score"]), 'dif_24':culc_diff(data[1]["data"][-1]["score"], data[1]["data"][-25]["score"])},
                        "3位":{'fan_num':data[2]["data"][-1]["score"], 'dif_60':culc_diff(data[2]["data"][-1]["score"], data[2]["data"][-3]["score"]), 'dif_24':culc_diff(data[2]["data"][-1]["score"], data[2]["data"][-25]["score"])},
                        "10位":{'fan_num':data[3]["data"][-1]["score"], 'dif_60':culc_diff(data[3]["data"][-1]["score"], data[3]["data"][-3]["score"]), 'dif_24':culc_diff(data[3]["data"][-1]["score"], data[3]["data"][-25]["score"])},
                        "100位":{'fan_num':data[4]["data"][-1]["score"], 'dif_60':culc_diff(data[4]["data"][-1]["score"], data[4]["data"][-3]["score"]), 'dif_24':culc_diff(data[4]["data"][-1]["score"], data[4]["data"][-25]["score"])},
                        "1000位":{'fan_num':data[5]["data"][-1]["score"], 'dif_60':culc_diff(data[5]["data"][-1]["score"], data[5]["data"][-3]["score"]), 'dif_24':culc_diff(data[5]["data"][-1]["score"], data[5]["data"][-25]["score"])},
                        "3000位":{'fan_num':data[6]["data"][-1]["score"], 'dif_60':culc_diff(data[6]["data"][-1]["score"], data[6]["data"][-3]["score"]), 'dif_24':culc_diff(data[6]["data"][-1]["score"], data[6]["data"][-25]["score"])}
                        }
        except:
            try:#2～23時間目
                return {"1位":{'fan_num':data[0]["data"][-1]["score"], 'dif_60':culc_diff(data[0]["data"][-1]["score"], data[0]["data"][-3]["score"]), 'dif_24':data[0]["data"][-1]["score"]}, 
                            "2位":{'fan_num':data[1]["data"][-1]["score"], 'dif_60':culc_diff(data[1]["data"][-1]["score"], data[1]["data"][-3]["score"]), 'dif_24':data[1]["data"][-1]["score"]},
                            "3位":{'fan_num':data[2]["data"][-1]["score"], 'dif_60':culc_diff(data[2]["data"][-1]["score"], data[2]["data"][-3]["score"]), 'dif_24':data[2]["data"][-1]["score"]},
                            "10位":{'fan_num':data[3]["data"][-1]["score"], 'dif_60':culc_diff(data[3]["data"][-1]["score"], data[3]["data"][-3]["score"]), 'dif_24':data[3]["data"][-1]["score"]},
                            "100位":{'fan_num':data[4]["data"][-1]["score"], 'dif_60':culc_diff(data[4]["data"][-1]["score"], data[4]["data"][-3]["score"]), 'dif_24':data[4]["data"][-1]["score"]},
                            "1000位":{'fan_num':data[5]["data"][-1]["score"], 'dif_60':culc_diff(data[5]["data"][-1]["score"], data[5]["data"][-3]["score"]), 'dif_24':data[5]["data"][-1]["score"]},
                            "3000位":{'fan_num':data[6]["data"][-1]["score"], 'dif_60':culc_diff(data[6]["data"][-1]["score"], data[6]["data"][-3]["score"]), 'dif_24':data[6]["data"][-1]["score"]}
                            }
            except:#1時間目のみ
                return {"1位":{'fan_num':data[0]["data"][-1]["score"], 'dif_60':data[0]["data"][-1]["score"], 'dif_24':data[0]["data"][-1]["score"]}, 
                            "2位":{'fan_num':data[1]["data"][-1]["score"], 'dif_60':data[1]["data"][-1]["score"], 'dif_24':data[1]["data"][-1]["score"]},
                            "3位":{'fan_num':data[2]["data"][-1]["score"], 'dif_60':data[2]["data"][-1]["score"], 'dif_24':data[2]["data"][-1]["score"]},
                            "10位":{'fan_num':data[3]["data"][-1]["score"], 'dif_60':data[3]["data"][-1]["score"], 'dif_24':data[3]["data"][-1]["score"]},
                            "100位":{'fan_num':data[4]["data"][-1]["score"], 'dif_60':data[4]["data"][-1]["score"], 'dif_24':data[4]["data"][-1]["score"]},
                            "1000位":{'fan_num':data[5]["data"][-1]["score"], 'dif_60':data[5]["data"][-1]["score"], 'dif_24':data[5]["data"][-1]["score"]},
                            "3000位":{'fan_num':data[6]["data"][-1]["score"], 'dif_60':data[6]["data"][-1]["score"], 'dif_24':data[6]["data"][-1]["score"]}
                            }
                

def make_image(now_time, font_color="black"):#画像生成部
    base_image_path = "haikei.jpg"
    base_img = Image.open(base_image_path).copy().convert('RGBA')
    space = Image.open("night.jpg").copy().convert('RGBA')
    # try:
    #     with open('border/' + str(now_time) + '.json', 'r', encoding="utf-8") as f:
    #         border = json.load(f)
        
    #     with open('border/' + str(now_time-100) + '.json', 'r', encoding="utf-8") as f:
    #         border_b24 = json.load(f)
    #     print("Ver.origin")
    # except:
    #     print("Ver.matsurihime")    
    # get fontsize
    text = "3rd Aniversary" 
    font_size = 64
    height = 140
    width = 300
    img = add_text_to_image(base_img, text, font_size, font_color, height, width) # dummy for get text_size

    text = "プロデューサーズカップ" 
    font_size = 64
    height = 240
    width = 200
    img = add_text_to_image(base_img, text, font_size, font_color, height, width) # dummy for get text_size
    
    text = "現在時刻:"
    font_size = 40
    height = 405
    width = 185
    img = add_text_to_image(base_img, text, font_size, font_color, height, width) # dummy for get text_size
    
    text = str(datetime.datetime.now())[:-7]
    font_size = 40
    height = 412
    width = 403
    img = add_text_to_image(base_img, text, font_size, font_color, height, width) # dummy for get text_size
    
    text = "by:@Pcup_borderbot"
    font_size = 13
    height = base_img.height - 15
    width = 0
    img = add_text_to_image(base_img, text, font_size, font_color, height, width) # dummy for get text_size

    past_time = (datetime.datetime.now().day-12)*24+datetime.datetime.now().hour-15
    text = "開始から"+str(past_time)+"時間経過(残り"+str(pcup_whole_time - past_time)+"時間)"
    font_size = 40
    height = 500
    width = 230
    img = add_text_to_image(base_img, text, font_size, font_color, height, width) # dummy for get text_size
    
    past_time = (datetime.datetime.now().day-12)*24+datetime.datetime.now().hour-15
    text = "※13～19日は6時間/日のお休み時間があります。"
    font_size = 15
    height = base_img.height - 30
    width = 796
    img = add_text_to_image(base_img, text, font_size, font_color, height, width) # dummy for get text_size
    
    past_time = (datetime.datetime.now().day-12)*24+datetime.datetime.now().hour-15
    text = "※データ習得時間により差が出るため60分速は参考値です。"
    font_size = 15
    height = base_img.height - 15
    width = 730
    img = add_text_to_image(base_img, text, font_size, font_color, height, width) # dummy for get text_size
    # img.save("test.png")
    # exit(0)
    #kogane_data = get_data()
    mano_data = make_json(1, now_time)
    img_mano = make_rank('mano', mano_data)
    # print(1)
    hiori_data = make_json(2, now_time)
    img_hiori = make_rank('hiori', hiori_data)
    meguru_data = make_json(3, now_time)
    img_meguru = make_rank('meguru', meguru_data)
    # print(2)
    kogane_data = make_json(4, now_time)
    img_kogane = make_rank('kogane', kogane_data)
    mamimi_data = make_json(5, now_time)
    img_mamimi = make_rank('mamimi', mamimi_data)
    sakuya_data = make_json(6, now_time)
    img_sakuya = make_rank('sakuya', sakuya_data)
    yuika_data = make_json(7, now_time)
    img_yuika = make_rank('yuika', yuika_data)
    kiriko_data = make_json(8, now_time)
    img_kiriko = make_rank('kiriko', kiriko_data)
    # print(3)
    kaho_data = make_json(9, now_time)
    img_kaho = make_rank('kaho', kaho_data)
    chiyoko_data = make_json(10, now_time)
    img_chiyoko = make_rank('chiyoko', chiyoko_data)
    juri_data = make_json(11, now_time)
    img_juri = make_rank('juri', juri_data)
    rinze_data = make_json(12, now_time)
    img_rinze = make_rank('rinze', rinze_data)
    natsuha_data = make_json(13, now_time)
    img_natsuha = make_rank('natsuha', natsuha_data)
    # print(4)
    amana_data = make_json(14, now_time)
    img_amana = make_rank('amana', amana_data)
    tenka_data = make_json(15, now_time)
    img_tenka = make_rank('tenka', tenka_data)
    chiyuki_data = make_json(16, now_time)
    img_chiyuki = make_rank('chiyuki', chiyuki_data)
    # print(5)
    asahi_data = make_json(17, now_time)
    img_asahi = make_rank('asahi', asahi_data)
    fuyuko_data = make_json(18, now_time)
    img_fuyuko = make_rank('fuyuko', fuyuko_data)
    mei_data = make_json(19, now_time)
    img_mei = make_rank('mei', mei_data)
    # print(6)
    tooru_data = make_json(20, now_time)
    img_tooru = make_rank('tooru', tooru_data)
    madoka_data = make_json(21, now_time)
    img_madoka = make_rank('madoka', madoka_data)
    koito_data = make_json(22, now_time)
    img_koito = make_rank('koito', koito_data)
    hinana_data = make_json(23, now_time)
    img_hinana = make_rank('hinana', hinana_data)
    # print(7)
    nichika_data = make_json(24, now_time)
    img_nichika = make_rank('nichika', nichika_data)
    mikoto_data = make_json(25, now_time)
    img_mikoto = make_rank('mikoto', mikoto_data)
    # print(8)
    #イルミネ
    dst11 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst12 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    
    #アンティーカ
    dst21 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst22 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst23 = Image.new('RGB', (img_mano.width*2, img_mano.height))

    #放クラ
    dst31 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst32 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst33 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    
    #アルスト
    dst41 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst42 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    
    #ストレイ
    dst51 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst52 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    
    #ノクチル
    dst61 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst62 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst63 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    
    #シーズ
    dst71 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    dst72 = Image.new('RGB', (img_mano.width*2, img_mano.height))
    
    
    dst1 = Image.new('RGB', (img_mano.width*2, img_mano.height*2))
    dst2 = Image.new('RGB', (img_mano.width*2, img_mano.height*3))
    dst3 = Image.new('RGB', (img_mano.width*2, img_mano.height*3))
    dst4 = Image.new('RGB', (img_mano.width*2, img_mano.height*2))
    dst5 = Image.new('RGB', (img_mano.width*2, img_mano.height*2))
    dst6 = Image.new('RGB', (img_mano.width*2, img_mano.height*3))
    dst7 = Image.new('RGB', (img_mano.width*2, img_mano.height*2))
    
    illumine = Image.open('logo/illumine.png').convert('RGBA')
    img_illu = img.copy()
    bg_clear = Image.new("RGBA", img.size, (255, 255, 255, 0))
    bg_clear.paste(illumine, (img.width-236, 0))
    img_illu = Image.alpha_composite(img_illu, bg_clear)

    dst11.paste(img_illu, (0, 0))
    dst11.paste(img_mano, (img_mano.width, 0))
    
    dst12.paste(img_hiori, (0, 0))
    dst12.paste(img_meguru, (img_mano.width, 0))

    lantica = Image.open('logo/lantica.png').convert('RGBA')
    img_lantica = img.copy()
    bg_clear = Image.new("RGBA", img.size, (255, 255, 255, 0))
    bg_clear.paste(lantica, (img.width-304, 0))
    img_lantica = Image.alpha_composite(img_lantica, bg_clear)
    dst21.paste(img_lantica, (0, 0))
    dst21.paste(img_kogane, (img_mano.width, 0))
    
    dst22.paste(img_mamimi, (0, 0))
    dst22.paste(img_sakuya, (img_mano.width, 0))
    
    dst23.paste(img_yuika, (0, 0))
    dst23.paste(img_kiriko, (img_mano.width, 0))
    
    houkura = Image.open('logo/houkura.png').convert('RGBA')
    img_houkura = img.copy()
    bg_clear = Image.new("RGBA", img.size, (255, 255, 255, 0))
    bg_clear.paste(houkura, (img.width-242, 0))
    img_houkura = Image.alpha_composite(img_houkura, bg_clear)
    dst31.paste(img_houkura, (0, 0))
    dst31.paste(img_kaho, (img_mano.width, 0))
    dst32.paste(img_chiyoko, (0, 0))
    dst32.paste(img_juri, (img_mano.width, 0)) 
    dst33.paste(img_rinze, (0, 0))
    dst33.paste(img_natsuha, (img_mano.width, 0)) 

    alsto = Image.open('logo/alsto.png').convert('RGBA')
    img_alsto = img.copy()
    bg_clear = Image.new("RGBA", img.size, (255, 255, 255, 0))
    bg_clear.paste(alsto, (img.width-184, 0))
    img_alsto = Image.alpha_composite(img_alsto, bg_clear)
    dst41.paste(img_alsto, (0, 0))
    dst41.paste(img_amana, (img_mano.width, 0))
    dst42.paste(img_tenka, (0, 0))
    dst42.paste(img_chiyuki, (img_mano.width, 0))
    
    stray = Image.open('logo/stray.png').convert('RGBA')
    img_stray = img.copy()
    bg_clear = Image.new("RGBA", img.size, (255, 255, 255, 0))
    bg_clear.paste(stray, (img.width-381, 0))
    img_stray = Image.alpha_composite(img_stray, bg_clear)
    dst51.paste(img_stray, (0, 0))
    dst51.paste(img_asahi, (img_mano.width, 0))
    dst52.paste(img_fuyuko, (0, 0))
    dst52.paste(img_mei, (img_mano.width, 0))

    noctchill = Image.open('logo/noctchill.png').convert('RGBA')
    img_noctchill = img.copy()
    bg_clear = Image.new("RGBA", img.size, (255, 255, 255, 0))
    bg_clear.paste(noctchill, (img.width-390, 0))
    img_noctchill = Image.alpha_composite(img_noctchill, bg_clear)
    dst61.paste(img_noctchill, (0, 0))
    dst61.paste(img_tooru, (img_mano.width, 0))
    dst62.paste(img_madoka, (0, 0))
    dst62.paste(img_hinana, (img_mano.width, 0))
    dst63.paste(img_koito, (0, 0))
    dst63.paste(space, (img_mano.width, 0))

    shiis = Image.open('logo/shiis.png').convert('RGBA')
    img_shiis = img.copy()
    bg_clear = Image.new("RGBA", img.size, (255, 255, 255, 0))
    bg_clear.paste(shiis, (img.width-198, 0))  
    img_shiis = Image.alpha_composite(img_shiis, bg_clear)
    dst71.paste(img_shiis, (0, 0))
    dst71.paste(img_nichika, (img_mano.width, 0))
    dst72.paste(img_mikoto, (0, 0))
    dst72.paste(space, (img_mano.width, 0))
    
    dst1.paste(dst11, (0, 0))
    dst1.paste(dst12, (0, img_mano.height))   
    
    dst2.paste(dst21, (0, 0))
    dst2.paste(dst22, (0, img_mano.height))
    dst2.paste(dst23, (0, img_mano.height*2))

    dst3.paste(dst31, (0, 0))
    dst3.paste(dst32, (0, img_mano.height))
    dst3.paste(dst33, (0, img_mano.height*2))
    
    dst4.paste(dst41, (0, 0))
    dst4.paste(dst42, (0, img_mano.height))

    dst5.paste(dst51, (0, 0))
    dst5.paste(dst52, (0, img_mano.height))
    
    dst6.paste(dst61, (0, 0))
    dst6.paste(dst62, (0, img_mano.height))
    dst6.paste(dst63, (0, img_mano.height*2))
    
    dst7.paste(dst71, (0, 0))
    dst7.paste(dst72, (0, img_mano.height))


    dst1.save("border1.png")
    dst2.save("border2.png")
    dst3.save("border3.png")
    dst4.save("border4.png")
    dst5.save("border5.png")
    dst6.save("border6.png")
    dst7.save("border7.png")

def make_rank(idol_name, kogane_data, font_color="black"):#順位部分生成部
    base_image_path_2 = "background.jpg"
    base_img_2 = Image.open(base_image_path_2).copy()  
    font_path = "rn3lo-1vsc6.ttf"
    kogane_pic_dir = f"idol_fig/{idol_name}.png"
    kogane_pic = Image.open(kogane_pic_dir).convert("RGBA") .resize((330, 418))
    base_img_2.paste(kogane_pic, (-50, 207), kogane_pic)
    try:
        text = kogane_data['1位']['name'].ljust(10)
        text = "                     名前          ファン数   +60m    +24h"
        font_size = 30
        height = 60
        width = 260
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width)
        
        # get fontsize
        text = "1位"
        font_size = 40
        height = 150
        width = 260
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = kogane_data['1位']['name'].ljust(10)
        font_size = 20
        height = 162
        width = 430
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['1位']['fan_num']).rjust(10)
        font_size = 20
        height = 162
        width = 650
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['1位']['dif_60']).rjust(8)
        font_size = 20
        height = 162
        width = 810
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['1位']['dif_24']).rjust(9)
        font_size = 20
        height = 162
        width = 950
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = "2位"
        font_size = 40
        height = 220
        width = 260
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = kogane_data['2位']['name'].ljust(10)
        font_size = 20
        height = 232
        width = 430
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['2位']['fan_num']).rjust(10)
        font_size = 20
        height = 232
        width = 650
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['2位']['dif_60']).rjust(8)
        font_size = 20
        height = 232
        width = 810
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['2位']['dif_24']).rjust(9)
        font_size = 20
        height = 232
        width = 950
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = "3位"
        font_size = 40
        height = 290
        width = 260
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = kogane_data['3位']['name'].ljust(10)
        font_size = 20
        height = 302
        width = 430
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['3位']['fan_num']).rjust(10)
        font_size = 20
        height = 302
        width = 650
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['3位']['dif_60']).rjust(8)
        font_size = 20
        height = 302
        width = 810
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['3位']['dif_24']).rjust(9)
        font_size = 20
        height = 302
        width = 950
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = "10位"
        font_size = 40
        height = 360
        width = 260
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = kogane_data['10位']['name'].ljust(10)
        font_size = 20
        height = 372
        width = 430
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['10位']['fan_num']).rjust(10)
        font_size = 20
        height = 372
        width = 650
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['10位']['dif_60']).rjust(8)
        font_size = 20
        height = 372
        width = 810
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['10位']['dif_24']).rjust(9)
        font_size = 20
        height = 372
        width = 950
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = "100位"
        font_size = 40
        height = 430
        width = 260
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = kogane_data['100位']['name'].ljust(10)
        font_size = 20
        height = 442
        width = 430
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['100位']['fan_num']).rjust(10)
        font_size = 20
        height = 442
        width = 650
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['100位']['dif_60']).rjust(8)
        font_size = 20
        height = 442
        width = 810
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['100位']['dif_24']).rjust(9)
        font_size = 20
        height = 442
        width = 950
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = "1000位"
        font_size = 40
        height = 500
        width = 260
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = kogane_data['1000位']['name'].ljust(10)
        font_size = 20
        height = 512
        width = 430
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['1000位']['fan_num']).rjust(10)
        font_size = 20
        height = 512
        width = 650
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['1000位']['dif_60']).rjust(8)
        font_size = 20
        height = 512
        width = 810
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['1000位']['dif_24']).rjust(9)
        font_size = 20
        height = 512
        width = 950
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = "3000位"
        font_size = 40
        height = 570
        width = 260
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = kogane_data['3000位']['name'].ljust(10)
        font_size = 20
        height = 582
        width = 430
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['3000位']['fan_num']).rjust(10)
        font_size = 20
        height = 582
        width = 650
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['3000位']['dif_60']).rjust(8)
        font_size = 20
        height = 582
        width = 810
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['3000位']['dif_24']).rjust(9)
        font_size = 20
        height = 582
        width = 950
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
    except:
        text = "                    ファン数          +60m         +24h"
        font_size = 30
        height = 90
        width = 280
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        # get fontsize
        text = "1位"
        font_size = 40
        height = 150
        width = 280
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        

        text = str(kogane_data['1位']['fan_num']).rjust(10)
        font_size = 25
        height = 160
        width = 460
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['1位']['dif_60']).rjust(8)
        font_size = 20
        height = 162
        width = 730
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['1位']['dif_24']).rjust(9)
        font_size = 20
        height = 162
        width = 910
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = "2位"
        font_size = 40
        height = 220
        width = 280
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        

        text = str(kogane_data['2位']['fan_num']).rjust(10)
        font_size = 25
        height = 230
        width = 460
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['2位']['dif_60']).rjust(8)
        font_size = 20
        height = 232
        width = 730
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['2位']['dif_24']).rjust(9)
        font_size = 20
        height = 232
        width = 910
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = "3位"
        font_size = 40
        height = 290
        width = 280
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        

        text = str(kogane_data['3位']['fan_num']).rjust(10)
        font_size = 25
        height = 300
        width = 460
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['3位']['dif_60']).rjust(8)
        font_size = 20
        height = 302
        width = 730
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['3位']['dif_24']).rjust(9)
        font_size = 20
        height = 302
        width = 910
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = "10位"
        font_size = 40
        height = 360
        width = 280
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        

        text = str(kogane_data['10位']['fan_num']).rjust(10)
        font_size = 25
        height = 370
        width = 460
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['10位']['dif_60']).rjust(8)
        font_size = 20
        height = 372
        width = 730
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['10位']['dif_24']).rjust(9)
        font_size = 20
        height = 372
        width = 910
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = "100位"
        font_size = 40
        height = 430
        width = 280
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        

        text = str(kogane_data['100位']['fan_num']).rjust(10)
        font_size = 25
        height = 440
        width = 460
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['100位']['dif_60']).rjust(8)
        font_size = 20
        height = 442
        width = 730
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['100位']['dif_24']).rjust(9)
        font_size = 20
        height = 442
        width = 910
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = "1000位"
        font_size = 40
        height = 500
        width = 280
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        

        text = str(kogane_data['1000位']['fan_num']).rjust(10)
        font_size = 25
        height = 510
        width = 460
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['1000位']['dif_60']).rjust(8)
        font_size = 20
        height = 512
        width = 730
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['1000位']['dif_24']).rjust(9)
        font_size = 20
        height = 512
        width = 910
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
        
        text = "3000位"
        font_size = 40
        height = 570
        width = 280
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size        

        text = str(kogane_data['3000位']['fan_num']).rjust(10)
        font_size = 25
        height = 580
        width = 460
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['3000位']['dif_60']).rjust(8)
        font_size = 20
        height = 582
        width = 730
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size

        text = str(kogane_data['3000位']['dif_24']).rjust(9)
        font_size = 20
        height = 582
        width = 910
        img = add_text_to_image(base_img_2, text, font_size, font_color, height, width) # dummy for get text_size
    
    return img
    
def tweet_with_imgs(tweet, files):#ツイート実行部
    api = twitter_api()
    media_ids = []
    for ii in range(len(files)):
        img = api.media_upload(files[ii])
        media_ids.append(img.media_id_string)

    api.update_status(status=tweet, media_ids=media_ids)

def tweet_picture(nowtime):#メイン
    # make_image(nowtime)
    text = str(nowtime.month) + "/" +  str(nowtime.day) + " " + str(nowtime.hour) + ":00 現在\nPカップ ボーダー\n"
    text += "(これはテストです。画像は前回のものです。 This is test tweet. Pictures are all past result.)"
    text += "\n#Pカップボーダー"
    print(text)
    tweet_with_imgs(text, ["border1.png", "border2.png", "border3.png", "border4.png"])
    tweet_with_imgs(text, ["border5.png", "border6.png", "border7.png"])

def twitter_api():#API叩き部
    consumer_key = 'RKIV0mhtVvOBwwAtIsRFrZJrM'
    consumer_secret = 'XlsCwCn3BUvAs6S5uq3R7AjPG22J5sHMFxeN33GVfmi852iK8H'
    access_token = '1212683781192081408-ZIiROrgSAW3osVxTnfpGJsEn5riwFN'
    access_secret = '7Aiq7ED2svJM1Erq91COHUfhYA3s8rEeh6vTPncrftRuy'
    auth            = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api             = tweepy.API(auth)

    return api

@retry(wait_fixed=10000)
def scraping_json(idol_id, now_time):
    try:
        unix_time = int(now_time.timestamp()*1000)
        u_b60 = unix_time - 60*60*1000
        u_b24 = unix_time - 60*60*24*1000
        rank = f"https://{api_domain}.execute-api.ap-northeast-1.amazonaws.com/dev/v1/{event_id}/getLatestRetrieve/{idol_id}?asOf={unix_time}"
        r = requests.get(rank).json()
        rank_id = r["body"]["id"]
        url = f"https://{api_domain}.execute-api.ap-northeast-1.amazonaws.com/dev/v1/getStandings/{rank_id}/1-3,10,100,1000,3000"
        rr = requests.get(url).json()
        rank_b60 = f"https://{api_domain}.execute-api.ap-northeast-1.amazonaws.com/dev/v1/{event_id}/getLatestRetrieve/{idol_id}?asOf={u_b60}"
        r_b60 = requests.get(rank_b60).json()
        try:
            rank_id_b60 = r_b60["body"]["id"]
            url = f"https://{api_domain}.execute-api.ap-northeast-1.amazonaws.com/dev/v1/getStandings/{rank_id_b60}/1-3,10,100,1000,3000"
            rr_b60 = requests.get(url).json()
        except:
            rr_b60 = {}
        rank_b24 = f"https://{api_domain}.execute-api.ap-northeast-1.amazonaws.com/dev/v1/{event_id}/getLatestRetrieve/{idol_id}?asOf={u_b24}"
        r_b24 = requests.get(rank_b24).json()
        try:
            rank_id_b24 = r_b24["body"]["id"]
            url = f"https://{api_domain}.execute-api.ap-northeast-1.amazonaws.com/dev/v1/getStandings/{rank_id_b24}/1-3,10,100,1000,3000"
            rr_b24 = requests.get(url).json()
            time.sleep(0.5)
            return [rr, rr_b60, rr_b24]
        except:
            time.sleep(0.5)
            return [rr, rr_b60]
    except:
        now = requests.get("https://api.matsurihi.me/sc/v1/events/fanRanking").json()
        now_id = now[0]["id"]
        rank = f"https://api.matsurihi.me/sc/v1/events/fanRanking/{now_id}/rankings/logs/{idol_id}/1,2,3,10,100,1000,3000"
        r = requests.get(rank).json()
        return r

# now = datetime.datetime.now()
# print(scraping_json(1, now))
# make_image(now)
while True:
    now = datetime.datetime.now()
    if((1 <= ((now.day-pcup_start_day)*24+now.hour-pcup_start_hour)<= pcup_whole_time) and now.minute==20):
        tweet_picture(now)
    time.sleep(60)
    
# tweet_picture(datetime.datetime.now())
