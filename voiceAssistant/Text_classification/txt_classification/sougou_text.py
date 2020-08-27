import os
from xml.dom import minidom
from urllib.parse import urlparse
import glob
from queue import Queue
from threading import Thread, Lock
import time

THREADLOCK = Lock()
# 解析的文本保存路径
corpus_dir = './SogouCS.corpus/'


def file_format(from_file, to_file):
    """对下载的文本进行格式处理"""
    try:
        # 原文本需要用 gb18030 打开
        with open(from_file, 'r', encoding='gb18030') as rf:
            lines = rf.readlines()
        # xml 格式有问题，需添加根节点
        lines.insert(0, '<data>\n')
        lines.append('</data>')
        with open(to_file, 'w', encoding='utf-8') as wf:
            for line in lines:
                line = line.replace('&', '')
                wf.write(line)
    except UnicodeDecodeError:
        print("转码出错", from_file)


def praser_handler(q: Queue):
    # 建立url和类别的映射词典
    dicurl = {'auto.sohu.com': 'qiche', 'it.sohu.com': 'hulianwang', 'health.sohu.com': 'jiankang',
              'sports.sohu.com': 'tiyu', 'travel.sohu.com': 'lvyou', 'learning.sohu.com': 'jiaoyu',
              'cul.sohu.com': 'wenhua', 'mil.news.sohu.com': 'junshi', 'business.sohu.com': 'shangye',
              'house.sohu.com': 'fangchan', 'yule.sohu.com': 'yule', 'women.sohu.com': 'shishang',
              'media.sohu.com': 'chuanmei', 'gongyi.sohu.com': 'gongyi', '2008.sohu.com': 'aoyun'}
    while not q.empty():
        file = q.get()
        with THREADLOCK:
            print("文件" + file)
        file_code = file.split('.')[-2]
        file_format(file, file)  # 进行格式处理
        doc = minidom.parse(file)
        root = doc.documentElement
        claimtext = root.getElementsByTagName("content")
        claimurl = root.getElementsByTagName("url")
        textnum = len(claimurl)
        for index in range(textnum):
            if claimtext[index].firstChild is None:
                continue
            url = urlparse(claimurl[index].firstChild.data)
            if url.hostname in dicurl:
                if not os.path.exists(corpus_dir + dicurl[url.hostname]):
                    os.makedirs(corpus_dir + dicurl[url.hostname])
                fp_in = open(corpus_dir + dicurl[url.hostname] + "/%s_%d.txt" % (file_code, index), "wb")
                fp_in.write(claimtext[index].firstChild.data.encode('utf8'))
                fp_in.close()


def sougou_text_praser(org_dir):
    # 用8个线程处理文本
    q = Queue()
    for file in glob.glob(org_dir + '*.txt'):
        q.put(file)
    for i in range(8):
        Thread(target=praser_handler, args=(q,)).start()
    while not q.empty():
        time.sleep(10)


def files_count(corpus_dir):
    # 统计各类别下的文本数
    folders = os.listdir(corpus_dir)
    total = 0
    for folder in folders:
        if folder.startswith('.DS'):
            continue
        fpath = os.path.join(corpus_dir, folder)
        files = os.listdir(fpath)
        num = len(files)
        total += num
        print(folder, num, sep=':')
    print('Total article:', total)


if __name__ == "__main__":

    org_dir = './SogouCS.reduced/'
    sougou_text_praser(org_dir)
    files_count(corpus_dir)
