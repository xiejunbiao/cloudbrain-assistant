"""
文本分类
实现读取文本，实现分词，构建词袋，保存分词后的词袋。
提取 tfidf 特征，保存提取的特征
"""
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
sys.path.append(rootPath)
from voiceAssistant.Text_classification.txt_classification.tfidf_feature import tokenizer
import joblib
from sklearn import metrics
import voiceAssistant.Text_classification.txt_classification.func_tools as ft
from voiceAssistant.Text_classification.txt_classification.tfidf_feature import vector_space
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


class TextClassifier:

    def __init__(self, clf_model, data_dir, model_path):
        """
        分类器
        :param clf_model:   分类器算法模型
        :param data_dir:    特征数据存放位置
        :param model_path:  模型保存路径
        """
        self.data_dir = data_dir
        self.model_path = model_path
        # 训练集数据
        self.train_data = os.path.join(data_dir, 'train_tfidf.data')
        #
        self.test_data = os.path.join(data_dir, 'test_tfidf.data')
        self.vocabulary_data = os.path.join(data_dir, 'vocabulary.data')
        self.clf = self._load_clf_model(clf_model)

    def _load_clf_model(self, clf_model):
        if os.path.exists(self.model_path):
            print('loading exists model...')
            return joblib.load(self.model_path)

        else:
            print('training model...')
            train_set = ft.readobj(self.train_data)
            clf = clf_model.fit(train_set.tdm, train_set.label)
            joblib.dump(clf, self.model_path, compress=3)
            return clf

    def _predict(self, tdm):
        """
        :param tdm:     # 特征矩阵
        :return:
        """
        # clf2.score(X, y)
        return self.clf.predict(tdm)

    def _predict_proba(self, tdm):
        """
        :param tdm:     # 特征矩阵
        :return:
        """
        return self.clf.predict_proba(tdm)

    def validation(self):
        """使用测试集进行模型验证"""
        print('starting validation...')
        test_set = ft.readobj(self.test_data)
        predicted1 = self._predict(test_set.tdm)
        actual1 = test_set.label
        actual = []
        predicted = []
        for i1 in actual1:
            actual.append(str(i1).split('\\')[-1])
        for i2 in predicted1:
            predicted.append(str(i2).split('\\')[-1])
        for flabel, file_name, expct_cate in zip(actual, test_set.filenames, predicted):
            if flabel != expct_cate:
                print(flabel, expct_cate)
        #         print(file_name, ": 实际类别:", flabel, " --> 预测类别:", expct_cate)
        print('准确率: {0:.7f}'.format(metrics.precision_score(actual, predicted, average='weighted')))
        print('召回率: {0:0.7f}'.format(metrics.recall_score(actual, predicted, average='weighted')))
        print('f1-score: {0:.7f}'.format(metrics.f1_score(actual, predicted, average='weighted')))

    def predict(self, text_dir=None, text_string=None, encoding='utf-8'):
        """应用模型预测"""
        vocabulary = ft.readobj(self.vocabulary_data)
        if text_dir:
            tfidf_bunch = vector_space(corpus_dir=text_dir, stop_words=None, vocabulary=vocabulary, encoding=encoding, seg=True, tier=1)
            return list(zip(tfidf_bunch.filenames, self._predict(tfidf_bunch.tdm)))
        elif text_string:
            corpus = [' '.join(tokenizer().cut(text_string, cut_all=True))]
            print(corpus)  # 分词后的结果
            vectorizer = TfidfVectorizer(vocabulary=vocabulary)
            tdm = vectorizer.fit_transform(corpus)
            print(tdm)  # 输出类别所占的比重
            return self._predict(tdm), self._predict_proba(tdm)
        else:
            return None


