import subprocess
from constants import portscp, host, remote_directory, loud_commands


def run(whatever, loud=loud_commands):
	if loud:
		print (whatever)
	output=subprocess.getoutput(whatever)
	if loud and output:
		print (output)

def scp(file_name, loud_commands=loud_commands):
	run('sftp'+portscp+' '+host + remote_directory + " <<< $'put " + file_name+"\nexit'", loud_commands)
