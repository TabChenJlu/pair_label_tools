import pandas as pd
import os
import configparser
import itertools
import sqlite3
import time
import random
import locale
import logging
import uuid
import traceback
from logging.config import fileConfig

basePath = os.path.dirname(os.path.realpath(__file__))

fileConfig(os.path.join(basePath, '../config/logging_config.ini'))
logger = logging.getLogger()

config = configparser.ConfigParser()
config.read(os.path.join(basePath, '../config/system.ini'))

raw_data_dir = config['path'].get('data_dir')
db_path = config['path'].get('db_path')
table = config['db'].get('table')
wait_state = config['db'].get('wait_state')
processing_state = config['db'].get('processing_state')
success_state = config['db'].get('success_state')
title = config['info']['title']
task_name = config['info']['task_name']
teacher_font_color = config['ui']['teacher_font_color']
student_font_colot = config['ui']['student_font_colot']

data_dict = {}
def loadAllText():
    data_dict = {}
    for file_name in os.listdir(raw_data_dir):
        index = file_name.split('.')[0]
        path = os.path.join(raw_data_dir, '{}.txt'.format(int(index)))
        data_dict[index] = open(path, 'r',encoding='utf-8').read()
    return data_dict

data_dict = loadAllText()

def get_session_id():
    return str(uuid.uuid4())

def loadText(index):
    return data_dict[str(index)]


def getNowTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

class database():
    def __init__(self):
        pass
    def connect(self):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    def execute(self, sql):
        self.connect()
        try:
            logger.info('Start execute sql:{}'.format(sql))
            self.cursor.execute(sql)
            self.conn.commit()
            result = self.cursor.fetchall()
            result = [dict(x) for x in result]
            self.conn.close()
            logger.info('Finish execute sql:{}'.format(sql))
        except:
            logger.error('Write to db fail,detail is {}'.format(traceback.format_exc()))
        finally:
            self.conn.close()
        return result
'''
state
- 0 未标注 
- 1 正在标注
- 2 标注完成
'''
class Pair():
    def __init__(self):
        self.state = True
        sql = "select * from pairs where state==0 limit 1"
        self.result = self.execute(sql)
        if len(self.result) == 0:
            self.state = False
            logger.info('All data have been labeled ~~')
        if self.state:
            logger.info('Start select one pair')
            self.result = self.result[0]
            self.i = self.result['index_i']
            self.j = self.result['index_j']
            self.id = self.result['id']
            sql = 'UPDATE {} SET state = {} WHERE id = {}'.format(
                table, processing_state, self.id)
            self.execute(sql)
            logger.info('Pair info i={},j={},id={}'.format(
                self.i, self.j, self.id))

    def execute(self, sql):
        db = database()
        result = db.execute(sql)
        return result

    def save(self, label):
        logger.info('Save result,id = {},label = {}'.format(self.id, label))
        sql = 'UPDATE {} SET label = {},state = {},label_time = "{}" WHERE id = {}'.format(
            table, label, success_state, getNowTime(), self.id)
        self.execute(sql)

    def relase(self):
        logger.info('Relase pair(id = {})'.format(self.id))
        sql = 'UPDATE {} SET state = {} WHERE id = {}'.format(
            table, wait_state, self.id)
        self.execute(sql)

    def get_index(self):
        return self.i, self.j

    def get_text(self):
        return loadText(self.i), loadText(self.j)

def save_label(id,label,user):
    logger.info('Start save result,id = {},label = {}'.format(id, label))
    
    sql = 'UPDATE {} SET label = {},state = {},label_time = "{}",user= "{}" WHERE id = {}'.format(
            table, label, success_state, getNowTime(), user,id)
    db = database()
    result = db.execute(sql)
    logger.info('Finish save result,id = {},label = {},user = {}'.format(id, label,user))
    return result

def release_pair(id):
    logger.info('Start release pair,id = {}'.format(id))
    
    sql = 'UPDATE {} SET state = {} WHERE id = {}'.format(
            table,wait_state,id)
    db = database()
    result = db.execute(sql)
    logger.info('Finish release pair,id = {}'.format(id))
    return result