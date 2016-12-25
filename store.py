import re
import os
import sys

print 'Input file path(.txt)'
path = raw_input()
try:
	f=open(path,'r')
except:
	sys.stderr.write('No file : %s\n' % path)
	exit(1)
file_name=path.rsplit('\\',1)[1].split('.')[0]
#os.system("curl -XDELETE http://127.0.0.1:9200/*")
count = 0
check_num=0
Is_issue = 0
value_t=['a']
type_t=['a']

while True:
	line = f.readline()
	if not line: break

	if re.search(r'[0-9]]',line):
		if count>0:
			command = """curl -H \"\"\"Content-Type: application/json\"\"\" -XPUT http://localhost:9200/"""+file_name+"""/checklist/"""+str(check_num)+"""?pretty -d \"{"""
			for i in range(1, len(type_t)):
				if i>1:
					command=command+","
				if value_t[i]=='':
					value_t[i]='_'
				command=command + """\"\"\""""+type_t[i]+"""\"\"\":\"\"\""""+value_t[i]+"""\"\"\""""
				

			command=command+"""}\""""	
			count=0	
		#	print command
			os.system(command)
			value_t[0:len(value_t)]=['a']
			type_t[0:len(type_t)]=['a']
		check_num=line[line.find('[',2)+1:line.find(']',3)]
		check_title=line.split(']')[2].strip()
		tmp = 'title'
		check_title=check_title.replace(' ','_')
		count+=1
		Is_issue=1
		value_t.append(check_title)
		type_t.append(tmp)
	if re.search(']', line):
		line = line.split(']')[1].strip()
		if line == 'HTTP request':
			type_=line.replace(' ','_')
			value_=''
			while True:
				line = f.readline()
				if line=='\n':
					break
				value_=value_+line
			value_=value_.replace(' ','_')
			value_=value_.replace('\n','__')
		
	
		if re.search(':', line):
			type_=line.split(':')[0].strip()
			value_=line.split(':')[1].strip()
			if Is_issue==1 and type_=='URL' or type_=='Referring page' or type_=='Affected page':				
				type_=type_.replace(' ','_')
				value_=line[line.find(':')+1:].strip()
				value_t.append(value_)
				type_t.append(type_)	
			elif type_=='All inputs' or type_=='Tags':
				value_ = line.split(':')[1].split(',')			
				temp = ''
				for i in range(0,len(value_)):
					value_[i]=value_[i].strip()
					if temp!='':
						temp=temp+','+value_[i]
					else:
						temp=value_[i]
				if type_=='All inputs':
					type_='All_inputs'

				value_t.append(temp)
				type_t.append(type_)	
			elif type_=='Description':
				line=f.readline()
				while True:
					line = f.readline()
					if re.search(']',line):
						break
					value_= value_+line
				value_=value_.strip()
				value_=value_.replace(' ','_')
				value_=value_.replace('\n','__')
				value_t.append(value_)
				type_t.append(type_)	
			
			elif type_=='References':
				temp =''
				while True:
					line = f.readline()
					if re.search('[*]',line):
						break
					if re.search('[~]',line):
						temp= temp+'-'+line.split('-')[1].strip()
				value_t.append(temp)
				type_t.append(type_)	
			elif type_=='Severity' or type_=='Digest' or type_=='Element' or type_=='Method':

			
				value_=line.split(':')[1].strip()
				value_t.append(value_)
				type_t.append(type_)				

			
if count>0:
			command = """curl -H \"\"\"Content-Type: application/json\"\"\" -XPUT http://localhost:9200/"""+file_name+"""/checklist/"""+str(check_num)+"""?pretty -d \"{"""
			for i in range(1, len(type_t)):
				if i>1:
					command=command+","
				if value_t[i]=='':
					value_t[i]='_'
				command=command + """\"\"\""""+type_t[i]+"""\"\"\":\"\"\""""+value_t[i]+"""\"\"\""""
				
			command=command+"""}\""""	
			os.system(command)
f.close()