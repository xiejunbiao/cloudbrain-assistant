"""
1、2020-04-28：根据领域词权重进行筛选页面意图
    优化将领域词打分策略嵌入进去增加内部方法
    _get_max_from_dict
2、
"""
__all__ = ['get_field_word']
import sys
import os
# from collections import Counter
# import ahocorasick
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
sys.path.append(rootPath)
from voiceAssistant.analysisAlgorithm.ahoCorasick import Ahocorasick
from voiceAssistant.getWord import get_score_field_intent


def _get_key(dict_, value) -> list:
    return [k for k, v in dict_.items() if v == value]


def _get_max_from_dict(dict_w) -> list:
    # 获取字典中value最大值所对应的键（当存在两个时返回字典中靠前的一个）
    field_key = max(dict_w, key=dict_w.get)
    result = dict_w[field_key]
    # _get_key(dict, result) 获取字典中value=result的所对应的键
    if len(_get_key(dict_w, result)) != 1:
        return dict_w.keys()
    else:
        return [field_key]


def get_field_word(words_dir, InputTxt):
    """

    :param words_dir:
    :param InputTxt:
    :return: 最大匹配词列表
    """

    result = []
    ah = Ahocorasick()
    for word in words_dir.keys():
        ah.addWord(word)
    ah.make()
    results = ah.search(InputTxt)
    word_dir_all = {}
    if len(results) == 0:
        return result

    for site in results:
        w = InputTxt[site[0]:site[1]+1]
        # 在词库中每个领域词对应的页面意图不止一个
        # 例如'工单' 包括投诉/建议工单、报修/报事工单
        # 所以下面使用for 对页面意图进行遍历
        for each_page_intend in words_dir[w]:
            if each_page_intend in word_dir_all.keys():
                # 列表合并
                word_dir_all[each_page_intend] = word_dir_all[each_page_intend] + get_score_field_intent(w)
            else:
                word_dir_all[each_page_intend] = get_score_field_intent(w)
    result_word_list = _get_max_from_dict(word_dir_all)
    return result_word_list


"""
以下使用python中的ahocorasick库（linux中需要安装）
其中没有考虑结果为空的情况
"""
# def search_field_word(words_dir, inputtxt):
#     actree = ahocorasick.Automaton()
#     for index, word in enumerate(words_dir.keys()):
#         actree.add_word(word, (index, word))
#     actree.make_automaton()
#     target_wds = []
#     word_list_all = []
#     contxt = []
#     # 此处应该没有考虑结果为空的情况
#     for i in actree.iter(inputtxt):
#         wd = i[1][1]  # i的形式为(index,(index,word))
#         contxt.append(inputtxt[i[0]+1:])
#         target_wds.append(wd)
#         word_list_all = word_list_all + words_dir[wd]
#     if len(word_list_all) == 1:
#         return word_list_all
#     else:
#         result_word_list = _get_word_max_score(word_list_all)
#         return result_word_list
