import speech_recognition as sr
import pyquran as pq
import arabic_reshaper
import pyarabic
from bidi.algorithm import get_display
import re
def main():
    text = SpeechToText()
    sura = eval(input("enter sura to compare: "))
    # beggin = eval(input("enter beggin ayah: "))
    # finish = eval(input("enter finish ayah: "))
    Compare(text, sura) # (text, sura number, ayah beggin, ahay end)

def SpeechToText():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Say Something:')
        audio = r.listen(source)
        print ('Done!')

    try:
        text = r.recognize_google(audio, language = 'ar-SA')

        printArabicOfVoice(text)
        return getArabicOfVoice(text)
        
    except Exception as e:                  # speech is unintelligible
        print('failed'.format(e))

def printArabic(text):
    
    text2 = transformTA2HA(text)
    reshaped_text = arabic_reshaper.reshape(text2)   # corrects the Arabic text shape
    bidi_text = get_display(reshaped_text)          # corrects the direction
    print(bidi_text)

def getArabic(text):
    
    text2 = transformTA2HA(text)
    reshaped_text = arabic_reshaper.reshape(text2)   # corrects the Arabic text shape
    bidi_text = get_display(reshaped_text)          # corrects the direction
    return bidi_text

def printArabicOfVoice(text):
    
    reshaped_text = arabic_reshaper.reshape(text)   # corrects the Arabic text shape
    bidi_text = get_display(reshaped_text)          # corrects the direction
    print(bidi_text)

def getArabicOfVoice(text):
    
    reshaped_text = arabic_reshaper.reshape(text)   # corrects the Arabic text shape
    bidi_text = get_display(reshaped_text)          # corrects the direction
    return bidi_text

def listToString(s):  # converts from list to string
    str1 = " " 
    
    return str1.join(s)

def transformTA2HA(text): # replaces all "ة" into "ه"
    text2 = re.sub("[إأآا]", "ا", text)
    text2 = re.sub("ى", "ي", text)
    text2 = re.sub("ؤ", "ء", text)
    text2 = re.sub("ئ", "ء", text)
    text2 = re.sub("ه", "ة", text)
    text2 = re.sub("گ", "ك", text)
    return text2
          
def getAyat(suraNumber):
    Q = pq.quran # Quran Object
    return Q.get_sura(suraNumber, with_tashkeel=False, basmalah=False)

def Compare(text, suraNumber, ayah_start = 0, ayah_end = 350):
    printArabic(getAyat(suraNumber))

main()