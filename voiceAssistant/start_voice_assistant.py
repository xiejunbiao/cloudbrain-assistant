#!/usr/bin/env bash
"""
1、2020-04-26:添加异常处理机制
"""

import sys
import os
import traceback

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
sys.path.append(rootPath)
from voiceAssistant.get_intention import GetIntention
from voiceAssistant.resultType.result_Interface_f import result_interface3, result_interface4
voice_gi = GetIntention()
result_100 = {'intentionType': 100,
              'queryType': 0,
              'instParas': '',
              'tipTxt': '小信没有理解您的意思。您可以这样说：'
                        '我要报修+【内容】'
                        '我要投诉+【内容】'
                        '我要查询+【投诉/报修】进展'
                        '我要查询+【商城订单】'
                        '我要查询+【物业常用电话】',
              'conTxt': ''}


def voice_start(areaCode, ownerCode, each):

    try:
        result = voice_gi.get_intention(areaCode, ownerCode, each)
    except Exception as e:
        print('traceback.print_exc():', traceback.print_exc())
        result = result_100

    return result_interface4(result)


if __name__ == '__main__':
    # f = open(r"E:\Document\python\hisense_test\Voice_Assistant_test\语音助手.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\hisense_test\Voice_Assistant_test\测试用例1_0.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\2_.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_1.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_2.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_3.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_4.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_5.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_6.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_101.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\python\project\测试用例\voiceAssistant\3_102.txt", 'r', encoding='utf-8-sig')
    # f = open(r"E:\Document\project\语音助手1-3\test_example.txt", 'r', encoding='utf-8-sig')
    # #
    # data_test = f.readlines()
    # data_tmp = []
    # for each_data in data_test:
    #     data_tmp.append(each_data.replace('\n', '').replace('，', '').split('\t'))

    # inputTxt = '查找物业活动'
    # # inputTxt = ''
    ownerCode = 0
    areaCode = 0
    # print(get_intention1(ownerCode, areaCode, inputTxt))
    # n = 0
    # f1 = open(r'E:\1-3-1.json', 'w', encoding='utf-8')
    # for each, classfiy in data_tmp:
    #     print(n, each, classfiy)
    #     n += 1
    #     # result_ = get_intention1(ownerCode, areaCode, each)
    #     result_ = voice_start(ownerCode, areaCode, each)
    #     print(result_)
    #     # result_ = json.dumps(result_, indent=4, ensure_ascii=False)
    #     # print(result_)
    #     f1.write(str(n) + '、' + each + '\n' + result_ + '\n')
    # f1.close()

    """
    
    """
    # ownerCode = 0
    # areaCode = 0

    #
    # each = '我要报修我家的灯坏了'
    # each = '我要查询报修'
    # each = '查报修'
    # each = '查一下报修'
    # each = '查查报修'
    # each = '搜索报修'
    # each = '我要搜索报修'
    # each = '查找报修单'
    # each = '查询报修单'
    # each = '我要查报修单'
    # each = '我报修的'
    # each = '我的物业账单'
    # each = '查询工单'
    # each = '投诉下下水道坏了'
    # each = '投诉下水道电话'
    # each = '查找下水道坏了'
    # each = '查询物业'
    # each = '查询物业'
    # each = '我想要投诉物业服务不好'
    # each = '我报修投诉进程太慢'
    # each = '我要搜一搜苹果'
    # each = '我要投诉下报修进度太慢'
    # each = '我想要搜索一下下水道报修工单'
    # each = '你好查找一下商城订单'
    # each = '你好想要查询一下我的优惠券'
    # each = '你好我想报修我的优惠券'
    # each = '上午好我要买西瓜'
    # each = '上午好,'
    # each = 'dfadfadf'
    # each = '我想购买下雨天用的雨伞'
    # each = '投诉'
    # each = '报修'
    # each = '晚安'
    # each = '午安'
    # each = '早安'
    # each = '上午好你好'
    # each = '上午好'
    each = ['早安',
            '晚安',
            '上午好', '报事报修',
            '投诉建议', '上午好我要买西瓜', '黑水西瓜',
            '我家水管漏水', '随着生活节奏越来越快',
            '眼睛是人类心灵的一扇窗子',
            '随着生活节奏越来越快',
            '电子产品使用越来越多',
            '眼睛的健康不容忽视',
            '我报修的工单',
            '足浴盐',
            '我工单的报修',
            '我奶奶的电话',
            '就餐前，必须洗手苹果',
            '我家的灯坏了',
            '我要表扬咱们物业师傅',
            '沃柑',
            '丑橘',
            '帮我找工单',
            '物业信息',
            '我家马桶坏了',
            '空调坏了',
            '空调',
            '买冰箱',
            '我家空调',
            '我家的空调滋滋的响',
            'aaaaaaaaaaaaaaaaaaaaaaa',
            '空调坏了，帮忙来修一下',
            '空调坏了，报修一下',
            '冰箱维修',
            '我家冰箱坏了'
            ]
    # #
    #
    for i in each:
        print(i)
    # #
        result_ = voice_start(ownerCode, areaCode, i)
        print(result_)

    # """
    # http://192.168.43.110:6603/bigdata-assistant/assistant/intentionparse?inputTxt=%E5%B7%A5%E5%8D%95&ownerCode=0&areaCode=0
    # """
