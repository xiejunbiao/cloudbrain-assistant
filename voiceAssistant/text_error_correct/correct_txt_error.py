# -*- encoding=utf-8 -*-
__all__ = ['CorrectTextError']
import requests
from voiceAssistant.setParameter import SetParameter


class CorrectTextError(object):

    def __init__(self):
        # 同义词

        self._synonym_store = {
                '查看': '查询',
                '查一下': '查询',
                '找一下': '查询',
                }
        self._synonym_store1 = {
                              '查看': '查询',
                              '查一下': '查询',
                              '找一下': '查询',
                              '我要查': '查询',
                              '看看': '查询',
                              '我想要投诉': '投诉',
                              '我投诉': '投诉',
                              '我想投诉': '投诉',
                              '我要投诉': '投诉',
                              '帮我投诉': '投诉',
                              '帮忙投诉': '投诉',
                              '帮投诉': '投诉',
                              '我想要报修': '报修',
                              '我报修': '报修',
                              '我想报修': '报修',
                              '我要报修': '报修',
                              '帮我报修': '报修',
                              '帮忙报修': '报修',
                              '帮报修': '报修',
                              '我想要报事': '报修',
                              '我报事': '报修',
                              '我想报事': '报修',
                              '我要报事': '报修',
                              '帮我报事': '报修',
                              '帮忙报事': '报修',
                              '帮报事': '报修',
                              '我想要建议': '投诉',
                              '我建议': '投诉',
                              '我想建议': '投诉',
                              '我要建议': '投诉',
                              '帮我建议': '投诉',
                              '帮忙建议': '投诉',
                              '帮建议': '投诉'
                              }
        self._special_words = ['下水道', '下雨天']
        self._stop_words = []
        # 如果定义特殊符号需要在
        """
        此处的#下水道是一个特殊的词，包括停用词stop_word和特殊词special_word
        为了能不影响意图的判断，使用特殊字符进行替换，如果是报修投诉类业务中
        含有形如下水道的那么使用add_words将其添加进去。其中特殊字符不可重复
        可以使用#、￥、#￥
        """

        self._add_words = {
            '#': '下'
        }
        # 错误词纠正
        self._homophonic_word = {
            '保修': '报修',
            '报销': '报修',
            '午夜': '物业',
            '雾夜黑': '物业费',
            'boos': '报事',
            'boss': '报事',
            '宝石': '报事',
            '报时': '报事',
            '报是': '报事',
            '交费': '缴费',
            '鲍氏': '报事',
            '报市': '报事',
            '宝是': '报事',
            '抱石': '报事',
            '建一': '建议',
            '优惠劵': '优惠券',
        }

        # 特殊表达数据定义
        self._sp = SetParameter()
        self.data = {
            'data_问候语': {'intentionType': self._sp.intent_code_dir['问候语'], 'queryType': 0, 'instParas': '',
                         'tipTxt': self._sp.greet_tiptxt_0, 'conTxt': ''},
            'data_报事报修': {'intentionType': self._sp.intent_code_dir['报事报修'], 'queryType': 0,  'instParas': '',
                          'tipTxt': '', 'conTxt': ''},
            'data_投诉建议': {'intentionType': self._sp.intent_code_dir['投诉建议'], 'queryType': 0, 'instParas': '',
                          'tipTxt': '', 'conTxt': ''},
            'data_商品购买': {'intentionType': self._sp.intent_code_dir['商品搜索'], 'queryType': 0, 'instParas': '',
                          'tipTxt': '', 'conTxt': ''},
            'data_查询订单': {'intentionType': self._sp.intent_code_dir['查询'], 'queryType': self._sp.field_code_dir['商城订单'],
                          'instParas': '', 'tipTxt': '', 'conTxt': ''},
            'data_查询电话': {'intentionType': self._sp.intent_code_dir['查询'], 'queryType': self._sp.field_code_dir['常用电话'],
                          'instParas': '', 'tipTxt': '', 'conTxt': ''},
            'data_查询物业活动': {'intentionType': self._sp.intent_code_dir['查询'], 'queryType': self._sp.field_code_dir['物业活动'],
                            'instParas': '', 'tipTxt': '', 'conTxt': ''},
            'data_查询物业缴费': {'intentionType': self._sp.intent_code_dir['查询'], 'queryType': self._sp.field_code_dir['物业缴费'],
                            'instParas': '', 'tipTxt': '', 'conTxt': ''},
            'data_查询报修报事工单': {'intentionType': self._sp.intent_code_dir['查询'], 'queryType': self._sp.field_code_dir['报修/报事工单'],
                              'instParas': '', 'tipTxt': '', 'conTxt': ''},
            'data_查询投诉建议工单': {'intentionType': self._sp.intent_code_dir['查询'], 'queryType': self._sp.field_code_dir['投诉/建议工单'],
                              'instParas': '', 'tipTxt': '', 'conTxt': ''},
            'data_查询优惠券': {'intentionType': self._sp.intent_code_dir['查询'], 'queryType': self._sp.field_code_dir['优惠券'],
                           'instParas': '', 'tipTxt': '', 'conTxt': ''}
        }
        self.special_expression = {
            '我报修的工单': self.data['data_查询报修报事工单'],
            '报修工单': self.data['data_查询报修报事工单'],
            '报事工单': self.data['data_查询报修报事工单'],
            '我报修过的工单': self.data['data_查询报修报事工单'],
            '我报事的工单': self.data['data_查询报修报事工单'],
            '我的保修单': self.data['data_查询报修报事工单'],
            '我的报修单': self.data['data_查询报修报事工单'],
            '我工单的报修': self.data['data_查询报修报事工单'],
            '我投诉的工单': self.data['data_查询投诉建议工单'],
            '我投诉过的工单': self.data['data_查询投诉建议工单'],
            '投诉工单': self.data['data_查询投诉建议工单'],
            '建议工单': self.data['data_查询投诉建议工单'],
            '我建议过的工单': self.data['data_查询投诉建议工单'],
            '我建议的工单': self.data['data_查询投诉建议工单'],
            '我表扬的工单': self.data['data_查询投诉建议工单'],
            '我表扬过的工单': self.data['data_查询投诉建议工单'],
            '我评价的工单': self.data['data_查询投诉建议工单'],
            '我评价过的工单': self.data['data_查询投诉建议工单'],
            '我说过的工单': self.data['data_查询投诉建议工单'],
            '报修一下,空调坏了': self.data['data_报事报修'],
            '报修一下，空调坏了': self.data['data_报事报修'],
            '空调坏了,报修一下': self.data['data_报事报修'],
            '空调坏了，报修一下': self.data['data_报事报修']
        }
        self.url_correct = "http://10.18.222.105:6603/bigdata-assistant/assistant/assistant-ec?"

    # 同义词替换
    def replace_synonym(self, input_txt) -> str:

        if input_txt in self._synonym_store.keys():
            return self._synonym_store[input_txt]
        else:
            return input_txt

    def replace_special_word(self, inputtxt) -> str:
        """
        在停用词前加上一个空格
        :param inputtxt:
        :return:
        """
        for key_w1 in self._special_words:
            # 为了不影响
            inputtxt = inputtxt.replace(key_w1, " " + key_w1)
        return inputtxt

    def stop_word(self) -> list:
        return self._stop_words

    def special_word(self) -> list:
        return self._special_words

    def add_word(self) -> dict:
        return self._add_words

    #
    def correct_homophonic_text(self, inputtxt):
        for word in self._homophonic_word.keys():
            inputtxt = inputtxt.replace(word, self._homophonic_word[word])
        return inputtxt

    def correct_homophonic_text_require(self, inputtxt):
        qurey_txt = "correct_txt=%s" % inputtxt
        url = self.url_correct + qurey_txt
        r0 = requests.get(url)
        page_dict = r0.json()
        return page_dict['result']

    def process_special_expression(self, **kwargs):

        data = kwargs['data']
        str_1, inputtxt = kwargs['str_1']
        print(str_1, inputtxt)
        # str_1为去除所有标点之后的文本
        # inputtxt为未去除标点的文本
        if str_1 in self.special_expression.keys():
            data = self.special_expression[str_1]

            # 当意图为投诉建议、报事报修或者商品搜索时需要将输入内容返回
            if data['intentionType'] in [self._sp.intent_code_dir['报事报修'],
                                         self._sp.intent_code_dir['投诉建议'],
                                         self._sp.intent_code_dir['商品搜索']]:
                data['conTxt'] = inputtxt
            return data, 1
        return data, 0


if __name__ == '__main__':
    cte = CorrectTextError()
    result = cte.correct_homophonic_text_require('报销雾夜黑')
    print(result)
