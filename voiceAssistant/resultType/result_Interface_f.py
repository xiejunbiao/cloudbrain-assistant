import json


def dumps_json(data):
    # return json.dumps(data, indent=4, ensure_ascii=False)
    return json.dumps(data, ensure_ascii=False)


# 返回原始格式
def result_interface1(result):
    """
    :return:
    """
    intentionType = int(result['intentionType'])
    queryType = int(result['queryType'])
    tiptxt = str(result['tipTxt'])
    contxt = str(result['conTxt'])
    instparas = str(result['instParas'])

    data = {'intentionType': intentionType,
            'queryType': queryType,
            'tiptxt': tiptxt,
            'contxt': contxt,
            'instparas': instparas
            }
    return dumps_json(data)


# 返回intentionType和queryType合并的格式
def result_interface2(result):
    """
    :return:
    """
    intentioncode = int(result['intentionType'])*1000 + int(result['queryType'])
    tiptxt = str(result['tipTxt'])
    contxt = str(result['conTxt'])
    instparas = str(result['instParas'])

    data = {'intentioncode': intentioncode,
            'tiptxt': tiptxt,
            'contxt': contxt,
            'instparas': instparas
            }
    return dumps_json(data)


# 返回intentionType和queryType合并且将tipTxt和conTxt合并的格式
def result_interface3(result):
    """

    :return:
    """
    intentioncode = int(result['intentionType'])*1000 + int(result['queryType'])
    response_content = str(result['tipTxt']) + str(result['conTxt']) + str(result['instParas'])
    intention_content = ''
    data = {'intentioncode': intentioncode,
            'response_content': response_content,
            'intention_content': intention_content
            }
    return dumps_json(data)


def result_interface4(result):
    response_content = ''
    intentionType = int(result['intentionType'])
    queryType = int(result['queryType'])
    tiptxt = str(result['tipTxt'])
    contxt = str(result['conTxt'])
    instparas = str(result['instParas'])

    if intentionType == 0:
        intention_code = 110001
        intention_content = '问候语'
        response_content = tiptxt
    elif intentionType == 1:
        # 提交保修工单
        intention_code = 310001
        intention_content = '提交报事报修工单'
        response_content = contxt
    elif intentionType == 2:
        # 提交投诉工单
        intention_code = 320001
        intention_content = '提交投诉建议工单'
        response_content = contxt
    elif intentionType == 4:
        # 商品搜索
        intention_code = 100000
        intention_content = '商品搜索'
        response_content = contxt
    elif intentionType == 3:
        if queryType == 1:
            # 商城订单查询
            intention_code = 100001
            intention_content = '商城订单查询'
        elif queryType == 2:
            # 查看物业活动
            intention_code = 100005
            intention_content = '查看物业活动'
        elif queryType == 3:
            # 常用电话查询
            intention_code = 100003
            intention_content = '电话查询'
        elif queryType == 4:
            # 查询报修报事工单
            intention_code = 310000
            intention_content = '查看报事报修工单'
        elif queryType == 5:
            # 查询投诉建议工单
            intention_code = 320000
            intention_content = '查看投诉建议工单'
        elif queryType == 6:
            # 查询物业缴费
            intention_code = 100004
            intention_content = '查看缴费工单'
        elif queryType == 7:
            # 查询优惠券
            intention_code = 100006
            intention_content = '优惠券查询'
        elif queryType == 8:
            # 查询购物车
            intention_code = 100002
            intention_content = '购物车查询'
        else:
            intention_code = 400000
            intention_content = '查看工单引导语'
            response_content = tiptxt
    else:
        intention_code = 110000
        intention_content = '默认引导语'
        response_content = tiptxt
    data = {
            'intention_code': intention_code,
            'response_content': response_content,
            'intention_content': intention_content
            }
    return dumps_json(data)

# def result_interface4(result):
#     """
#     语音助手编码

#             110000:'默认引导语',-----（您可以对我说：）
#  xz         110001:'默认引导语',-----（您可以对我说：）
#             100000:'商品搜索',
#  xz         100001:'商城订单查询',
#             100002:'购物车查询',
#             100003:'电话查询',
#             100004:'查看缴费工单',##缴费只能查看，不能提交工单
#             100005:'查看物业活动',
#  xz         100006:'优惠券查询',
#             310000:'查看报修工单',
#             310001:'提交报修工单',
#             320000:'查看投诉建议工单',
#             320001:'提交投诉建议工单',
#             400000:'查看工单引导语'------（您可以对我说：我要查询报修工单 投诉工单 缴费工单等"}）
#
#     有以下情况需要返回"response_content"里面的内容：
#     query:我想报修，我家的马桶坏了
#      {"intention_code": 310001, "intention_content": "提交报修工单", "response_content": "我家的马桶坏了"}
#     :param result:
#     :return:
#     """

# 110000: '默认引导语',
# 110001: '默认引导语',问候语
#
# 100000: '商品搜索',
# 100001: '订单查询',   xz
# 100002: '购物车查询',
# 100003: '电话查询',
# 100004: '查看缴费工单',  ##缴费只能查看，不能提交工单
# 100005: '查看物业活动',
# 100006:'优惠券查询',  xz
#
# 200000: '进入店铺',  ##暂时不考虑
# 310000: '查看报事报修工单',
# 310001: '提交报事报修工单',  # 提交报修的时候，要把后面的内容打印出来，并去除第一个标点
# 320000: '查看投诉建议工单',
# 320001: '提交投诉建议工单',

#
# 400000: '查看工单引导语'

