import re

def transform_func(text): # replaces all "ة" into "ه"
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ه", "ة", text)
    text = re.sub("گ", "ك", text)
    return text
def compare_func(text1,text2):
    text1=transform_func(text1)
    text2=transform_func(text2)
    return text1==text2

print(compare_func('فارس الاحمدي','فأرس الأحمدي'))