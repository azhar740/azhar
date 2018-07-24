from __future__ import print_function
import time
filename='abc.txt'
f=open(filename,'r')

d1={}
d2={}

#key1='flow_name'
#value1=['src_mac','dst_mac','src_ip','dst_ip','tcpsrc_port','tcpdst_port,','idle_timeout','hard_timeout','counters','age','active']

#key1='flow'
#value1='src_mac,dst_mac,src_ip,dst_ip','tcpsrc_port','tcpdst_port,','1','1','0','0','1']

capacity1=512
capacity2=1024

#d1.setdefault(key1,value1)


	
'''print('-------------------FLOW TABLE 1 -------------------------------------------------------------------')
for key,value in d1.items():
	print(key,value,sep=' ')
print('---------------------------------------------------------------------------------------------------')
'''
set_inactive=[]
set_active=[]
#set.append(key1)

def show(pagefault):
	print('-------------------FLOW TABLE 1 -------------------------------------------------------------------')
	for key,value in d1.items():
		print(key,value,sep=' ')
	print('---------------------------------------------------------------------------------------------------')
	print('\n')

	#print('Number of pagefault is %d ',pagefault)

#update age of the the inactive entries
#def update_age():


idle_time=20
hard_time=100
inactive_entry=0
active_entry=0

'''while(1):
        line=f.readline()
        line=line.rstrip()
        if(line==''):
                break
        line=line.split('*')
        line[1]=line[1].split(',')
        d1[line[0]]=line[1]'''

# updating idle and hard time out every second recursively
	#update(count,cnt,pagefault)
#print('--------------------------working------------------------------')
def update(count,cnt,pagefault):
        global idle_time
        global hard_time
        global inactive_entry
        global active_entry
        for key in d1:
                x=int(d1[key][6])-1
                y=int(d1[key][7])-1
                if( (y<=0 or x<=0) and len(d1)<=capacity1 and int(d1[key][9])==1):
                        d1[key][6]=str(idle_time)
                        d1[key][7]=str(hard_time)
                        d1[key][9]=str(0)
                        inactive_entry=inactive_entry+1
                        active_entry=active_entry-1
                        set_inactive.append(key)
                        set_active.remove(key)
                elif( (y<=0 or x<=0) and len(d1)<=capacity1 and int(d1[key][9])==0):
                        d1[key][6]=str(idle_time)
                        d1[key][7]=str(hard_time)
                        d1[key][9]=str(0)
                        set_inactive.remove(key)
                        set_inactive.append(key)

                else:
                        d1[key][6]=str(x)
                        d1[key][7]=str(y)
        time.sleep(1)
        cnt=cnt+1
        if cnt%5==0:
                show(pagefault)
        #if cnt%5==0:
        lru(count,cnt,pagefault)
        #update(count,cnt,pagefault)
def lru(count,cnt,pagefault):
	global idle_time
	global hard_time
	global inactive_entry
	global active_entry
	global capacity1
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
			if(line[0] in d1 and int(d1[line[0]][9])==1):
			        d1[line[0]][6]=str(idle_time) 
				d1[line[0]][8]=str(int(d1[line[0]][8])+1)
				set_active.remove(line[0])
				set_active.append(line[0])
				#print('\n---------------------------------------------')
				#print('set_active',set_active,sep=' ')
				#print('set_inactive',set_inactive,sep=' ')
				#print('\n---------------------------------------------')
				#print('deleted entry is',line[0],sep=' ')
				#d1[line[0]][9]==1
				#inactive_entry=inactive_entry-1
				#active_entry=active_entry+1
				
				
			elif( line[0] in d1 and int(d1[line[0]][9])==0 ):
				d1[line[0]][6]=str(idle_time) 
				d1[line[0]][8]=str(int(d1[line[0]][8])+1)
				set_active.append(line[0])
				set_inactive.remove(line[0])
				d1[line[0]][9]=str(1)
				inactive_entry=inactive_entry-1
				active_entry=active_entry+1
				'''print('\n---------------------------------------------')
				print(set_active)
				print(set_inactive)
				print('\n---------------------------------------------')
				'''
			else:
				pagefault=pagefault+1
				d1[line[0]]=entry
				set_active.append(line[0])
				active_entry=active_entry+1
				'''print('\n---------------------------------------------')
				print(set_active)
				print(set_inactive)
				print('\n---------------------------------------------')
				'''
		else:
			print('flow table is full now')
			if( line[0] in d1 and int(d1[line[0]][9])==0):
				d1[line[0]][6]=str(idle_time)      
                                d1[line[0]][8]=str(int(d1[line[0]][8])+1)
				d1[line[0]][9]=str(1)
				set_inactive.remove(line[0])
				set_active.append(line[0])
				active_entry=active_entry+1
				inactive_entry=inactive_entry-1
			elif( line[0] in d1 and int(d1[line[0]][9])==1):
				d1[line[0]][6]=str(idle_time)      
                                d1[line[0]][8]=str(int(d1[line[0]][8])+1)
				set_active.remove(line[0])
				set_active.append(line[0])
				
			elif(inactive_entry!=0):
				pagefault=pagefault+1
				print('I am comming in inactive entry')
				for flw in set_inactive:
					if flw in d1:
						print('inactive entry is deleted')
						del d1[flw]
						set_inactive.remove(flw)
						inactive_entry=inactive_entry-1
						break
				d1[line[0]]=entry
				set_active.append(line[0])
				active_entry=active_entry+1
				
			elif(active_entry!=0):
				pagefault=pagefault+1
				for flw in set_active:
					if flw in d1:
						print('active entry is deleted')
						del d1[flw]
						set_active.remove(flw)
						break
				d1[line[0]]=entry
				set_active.append(line[0])
				
		count=count+1
		'''if inactive_entry+active_entry<=len(d1):
                        print('yes')
                else:
                        print('No')'''
		if(count%16==0):
			print('\n')
			print('********* total entry read from file is %d',count)
			print('********* Number of pagefault is %d',pagefault)
			print('\n')
			print(active_entry,inactive_entry,sep=' ')
			print(len(set_active),len(set_inactive),sep=' ')
			break
		#print(set)
		#print('pagefault=',pagefault)
		#print('total entry ',count)
	update(count,cnt,pagefault)
	
lru(0,0,0)
