from pyrogram import Client, filters
import json
import requests
from quranInfo import *
import quran_finder
from hijri_converter import convert
import html2text
import quran_audio



app = Client("my_bot")

################### SALAH API ########################

def get_prayer_time(city):
    prayer = requests.get(f"http://api.aladhan.com/timingsByAddress?address={city}&method=4&school=0")

    prayer = prayer.json()
    fajr = prayer['data']['timings']['Fajr']
    dhuhr = prayer['data']['timings']['Dhuhr']
    asr = prayer['data']['timings']['Asr']
    maghrib = prayer['data']['timings']['Maghrib']
    isha = prayer['data']['timings']['Isha']
    
    salah_times = f'''\U0001f54b اوقات الصلاة {city.capitalize()} هم:

\U0001f554 Fajr: {fajr}
        
\U0001f550 Dhuhr: {dhuhr}
        
\U0001f55f Asr: {asr}
        
\U0001f556 Maghrib: {maghrib}
        
\U0001f563 Isha: {isha}'''
    return salah_times


##################### QURAN BIT #########################################

def confirm_surah(surah, verse):
    surah = int(surah)
    verse = int(verse)
    if not 0<surah<115:
        return 'There are only 114 Surahs, please try again.'

    else:
        if verse > quranInfo['surah'][surah][1]:
            return 'Invalid ayah'
        else:
            return 'success'


######################## HIJRI CALENDER #################################

def get_current_hijri():
    hijri = convert.Gregorian.today().to_hijri()
    return f'\U0001f5d3\ufe0f {hijri.day} {hijri.month_name()} {hijri.year} {hijri.notation(language="en")}'
    


####################### FORMATTING BIT ###################################

def format_hadith_text(html):
        h = html2text.HTML2Text()
        h.baseurl = "https://sunnah.com/"
        return h.handle(html.replace('`', 'ʿ').replace("</b>", '').replace("<i>", '*').replace("</i>", '*'))
    
    
def format_english_collection_name(collection_name):
    english_hadith_collections = {
        'ahmad': 'Musnad Ahmad ibn Hanbal',
        'bukhari': 'Sahīh al-Bukhārī',
        'muslim': 'Sahīh Muslim',
        'tirmidhi': 'Jamiʿ at-Tirmidhī',
        'abudawud': 'Sunan Abī Dāwūd',
        'nasai': "Sunan an-Nāsaʿī",
        'ibnmajah': 'Sunan Ibn Mājah',
        'malik': 'Muwatta Mālik',
        'riyadussalihin': 'Riyadh as-Salihīn',
        'adab': "Al-Adab al-Mufrad",
        'bulugh': 'Bulugh al-Maram',
        'shamail': "Shamā'il Muhammadiyyah",
        'mishkat': 'Mishkat al-Masabih',
        'qudsi40': 'Al-Arbaʿīn al-Qudsiyyah',
        'nawawi40': 'Al-Arbaʿīn al-Nawawiyyah',
        'hisn': 'Fortress of the Muslim (Hisn al-Muslim)'
    }

    return english_hadith_collections[collection_name]
    
    

####################### HADITH BIT ######################################

def get_hadith(collection, hadith_number):
    hadeeth_list = requests.get(f'https://api.sunnah.com/v1/collections/{collection}/hadiths/{hadith_number}', headers = {"X-API-Key": "sHpT4GWNK46MgRyAQlCmf6u2MJOc1a589Ntvw5Nx"})
    
    hadeeth_list = hadeeth_list.json()
    
    hadeeth = hadeeth_list['hadith'][0]['body']
    
    hadeeth = format_hadith_text(hadeeth)
    
    chapter_name = hadeeth_list['hadith'][0]['chapterTitle']
    
    chapter_name = format_hadith_text(chapter_name)
    
    try:
        grading = hadith_list['hadith'][0]["grades"][0]["grade"]
        #graded_by = hadith_list['hadith'][0]["grades"][0]["graded_by"]
    except:
        grading = ""
    
    combined = f"""**{chapter_name}**

{hadeeth}
__Reference: {format_english_collection_name(collection)} {hadith_number} \U0001f4ab__
"""
    
    return combined


####################### MUSHAF PAGES ###################################

def get_mushaf(surah, ayah):
    try:
        something = requests.get(f'https://api.alquran.cloud/ayah/{surah}:{ayah}')
        something = something.json()
        page = something['data']['page']
        formatted_page = str(page).zfill(3)
        
        return f'https://www.searchtruth.org/quran/images2/large/page-{formatted_page}.jpeg'
    
    except:
        return f'لم اجد الصفحة \U0001f4dc'
    

