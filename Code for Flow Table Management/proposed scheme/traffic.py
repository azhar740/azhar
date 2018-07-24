num=1024
filename='abc.txt'
entry='src_mac1,dst_mac1,src_ip1,dst_ip1,tcpscr_port1,tcpdst1_port,10,60,0,1'
cnt=0
with open(filename,'w') as f:
	for i in range(0,num):
		cnt=cnt+1
		line='flow'+str(cnt)+'*'+entry
		f.write(line)
		f.write('\n')	
