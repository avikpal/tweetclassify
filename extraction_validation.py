#!/usr/bin/env python
import re
lines = [line.strip() for line in open('valid.txt')]
f=open('output','w')
pred_flag=0
for string in lines:
  string = re.sub("['.,]",'',string)
	string = re.sub('["]','',string)
	string=string.replace('  ',' ')
	space_pos=[m.start() for m in re.finditer(' ',string)]
	i=len(space_pos)
	cntr=0
	twid=string[0:space_pos[cntr]]
	while(i>=2):
			temp=string[space_pos[cntr]+1:space_pos[cntr+1]]
			print temp
			cntr+=1
			i-=1
	temp=string[space_pos[cntr]+1:]
	print temp
	
