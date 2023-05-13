import json
import requests

def choose_language(lang):
    lang = lang.lower()
    if lang == 'الالبانية':
        return 'sq.ahmeti'
    elif lang == 'العربية':
        return 'ar'
    elif lang == 'الصينية':
        return 'zh.jian'
    elif lang == 'dutch':
        return 'nl.keyzer'
    elif lang == 'الانجليزية':
        return 'en.sahih'
    elif lang == 'الفارسية':
        return 'fa.ayati'
    elif lang == 'الفرنسية':
        return 'fr.hamidullah'
    elif lang == 'الالمانية':
        return 'de.aburida'
    elif lang == 'حصى':
        return 'ha.gumi'
    elif lang == 'الهندية':
        return 'hi.hindi'
    elif lang == 'الاندونيسية':
        return 'id.indonesian'
    elif lang == 'الايطالية':
        return 'it.piccardo'
    elif lang == 'اليابانية':
        return 'ja.japanese'
    elif lang == 'الكورية':
        return 'ko.korean'
    elif lang == 'الكردية':
        return 'ku.asan'
    elif lang == 'مالاي':
        return 'ms.basmeih'
    elif lang == 'malayalam':
        return 'ml.abdulhameed'
    elif lang == 'النرويجية':
        return 'no.berg'
    elif lang == 'البولندية':
        return 'pl.bielawskiego'
    elif lang == 'الروسية':
        return 'ru.kuliev'
    elif lang == 'الصومالية':
        return 'so.abduh'
    elif lang == 'الاسبانية':
        return 'es.cortes'
    elif lang == 'سواهيلي' or lang == 'كيسواهيلي':
        return 'sw.barwani'
    elif lang == 'السويدية':
        return 'sv.bernstrom'
    elif lang == 'تاجيك':
        return 'tg.ayati'
    elif lang == 'تاميل':
        return 'ta.tamil'
    elif lang == 'التركية':
        return 'tr.ates'
    elif lang == 'الاوردو':
        return 'ur.ahmedali'
    elif lang == 'uyghur':
        return 'ug.saleh'
    else:
        return 'en.asad'
    
def request_ayah(surah, verse, lang = 'en.asad'):
    lang = choose_language(lang)
    whole_surah = requests.get(f"http://api.alquran.cloud/v1/surah/{int(surah)}/editions/{lang}")
    
    whole_surah = whole_surah.json()
    
    verse = whole_surah['data'][0]['ayahs'][int(verse) - 1]['text']
    
    
    return verse
