import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import librosa
from pydub import AudioSegment
import pandas as pd 

def detect_apnea(arr,addr): #소리 0인 구간 카운팅
	i = 1
	if addr + i == len(arr): return 0 #마지막 부분에 혹시 걸릴 경우 (파일 짤릴 경우 예외 처리)
	while arr[addr+ i] == 0: 
		i = i + 1
		if addr + i == len(arr): break # 이 역시도 파일 짤릴 경우 예외처리
	return i #카운팅한 만큼 return
	
#sound=AudioSegment.from_wav("sample_006.wav")
#sound=sound.set_channels(1)
#sound.export("out_sample_006.wav", format="wav")
 
#spf = wave.open('out_sample_003.wav','r')

def DeTect(n,file_name):
	
	spf = wave.open(file_name,'r')
	signal = spf.readframes(-1)
	signal = np.frombuffer(signal, dtype=np.int16)
	framerate = spf.getframerate()
	
	if spf.getnchannels() == 2:
		print('Just mono files')
		sys.exit(0)
	
	
	Time = np.linspace(0,len(signal)/framerate, num=len(signal))
	temp_signal = signal.copy()
	temp_signal = np.abs(temp_signal)
	temp_Time = []
	temp = 0
	time = int(len(Time)/framerate) #음성 input 파일의 총 시간 구함
	
	for i in range(0,time): #44100으로 sampling된 파일 1초 단위로 만들기
		for j in range(0,framerate):
			temp = temp + temp_signal[i*framerate + j]
		temp_Time.append(temp/44100)
		temp = 0
	
	mag = librosa.amplitude_to_db(np.array(temp_Time)) #진폭 값 데시벨로 만들어 줌
	mag = np.around(mag)
	mag = np.where(mag<=26,0,mag) #26데시벨 기준 소곤소곤한 대화 수준 이 아래는 낙엽소리, 초침소리 정도임
	#평균 코골이 소리는 40db임 
	temp = 0
	apnea_count = 0
	apnea_Time = []
	Decibel_check = []
	
	if n <= 1:
		for i in range(840,time-1):
			Decibel_check.append(mag[i])
			if mag[i+1] == 0 and mag[i] != 0:
				temp = detect_apnea(mag,i)
				if temp >= 20 and temp <=60:
					apnea_count = apnea_count + 1
					apnea_Time.append(i)
					i = i + temp
				elif temp > 60:
					i = i + temp
				temp = 0
	else:
		for i in range(0,time-1):#359   time-1
			if mag[i+1] == 0 and mag[i] != 0:
				temp = detect_apnea(mag,i)
				if temp >= 20 and temp <=60: #20 ~ 60초 사이의 소리 없는 구간은 무호흡으로 간주
					apnea_count = apnea_count + 1 #무호흡 카운팅
					apnea_Time.append(i) # 무호흡이 발생한 시간을 저장
					i = i + temp
				elif temp > 60: #60초 이상 소리가 없을 경우는 호흡으로 간주
					i = i + temp
				temp = 0	


	for i in range(0,len(apnea_Time)): #무호흡 시간 출력
		print(apnea_Time[i])


	#평균 코골이 계산
	mean = [0,0]
	for i in range(0,time-1):
		if mag[i] !=0:
			mean[0] = mean[0] + mag[i]
			mean[1] = mean[1] + 1
	
	result_array = [0,0,0,0]
	
	#result_array[0] = 무호흡 판단
	#result_array[1] = 최고 dB
	#result_array[2] = 평균 dB 
	#result_array[3] = 현재 음원파일에서 나온 무호흡 카운트
	
	
	result_array[2] = np.around(mean[0] / mean[1]) 

	result_array[3] = len(apnea_Time)
	
	if apnea_count >= 5:
		#print('수면 무호흡')
		result_array[0] = 1
	else:
		#print('정상 호흡')
		result_array[0] = 0
		
	#print('수면중 무호흡 횟수:', apnea_count)	
	
	if n <= 1:
		result_array[1] = np.max(np.array(Decibel_check))
	else:
		result_array[1] = np.max(mag)
	
	#44100개 까지가 1초 

	'''
	plt.figure(figsize=(30, 4))
	plt.title('Signal Wave...')
	plt.xlabel('Time Sequence')
	plt.ylabel('DB')
	plt.plot(mag[4000:4200],marker='o')
	plt.show()
	'''
	return result_array



'''
spf = wave.open('out_sample_006.wav','r') 


#Extract Raw Audio from Wav File
signal = spf.readframes(-1) # -1 프레임의 오디오를 bytes 객체로 읽고 반환   N(여기선 -1) * sample_width * n_channels bytes야
signal = np.frombuffer(signal, dtype=np.int16)
framerate = spf.getframerate()

 
#If Stereo
if spf.getnchannels() == 2:
    print('Just mono files')
    sys.exit(0)
    
	
Time = np.linspace(0,len(signal)/framerate, num=len(signal))



temp_signal = signal.copy()
temp_signal = np.abs(temp_signal)
temp_Time = []
temp = 0
time = int(len(Time)/framerate) #음성 input 파일의 총 시간 구함


for i in range(0,time): #44100으로 sampling된 파일 1초 단위로 만들기
	for j in range(0,framerate):
		temp = temp + temp_signal[i*framerate + j]
	temp_Time.append(temp/44100)
	temp = 0


mag = librosa.amplitude_to_db(np.array(temp_Time)) #진폭 값 데시벨로 만들어 줌
mag = np.around(mag)
mag = np.where(mag<=26,0,mag) #26데시벨 기준 소곤소곤한 대화 수준 이 아래는 낙엽소리, 초침소리 정도임
#평균 코골이 소리는 40db임 
temp = 0
apnea_count = 0
apnea_Time = []

for i in range(0,3600):#359   time-1
	if mag[i+1] == 0 and mag[i] != 0:
		temp = detect_apnea(mag,i)
		if temp >= 20 and temp <=60: #20 ~ 60초 사이의 소리 없는 구간은 무호흡으로 간주
			apnea_count = apnea_count + 1 #무호흡 카운팅
			apnea_Time.append(i) # 무호흡이 발생한 시간을 저장
			i = i + temp
		elif temp > 60: #60초 이상 소리가 없을 경우는 호흡으로 간주
			i = i + temp
		temp = 0	
			
for i in range(0,len(apnea_Time)): #무호흡 시간 출력
	print(apnea_Time[i])

if apnea_count >= 5:
	print('수면 무호흡')
else:
	print('정상 호흡')
	
print('수면중 무호흡 횟수:', apnea_count)	
#44100개 까지가 1초 


plt.figure(figsize=(30, 4))
plt.title('Signal Wave...')
plt.xlabel('Time Sequence')
plt.ylabel('DB')
plt.plot(mag[4000:4200],marker='o')
plt.show()
'''
