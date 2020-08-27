# 设置函数
# listTemp 为列表 平分后每份列表的的个数n
from string import punctuation
import re
import jieba
import os, sys
pathDir = os.path.dirname(__file__)
curPath = os.path.abspath(pathDir)
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
sys.path.append(rootPath)
from voiceAssistant.Text_classification.test_2 import B

add_punc = '，。、【】“”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=擅长于的&#@￥'
all_punc = punctuation + add_punc


def func(listTemp, n):
    for i in range(0, len(listTemp), n):
        yield listTemp[i:i + n]


def sentence_cut(x):  # cut words and delete punctuation
    x = re.sub(r'[A-Za-z0-9]|/d+', '', x)  # delet numbers and letters
    testline = jieba.cut(x, cut_all=False)
    testline = ' '.join(testline)
    testline = testline.split(' ')
    te2 = []
    for i in testline:
        te2.append(i)
        if i in all_punc:
            te2.remove(i)
    return te2


class S(object):
    def __init__(self):
        self.r = 1

    def s1(self, taa):

        return self.r

    def s2(self):
        b = B()

        print(b.b1())


if __name__ == '__main__':

    # listTemp = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # # func(listTemp, 3)
    #
    # # 返回的temp为评分后的每份可迭代对象
    #
    # temp = func(listTemp, int(len(listTemp)/2))
    #
    # for i in temp:
    #     print(i)
    # print(len(punctuation), punctuation)
    test = S()
    print(test.s2())
