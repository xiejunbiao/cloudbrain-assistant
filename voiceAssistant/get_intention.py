# -*- encoding=utf-8 -*-
__all__ = ['get_intention']
import json
import sys
import os
import traceback
import copy
pathDir = os.path.dirname(__file__)
curPath = os.path.abspath(pathDir)
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
sys.path.append(rootPath)
from voiceAssistant.getWord import get_word_inverted_index
from voiceAssistant.intentGreet.get_intention_word import GetIntentByRe
from voiceAssistant.fieldWord.get_field_word1 import get_field_word
from voiceAssistant.text_error_correct.correct_txt_error import CorrectTextError
from voiceAssistant.setParameter import SetParameter
from voiceAssistant.rePattern.pattern_obj import GetPatternByRe
from voiceAssistant.rePattern.pattern_str import pattern_intent_combine, pattern_intent_divide
from voiceAssistant.Text_classification.txt_classification.classification_model import predict_model


def _get_pattern_obj(str_):
    gibr = GetPatternByRe(str_)
    return gibr.get_compile_ptn()


# 获得四个模式串
pattern_divide = pattern_intent_divide()


class GetIntention(object):
    def __init__(self):
        self._sp = SetParameter()  # 返回参数设置
        self._sr = CorrectTextError()  # 同义词替换等
        self._intent_code_dir = self._sp.intent_code_dir
        self._field_code_dir = self._sp.field_code_dir
        self._except_code_dir = self._sp.except_code_dir
        self._TipTxt_100 = self._sp.except_TipTxt_100
        self._TipTxt_greet_0 = self._sp.greet_tiptxt_0
        self._TipTxt_greet1_0 = self._sp.greet1_tiptxt_0
        self._TipTxt_101 = self._sp.except_TipTxt_101
        self._TipTxt_102 = self._sp.except_TipTxt_102
        self._intend_word_dir, self._field_word_dir, self._intend_word_div = get_word_inverted_index()
        self._get_intent_word = GetIntentByRe()

        # 初始化编译模式串
        self.pattern_great = _get_pattern_obj(pattern_divide['pattern_greet'])
        self.pattern_repair = _get_pattern_obj(pattern_divide['pattern_repair'])
        self.pattern_complaint = _get_pattern_obj(pattern_divide['pattern_complaint'])
        self.pattern_quary = _get_pattern_obj(pattern_divide['pattern_quary'])
        self.pattern_buy = _get_pattern_obj(pattern_divide['pattern_buy'])
        self.pattern_combine = _get_pattern_obj(pattern_divide['pattern_combine'])
        self.punc = self._sp.punc
        self.greet_list = self._sp.greet_time_list
        # self.special_word = self.sr.special_word()
        # self.add_word = self.sr.add_word()

        # sklearn 三种方法进行文本分类
        self.path_fearture_space = os.path.join(pathDir, 'Text_classification', 'data_models/')
        self.path_models = os.path.join(pathDir, 'Text_classification', 'data_models/')
        self.clf_model = self._sp.clf_models
        # 有以下三个模型可供选择
        # RandomForestClassifier   LogisticRegression   MultinomialNB SVM
        self.classifier = predict_model(self.clf_model['LogisticRegression'], self.path_fearture_space, self.path_models)
        self.alpha = self._sp.alpha

    def get_intent_result(self, input_txt, data):

        # data = {
        #     'intentionType': 100,
        #     'queryType': 0,
        #     'instParas': '',
        #     'tipTxt': '',
        #     'conTxt': ''
        #     }

        try:
            repair_pattern = self.pattern_repair.search(input_txt).group()
            if repair_pattern:
                repair_intent = repair_pattern
                contxt = input_txt.replace(repair_intent, '')
                contxt = self.remove_punc_start(contxt)
                data['intentionType'] = 1
                data['conTxt'] = contxt.replace(' ', '')
                return data, 1

            complaint_pattern = self.pattern_complaint.search(input_txt).group()
            if complaint_pattern:
                complaint_intent = complaint_pattern
                contxt = input_txt.replace(complaint_intent, '')
                contxt = self.remove_punc_start(contxt)
                data['intentionType'] = 2
                data['conTxt'] = contxt.replace(' ', '')
                return data, 1

            # 查询意图匹配
            quary_pattern = self.pattern_quary.search(input_txt).group()
            if quary_pattern:
                quary_intent = quary_pattern
                contxt = input_txt.replace(quary_intent, '')
                data, quary_succeed = self.get_querytype(contxt, data)
                return data, 1

            buy_pattern = self.pattern_buy.search(input_txt).group()
            if buy_pattern:
                buy_intent = buy_pattern
                contxt = input_txt.replace(buy_intent, '')
                contxt = self.remove_punc_start(contxt)
                data['intentionType'] = 4
                data['conTxt'] = contxt.replace(' ', '')
                return data, 1
            return data, 0
        except:
            print('traceback.print_exc():', traceback.print_exc())
            return data, 0

    def get_querytype(self, ConTxt, data):
        """
        '查询'意图清晰的情况下,获得查询类型，以及异常处理
        :param ConTxt:
        :return: 返回查询领域类型和提示
        """
        field_word = get_field_word(self._field_word_dir, ConTxt)

        # field_word = search_field_word(self.field_word_dir, ConTxt)
        if len(field_word) == 1:
            data['intentionType'] = 3
            data['queryType'] = self._field_code_dir[field_word[0]]
            return data, 1
        elif len(field_word) >= 1:
            data['intentionType'] = 3
            data['queryType'] = self._except_code_dir['102异常']
            TipTxt = self._TipTxt_102
            for txt in field_word:
                TipTxt = TipTxt + txt + '、'
            TipTxt = TipTxt[:-1]
            data['tipTxt'] = TipTxt
            return data, 1
        else:
            # 商品购买识别
            data, succeed = self.txt_forecast(self.classifier, ConTxt, data)
            if succeed == 1:
                return data, 1
            data['intentionType'] = self._except_code_dir['100异常']
            # data['queryType'] = self._except_code_dir['101异常']
            data['tipTxt'] = self._TipTxt_100
            return data, 1

    def get_no_intent_querytype(self, ConTxt):
        """
        # 意图不清晰的情况下,获得查询类型，以及异常处理
        :param ConTxt:
        :return: 返回查询领域类型和提示
        """
        queryType = 0
        TipTxt = ''
        field_word = get_field_word(self._field_word_dir, ConTxt)
        if len(field_word) == 1:
            queryType = self._field_code_dir[field_word[0]]
            return queryType, TipTxt, 1
        if len(field_word) > 1:
            queryType = self._except_code_dir['102异常']
            TipTxt = self._TipTxt_102
            for txt in field_word:
                TipTxt = TipTxt + txt + '、'
            TipTxt = TipTxt[:-1]  # 去掉最后的顿号
            return queryType, TipTxt, 1

        return queryType, TipTxt, 0

    def get_greet_result(self, greet_txt, data):
        """
        # 根据时间来智能回复
        # if greet_txt in self.greet_list:
        #     tipTxt = greet_txt + self._TipTxt_greet1_0
        #     data['tipTxt'] = tipTxt
        #     data['intentionType'] = self._intent_code_dir['问候语']
        #     return data
        """
        tipTxt = self._TipTxt_greet_0
        data['tipTxt'] = tipTxt
        data['intentionType'] = self._intent_code_dir['问候语']
        return data

    def remove_punc_start(self, input_txt):
        if not input_txt:
            return input_txt
        else:
            if input_txt[0] in self.punc:
                input_txt = input_txt[1:]
        return input_txt

    def remove_punc_end(self, input_txt):

        if not input_txt:
            return input_txt
        else:
            if input_txt[-1] in self.punc:
                input_txt = input_txt[:-1]
        return input_txt

    def remove_punc_all(self, inputtxt):
        txt = copy.deepcopy(inputtxt)
        for each_punc in self.punc:
            txt.replace(each_punc, '')
        return txt, inputtxt

    def txt_forecast(self, classifier, input_txt, data):
        if len(input_txt.strip()) == 0:
            return data, 0
        result, proba = classifier.txt_predict(input_txt)

        # print(result, max(proba))
        # type_list = ['不可识别', '商品搜索', '家具报修', '建议与投诉', '查询电话号码', '问候语']
        # print([{key: '{0:.7f}'.format(value)} for key, value in zip(type_list, proba)])

        # print(max(proba), self.alpha[result])
        if max(proba) > self.alpha[result] and result != '不可识别':
            if result in self._intent_code_dir.keys():  # 判断类别在意图词中是否存在
                data['intentionType'] = self._intent_code_dir[result]
                data['conTxt'] = self.remove_punc_end(input_txt.replace(' ', ''))

            elif result in self._field_code_dir.keys():  # 判断类别在领域词中是否存在
                data['intentionType'] = int(self._intent_code_dir['查询'])
                data['queryType'] = self._field_code_dir[result]
            return data, 1
        else:
            return data, 0

    def get_intention(self, areaCode, ownerCode, inputTxt):
        """

        :param ownerCode:
        :param areaCode:
        :param inputTxt:
        :return:
        """
        data = {
            'intentionType': 100,
            'queryType': 0,
            'instParas': '',
            'tipTxt': '',
            'conTxt': ''}
        # 如果输入为空
        if not inputTxt:
            tipTxt = self._TipTxt_100
            data['tipTxt'] = tipTxt
            return data
        # 输入文本的预处理
        inputTxt = self.remove_punc_end(inputTxt)
        inputTxt = self._sr.correct_homophonic_text(inputTxt)
        inputTxt = self._sr.replace_special_word(inputTxt)

        # 1、获取问候语----------------------------------------------
        great_intent, inputTxt = self._get_intent_word.get_greet_intent(inputTxt)
        # print(1, great_intent, "\t", 2, inputTxt)
        inputTxt = self.remove_punc_start(inputTxt)
        if not inputTxt:
            return self.get_greet_result(great_intent, data)

        # 2、处理特殊表达---------------------------------------------
        data, succeed = self._sr.process_special_expression(str_1=self.remove_punc_all(inputTxt),
                                                            inputtxt=inputTxt,
                                                            data=data)
        if succeed == 1:
            return data
        # 3、获取意图词通过正则表达式------------------------------------
        data, succeed = self.get_intent_result(inputTxt, data)
        # print(1, intend_word, "\t", 2, contxt)
        if succeed == 1:
            return data
        else:

            # 4、无意图的领域词分析---------------------------------------
            query_type, tip_txt, succeed = self.get_no_intent_querytype(inputTxt)
            if succeed == 1:
                data['intentionType'] = int(self._intent_code_dir['查询'])
                data['queryType'] = query_type
                data['tipTxt'] = tip_txt
                return data

            # 5、文本分类算法分析输入意图----------------------------------
            data, succeed = self.txt_forecast(self.classifier, inputTxt, data)
            # print('1、----------------------')
            # print(data)
            # print('-------------------------', succeed)
            if succeed == 1:
                return data

        # 不可识别类做默认引导回复------------------------------------------
        data['intentionType'] = int(self._except_code_dir['100异常'])
        data['queryType'] = 0
        data['tipTxt'] = self._TipTxt_100
        return data


