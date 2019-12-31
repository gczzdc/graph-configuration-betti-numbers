import subprocess
from constants import host, remote_directory, loud_commands


def run(whatever, loud=loud_commands):
	#this is a dangerous command
	if loud:
		print (whatever)
	process = subprocess.run(' '.join(whatever), shell=True, capture_output=True)
	output = process.stdout
	error = process.stderr
	if loud and output:
		print ('output:\n',output)
	if loud and error:
		print ('error:\n',error)

def scp(file_name, loud_commands=loud_commands):
	run(('sftp', host + remote_directory, "<<<", "$'put " + file_name+"\nexit'"))
