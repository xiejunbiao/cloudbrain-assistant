__all__ = ['get_intent_word']
import sys
import os
import re
import traceback
from collections import Counter
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
sys.path.append(rootPath)
from voiceAssistant.analysisAlgorithm.ahoCorasick import Ahocorasick
from voiceAssistant.rePattern.pattern_str import pattern_intent_combine, pattern_intent_divide
from voiceAssistant.rePattern.pattern_obj import GetPatternByRe
# import ahocorasick


def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]


def get_intent_word(words_dict, InputTxt):
    """

    :param words_dir:
    :param InputTxt:
    :return: 最大匹配词意图词和意图内容
    """
    contxt = []
    ah = Ahocorasick()
    # words = list(intend_word_dir.keys()) + list(field_word_dir.keys())
    # intent_words = intend_word_dir.keys()
    # field_words = field_word_dir.keys()
    for word in words_dict.keys():
        ah.addWord(word)
    ah.make()
    results = ah.search(InputTxt)
    word_score = []
    if len(results) == 0:
        return '', InputTxt
    else:
        for site in results:
            w = InputTxt[site[0]:site[1]+1]
            # print(w)
            contxt.append(InputTxt[site[1]+1:])
            # contxt.append(str(InputTxt).replace(w, ''))
            word_score = word_score + words_dict[w]
    count_result = Counter(word_score)
    # print(count_result)
    result = count_result[max(count_result, key=count_result.get)]
    intent_word = get_key(count_result, result)[0]
    return intent_word, contxt[0]  # 如果意图词有多个 此处仅取最多的或者靠前的一个


pattern_divide = pattern_intent_divide()
gibr = GetPatternByRe(pattern_intent_combine())
compile_ptn = gibr.get_compile_ptn()


def _get_pattern_obj(str_):
    gibr = GetPatternByRe(str_)
    return gibr.get_compile_ptn()


def get_intent(word_dict, inputtxt):
    try:
        intend = compile_ptn.search(inputtxt).group()
        contxt = _get_txt_from_intent(intend, inputtxt)
        if intend in word_dict.keys():
            intend = word_dict[intend][0]
        else:
            intend = ''
    except Exception as e:
        print(e)
        intend = ''
        contxt = inputtxt
    return intend, contxt


def _get_txt_from_intent(txt1, txt2):
    """
    在txt2中获取txt1之后的所有文本
    :param txt1:
    :param txt2:
    :return:
    """
    ptn_str = '(%s)(.*)' % txt1
    ptn = re.compile(ptn_str)
    contxt = ptn.search(txt2).group(2)
    return contxt


class GetIntentByRe(object):
    def __init__(self):
        self.pattern_greet = _get_pattern_obj(pattern_divide['pattern_greet'])
        self.pattern_repair = _get_pattern_obj(pattern_divide['pattern_repair'])
        self.pattern_complaint = _get_pattern_obj(pattern_divide['pattern_complaint'])
        self.pattern_quary = _get_pattern_obj(pattern_divide['pattern_quary'])
        self.pattern_buy = _get_pattern_obj(pattern_divide['pattern_buy'])
        self.pattern_combine = _get_pattern_obj(pattern_divide['pattern_combine'])

    def get_intent(self, input_txt):
        data = {
            'intentionType': 100,
            'queryType': 0,
            'instParas': '',
            'tipTxt': '',
            'conTxt': ''
            }
        intent = ''
        try:
            repair_intent = self.pattern_repair.search(input_txt).group()
            # if repair_intent in word_dict['报修']:
            if repair_intent:
                contxt = input_txt.replace(repair_intent, '')
                data['intentionType'] = 1
                data['conTxt'] = contxt
                return data, 1

            complaint_intent = self.pattern_complaint.search(input_txt).group()
            # if complaint_intent in word_dict['投诉']:
            if complaint_intent:
                contxt = input_txt.replace(repair_intent, '')
                data['intentionType'] = 2
                data['conTxt'] = contxt
                return data, 1

            quary_intent = self.pattern_quary.search(input_txt).group()
            # if quary_intent in word_dict['查询']:
            if quary_intent:
                contxt = input_txt.replace(repair_intent, '')
                queryType, tipTxt = self.get_intent_result.get_querytype(contxt)
                data['intentionType'] = 3
                data['queryType'] = queryType
                data['tipTxt'] = tipTxt
                return data, 1

            buy_intent = self.pattern_buy.search(input_txt).group()
            # if buy_intent in word_dict['购买']:
            if buy_intent:
                contxt = input_txt.replace(repair_intent, '')
                data['intentionType'] = 4
                data['conTxt'] = contxt
                return data, 1
            return intent, input_txt
        except:
            print('traceback.print_exc():', traceback.print_exc())
            return intent, input_txt

    def get_greet_intent(self, txt):
        try:
            result = self.pattern_greet.search(txt).group()
            outtxt = txt.replace(result, '')
            if result:
                return result, outtxt
            else:
                return '', txt
        except:
            print('traceback.print_exc():', traceback.print_exc())
            return '', txt



"""
以下使用python中的ahocorasick库（linux中需要安装）
"""
# def search_intent_word(words_dir, inputtxt):
#     actree = ahocorasick.Automaton()
#     for index, word in enumerate(words_dir.keys()):
#         actree.add_word(word, (index, word))
#     actree.make_automaton()
#     target_wds = []
#     word_score = []
#     contxt = []
#     for i in actree.iter(inputtxt):
#         wd = i[1][1]  # i的形式为(index,(index,word))
#         contxt.append(inputtxt[i[0]+1:])
#         target_wds.append(wd)
#         word_score = word_score + words_dir[wd]
#     count_result = Counter(word_score)
#     # print(count_result)
#     result = count_result[max(count_result, key=count_result.get)]
#     intent_word = get_key(count_result, result)[0]
#     return intent_word, contxt[0]

if __name__ == '__main__':
    # inputtxt = "我要查询我的报修工单"
    # inputtxt = "我购买苹果"
    # inputtxt = "想要买苹果"
    # inputtxt = "我想要苹果"
    # inputtxt = "搜索下苹果"
    # inputtxt = "搜一搜苹果"
    inputtxt = "搜索搜索下水道报修工单"
    print(inputtxt)
    intent_word = get_intent({}, inputtxt)
    print(intent_word)