###################### BOT COMMANDS ######################################


@app.on_message(filters.command(commands='الصلاة', prefixes=['!','/'],case_sensitive=False))
def salah(client, message):
    cities = message.text.lower().split()
    city = cities [1]
    try:
        message.reply_text(text = get_prayer_time(city), quote = True)
        
    except:
        message.reply_text(text = "توقيت الصلاة ل {city} لم اجده")
        

@app.on_message(filters.command(commands='قران', prefixes=['!','/'], case_sensitive = False))
def quran(client, message):
    words = message.text.lower().split()
    try:
        surah, verse = words[1].split(':')
        if confirm_surah(surah, verse) == 'success':
            if len(words) == 2:
                message.reply_text(text = f'__"{quran_finder.request_ayah(surah,verse)}"__\n\n**\u2728 Quran {surah}:{verse}**', quote = True)
            elif len(words) > 2:
                message.reply_text(text = f'__"{quran_finder.request_ayah(surah,verse,words[2])}"__\n\n**\u2728 Quran {surah}:{verse}**', quote = True)
        else:
            message.reply_text(text = confirm_surah(surah, verse), quote = True)
    except:
        message.reply_text(text = """الهيئة الصحيحة:

!قران [السورة:الاية] <اللغة>
                           
مثال:
                           
!قران 1:1 العربية

استعمل !اللغات لجلب قائمة اللغات \U0001f30d""", quote = True)
        


@app.on_message(filters.command(commands='هجري', prefixes=['!','/'], case_sensitive = False))
def hijri_date(client, message):
    message.reply_text(text = get_current_hijri(), quote=True)
            
    
@app.on_message(filters.command(commands='حديث', prefixes=['!', '/'], case_sensitive = False))
def hadith_message(client, message):
    words = message.text.lower().split()
    try:
        collection, hadith_number = words[1], words[2]
        message.reply_text(text = get_hadith(collection, hadith_number) , quote = True)
        
    except:
        message.reply_text(text = '''الهيئة الصحيحة:

!حديث [الكتاب] [رقم الحديث]

مثال:

!حديث bukhari 1

استعمل !كتب لجلب قائمة الكتب \U0001f4d6''', quote = True)
    
@app.on_message(filters.command(commands='مصحف', prefixes=['!', '/'], case_sensitive = False))
def get_mushaf_page(client, message):
    words = message.text.split()
    try:
        surah, ayah = map(int, words[1].split(':'))
        message.reply_text(text = get_mushaf(surah, ayah), quote = True)
    except:
        message.reply_text(text = '''الهيئة الصحيحة:
                           
!مصحف [رقم السورة]:[رقم الاية]

مثال:

!مصحف 2:255''', quote = True)
        
@app.on_message(filters.command(commands='اية', prefixes=['!', '/'], case_sensitive = False))
def get_ayah(client, message):
    words = message.text.lower().split()
    try:
        surah, ayah = map(int, words[1].split(':'))
        message.reply_text(text = f'http://cdn.alquran.cloud/media/image/{surah}/{ayah}', quote = True)
        
    except:
        message.reply_text(text = '''الهيئة الصحيحة:

!اية [رقم السورة]:[رقم الاية]

مثال: 

!اية 2:255''', quote = True)
        
@app.on_message(filters.command(commands='مسموع', prefixes=['!', '/'], case_sensitive = False))
def quran_audio_send(client, message):
    words = message.text.split()
    try:
        surah, ayah = map(int, words[1].split(':'))
        if len(words)>2:
            reciter = ' '.join(words[2:])
            message.reply_text(text = quran_audio.request_audio(surah, ayah, reciter), quote = True)
        else:
            message.reply_text(text = quran_audio.request_audio(surah, ayah), quote = True)
    except:
        message.reply_text(text = '''الهيئة الصحيحة:
                           
!مسموع [رقم السورة]:[رقم الاية] [القارئ]

مثال:

!مسموع 2:255 هاني الرفعي

استعمل هذا الامر !reciters لجلب قائمة القراء \U0001f399\ufe0f''', quote = True)
        

