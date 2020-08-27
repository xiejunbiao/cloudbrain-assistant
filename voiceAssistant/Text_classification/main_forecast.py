from voiceAssistant.Text_classification.txt_classification.classification_model import predict_model
import json
data_dir = r'E:\Document\project\data_\data_split\data_k\\data_1\\'
model_path = r'E:\Document\project\data_\data_split\data_k\\data_1\\'


def txt_forecast(classifier, input_txt, data):
    result, proba = classifier.txt_predict(input_txt)
    if max(proba) > 0.9:
        return result
    else:
        return '不可识别'


if __name__ == '__main__':
    # 向量空间和模型路径
    clf = ['MultinomialNB', 'LogisticRegression', 'RandomForestClassifier']
    classifier = predict_model(clf[0], data_dir, model_path)
    text_list = ['物业服务态度不好', '我爸电话号码', '购买苹果',
                 '你好你吃饭了吗', '报修', '我要报修', '物业服务不好', '大脑中大约有80%的知识都是通过眼睛获取的',
                 '更是人类感官中最重要的器官', '是人类心灵', '中国两会协商的福利政策']
    type_list = ['不可识别', '商品搜索', '家具报修', '建议与投诉', '查询电话号码', '问候语']

    for txt in text_list:
        result = classifier.txt_predict(txt)
        print(str(result[0][0]).split('\\')[-1])
        print(result[1])
        # print([{key: '{0:.7f}'.format(value)} for key, value in zip(type_list, result[1][0])])
