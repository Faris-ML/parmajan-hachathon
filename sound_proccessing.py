import speech_recognition as sr
import pyquran as pq
import arabic_reshaper
import pyarabic
from bidi.algorithm import get_display
import re
import jellyfish as jf


# sura = eval(input("enter sura to compare: "))
# beggin = eval(input("enter beggining ayah: "))
# finish = eval(input("enter finishing ayah: "))

def process(sura, beggin, finish):
    
    text = SpeechToText(sura)
    
    #text1 = "بسم الله"
    #text2 = "اعوذ بالله من الشيطان الرجيم بسم الله الرحمن الرحيم الم ذلك الكتاب"
    #text3 = "اعوذ بالله من الشيطان الرجيم الم ذلك الكتاب"
    #text4 = "قل هو الله الأحد"

    #text = getArabic(checkBasmalah(sura, transform(text4)))

    print(Compare(text, sura, beggin, finish)) # (text, sura number, ayah beggin, ahay end)
    #return Compare(text, sura, beggin, finish) # (text, sura number, ayah beggin, ahay end)

def SpeechToText(sura):

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Say Something:')
        audio = r.listen(source)
        print ('Done!')
        saveAudio(audio)

    try:
        text = r.recognize_google(audio, language = 'ar-SA')

        #printArabic(text) ####
        text2 = transform(text)
        text3 = checkBasmalah(sura, text2)
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

def checkBasmalah(sura, text0):
    
    text = text0.split() # from string into list
    
    if (text[0] == "اعوذ"):
        text2 = removeAooth(text)
        return checkBasmalah(sura ,listToString(text))

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

# def checkExtra(text, textMaster):

#     if (len(text) > len(textMaster)):
#         return removeExtra(text, len(textMaster))

#     else:
#         return text
    
# def removeExtra(text, length):


def getAyat(sura, start, end):
    
    if (end == 0):
        ayat = sura[(start - 1):]
        return ayat

    else:
        ayat = sura[(start - 1): (end)]
        return ayat

def getSura(suraNumber):

    Q = pq.quran # Quran Object
    return Q.get_sura(suraNumber, with_tashkeel=False, basmalah=False) # returns list

def getLevenshteinRatio(text, text2):

    return round(((len(text2) - jf.levenshtein_distance(text, text2)) / len(text2)) , 2) * 100 

def Compare(text, suraNumber, ayah_start = 1, ayah_end = 0):
    
    #print(text)##
    #print("-------")###
    text2 = getArabic(transform(listToString(getAyat(getSura(suraNumber), ayah_start , ayah_end))))
    #print(text2)
    
    try:
        
        #text = checkExtra(text, text2)

        percent = getLevenshteinRatio(text, text2)
        #print(percent)
        return getReport(percent)

    except Exception as e:                
        
        return ('failed'.format(e))

    #getUnsimilarityLocation(text, text2)

def getReport(percent):
          
    if(90 <= percent and percent <= 100):
        return "A+"

    elif(85 <= percent and percent < 90):
        return "A"

    elif(80 <= percent and percent < 85):
        return "B+"

    elif(75 <= percent and percent < 80):
        return "B"

    elif(70 <= percent and percent < 75):
        return "C+"

    elif(65 <= percent and percent < 70):
        return "C"

    elif(60 <= percent and percent < 65):
        return "D+"

    elif(55 <= percent and percent < 60):
        return "D"

    else:
        return "F"

# def indicesOfSimilarity(text, textMaster):
    
    # text = text.split(" ")
    # #print(text)
    # textMaster = textMaster.split(" ")
    # #print(textMaster)

    # indices = set(textMaster).intersection(text)
    # indices
    # indices
    # indices   
    # indices

    # filter out non-matching using levenshtien
    # score lower than 35% collected index and labeled RED
    # score between 36 - 75% indexed ORANGE
    # score over 75% and longer than 5 letters YELLOW
    # score over 75% and is 5 letter or less GREEN (passed)
    # else is considered passed
    # percentages are susceptable to change


    #indices = set(text) & set(textMaster)

    #indices = "fail"

    # return indices

#process(sura, beggin, finish)