from __future__ import print_function
import time
filename='abc1.txt'
f=open(filename,'r')

d1={}
d2={}

#key1='flow_name'
#value1=['src_mac','dst_mac','src_ip','dst_ip','tcpsrc_port','tcpdst_port,','idle_timeout','hard_timeout',]

key1='flow'
value1=['src_mac','dst_mac','src_ip','dst_ip','tcpsrc_port','tcpdst_port,','60','300','0']

capacity1=512
capacity2=1024

d1.setdefault(key1,value1)

set=[]
set.append(key1)

count=0

def show(pagefault):
	print('-------------------FLOW TABLE------------------------')
	for key,value in d1.items():
		print(key,value,sep=' ')
	print('-----------------------------------------------------')
	#print('Number of pagefault is %d ',pagefault)

# updating idle and hard time out every second recursively
def update(count,cnt,pagefault):
	for key,val in d1.items():
		x=int(d1[key][6])-1
		y=int(d1[key][7])-1
		if(y<=0):
			del d1[key]
			if key in set:
				set.remove(key)
			print('\n')
			print('entry is deleted because of hard time out!!!')
			print('\n')
		elif(x<=0):
			if key in set:
				set.remove(key)
			del d1[key]
			print('\n')
			print('entry is deleted because of idle time out!!!')
			print('\n')
		else:
			d1[key][6]=str(x)
			d1[key][7]=str(y)
	time.sleep(1)
	cnt=cnt+1
	#if cnt%2==0:
	show(pagefault)
	#if cnt%5==0:
	lru(count,cnt,pagefault)
	#update(count,cnt,pagefault)
#lru algorithm
def lru(count,cnt,pagefault):
	while(1):
		line=f.readline()
		if line=='':
			print('##### file is going to read again #####')
			f.seek(0,0)
			continue
		#print('entry is pushed in flow table')
		line=line.rstrip()
		line=line.split('*')
		entry=line[1].split(',')
		if len(d1)<capacity1: 
			if line[0] in d1:
				print('entry is present in flow table')
				entry[6]=str(20) 
				z=int(entry[8])+1
				entry[8]=str(z)
				d1[line[0]]=entry 
				set.remove(line[0])
				set.append(line[0])
			else:
				print('Not present')
				pagefault=pagefault+1
				d1[line[0]]=entry
				set.append(line[0])
		else:
			print('flow table is full now')
			if line[0] in d1:
				entry[6]=str(20)      
                                z=int(entry[8])+1                  
                                entry[8]=str(z)
                                d1[line[0]]=entry
				set.remove(line[0])
				set.append(line[0])
			else:
				pagefault=pagefault+1
				for flw in set:
					if flw in d1:
						print('least recently used entry is deleted')
						del d1[flw]
						set.remove(flw)
						break
				d1[line[0]]=entry
				set.append(line[0])
				
		count=count+1
		if(count%16==0):
			print('\n')
			print('********* total entry read from file is %d',count)
			print('********* Number of pagefault is %d',pagefault)
			print('\n')
			break
		#print(set)
		#print('pagefault=',pagefault)
		#print('total entry ',count)
	update(count,cnt,pagefault)

lru(1,0,1)		
