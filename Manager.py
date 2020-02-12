import WAV
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import librosa
from pydub import AudioSegment
import pandas as pd 

def sound_print(decibel):
	if decibel < 30:
		print('나뭇잎 부딫히는 정도의 소리입니다')
	elif decibel >= 30 and decibel <=35:
		print('조용한 농촌, 조용한 공원 정도의 소리입니다')
	elif decibel >35 and decibel < 55:
		print('조용한 사무실, 주택의 거실 정도의 소리입니다')
	elif decibel >= 55 and decibel < 70:
		print('보통의 대화소리, 백화점내 소음 정도의 소리입니다')
	elif decibel >= 70 and decibel <80:
		print('전화벨소리, 시끄러운 사무실 소음 정도의 소리입니다')
	elif decibel >=80 and decibel <90:
		print('철로변 및 지하철 소음 정도의 소리입니다')
	else:
		print('소음이 심한 공장의 소음보다 큰 소리입니다.')

# result[0] = 무호흡 환자 진단 카운팅 (수면 중 무호흡이라고 판단 된 횟수)
# result[1] = 가장 큰 소음 dB
# result[2] = 평균 소음 dB
# result[3] = 수면중 무호흡 횟수

def Manage(file_name): #c => count, c_a = count_apnea
	count = 0
	count_apnea = 0
	#file = 'out_sample_007_' + str(n) +'.wav'
	file = file_name
	print(file)
	#result = WAV.DeTect(n,str)
	temp = WAV.DeTect(2,file)
	result = [0,0,0,0]
	result[0] = temp[0] # 무호흡 환자 진단 카운트
	result[1] = temp[3] # 무호흡 횟수 카운트
	result[2] = temp[1] #가장 큰 소음 dB
	result[3] = temp[2] #평균 소음 dB
	return result

def Max_period(file_name, Max_dB):
	spf = wave.open(file_name,'r')
	signal = spf.readframes(-1)
	signal = np.frombuffer(signal, dtype=np.int16)
	framerate = spf.getframerate()

	temp_signal = signal.copy()
	temp_signal = np.abs(temp_signal)
	temp_Time = []
	temp = 0
	time = int(len(signal)/framerate) #음성 input 파일의 총 시간 구함
	
	for i in range(0,time): #44100으로 sampling된 파일 1초 단위로 만들기
		for j in range(0,framerate):
			temp = temp + temp_signal[i*framerate + j]
		temp_Time.append(temp/44100)
		temp = 0
	
	mag = librosa.amplitude_to_db(np.array(temp_Time)) #진폭 값 데시벨로 만들어 줌
	mag = np.around(mag)
	
	max = np.where(mag==Max_dB)
	max_term = max[0][0]

	fig = plt.gcf()
	if max_term-60 < 0:
		plt.plot(range(0,max_term+60), mag[0:max_term+60])
	elif max_term+60>len(mag):
		plt.plot(range(max_term-60,len(mag)),mag[max_term-60:])
	else:
		plt.plot(range(max_term-60,max_term+60),mag[max_term-60:max_term+60])
	plt.show()
	fig.savefig('./jimmy3663/jimmy3663_max.png', dpi=300)

def Manager(file_name):	
	count = 0
	count_apnea = 0
	Max_dB = 0
	Mean_dB = 0
	Max_dB_Time = 0
	value = [0,0,0,0] 
	'''
	value[0] = 수면중 무호흡 횟수 count_apnea
	value[1] = 현재 무호흡 상태 ==>무호흡 환자인지 아닌지 1>= 무호흡 환자, 그외 정상
	value[2] = Max dB
	value[3] = Mean_dB
	'''

	result = Manage(file_name)
	count = count + result[0]
	count_apnea = count_apnea + result[1]
	if Max_dB > result[2] or Max_dB == 0:
		Max_dB = result[2]
	Mean_dB = Mean_dB + result[3]

	'''
	for i in range(1,5):
		result = Manage(i)
		count = count + result[0]
		count_apnea = count_apnea + result[1]
		if Max_dB < result[2] or Max_dB == 0:
			Max_dB = result[2]
		Mean_dB = Mean_dB + result[3]
	'''
	Max_period(file_name, Max_dB)
	print('수면중 무호흡 횟수는 ', count_apnea,'이며') 
	
	print('현재 무호흡 상태는', end = ' ')
	if count >= 1:
		print('무호흡 환자입니다.')
	else:
		print('정상 입니다.')
	print('수면중 가장 큰 소음은 ',Max_dB,'dB 로 해당 소음은', end =' ')
	sound_print(Max_dB)
	#int(Mean_dB/2)
	print('평균 코골이의 정도는', Mean_dB,'dB 로 해당 소음은', end = ' ')
	sound_print(Mean_dB)
	
	value[0] = count_apnea
	value[1] = count
	value[2] = Max_dB
	value[3] = Mean_dB
	
	return value 

#Manager("out_tests.wav")
