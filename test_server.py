import requests
from voiceAssistant.start_voice_assistant import voice_start


def test_server(input_txt):
    # url="http://10.18.222.105:6611/bigdata-search/search/searchForGoods_etl_test?shopCode=-1&areaCode=-1&sortMethod=1&page=1&rows=10&searchKey=洗发水"
    # url = "http://10.18.222.105:6603/cloudbrain-assistant/assistant/intentionparse?inputTxt=%s" % input_txt
    # url1 = "http://10.18.226.58:6603/cloudbrain-assistant/assistant/intentionparse?inputTxt=%s&ownerCode=a" % input_txt
    # 通过url
    # r0 = requests.get(url)
    # page_dict = r0.json()
    #
    # 通过本地
    r0 = voice_start(1, 1, input_txt)
    page_dict = r0

    return page_dict


if __name__ == '__main__':
    f = open(r"C:\Users\xiejunbiao\Desktop\测试用例\测试用例1-3.txt", 'r', encoding='utf-8-sig')
    data_test = f.readlines()
    data_tmp = []
    for each_data in data_test:
        data_tmp.append(each_data.replace('\n', '').replace('，', ''))
    ownerCode = 0
    areaCode = 0
    n = 0
    f = open(r'C:\Users\xiejunbiao\Desktop\测试用例\测试用例1-3-5result.json', 'w', encoding='utf-8')
    for each in data_tmp:
        n += 1
        print(n, each)
        result_ = test_server(each)
        print(result_)
        f.write(str(n) + '、' + each + '\n' + str(result_) + '\n')
    f.close()
