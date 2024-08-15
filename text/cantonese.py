import sys
sys.path.append('/home/weizhenbian/vits_emo')
import re
import cn2an
import opencc
import jyutping
from text.symbols import symbols
converter = opencc.OpenCC('t2s')


# 初始化声母和韵母列表
_pad = "_"
punctuation = ['.', '!', '?',',','~','$']  # 标点符号列表
consonants = ['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'ng', 'h', 'gw', 'kw', 'w', 'z', 'c', 's', 'j']
vowels = ['aa', 'aai', 'aau', 'aam', 'aan', 'aang', 'aap', 'aat', 'aak', 'ai', 'au', 'am', 'an', 'ang',
          'ap', 'at', 'ak', 'e', 'ei', 'eng', 'ek', 'oe', 'oeng', 'oek', 'eoi', 'eon', 'eot', 'o', 'oi',
          'ou', 'on', 'ong', 'ot', 'ok', 'i', 'iu', 'im', 'in', 'ing', 'ip', 'it', 'ik', 'yu', 'yun', 'yut',
          'u', 'ui', 'un', 'ung', 'ut', 'uk', 'm', 'ng']

tones = ['1', '2', '3', '4', '5', '6']




def parse_jyutping(jyutping):
    # 匹配声母、韵母和声调或标点符号
    pattern = f"({'|'.join(consonants)})?({'|'.join(vowels)})({tones})|([\.,!?$])"
    matches = re.finditer(pattern, jyutping)
    elements = []
    for m in matches:
        if m.group(4):  # 检查是否是标点符号
            elements.append(m.group(4))
        else:
            consonant = m.group(1) if m.group(1) else m.group(2)  # 如果没有声母，则使用韵母作为声母
            elements.append(consonant)
            elements.append(f"{m.group(2)}{m.group(3)}")
    return elements

# List of (Latin alphabet, ipa) pairs:
_latin_to_ipa = [(re.compile('%s' % x[0]), x[1]) for x in [
    ('A', 'ei˥'),
    ('B', 'biː˥'),
    ('C', 'siː˥'),
    ('D', 'tiː˥'),
    ('E', 'iː˥'),
    ('F', 'e˥fuː˨˩'),
    ('G', 'tsiː˥'),
    ('H', 'ɪk̚˥tsʰyː˨˩'),
    ('I', 'ɐi˥'),
    ('J', 'tsei˥'),
    ('K', 'kʰei˥'),
    ('L', 'e˥llou˨˩'),
    ('M', 'ɛːm˥'),
    ('N', 'ɛːn˥'),
    ('O', 'ou˥'),
    ('P', 'pʰiː˥'),
    ('Q', 'kʰiːu˥'),
    ('R', 'aː˥lou˨˩'),
    ('S', 'ɛː˥siː˨˩'),
    ('T', 'tʰiː˥'),
    ('U', 'juː˥'),
    ('V', 'wiː˥'),
    ('W', 'tʊk̚˥piː˥juː˥'),
    ('X', 'ɪk̚˥siː˨˩'),
    ('Y', 'waːi˥'),
    ('Z', 'iː˨sɛːt̚˥')
]]

custom_jyutping = {
    "咁": "gam2",
    "哋": "dei6",
    "唔": "m4",
    " ": "",
    "笋":"",
    "  ": " ",
    "?":"?",
    ",":",",
    "睇":"tai2",
    "嚟":"lai4",
    "嘅":"ge3",
    "黐":"chi1",
    "!":"!",
    ".":".",
    "乜":"mat1",
    "嘢":"ye5",
    "-":"-",
    "%":"%",
    "咗":"jo2",
    "佢":"keui5",
    "啲":"di1",
    "冇":"mou5",
    "喺":"hai2",
    "拎":"ling1",
    "攞":"lo2",
    "喎":"wo3",
    "諗":"nam2",
    "裏":"leui5",
    "㗎":"ga3",
    "啱":"ngaam1",
    "嗰":"go2",
    "畀":"bei2",
    "咩":"me1",
    "嗌":"aai3",
    "俾":"bei2",
    "瞓":"fan3",
    "咔":"ka1",
    "嚓":"chaat3",
    "嬲":"nau1",
    "劏":"tong1",
    "囝":"jai4",
    "嘞":"laak3",
    "撃":"gik1",
    "誒":"ei6",
    "啫":"je1",
    "樑":"leung4",
    "荺":"wan5",
    "斉":"chai4",
    "豔":"yim6",
    "啖":"daam6",
    "嘦":"jiu3",
    "嘞":"laak3",
    "鎚":"cheui4",
    "慳":"haan1",
    "谂":"nam2",
    "啰":"lo1",
    "锺":"jung1",
    "呃":"aak1",
    "氾":"faan4",
    "麽":"mo1",
    "嗱":"na4",
    "喳":"ja1",
    "掟":"deng3",
    "冚":"ham6",
    "馀":"yu4",
    "煲":"bou1",
    "讬":"tok3",
    "呲":"ji1",
    "啗":"daam6",
    "诶":"ei6",
    "啵":"bo3",
    "偈":"gai2",
    "鎗":"cheung1",
    "揸":"ja1",
    "噌":"jang1",
    "撚":"nan2",
    "搒":"pong3",
    "嗷":"ngou4",
    "悭":"haan1",
    
    "邨":"chyun1",
    "俬":"si1",
    "铸":"jyu3",
    "槿":"gan2",
    "嘥":"saai1",
    "瞢":"mung4",
    "叻":"lek1",
    "嘚":"dak1",
    "咣":"gwong1",
    "怼":"deui6",
    "喐":"yuk1",
    "嗞":"ji1",
    "揿":"gam6",
    "嘭":"baang4",
    "揼":"dam2",
    "銮":"lyun4",
    "噏":"ap1",
    "覚":"gok3",
    "呦":"yau1",
    "餸":"sung3",
    "渖":"sam2",
    "唰":"chaat3",
    "嘣":"bang1",
    "纡":"yu1",
    "濑":"laai6",
    "茨":"chi4",
    "$":"$",
    "𠮶":"ngaa3",
    "㖞":"wa1",
    '梿':'lin4',
    '炆':'man1',
    '㓥':'tong1',
    '冧':'lam3',
    '妁':'jeuk3',
    '濠':'hou4',
    '孖':'ma1',
    '𩠌':'sung3',
    '蹉':'cho1',
    '跎':'to4',
    '汴':'bin6',
    '蚝':'hou4',
    '晟':'sing4',
    '瞅':'chau2',
    '徇':'seun1',
    '娑':'so1',
    '抺':'mui6',
    '咿':'yi1',
    '麾':'fai1',
    '':'',
    '':'',
    '':'',
    '':'',
    '':'',
    '':'',
    '':'',
    '':'',
    '':'',
    '':'',
    '':'',
    '':'',
    '':'',
    '':'',
    '':'',
    '':'',


}


def number_to_cantonese(text):
    return re.sub(r'\d+(?:\.?\d+)?', lambda x: cn2an.an2cn(x.group()), text)


def latin_to_ipa(text):
    for regex, replacement in _latin_to_ipa:
        text = re.sub(regex, replacement, text)
    return text

def classify_characters(input_string):
    # 汉字的Unicode范围
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    # 标点符号的Unicode范围，可以根据需要添加其他符号
    punctuation_pattern = re.compile(r'[，。！？、；：. ,$]')
    classification = []

    for char in input_string:
        if re.match(chinese_pattern, char):
            classification.append(2)  # 汉字
        elif re.match(punctuation_pattern, char):
            classification.append(1)  # 标点
        else:
            classification.append(0)  # 其他字符，可以根据需要调整或处理

    return classification

def cantonese_to_ipa(text):
    text = number_to_cantonese(text.upper())
    text = converter.convert(text)
    #text = re.sub(r'[A-Z]', lambda x: latin_to_ipa(x.group())+' ', text)
    text = re.sub(r'[、；：]', '，', text)
    text = re.sub(r'\s*，\s*', ',', text)
    text = re.sub(r'\s*。\s*', '.', text)
    text = re.sub(r'\s*？\s*', '?', text)
    text = re.sub(r'\s*！\s*', '!', text)
    text = re.sub(r'\s*$', '', text)
    jyutping_list = jyutping.get(text)

    text_words = list(text)

    punctuation = "$，。、；：！？“”‘’（）《》「」『』【】.,;:!?\"'()<>[]{}"

    result_list = []
    no_jyutping_words = []  # 用于收集没有拼音的字

    for word, jp in zip(text_words, jyutping_list):
        if jp is None:
            if word in custom_jyutping:
                result_list.append(custom_jyutping[word])

            elif word in punctuation:
                result_list.append(word)
            else:
                result_list.append("ngaa3")  # 如果是标点符号，保留原文
                no_jyutping_words.append(word)  # 添加到没有拼音的字列表
        else:
            result_list.append(jp)

    # 输出处理后的拼音列表
    # 如果存在没有拼音的字，则输出这些字
    if no_jyutping_words:
        print(text)
        print("处理后的拼音列表：", result_list)
        print("没有拼音的字：", ' '.join(no_jyutping_words))
  
    text = ' '.join(result_list)
    #print("start")
    #print(text)
    par = parse_jyutping(text)
    #print(par)
    #result_indices = [symbols.index(symbol) for symbol in par if symbol in symbols]
    #print(result_indices)
    return par