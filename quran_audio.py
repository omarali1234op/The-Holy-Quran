import requests
import json


def choose_reciter(reciter):
    reciter = reciter.lower()
    if reciter == "عبدالباسط":
        return "ar.abdulbasitmurattal"
    elif reciter == "عبدالله بسفر":
        return "ar.abdullahbasfar"
    elif reciter == "عبدالرحمان السديسي":
        return "ar.abdurrahmaansudais"
    elif reciter == "عبدالصمد":
        return "ar.abdulsamad"
    elif reciter == "ابوبكر الشطري":
        return "ar.shaatree"
    elif reciter == "احمد ابن الاعجمي":
        return "ar.ahmedajamy"
    elif reciter == "العفاسي":
        return "ar.alafasy"
    elif reciter == "هاني الرفعي":
        return "ar.hanirifai"
    elif reciter == "حساري":
        return "ar.husary"
    elif reciter == "حساري(مجود)":
        return "ar.husarymujawwad"
    elif reciter == "حديفي":
        return "ar.hudhaify"
    elif reciter == "ابراهيم اخدر":
        return "ar.ibrahimakhbar"
    elif reciter == "ماهر المعقيلي":
        return "ar.mahermuaiqly"
    elif reciter == "منشاوي":
        return "ar.minshawi"
    elif reciter == "منشاوي(مجود)":
        return "ar.minshawimujawwad"
    elif reciter == "محمد ايوب":
        return "ar.muhammadayyoub"
    elif reciter == "محمد جبريل":
        return "ar.muhammadjibreel"
    elif reciter == "saood bin ibraaheem ash-shuraym":
        return "ar.saoodshuraym"
    elif reciter == "ibrahim walk":
        return "en.walk"
    elif reciter == "fooladvand - hedayatfar":
        return "fa.hedayatfarfooladvand"
    elif reciter == "parhizgar":
        return "ar.parhizgar"
    elif reciter == "shamshad ali khan":
        return "ur.khan"
    elif reciter == "chinese":
        return "zh.chinese"
    elif reciter == "youssouf leclerc":
        return "fr.leclerc"
    elif reciter == "ayman sowaid":
        return "ar.aymanswoaid"
    else:
        return "ar.alafasy"
    

def request_audio(surah, ayah, reciter = "Alafasy"):
    reciter = choose_reciter(reciter)
    
    something1 = requests.get(f'https://api.alquran.cloud/ayah/{surah}:{ayah}')
    something1 = something1.json()
    
    ayah_number_in_quran = something1['data']['number']
    
    return f'http://cdn.alquran.cloud/media/audio/ayah/{reciter}/{ayah_number_in_quran}'
    
