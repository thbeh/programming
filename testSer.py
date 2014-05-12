import platform
import socket
import serial
import time
import getDiskUsage
import getnifs
import getPlatform
 
def loop():
	buttonPressed = ser.read()
	if (buttonPressed == '1'):
		doOS();
	elif (buttonPressed == '2'):
		doIP();
	elif (buttonPressed == '3'):
		doDU();

def doOS():
	print 'OS'
	lsbinfo = getPlatform.get_lsb_information()
	os = platform.uname()
	info = '~'+lsbinfo['DESCRIPTION']+'~'+os[2]
	print info 
	ser.write(info)

def doIP():
	print 'IP'
	network = ''
	nifs = getnifs.get_network_interfaces()
	for ni in nifs:
		if ni.name == 'lo':
			continue
		else:
			nif = ni.name[:1]+ni.name[-1:]
			network += '~'+nif+'#'+str(ni.addresses.get(socket.AF_INET))
	print network 
	ser.write(network)
def doDU():
	print 'Disk'
	diskU = ''
	for part in getDiskUsage.disk_partitions():
    		pt1 = getDiskUsage.disk_usage(part.mountpoint)
#   		print pt1.x
#   		print pt1.y
#   		print pt1.z
		balance = int(round((100.0 - pt1.z)/4))
#		print balance
		#stat = (pt1.x).ljust(6)+'{:4d}'.format(pt1.y)+'G '+'{:3.0f}'.format(pt1.z)+'%'
		stat = '~'+(pt1.x).ljust(6)+'{:4d}'.format(pt1.y)+'G'+'#'+str(balance)
		diskU += stat
	print diskU
	ser.write(diskU)

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) #port is 11 (for COM12, and baud rate is 9600 /dev/ttyUSB0
time.sleep(2)    #wait for the Serial to initialize
while True:
	loop()

