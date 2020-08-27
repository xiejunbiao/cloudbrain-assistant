# -*- encoding=utf-8 -*-
__all__ = ['CorrectTextError']
import json


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
        self._stop_words = ['下水道', '下雨天']

        # 如果定义特殊符号需要在
        self._special_words = {
            '报修查询': '查询报修',
            '物业查询': '查询物业',
            '下水道': '#下水道'
        }
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

    # 同义词替换
    def replace_synonym(self, input_txt) -> str:

        if input_txt in self._synonym_store.keys():
            return self._synonym_store[input_txt]
        else:
            return input_txt

    def replace_stopword(self, inputtxt) -> str:
        """
        在停用词前加上一个空格
        :param inputtxt:
        :return:
        """
        for key_w1 in self._stop_words:
            # 为了不影响
            inputtxt = inputtxt.replace(key_w1, " " + key_w1)
        return inputtxt

    def stop_word(self) -> list:
        return self._stop_words

    def special_word(self) -> dict:
        return self._special_words

    def add_word(self) -> dict:
        return self._add_words

    #
    def correct_homophonic_text(self, inputtxt):
        for word in self._homophonic_word.keys():
            inputtxt = inputtxt.replace(word, self._homophonic_word[word])
        return json.dumps({'result': inputtxt}, ensure_ascii=False)


if __name__ == '__main__':
    cte = CorrectTextError()
    result = cte.correct_homophonic_text('报销雾夜黑')
    print(result)
