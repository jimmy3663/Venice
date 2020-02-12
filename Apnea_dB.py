import pymysql
import os
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

def Find_dB_value():
	f = open('./jimmy3663/apnea_2010.txt',mode='rt',encoding='utf-8')
	temp = f.readline()
	f.close()
	value = temp.split(' ')
	return value
def Insert_dB_value(value):
	'''
	value[0] = count_apnea
	value[1] = count
	value[2] = Max_dB
	value[3] = Mean_dB
	'''
	'''
	conn = pymysql.connect(host='localhost', user='root', password='abc1234!@#$', db='sleep', charset='utf8')
	curs = conn.cursor()
	sql = "select audio_path from sleep_status where id = 'test1@kw.ac.kr'";
	curs.execute(sql)
	conn.commit()
	row = curs.fetchall()
	path = row.index('test1@kw.ac.kr')
	conn.close()
	'''
	f = open('./test1@kw.ac.kr/Apnea_2020_02_10.txt',mode='wt',encoding='utf-8')
	for i in range(0,4):
		temp = str(value[i])+' '
		f.write(temp)
	f.close()