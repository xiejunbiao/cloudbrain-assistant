# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 18:16:38 2020

@author: lijiangman
"""

from server.bigdata_voice_assis_web_server import start
    
import logging
logger = logging.getLogger()  # # initialize logging class
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    logger.info("starting voice assistant service")
    start()
