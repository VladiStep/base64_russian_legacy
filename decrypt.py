#p = previous, c = current, s = size, t = time
import sys, os, time, codecs

bytes = []
bytes_1 = []
p_s = 0
speed_enabled = True

def measureSpeed(c_s, unit):
	global p_t_1, p_s
	c_t = time.time()
	try: speed = (c_s-p_s) / (c_t-p_t_1)
	except: return -1
	if unit == 'bit': speed_kb = speed / 8 // 1024
	else: speed_kb = speed // 1024
	p_s = c_s
	p_t_1 = c_t
	return int(speed_kb)

if len(sys.argv) < 2:
	print('Перетащите файл на меня.')
	print('(Нажмите Enter для завершения)')
	input()
	sys.exit()

if len(sys.argv) != 3:
	print('Включить вывод процентов?(без вывода быстрее)(1/0): ',end='')
	out_enabled = input()
else: out_enabled = '0'
if out_enabled == '1' and (os.path.getsize(sys.argv[1]) >= 55): out_enabled = True
else: out_enabled = False
if out_enabled:
	print('Измерять скорость?(немного замедляет) (1/0): ',end='')
	speed_enabled = input()
	if speed_enabled == '1': speed_enabled = True
	else: speed_enabled = False

if len(sys.argv) != 3: os.system('cls')

p_t = time.time()
p_t_1 = p_t

if len(sys.argv) != 3:
	if not out_enabled: print('Подготовка файла...',end='',flush=True)
f = codecs.open(sys.argv[1],'r','utf-8')
f_read = f.read()
f.close()
for byte in f_read:
	if byte.isdigit():
		bytes[-1] = bytes[-1][:int(byte)]
		break
	bytes.append(str(bin(ord(byte)-1040))[2:].zfill(6))
	if out_enabled:
		if (len(bytes) % int(len(f_read)*0.05) == 0) or (len(bytes) == len(f_read)):
			if speed_enabled: s_read = 'Подготовка файла: {0:.0f}%, скорость - {1} КБ/с'.format(float(len(bytes))/len(f_read)*100, measureSpeed(len(bytes)*6, 'bit'))
			else: s_read = 'Подготовка файла: {0:.0f}%'.format(float(len(bytes))/len(f_read)*100)
			print('\b'*(len(s_read)+10)+s_read+' '*5,end='',flush=True)
			print('\b'*5,end='',flush=True)
f_read = ''

bytes_1 = ''.join(bytes)

if speed_enabled:
	p_t_1 = time.time()
	p_s = 0
if out_enabled: print('\b'*len(s_read),end='',flush=True)

if len(sys.argv) != 3:
	if not out_enabled: print('\b'*19+'Расшифровка файла...',end='',flush=True)
bytes = ''
f_out = open(os.path.splitext(sys.argv[1])[0]+'.decrypted','wb')
for i in range(len(bytes_1)):
	if i != 0 and (i+1)%8 == 0:
		f_out.write((int(bytes_1[i-7:i+1],2)).to_bytes(1,'big'))
		if out_enabled:
			if ((i+1) % int(len(bytes_1)*0.05) == 0) or (i-1 == len(bytes_1)):
				if speed_enabled: s_decry = 'Расшифровка файла: {0:.0f}%, скорость - {1} КБ/с'.format(float(i)/len(bytes_1)*100, measureSpeed(os.path.getsize(os.path.splitext(sys.argv[1])[0]+'.decrypted'), 'byte'))
				else: s_decry = 'Расшифровка файла: {0:.0f}%'.format(float(i)/len(bytes_1)*100)
				print('\b'*(len(s_decry)+10)+s_decry+' '*5,end='',flush=True)
				print('\b'*5,end='',flush=True)
f_out.close()

if len(sys.argv) != 3:
	if not out_enabled: s_decry = 'Расшифровка файла...'
	print('\b'*len(s_decry)+'Завершено. Затраченное время (в секундах): {0:.0f}.'.format(time.time()-p_t)+' '*10)
	input()