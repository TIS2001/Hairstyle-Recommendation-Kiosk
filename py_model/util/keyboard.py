from tkinter import *
import time

choseong_list = [char for char in "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"]
jungseong_list = [char for char in "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"]
jongseong_list = [char for char in " ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"]
ko_dict = {'q':'ㅂ', 'Q':'ㅃ', 'w':'ㅈ', 'W':'ㅉ', 
        'e':'ㄷ', 'E':'ㄸ', 'r':'ㄱ', 'R':'ㄲ', 't':'ㅅ', 
        'T':'ㅆ', 'y':'ㅛ', 'u':'ㅕ', 'i':'ㅑ', 'o':'ㅐ', 
        'p':'ㅔ', 'a':'ㅁ', 's':'ㄴ', 'd':'ㅇ', 'f':'ㄹ', 
        'g':'ㅎ', 'h':'ㅗ', 'j':'ㅓ', 'k':'ㅏ', 'l':'ㅣ', 
        'z':'ㅋ', 'x':'ㅌ', 'c':'ㅊ', 'v':'ㅍ', 'b':'ㅠ', 
        'n':'ㅜ', 'm':'ㅡ', 'O':'ㅒ', 'P':'ㅖ', 'Y':'ㅛ', 
        'U':'ㅕ', 'I':'ㅑ', 'H':'ㅗ', 'J':'ㅓ', 'K':'ㅏ', 
        'L':'ㅣ', 'B':'ㅠ', 'N':'ㅜ', 'M':'ㅡ', 'A':'ㅁ',
        'S':'ㄴ', 'D':'ㅇ', 'F':'ㄹ', 'G':'ㅎ', 'Z':'ㅋ',
        'X':'ㅌ', 'C':'ㅊ', 'V':'ㅍ'}

def en2ko(main_input):
    start_time = time.time()
    # convert en 2 ko
    ko_word = []
    for c in main_input:
        try:
            ko_word.append(ko_dict[c])
        except:
            ko_word.append(c)
    ko_word = list(''.join(ko_word)) + ['\n']

    # seperate by one letter
    words = []
    start = 0
    for i in range(1, len(ko_word)):
        if (i == len(ko_word)-1):
            words.append(ko_word[start:len(ko_word)])
        elif (ko_word[i] in choseong_list and ko_word[i+1] in jungseong_list) or (ko_word[i] not in choseong_list and ko_word[i] not in jungseong_list):
            words.append(ko_word[start:i])
            start = i

    # convert dubble letter
    for word in words:
        if len(word) > 2 and word[0] in choseong_list and word[1] in jungseong_list:
            if word[1] in jungseong_list and word[2] in jungseong_list:
                b = word[1]
                word[1] = make_jungseong_list(word[1:3])
                if (b != word[1]):
                    word.pop(2)
            if len(word) >= 4 and word[2] in jongseong_list and word[3] in jongseong_list:
                b = word[2]
                word[2] = make_jongseong_list(word[2:4])
                if (b != word[2]):
                    word.pop(3)
    #combine each letter
    output_list = []
    for char in words:
        jongseong_index = 0
        if len(char) > 1 and char[0] in choseong_list and char[1] in jungseong_list:
            choseong_index = choseong_list.index(char.pop(0))
            jungseong_index = jungseong_list.index(char.pop(0))
            if len(char) > 0 and char[0] in jongseong_list:
                jongseong_index = jongseong_list.index(char.pop(0))
            character_code = jongseong_index + 0xAC00 + (choseong_index * 21 * 28) + (jungseong_index * 28)
            output_list.append(chr(character_code))
        while char:
            output_list.append(char.pop(0))
    return ''.join(output_list)

def make_jongseong_list(char_list):
    if char_list[0] == 'ㄱ' and char_list[1] == 'ㄱ':
        return "ㄲ"
    if char_list[0] == 'ㄱ' and char_list[1] == 'ㅅ':
        return "ㄳ"
    if char_list[0] == 'ㄴ' and char_list[1] == 'ㅈ':
        return "ㄵ"
    if char_list[0] == 'ㄴ' and char_list[1] == 'ㅎ':
        return "ㄶ"
    if char_list[0] == 'ㄹ' and char_list[1] == 'ㄱ':
        return "ㄺ"
    if char_list[0] == 'ㄹ' and char_list[1] == 'ㅁ':
        return "ㄻ"
    if char_list[0] == 'ㄹ' and char_list[1] == 'ㅂ':
        return "ㄼ"
    if char_list[0] == 'ㄹ' and char_list[1] == 'ㅅ':
        return "ㄽ"
    if char_list[0] == 'ㄹ' and char_list[1] == 'ㅌ':
        return "ㄾ"
    if char_list[0] == 'ㄹ' and char_list[1] == 'ㅍ':
        return "ㄿ"
    if char_list[0] == 'ㄹ' and char_list[1] == 'ㅎ':
        return "ㅀ"
    if char_list[0] == 'ㅂ' and char_list[1] == 'ㅅ':
        return "ㅄ"
    return char_list[0]

def make_jungseong_list(char_list):
    if char_list[0]=='ㅗ' and char_list[1] == 'ㅏ':
        return "ㅘ"
    if char_list[0]=='ㅗ' and char_list[1] == 'ㅐ':
        return "ㅙ"
    if char_list[0]=='ㅗ' and char_list[1] == 'ㅣ':
        return "ㅚ"
    if char_list[0]=='ㅜ' and char_list[1] == 'ㅓ':
        return "ㅝ"
    if char_list[0]=='ㅜ' and char_list[1] == 'ㅔ':
        return "ㅞ"
    if char_list[0]=='ㅜ' and char_list[1] == 'ㅣ':
        return "ㅟ"
    if char_list[0]=='ㅡ' and char_list[1] == 'ㅣ':
        return "ㅢ"
    return char_list[0]
