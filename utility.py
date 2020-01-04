import subprocess
from constants import host, remote_directory, loud_commands


def run(whatever, loud=loud_commands):
	#this is a dangerous command
	if loud:
		print (whatever,end='\n\n')
	process = subprocess.run(' '.join(whatever), shell=True, capture_output=True)
	if loud:
		print(process, end='\n\n\n')


def scp(file_name, loud_commands=loud_commands, subdirectory=None):
	if subdirectory:
		formatted_subdirectory = '/{}'.format(subdirectory)
	else:
		formatted_subdirectory = ''
	run(('sftp', 
			host + remote_directory + formatted_subdirectory, 
			"<<<", 
			"$'put {}\nexit'".format(file_name)), 
		loud_commands)
