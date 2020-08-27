# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:01:02 2019

@author: lijiangman
"""

"""
多线程
增加  @run_on_executor
"""

import traceback
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.web
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
# from analyse.analyzer import chat_with_you
from voiceAssistant.start_voice_assistant import voice_start
from program_correction_text.txt_correct_main import start_fun
from format_importer_1_13_2.update_main import data_update_start
from format_importer_1_13_2.init_main import data_init_start
import logging
logging.basicConfig()


def getLogger():
    logger = logging.getLogger("VOICE_ASSISTANT")
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


class VoiceAssistantHandler(tornado.web.RequestHandler):
    
    executor = ThreadPoolExecutor(20)
    
    def initialize(self, logger):
        self.__logger = logger

    @tornado.gen.coroutine
    def get(self):
        
        """get请求"""
        query = self.get_argument('inputTxt')
        areaCode = self.get_argument('areaCode', default='')
        ownerCode = self.get_argument('ownerCode', default='')
        page_json = yield self.get_query_answer(areaCode, ownerCode, query)
        self.write(page_json)

    @run_on_executor
    def get_query_answer(self, areaCode, ownerCode, query):
        
        """把异常写进日志"""
        try:
            self.__logger.info("query-"+query)  # #用query-作为分隔符
            intention_json = voice_start(areaCode, ownerCode, query)
            self.__logger.info("intention_json-"+intention_json)

        except Exception as e:
            self.__logger.info("error:")
            self.__logger.info(e)
            self.__logger.info("traceback My:")
            self.__logger.info(traceback.format_exc())  # #返回异常信息的字符串，可以用来把信息记录到log里
            intention_json = {}

        return intention_json


class TxtCorrectHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(20)

    def initialize(self, logger):
        self.__logger = logger

    @tornado.gen.coroutine
    def get(self):

        """get请求"""
        query = self.get_argument('inputTxt')
        page_json = yield self.get_query_answer(query)
        self.write(page_json)

    @run_on_executor
    def get_query_answer(self, query):

        """把异常写进日志"""
        try:
            self.__logger.info("query-" + query)  # #用query-作为分隔符
            intention_json = start_fun(query)
            self.__logger.info("intention_json-" + intention_json)

        except Exception as e:
            self.__logger.info("error:")
            self.__logger.info(e)
            self.__logger.info("traceback My:")
            self.__logger.info(traceback.format_exc())  # #返回异常信息的字符串，可以用来把信息记录到log里
            intention_json = {}

        return intention_json


class SynMysqlDataInitHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(20)

    def initialize(self, logger):
        self.__logger = logger

    @tornado.gen.coroutine
    def get(self):

        """get请求"""
        # query = self.get_argument('inputTxt', default='')
        # areaCode = self.get_argument('areaCode', default='')
        # ownerCode = self.get_argument('ownerCode', default='')
        page_json = yield self.get_query_answer()
        self.write(page_json)

    @run_on_executor
    def get_query_answer(self):

        """把异常写进日志"""
        try:
            self.__logger.info("query-" + '无需参数输入')  # #用query-作为分隔符
            intention_json = data_init_start()
            self.__logger.info("exception_json-" + intention_json)
        except Exception as e:
            self.__logger.info("error:")
            self.__logger.info(e)
            self.__logger.info("traceback My:")
            self.__logger.info(traceback.format_exc())  # #返回异常信息的字符串，可以用来把信息记录到log里
            intention_json = {}

        return intention_json


class SynMysqlDataUpdateHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(20)

    def initialize(self, logger):
        self.__logger = logger

    @tornado.gen.coroutine
    def get(self):

        """get请求"""
        # query = self.get_argument('inputTxt')
        page_json = yield self.get_query_answer()
        self.write(page_json)

    @run_on_executor
    def get_query_answer(self):

        """把异常写进日志"""
        try:
            # self.__logger.info("query-" + query)  # #用query-作为分隔符
            intention_json = data_update_start()
            self.__logger.info("intention_json-" + intention_json)

        except Exception as e:
            self.__logger.info("error:")
            self.__logger.info(e)
            self.__logger.info("traceback My:")
            self.__logger.info(traceback.format_exc())  # #返回异常信息的字符串，可以用来把信息记录到log里
            intention_json = {}

        return intention_json


def start():
    port = 6603
    logger = getLogger()
    app = tornado.web.Application(handlers=[
        (r"/cloudbrain-assistant/assistant/intentionparse", VoiceAssistantHandler,  dict(logger=logger)),
        (r"/cloudbrain-assistant/assistant/assistant-ec", TxtCorrectHandler,  dict(logger=logger)),
        # (r"/cloudbrain/sqyn_to_sc/init_data", SynMysqlDataInitHandler,  dict(logger=logger)),
        # (r"/cloudbrain/sqyn_to_sc/update_data", SynMysqlDataUpdateHandler,  dict(logger=logger))
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(port)
    http_server.start(10)
    tornado.ioloop.IOLoop.instance().start()

    """
    ,
        (r"/cloudbrain/sqyn_to_sc/init_data", SynMysqlDataInitHandler,  dict(logger=logger)),
        (r"/cloudbrain/sqyn_to_sc/update_data", SynMysqlDataUpdateHandler,  dict(logger=logger))
    """
  
    """
    请求url:
    http://10.18.222.105:6603/cloudbrain-assistant/assistant/intentionparse?inputTxt=我要报修&ownerCode=a
    http://10.18.222.105:6603/cloudbrain-assistant/assistant/intentionparse?inputTxt=报修
    http://10.18.222.105:6603/bigdata-assistant/assistant/answerOfquery_test1?query=报修
    /bigdata-assistant/assistant/intentionparse
    http://10.18.226.58:6603/cloudbrain-assistant/assistant/intentionparse?inputTxt=我要报修&ownerCode=a
    """
    """
    http://10.18.222.105:6603/cloudbrain/sqyn_to_sc/init_data
    /cloudbrain/sqyn_to_sc/update_data
    """


if __name__ == "__main__":

    print('the main is not this path')
