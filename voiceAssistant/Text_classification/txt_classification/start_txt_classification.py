#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import jieba
import sys
# import imp
# imp.reload(sys)
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import glob
import os
import random
import copy
import shutil
from threading import Thread, Lock
from queue import Queue


# 保存至文件
def savefile(savepath, content):
    with open(savepath, "wb") as fp:
        fp.write(content)


def _readfile(path):
    """
    读取文件
    """
    # 函数名前面带一个_,是标识私有函数
    # 仅仅用于标明而已，不起什么作用，
    # 外面想调用还是可以调用，
    # 只是增强了程序的可读性
    with open(path, "rb") as fp:  # with as句法前面的代码已经多次介绍过，今后不再注释
        content = fp.read()
    return content


def text_transform(file_path):
    of = open(file_path, 'r', encoding='utf-8-sig')

    # print(of.readlines())
    word_list = []
    f = open(r'C:\Users\xiejunbiao\Desktop\\商品搜索\goods_all.txt', 'w', encoding='utf-8')
    for each in of.readlines():
        content = str(each).replace("\n", "")  # 删除换行
        content = str(content).replace(" ", "")  # 删除空行、多余的空格
        txt_list = content.split(',')
        for txt_each in txt_list:
            if txt_each not in word_list and txt_each:
                word_list.append(txt_each+'\t'+'商品搜索')
                f.write(txt_each+'\t'+'商品搜索' + '\n')
    f.close()
    print(len(word_list))


def category_split_all_data(dir_path, file_path_save=None):
    file_path = dir_path + os.listdir(dir_path)[0]
    of = open(file_path, 'r', encoding='utf-8-sig')
    num_dict = {}
    txt_dict = {}
    category_list = []
    path_root = os.path.split(dir_path)[0]
    # path_save = os.path.split(path_root)[0] + '\\data_all'
    path_save = os.path.join(os.path.split(path_root)[0], 'category_split_all_data')
    if file_path_save is not None:
        path_save = os.path.join(file_path_save, 'category_split_all_data')
    print(path_save)
    check_dir_exist(path_save)
    for each in of.readlines():
        content = str(each).replace("\n", "")  # 删除换行
        content = str(content).replace(" ", "")  # 删除空行、多余的空格
        content = content.split('\t')
        path_temp = os.path.join(path_save, content[1])
        if content[1] not in num_dict.keys():
            num_dict[content[1]] = 1
            txt_dict[content[1]] = [content[0]]
        else:
            num_dict[content[1]] += 1
            txt_dict[content[1]].append(content[0])
        check_dir_exist(path_temp)
        save_file_txt(os.path.join(path_temp, '%s_%s.txt' % (content[1], num_dict[content[1]])), content[0])
    return txt_dict


def split_data_k(file_txt_from, file_path_save, k):
    if file_txt_from is None:
        print('请确定数据文件（.txt）路径')
    if k is None:
        print('请确定你要将数据集划分的份数‘K’')
    if file_path_save is None:
        print('请确保数据保存的路径')
    #     category
    # dir_end = os.path.split(file_txt_from)[0]
    data_set_path_save = os.path.join(file_path_save, 'data_k')
    check_dir_exist(data_set_path_save)
    data_all = category_split_all_data(file_txt_from, file_path_save)

    for key_category in data_all.keys():
        print(key_category)
        lenth = int(len(data_all[key_category])/k)
        mod_ = len(data_all[key_category]) % k
        random.shuffle(data_all[key_category])
        temp_list = func(data_all[key_category], lenth, mod_, k)
        for i in range(len(temp_list)):
            num_data = 0
            end_path_save = os.path.join(data_set_path_save, 'data_%s' % (i+1))
            check_dir_exist(end_path_save)
            test_path = os.path.join(end_path_save, 'test')
            check_dir_exist(test_path)
            train_path = os.path.join(end_path_save, 'train')
            check_dir_exist(train_path)
            num_data = save_file(test_path, temp_list[i], key_category, num_data)
            save_file(train_path, and_list(temp_list, i), key_category, num_data)


def save_file(file_path, data_list, category, num_):
    path = os.path.join(file_path, category)
    check_dir_exist(path)
    for i1 in range(len(data_list)):
        save_file_txt(os.path.join(path, '%s_%s.txt' % (category, num_)), data_list[i1])
        num_ += 1
    return num_


def and_list(list1, i):
    temp_list = copy.deepcopy(list1)
    result = []
    del temp_list[i]
    for each_list in temp_list:
        result = result + each_list
    return result


def func(listTemp, lenth, mod_, n):
    list_data = []
    for i in range(n):
        if i < mod_:
            if i == 0:
                list_data.append(listTemp[lenth * i:(lenth * (i+1) + 1)])
            else:
                list_data.append(listTemp[lenth * i+1:(lenth * (i + 1) + 1)])
        else:
            list_data.append(listTemp[lenth * i:lenth * (i+1)])
    return list_data


def check_dir_exist(dir):
    # 坚持目录是否存在，不存在则创建
    if not os.path.exists(dir):
        os.mkdir(dir)
        # print(dir)


def save_file_txt(file_name, content):
    f = open(file_name, 'w', encoding='utf-8')
    f.write(content)
    f.close()


''''' 
if __name__=="__main__": 
简单来说如果其他python文件调用这个文件的函数，或者把这个文件作为模块 
导入到你的工程中时，那么下面的代码将不会被执行，而如果单独在命令行中 
运行这个文件，或者在IDE（如pycharm）中运行这个文件时候，下面的代码才会运行。 
即，这部分代码相当于一个功能测试。 

'''
if __name__ == "__main__":
    # text_transform('E:\\Document\\project\\语音助理1.1\\goods_short.txt')
    # file_path = r'E:\Document\project\data_\data_on\\'
    file_path = r'E:\Document\project\data_\original_data\\'
    category_split_all_data(file_path)
    # path_save = r'E:\Document\project\data_\data_split\\'
    # split_data_k(file_path, path_save, 5)
