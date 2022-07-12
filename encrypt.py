#p = previous, c = current, s = size, t = time
import sys, os, time

s = []
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
if out_enabled == '1' and (os.path.getsize(sys.argv[1]) >= 20): out_enabled = True
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
f = open(sys.argv[1],'rb')
f_read = f.read()
for f_byte in f_read:
	s.append(str(bin(f_byte))[2:].zfill(8))
	if out_enabled:
		if (len(s) % int(len(f_read)*0.05) == 0) or (len(s)-1 == len(f_read)):
			if speed_enabled: s_read = 'Подготовка файла: {0:.0f}%, скорость - {1} КБ/с'.format(float(len(s))/len(f_read)*100, measureSpeed(len(s), 'byte'))
			else: s_read = 'Подготовка файла: {0:.0f}%'.format(float(len(s))/len(f_read)*100)
			print('\b'*(len(s_read)+10)+s_read+' '*5,end='',flush=True)
			print('\b'*5,end='',flush=True)
f_read = ''
f.close()
s = ''.join(s)

if speed_enabled: 
	p_t_1 = time.time()
	p_s = 0
if out_enabled: print('\b'*len(s_read),end='',flush=True)

if len(sys.argv) != 3:
	if not out_enabled: print('\b'*19+'Шифрование файла...',end='',flush=True)
f_out = open(os.path.splitext(sys.argv[1])[0]+'_encrypted.txt','wb')
for i in range(len(s)):
	if i != 0 and (i+1)%6 == 0:
		f_out.write(chr(1040+int(s[i-5:i+1],2)).encode())
		if (i+1)+6 > len(s): s_end = s[i+1:len(s)]
	if out_enabled:
		if (i % int(len(s)*0.05) == 0) or (i+1 == len(s)):
			if speed_enabled: s_crypt = 'Шифрование файла: {0:.0f}%, скорость - {1} КБ/с'.format(float(i)/(len(s))*100, measureSpeed(os.path.getsize(os.path.splitext(sys.argv[1])[0]+'_encrypted.txt'), 'byte'))
			else: s_crypt = 'Шифрование файла: {0:.0f}%'.format(float(i)/(len(s))*100)
			print('\b'*(len(s_crypt)+10)+s_crypt+' '*5,end='',flush=True)
			print('\b'*5,end='',flush=True)

if len(s)%6 != 0:
	s_len = len(s_end)
	for i in range(6-s_len):
		s_end += '0'
	f_out.write(chr(1040+int(s_end,2)).encode())
	f_out.write(chr(48+s_len).encode())
f_out.close()

if len(sys.argv) != 3:
	if not out_enabled: s_crypt = 'Шифрование файла...'
	print('\b'*len(s_crypt)+'Завершено. Затраченное время (в секундах): {0:.0f}.'.format(time.time()-p_t)+' '*5)
	input()