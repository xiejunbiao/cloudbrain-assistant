import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
sys.path.append(rootPath)
from voiceAssistant.Text_classification.txt_classification.segmentation_word import main_segmentation
from voiceAssistant.Text_classification.txt_classification.tfidf_feature import main_tfidf
from voiceAssistant.Text_classification.txt_classification.classification_model import trainModel
from voiceAssistant.Text_classification.txt_classification.start_txt_classification import split_data_k


if __name__ == '__main__':
    # original_file_path = r'E:\Document\project\data_\original_data\\'
    path_save = r'E:\Document\project\data_\data_split\\'
    file_path = r'E:\Document\project\data_\data_split\data_k\\'
    k = 6
    # 划分数据集
    # split_data_k(original_file_path, path_save, k)
    # print('划分数据集完成')
    # # 分词
    # main_segmentation(file_path, k)
    # print('分词完成')
    # tf-idf
    main_tfidf(file_path, k)
    # 训练
    print('开始训练')
    train_model_obj = trainModel(file_path, k)
    train_model_obj.train_main('MultinomialNB')
    train_model_obj.train_main('LogisticRegression')
    train_model_obj.train_main('RandomForestClassifier')
    train_model_obj.train_main('SVM')
