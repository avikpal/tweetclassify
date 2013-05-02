#!/usr/bin/env python
import re  

lines = [line.strip() for line in open('training.txt')]

sports={}
politics={}
sports_hash_url=[]
politics_hash_url=[]
sports_count=0
politics_count=0

for string in lines:
	
	string = re.sub("[',+]",' ',string)
	string = re.sub('["]',' ',string)
	
	string=string.replace('  ',' ')
	string=string.replace('  ',' ')
	string=string.replace('  ',' ')
	words=string.count(' ')+1
	space_pos= [m.start() for m in re.finditer(' ',string)]
	print string
	if(string[space_pos[0]+1]=='S'):
		sports_count+=1
		i=len(space_pos)
		cntr=1
		
		while(i>2):
			temp=string[space_pos[cntr]+1:space_pos[cntr+1]]
			
			if temp[0]=='#':
 				sports_hash_url.append(temp)
			elif len(temp)>4:
				if temp[0:3]=='http':
					sports_hash_url.append(temp)
									
				elif temp in sports:
					
					sports[temp]+=1
					
 				else:
					sports[temp]=0
					
			elif temp in sports:
				#print 'in here'
				sports[temp]+=1
				#print sports[temp]
				#sports_count+=1
 			else:
				sports[temp]=0
				#sports_count+=1	
			cntr+=1
			i-=1
		temp=string[space_pos[cntr]+1:]
		if temp in sports:
			sports[temp]+=1
			#sports_count+=1
 		else:
			sports[temp]=0	
			#sports_count+=1				      
	
	else:
		politics_count+=1
		i=len(space_pos)
		cntr=1
		while(i>2):
			temp=string[space_pos[cntr]+1:space_pos[cntr+1]]
			print temp
			if temp[0]=='#':
 				politics_hash_url.append(temp)
				#sports_count+=1;
			elif len(temp)>4:
				if temp[0:3]=='http':
					politics_hash_url.append(temp)
					#sports_count+=1				
				elif temp in politics:
					print 'in here'
					politics[temp]+=1
					print politics[temp]
					#sports_count+=1
 				else:
					politics[temp]=0
					#sports_count+=1
			elif temp in politics:
				print 'in here'
				politics[temp]+=1
				print politics[temp]
				#sports_count+=1
 			else:
				politics[temp]=0
				#sports_count+=1	
			cntr+=1
			i-=1
		temp=string[space_pos[cntr]+1:]
		if temp in politics:
			politics[temp]+=1
			#sports_count+=1
 		else:
			politics[temp]=0	
			#sports_count+=1	
	
#print politics_hash_url
#print sports_hash_url	

#now is code for calculations....
vocab_size=len(sports)+len(politics)+len(politics_hash_url)+len(sports_hash_url)

prior_sports=(len(sports)+len(sports_hash_url))/(vocab_size*(1.0))
prior_politics=(len(sports)+len(politics_hash_url))/(vocab_size*(1.0))


def count_word(string,flag):
	#print string
	#print 'in func'
	if(flag==1): #sports
		#print string[0]
		if string==' ':
			return 0
		if string[0]=='#':
			if string in sports_hash_url:
				return -1
			else:
				return  0
		elif len(string)>4:
			#print 'in check'
				
			if string[0:3]=='http':
				#print 'in if'
				if string in sports_hash_url:
					return -1
				else:
					return  0
			elif string in sports:
				#print 'in sports'
				#print string
				#print sports[string]
				return sports[string]
			else:
				#print 'not in sports'
				return 0
		elif string in sports:
			#print 'in sports'
			#print string
			#print sports[string]
			return sports[string]
		else:
			#print 'not in sports'
			return 0
		 
	else:#politics
		if string==' ':
			return 0
				
		if string[0]=='#':
			if string in politics_hash_url:
				return -1
			else:
				return  0
		elif len(string)>4:
			if string[0:3]=='http':
				if string in politics_hash_url:
					return -1
				else:
					return  0
			elif string in politics:
				#print 'in politics'
				#print string
				#print politics[string]
				return politics[string]
			else:
				return 0
		elif string in politics:
			#print 'in politics'
			#print string
			#print politics[string]
			return politics[string]
		else:
			return 0 



lines = [line.strip() for line in open('validation.txt')]
f=open('output.txt','w')
pred_flag=0
i=0
for string in lines:
	string = re.sub("[',+]",' ',string)
	string = re.sub('["]',' ',string)
	string=string.replace('  ',' ')
	string=string.replace('  ',' ')
	string=string.replace('  ',' ')
	space_pos=[m.start() for m in re.finditer(' ',string)]
	i=len(space_pos)
	cntr=0
	#print string
	#print space_pos
	twid=string[0:space_pos[cntr]]
	#print twid
	#print string[space_pos[cntr]+1]
	pred_politics=prior_politics
	pred_sports=prior_sports
	while(i>=2):
			temp=string[space_pos[cntr]+1:space_pos[cntr+1]]
			sport=count_word(temp,1)
			politic=count_word(temp,0)
			if sport==-1:
				pred='Sports'
				pred_flag=1
			elif politic==-1:
				pred='Politics'
				pred_flag=1
			else:	
				#print temp
				#print count_word(temp,1)
				pred_sports*=(sport+1)/((sports_count+vocab_size)*1.0)
				#print pred_sports
				pred_politics*=(politic+1)/((politics_count+vocab_size)*1.0)
				#print pred_politics
			cntr+=1
			i-=1
	temp=string[space_pos[cntr]+1:]
	print temp
	if sport== -1:
		pred='Sports'
		pred_flag=1		
	elif politic==-1:
		pred='Politics'
		pred_flag=1				
	else:
		pred_sports*=(sport+1)/((sports_count+vocab_size)*1.0)
		pred_politics*=(politic+1)/((politics_count+vocab_size)*1.0)
	
	if pred_flag ==0:
		final_pred='Sports' if pred_sports>pred_politics else 'Politics'
	else: 
		final_pred=pred
	out=twid+' '+final_pred 
	f.write(out)
	f.write('\n')

f.close()

