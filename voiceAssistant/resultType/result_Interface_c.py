import json


def dumps_json(data):
    return json.dumps(data, indent=4, ensure_ascii=False)


class ResultInterface(object):
    def __init__(self, result):
        """
        result = {'intentionType': IntentionType,
                'queryType': queryType,
                'instParas': InstParas,
                'tipTxt': TipTxt,
                'conTxt': ConTxt.replace(' ', '')
                }
        :param result:
        """
        self.intentionType = int(result['intentionType'])
        self.queryType = int(result['queryType'])
        self.tiptxt = str(result['tipTxt'])
        self.contxt = str(result['conTxt'])
        self.instparas = str(result['instParas'])
        self.intention_content = ''
        self.intentioncode = self.intentionType * 1000 + self.queryType
        self.response_content = self.tiptxt + self.contxt + self.instparas

    def result_interface1(self):
        """
        :return:
        """
        data = {'intentionType': self.intentionType,
                'queryType': self.queryType,
                'tiptxt': self.tiptxt,
                'contxt': self.contxt,
                'instparas': self.instparas
                }
        return dumps_json(data)

    def result_interface2(self):
        """
        :return:
        """
        data = {'intentioncode': self.intentioncode,
                'tiptxt': self.tiptxt,
                'contxt': self.contxt,
                'instparas': self.instparas
                }
        return dumps_json(data)

    def result_interface3(self):
        """

        :return:
        """
        data = {'intentioncode': self.intentioncode,
                'response_content': self.response_content,
                'intention_content': self.intention_content
                }
        return dumps_json(data)
