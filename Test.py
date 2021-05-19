import speech_recognition as sr
import pyquran as pq
import arabic_reshaper
import pyarabic
from bidi.algorithm import get_display
import re
import jellyfish as jf

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
        saveAudio(audio)

    try:
        text = r.recognize_google(audio, language = 'ar-SA')

        printArabicOfVoice(text)
        return getArabicOfVoice(text)
        
    except Exception as e:                  # speech is unintelligible
        print('failed'.format(e))

def saveAudio(audio):
    
    # TODO
    # insert into a database
    # f9o0oly
    with open('audio_file1.wav','wb') as file:
        file.write(audio.get_wav_data())

def printArabic(text):
    
    text3 = listToString(text)
    text2 = transform(text3)
    reshaped_text = arabic_reshaper.reshape(text2)   # corrects the Arabic text shape
    bidi_text = get_display(reshaped_text)          # corrects the direction
    print(bidi_text)

def getArabic(text):
    
    text3 = listToString(text)
    text2 = transform(text3)
    reshaped_text = arabic_reshaper.reshape(text2)   # corrects the Arabic text shape
    bidi_text = get_display(reshaped_text)          # corrects the direction
    return bidi_text

def printArabicOfVoice(text):
    
    text2 = transform(text)
    reshaped_text = arabic_reshaper.reshape(text)   # corrects the Arabic text shape
    bidi_text = get_display(reshaped_text)          # corrects the direction
    print(bidi_text)

def getArabicOfVoice(text):
    
    text2 = transform(text)
    reshaped_text = arabic_reshaper.reshape(text)   # corrects the Arabic text shape
    bidi_text = get_display(reshaped_text)          # corrects the direction
    return bidi_text

def listToString(s):  # converts from list to string
    str1 = " " 
    
    return str1.join(s)

def transform(text): # replaces all "ة" into "ه"
    
    ta = u'\u0629' #"ة"
    ha = u'\u0647' #"ه"
    alif_maq = u'\u0649' #"ى"
    ya = u'\u064A' #"ي"

    text = re.sub("[إأآا]", "ا", text)
    text = re.sub(ta, ha, text)
    text = re.sub(alif_maq, ya, text)

    return text
          
def getAyat(suraNumber):
    Q = pq.quran # Quran Object
    return Q.get_sura(suraNumber, with_tashkeel=False, basmalah=True)

def Compare(text, suraNumber, ayah_start = 0, ayah_end = 350):
    printArabic(getAyat(suraNumber))
    text2 = getArabic(getAyat(suraNumber))
    print(round(((len(text2) - jf.levenshtein_distance(text, text2)) / len(text2)) , 2) * 100)

main()