@app.on_message(filters.command(commands=['help','start'], prefixes=['!', '/'], case_sensitive = False))
def help_message(client, message):
    message.reply_text(text= '''**المساعد**:
    
\U0001f4cc !قران: استعمل هذا الامر + رقم السورة:رقم الاية + اللغة لجلب الاية المطلوبة بللغة المطلوبة.

\U0001f4cc !مسموع: استعمل هذا الامر + رقم السورة:رقم الاية + القارئ لجلب اوديو للاية المطلوبة.
    
\U0001f4cc !حديث: استعمل هذا الامر + اسم الكتاب رقم الحديث للحصول على الحديث المطلوب.
    
\U0001f4cc !مصحف: استعمل هذا الامر + رقم السورة :رقم الاية لجلب سورة عن الصفحة التي تحتوي على الاية من المصحف.

\U0001f4cc !اية: استعمل هذا الامر + رقم السورة:رقم الأية لجلب صورة عن الاية المطلوبة.
    
\U0001f4cc !الصلاة: استعمل هذا الامر + اسم المدينة لجلب وقت الصلاة في المدينة.
    
\U0001f4cc !هجري: تستعمل لجلب التاريخ الهجري.

\U0001f4cc !كتب: تستعمل لجلب قائمة الحديث المتوفر.

\U0001f4cc !اللغات: تستعمل لجلب قائمة الترجمة.

\U0001f4cc !القراء: تستعمل لجلب قائمة قراء القرأن''', quote = True)
    
@app.on_message(filters.command(commands='كتب', prefixes=['!', '/'], case_sensitive = False))
def hadith_books_list(client, message):
    message.reply_text(text = '''قائمة كتب الحديث المتوفرة:

البخاري: \u2728 bukhari \u2728

مسلم: \u2728 muslim \u2728

الترمذي: \u2728 tirmidhi \u2728

ابوداوود: \u2728 abudawud \u2728

رياض الصالحين: \u2728 riyadussalihin \u2728

اداب: \u2728 adab \u2728

بلوغ: \u2728 bulugh \u2728

حصن: \u2728 hisn \u2728''', quote = True)
    
@app.on_message(filters.command(commands='اللغات', prefixes=['!', '/'], case_sensitive = False))
def quran_languages(client, message):
    message.reply_text(text = '''قائمة اللغات \U0001f30d:

الالبانية  \U0001f1e6\U0001f1f1
العربية  \U0001f1f8\U0001f1e6
الصينية  \U0001f1e8\U0001f1f3
Dutch \U0001f1e9\U0001f1f0
الانجليزية  \U0001f1ec\U0001f1e7
الفارسية  \U0001f1ee\U0001f1f7
الفرنسية  \U0001f1eb\U0001f1f7
الالمانية  \U0001f1e9\U0001f1ea
حصى  \U0001f1f3\U0001f1ec
الهندية  \U0001f1ee\U0001f1f3
الاندونيسية  \U0001f1ee\U0001f1e9
الايطالية  \U0001f1ee\U0001f1f9
اليابانية  \U0001f1ef\U0001f1f5
الكورية  \U0001f1f0\U0001f1f7
الكردية  \U0001f1ee\U0001f1f7
مالاي \U0001f1ee\U0001f1e9
Malayalam  \U0001f1ee\U0001f1f3
النرويجية  \U0001f1f3\U0001f1f4
البولندية  \U0001f1f5\U0001f1f1
الروسية \U0001f1f7\U0001f1fa
الصومالية \U0001f1f8\U0001f1f4
الاسبانية  \U0001f1ea\U0001f1f8
سواهيلي \U0001f1f9\U0001f1ff
السويدية  \U0001f1f8\U0001f1ea
تاجيك  \U0001f1f9\U0001f1ef
تاميل  \U0001f1ee\U0001f1f3
التركية  \U0001f1f9\U0001f1f7
الاوردو  \U0001f1f5\U0001f1f0
Uyghur  \U0001f1e8\U0001f1f3''', quote = True)
    
@app.on_message(filters.command(commands='القراء', prefixes=['!', '/'], case_sensitive = False))
def quran_reciters(client, message):
    message.reply_text(text = '''قائمة القراء \U0001f399\ufe0f:
                       
عبدالباسط
عبدالله بسفر
عبدرحمان السديسي
عبدالصمد
ابوبكر الشطري
احمد ابن الاعجمي
العفاسي
هاني الرفعي
حساري
حساري(مجود)
حديفي
ابراهيم اخدر
ماهر المعقيلي
منشاوي
منشاوي(مجود)
محمد ايوب
محمد جبريل


ايمن
Ibrahim Walk - __English__
Fooladvand - Hedayatfar - __Farsi__
Shamshad Ali Khan - __Urdu__
Chinese - __Chinese__
Youssouf Leclerc - __French__''', quote = True)


app.run()
