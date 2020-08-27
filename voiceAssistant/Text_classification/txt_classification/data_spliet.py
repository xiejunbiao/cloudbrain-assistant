#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将文本分类数据集分为训练集和测试集
@author: CSD
"""
import glob
import os
import random
import shutil
from threading import Thread, Lock
from queue import Queue


THREADLOCK = Lock()


def check_dir_exist(dir):
    # 坚持目录是否存在，不存在则创建
    if not os.path.exists(dir):
        os.mkdir(dir)


def copyfile(q):
    while not q.empty():
        full_folder, train, test, divodd = q.get()
        # glob.glob(full_folder) 查找符合规则的文件
        files = glob.glob(full_folder)
        filenum = len(files)
        testnum = int(filenum * divodd)
        # n = 5
        # divodd = 1 / n
        # num_list = []
        # for i in range(n):
        #     num_list.append(filenum * divodd * (i + 1))

        # 将数据打乱
        testls = random.sample(list(range(filenum)), testnum)

        for i in range(filenum):
            if i in testls:
                shutil.copy(files[i], os.path.join(test, os.path.basename(files[i])))
            else:
                shutil.copy(files[i], os.path.join(train, os.path.basename(files[i])))
        with THREADLOCK:
            print(full_folder)


def data_divi(from_dir, to_dir, divodd=0.2):
    train_folder = os.path.join(to_dir, "train")
    test_folder = os.path.join(to_dir, "test")
    check_dir_exist(train_folder)
    check_dir_exist(test_folder)

    q = Queue()

    for basefolder in os.listdir(from_dir):
        if basefolder.startswith('.DS'):
            continue
        full_folder = os.path.join(from_dir, basefolder)
        print(basefolder)
        train = os.path.join(train_folder, basefolder)
        check_dir_exist(train)
        test = os.path.join(test_folder, basefolder)
        check_dir_exist(test)
        full_folder += "/*.txt"
        q.put((full_folder, train, test, divodd))

    for i in range(8):
        Thread(target=copyfile, args=(q,)).start()


if __name__ == "__main__":
    # corpus_dir = 'E:\\Document\\project\\data_\\data_all'
    # corpus_dir = 'E:\\Document\\project\\data_\\data_all_no'
    # corpus_dir = 'E:\\Document\\project\\data_\\data_set_goods\\data_3\\train'

    corpus_dir = 'E:\\Document\\project\\data_\\data_set_no\\data_3\\train'

    # exp_path = 'E:\\Document\\project\\data_\\data_set_no\\data_1'
    # exp_path = 'E:\\Document\\project\\data_\\data_set_no\\data_2'
    # exp_path = 'E:\\Document\\project\\data_\\data_set_no\\data_3'
    exp_path = 'E:\\Document\\project\\data_\\data_set_no\\data_4'
    # exp_path = 'E:\\Document\\project\\data_\\data_set_no\\data_5'
    # exp_path = 'E:\\Document\\project\\data_\\data_set'
    # exp_path = 'E:\\Document\\project\\data_\\data_set_goods\\data_1'
    # exp_path = 'E:\\Document\\project\\data_\\data_set_goods\\data_2'
    # exp_path = 'E:\\Document\\project\\data_\\data_set_goods\\data_3'
    # exp_path = 'E:\\Document\\project\\data_\\data_set_goods\\data_4'
    # exp_path = 'E:\\Document\\project\\data_\\data_set_goods\\data_5'
    # exp_path = 'E:\\Document\\project\\data_\\data_cross_validation\\data_1'
    # exp_path = 'E:\\Document\\project\\data_\\data_cross_validation\\data_2'
    # exp_path = 'E:\\Document\\project\\data_\\data_cross_validation\\data_3'
    # exp_path = 'E:\\Document\\project\\data_\\data_cross_validation\\data_4'
    # exp_path = 'E:\\Document\\project\\data_\\data_cross_validation\\data_5'
    # 划分比例
    # divodd = 0.2
    # divodd = 0.25
    # divodd = 1/3
    divodd = 0.5
    data_divi(corpus_dir, exp_path, divodd)