class trainModel(object):
    def __init__(self, path_, k):
        self.k = k
        self.path_ = path_

    def _train_MultinomialNB(self):
        # 多项式贝叶斯
        for i in range(self.k):
            print(i, '----------------------多项式贝叶斯---------------------------')
            data_dir = os.path.join(self.path_, 'data_%s\\' % str(i + 1))
            clf = MultinomialNB(alpha=0.001)
            model_path = data_dir + 'models\\NBclassifier.pkl'
            classifier = TextClassifier(clf, data_dir + '/fearture_space', model_path)
            classifier.validation()

    def _train_RandomForestClassifier(self):
        # 随机森林
        for i in range(self.k):
            print(i, '----------------------随机森林---------------------------')
            data_dir = os.path.join(self.path_, 'data_%s\\' % str(i + 1))
            clf = RandomForestClassifier(bootstrap=True, oob_score=True, criterion='gini')
            model_path = data_dir + 'models\\Radfclassifier.pkl'

            classifier = TextClassifier(clf, data_dir + '/fearture_space', model_path)
            classifier.validation()

    def _train_LogisticRegression(self):
        # Logistic 回归算法
        for i in range(self.k):
            print(i, '----------------------Logistic 回归算法---------------------------')
            data_dir = os.path.join(self.path_, 'data_%s\\' % str(i + 1))
            clf = LogisticRegression(C=1000.0)
            model_path = data_dir + 'models\\LRclassifier.pkl'
            classifier = TextClassifier(clf, data_dir + '/fearture_space', model_path)
            classifier.validation()

    def _train_SVM(self):
        # svm 支持向量机
        for i in range(self.k):
            print(i, '----------------------svm 支持向量机---------------------------')
            data_dir = os.path.join(self.path_, 'data_%s\\' % str(i + 1))
            clf = SVC(C=10.0, probability=True)
            model_path = data_dir + 'models\\SVM.pkl'
            classifier = TextClassifier(clf, data_dir + '/fearture_space', model_path)
            classifier.validation()

    def train_main(self, model):
        if model == 'MultinomialNB':
            self._train_MultinomialNB()
        if model == 'LogisticRegression':
            self._train_LogisticRegression()

        if model == 'RandomForestClassifier':
            self._train_RandomForestClassifier()

        if model == 'SVM':
            self._train_SVM()


class predict_model(object):
    def __init__(self, clf_model, data_path, models_path):
        """
        clf_model:模型
        data_path：tf-idf路径
        models_path：模型路径
        """
        self.clf_model = clf_model
        self.data_path = data_path
        self.models_path = models_path
        self.Classifier = self._get_clf()

    def _get_clf(self):
        if self.clf_model == 'MultinomialNB':
            clf = MultinomialNB(alpha=0.001)
            model_path = self.models_path + 'models/NBclassifier.pkl'
            return TextClassifier(clf, self.data_path + '/fearture_space', model_path)
        if self.clf_model == 'LogisticRegression':
            clf = LogisticRegression(C=1000.0)
            model_path = self.models_path + 'models/LRclassifier.pkl'
            return TextClassifier(clf, self.data_path + '/fearture_space', model_path)
        if self.clf_model == 'RandomForestClassifier':
            clf = RandomForestClassifier(bootstrap=True, oob_score=True, criterion='gini')
            model_path = self.models_path + 'models/Radfclassifier.pkl'
            return TextClassifier(clf, self.data_path + '/fearture_space', model_path)
        if self.clf_model == 'SVM':
            clf = SVC(C=10.0, probability=True)
            model_path = self.models_path + 'models/SVM.pkl'
            return TextClassifier(clf, self.data_path + '/fearture_space', model_path)
        return 0

    def txt_predict(self, txt):
        result, proba = self.Classifier.predict(text_string=txt)
        return str(result[0]).split('\\')[-1], proba[0]

    def dir_predict(self, txt):
        result, proba = self.Classifier.predict(text_string=txt)
        return str(result[0]).split('\\')[-1], proba[0]


