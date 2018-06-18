# -*- coding: utf-8 -*-
# author: Tiancheng Zhao
import logging
from simdial.config import Config

logging.basicConfig(filename='simdial.log' if Config.debug is False else None, level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