if __name__ == '__main__':
    # f = open(r"E:\Document\python\hisense_test\Voice_Assistant_test\语音助手.txt", 'r', encoding='utf-8-sig')
    f = open(r"E:\Document\python\hisense_test\Voice_Assistant_test\测试用例1_0.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\2_.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_1.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_2.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_3.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_4.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_5.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_6.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_101.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_102.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_102.txt", 'r', encoding='utf-8-sig')

    data_test = f.readlines()
    data_tmp = []
    for each_data in data_test:
        data_tmp.append(each_data.replace('\n', '').replace('，', ''))

    inputTxt = '报修我家的物业不好好干活'
    # inputTxt = ''
    ownerCode = 0
    areaCode = 0
    gi = GetIntention()
    # print(get_intention1(ownerCode, areaCode, inputTxt))
    n = 0
    f = open(r'E:\Document\python\hisense_test\Voice_Assistant_test\result2.json', 'w', encoding='utf-8')
    for each in data_tmp:
        # print(n, each)
        n += 1
        # result_ = get_intention1(ownerCode, areaCode, each)
        result_ = gi.get_intention(ownerCode, areaCode, each)
        print(result_)
        f.write(str(n) + '、' + each + '\n' + json.dumps(result_, indent=4, ensure_ascii=False) + '\n')
    f.close()