if __name__ == '__main__':

    # data_dir = 'E:\\Document\\project\\data_\\data_set\\'

    # 多项式贝叶斯
    for i in range(5):
        data_dir = 'E:\\Document\\project\\data_\\data_set_goods\\data_%s\\' % str(i+1)
        clf = MultinomialNB(alpha=0.001)
        model_path = data_dir + 'models\\NBclassifier.pkl'

        classifier = TextClassifier(clf, data_dir + '/fearture_space', model_path)
        classifier.validation()

    # 随机森林
    for i in range(5):
        data_dir = 'E:\\Document\\project\\data_\\data_set_goods\\data_%s\\' % str(i+1)
        clf = RandomForestClassifier(bootstrap=True, oob_score=True, criterion='gini')
        model_path = data_dir + 'models\\Radfclassifier.pkl'

        classifier = TextClassifier(clf, data_dir + '/fearture_space', model_path)
        classifier.validation()

    # Logistic 回归算法
    for i in range(5):
        data_dir = 'E:\\Document\\project\\data_\\data_set_goods\\data_%s\\' % str(i+1)
        clf = LogisticRegression(C=1000.0)
        model_path = data_dir + 'models\\LRclassifier.pkl'

        classifier = TextClassifier(clf, data_dir + '/fearture_space', model_path)
        classifier.validation()

    #
    # 预测一个文本字符串
    # file_path = 'C:\\Users\\xiejunbiao\\Desktop\\测试用例\\测试用例1_0.txt'
    # file_path = 'E:\\Document\\project\\data_\\original_data\\original_data.txt'
    # f = open(file_path, 'r', encoding='utf-8-sig')
    # data_test = f.readlines()
    # data_tmp = []
    # # data_test = f.readlines()
    # # data_tmp = []
    # for each_data in data_test:
    #     data_tmp.append(each_data.replace('\n', '').replace('，', ''))
    # # for each_data in data_test:
    # #     content = str(each_data).replace("\n", "")  # 删除换行
    # #     content = str(content).replace(" ", "")  # 删除空行、多余的空格
    # #     content = content.split('\t')
    # #     if content[1] == '商品搜索':
    # #
    # #         data_tmp.append(content)
    #
    # n = 0
    # # f1 = open(r'E:\1_0_c.json', 'w', encoding='utf-8')
    # for each in data_tmp:
    #     n += 1
    #     # result_ = get_intention1(ownerCode, areaCode, each)
    #     # result_ = voice_start(ownerCode, areaCode, each)
    #     # classifier = TextClassifier(clf, data_dir + '/fearture_space', model_path)
    #     result_ = classifier.predict(text_string=each)
    #     result = str(result_[0]).split('\\')[-1]
    #     print(n, each, result)
    #     # if result != each[1]:
    #     # print(n, each)
    #     # if
    #     #     print(result_)
    #
    # #     f1.write(str(n) + '、' + each + '\n' + result_ + '\n')
    # # f1.close()
    #
    #
    #

    # 个例测试
    data_dir = 'E:\\Document\\project\\data_\\data_set_goods\\data_%s' % str(0 + 1)

    clf = MultinomialNB(alpha=0.001)
    model_path = data_dir + 'models\\NBclassifier.pkl'

    # clf = LogisticRegression(C=1000.0)
    # model_path = data_dir + 'models\\LRclassifier.pkl'

    # clf = MultinomialNB(alpha=0.001)
    # model_path = data_dir + 'models\\NBclassifier.pkl'
    classifier = TextClassifier(clf, data_dir + '/fearture_space', model_path)
    text_list = ['物业服务态度不好', '我爸电话号码', '购买苹果',
                 '你好你吃饭了吗', '报修', '我要报修', '物业服务不好', '大脑中大约有80%的知识都是通过眼睛获取的',
                 '更是人类感官中最重要的器官', '是人类心灵', '中国两会协商的福利政策']
    type_list = ['不可识别', '商品搜索', '家具报修', '建议与投诉', '查询电话号码', '问候语']
    for text_string in text_list:

        ret = classifier.predict(text_string=text_string)
        print(text_string, str(ret[0][0]).split('\\')[-1])
        print([{key: '{0:.7f}'.format(value)} for key, value in zip(type_list, ret[1][0])])
