__all__ = ['get_field_word']
import sys
import os
from collections import Counter
# import ahocorasick
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
sys.path.append(rootPath)
from voiceAssistant.analysisAlgorithm.ahoCorasick import Ahocorasick


def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]


def get_field_word(words_dir, InputTxt):
    """

    :param words_dir:
    :param input:
    :return: 最大匹配词列表
    """
    result = []
    ah = Ahocorasick()
    for word in words_dir.keys():
        ah.addWord(word)
    ah.make()
    results = ah.search(InputTxt)
    word_score = []
    if len(results) == 0:
        return result
    else:
        for site in results:
            w = InputTxt[site[0]:site[1]+1]
            # print(w)
            word_score = word_score + words_dir[w]
    count_result = Counter(word_score)
    # print(count_result)
    field_key = max(count_result, key=count_result.get)
    result = count_result[field_key]

    if len(get_key(count_result, result)) != 1:
        return count_result.keys()
    return [field_key]


"""
以下使用python中的ahocorasick库（linux中需要安装）
"""


# def get_field_word(words_dir, inputtxt):
#     actree = ahocorasick.Automaton()
#     for index, word in enumerate(words_dir.keys()):
#         actree.add_word(word, (index, word))
#     actree.make_automaton()
#     target_wds = []
#     word_score = []
#     contxt = []
#     for i in actree.iter(inputtxt):
#         wd = i[1][1]  # i的形式为(index,(index,word))
#         print(wd)
#         contxt.append(inputtxt[i[0]+1:])
#         target_wds.append(wd)
#         word_score = word_score + words_dir[wd]
#     count_result = Counter(word_score)
#     print(count_result)
#     field_key = max(count_result, key=count_result.get)
#     result = count_result[field_key]
#
#     if len(get_key(count_result, result)) != 1:
#         return count_result.keys()
#     return [field_key]
