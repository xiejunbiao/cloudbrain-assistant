# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 18:16:38 2020

@author: lijiangman
"""


from voiceAssistant.start_voice_assistant import voice_start

    
if __name__ == '__main__':
    
    texts = ['我要买苹果', '买苹果', '订单啊呵呵'
             , '我想报修', '报修'
             ,'我想要啊啊投诉啊'
             , '打开报修', '打开进入报修'
             ,'我想要苹果', '有没有苹果', '我想要地球'
             ,'我要打开海信广场.', '海信广场。', '永旺', '信我家'
             ,'海信广场超市的', '信我家生活服务店', '信我家生活服务馆'
             , '海信广场的苹果。', '海信广场超市的地球。']
    
    # search_test={'我要买苹果', '买苹果', '我想要苹果', '有没有苹果'}
    
    for text in texts:
        print('********')
        intention_json = voice_start(0, 0, text)
        print(text, '\n', intention_json)
