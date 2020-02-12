import pymysql
import os
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

def mysqlcon(message):
	conn = pymysql.connect(host='localhost', user='root', password='jimmy0', db='sleep', charset='utf8')

	curs = conn.cursor()
	'''
	print('register : (ID), (name), (age), (Birth), (height), (weight), (password)')

	ID = input('ID: ')
	ID = "'"+ID+"'"

	name = input('name: ')
	name = "'"+name+"'"

	age = input('age: ')

	birth = input('birth (in format(19xx-xx-xx)): ')
	birth="'"+birth+"'"

	hegith = input('hegith: ')
	weight = input('weight: ')

	password = input('password: ')
	password="'"+password+"'"
	
	sql = 'insert into user values('+ID+','+name+','+age+','+birth+','+hegith+','+weight+','+password+')'
	'''
	
	new_buf = message[2:]
	id_count = 0
	for i in range(0, len(new_buf)):
		if new_buf[i] == "'":
			break
		id_count += 1	#아이디 길이 자리수+5

	id_lenght = int(new_buf[1:id_count]) #진짜 아이디 길이
	id_count = id_count-1
	user_id = new_buf[2+id_count:2+id_count+id_lenght]
	print(user_id)
	sql = "select * from user where user_id = '"+user_id+"'"
	curs.execute(sql)

	row = curs.fetchall()
	if len(row) > 0:
		conn.close()
		return 1 
	else:
		new_buf = new_buf[1+id_count:]
		sql = 'insert into user values('+new_buf+')'
		curs.execute(sql)
		conn.commit()

		sql = 'select * from user'
		curs.execute(sql)
		row = curs.fetchall()

		for i in range(0, len(row)):
			print(row[i])
		conn.close()
		return 0

	

