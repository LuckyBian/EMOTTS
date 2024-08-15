""" from https://github.com/keithito/tacotron """
import sys
sys.path.append('/home/weizhenbian/vits_emo')
import re
from text.symbols import symbols
from text import english
from text import chinese
from text.chinese import g2pzh
from text.english import g2pen
#from chinese import g2p
from text.cantonese import cantonese_to_ipa
#_symbol_to_id = {s: i for i, s in enumerate(symbols)}
#_id_to_symbol = {i: s for i, s in enumerate(symbols)}

_curly_re = re.compile(r'(.*?)\{(.+?)\}(.*)')

def add_dollar_signs_to_list(input_list):
    # 初始化结果列表，并在开头添加$
    result = ['$$']
    
    # 遍历输入列表
    for item in input_list:
        # 如果item不是标点符号，添加item和$
        if not re.match(r'[^\w\s]', item):  # 使用正则表达式检查item是否为标点符号
            result.append(item)
            result.append('$')
        else:
            # 如果是标点符号，仅添加item
            result.append(item)
    
    # 检查最后一个元素是否为$，如果不是则添加（处理末尾标点符号的情况）
    if result[-1] != '$$':
        result.append('$$')
        

    
    return result

def add_dollar_signs_to_list2(input_list):
    # 初始化结果列表，并在开头添加$
    result = ['$']
    
    # 遍历输入列表
    for item in input_list:
        # 如果item不是标点符号，添加item和$
        if not re.match(r'[^\w\s]', item):  # 使用正则表达式检查item是否为标点符号
            result.append(item)
            result.append('$')
        else:
            # 如果是标点符号，仅添加item
            result.append(item)
    
    # 检查最后一个元素是否为$，如果不是则添加（处理末尾标点符号的情况）
    if result[-1] != '$':
        result.append('$')
    
    return result


def get_arpabet(word, dictionary):
    word_arpabet = dictionary.lookup(word)
    if word_arpabet is not None:
        return "{" + word_arpabet[0] + "}"
    else:
        return word


def text_to_sequence(text):
    sequence = []
    clean_text = chinese.text_normalize(text)
    text = chinese.g2pzh(clean_text)
    # ['w', 'o3', 'j', 'in1', 't', 'ian1', 'h', 'en3', 'g', 'ao1', 'x', 'ing4', ',', 'AA', 'a5', 'AA', 'a5', 'AA', 'a5']
    text = add_dollar_signs_to_list(text)
    #print(text)
    sequence = [symbols.index(symbol) for symbol in text if symbol in symbols]

    return sequence

def text_to_sequence2(text):
    sequence = []
    clean_text = chinese.text_normalize(text)
    text = chinese.g2pzh(clean_text)
    # ['w', 'o3', 'j', 'in1', 't', 'ian1', 'h', 'en3', 'g', 'ao1', 'x', 'ing4', ',', 'AA', 'a5', 'AA', 'a5', 'AA', 'a5']
    #text = add_dollar_signs_to_list2(text)
    print(text)
    sequence = [symbols.index(symbol) for symbol in text if symbol in symbols]

    return sequence

def sequence_to_text(sequence):
    '''Converts a sequence of IDs back to a string'''
    result = []
    for symbol_id in sequence:
        if symbol_id in _id_to_symbol:
            s = _id_to_symbol[symbol_id]
            result.append(s)
    return result


def _clean_text(text):
    text = chinese.text_normalize(text)
    return text


def _symbols_to_sequence(symbols):
    return [_symbol_to_id[s] for s in symbols if _should_keep_symbol(s)]


def _arpabet_to_sequence(text):
    return _symbols_to_sequence(['@' + s for s in text.split()])


def _should_keep_symbol(s):
    return s in _symbol_to_id and s != '_' and s != '~'
