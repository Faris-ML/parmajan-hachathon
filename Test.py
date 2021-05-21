import speech_recognition as sr
import pyquran as pq
import arabic_reshaper
import pyarabic
from bidi.algorithm import get_display
import re
import jellyfish as jf


sura = eval(input("enter sura to compare: "))
beggin = eval(input("enter beggining ayah: "))
finish = eval(input("enter finishing ayah: "))

def main(sura, beggin, finish):
    
    text = SpeechToText()

    Compare(text, sura, beggin, finish) # (text, sura number, ayah beggin, ahay end)

def SpeechToText():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Say Something:')
        audio = r.listen(source)
        print ('Done!')
        saveAudio(audio)

    try:
        text = r.recognize_google(audio, language = 'ar-SA')

        printArabic(text) ####
        text2 = transform(text)
        text3 = checkBasmalah(text2)
        return getArabic(text3)
        
    except Exception as e:                  # speech is unintelligible
        print('failed'.format(e))

def saveAudio(audio):
    
    # TODO
    # insert into a database
    # f9o0oly
    with open('audio_file1.wav','wb') as file:
        file.write(audio.get_wav_data())

def printArabic(text):
    
    text2 = transform(text)
    reshaped_text = arabic_reshaper.reshape(text2)   # corrects the Arabic text shape
    bidi_text = get_display(reshaped_text)           # corrects the direction
    print(bidi_text)

def getArabic(text):
    
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

def checkBasmalah(text0):
    
    global sura
    text = text0.split() # from string into list

    if (text[0] == "اعوذ" and text[5] == "بسم"):
        if (sura == 1):
            text2 = removeAooth(text)
            return listToString(text2)
            
        else:
            text2 = removeBasmalah(removeAooth(text))
            return listToString(text2) 
    
    elif (text[0] == "اعوذ"):
        text2 = removeAooth(text)
        return listToString(text2)

    elif (text[0] == "بسم"):
        if (sura == 1):
            return listToString(text)

        else:
            text2 = removeBasmalah(text)
            return listToString(text2)

    else:
        return listToString(text)

def removeAooth(text):

    del text[0:5]
    return text

def removeBasmalah(text):

    del text[0:4]
    return text

def getAyat(sura, start, end):
    
    if (end == 0):
        ayat = sura[(start - 1):]
        return ayat

    else:
        ayat = sura[(start - 1): (end - 1)]
        return ayat

def getSura(suraNumber):

    Q = pq.quran # Quran Object
    return Q.get_sura(suraNumber, with_tashkeel=False, basmalah=False) # returns list

def getLevenshteinRatio(text, text2):

    return round(((len(text2) - jf.levenshtein_distance(text, text2)) / len(text2)) , 2) * 100 

def Compare(text, suraNumber, ayah_start = 1, ayah_end = 0):
    
    print(text)##
    print("-------")###
    text2 = getArabic(transform(listToString(getAyat(getSura(suraNumber), ayah_start , ayah_end))))
    print(text2)
    
    print(getLevenshteinRatio(text, text2))

    getUnsimilarityLocation(text, text2)

def getUnsimilarityLocation(text, text2):
        #TODO
        #compare
        #return indecise of where text2 is missing
    return


main(sura, beggin, finish)