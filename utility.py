import subprocess
from constants import host, remote_directory, loud_commands


def run(whatever, loud=loud_commands):
	#this is a dangerous command
	if loud:
		print (whatever,end='\n\n')
	process = subprocess.run(' '.join(whatever), shell=True, capture_output=True)
	if loud:
		print(process, end='\n\n\n')


def scp(file_name, loud_commands=loud_commands):
	run(('sftp', host + remote_directory, "<<<", "$'put " + file_name+"\nexit'"), loud_commands)
