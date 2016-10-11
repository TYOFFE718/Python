#!/bin/env python

import os, sys, paramiko, argparse, subprocess,re 
from datetime import date,timedelta
from time import strftime



""" parseWebLogs - parse web server logs 
	Description: This script will retrieve and parse logs for a given day.
	
	-c|--config <file> 		Parse this configuration file
	-d|--date <YYYYMMDD> 	Date override.
	-h|--help 				Output help.
	-v|--version			Output version.
"""

# set debug
debug = 1

# error class
class logerrors(Exception): pass

### methods
## readconfig(file) - parse this config file
def readconfig(file):
	config = dict()
	findComment = re.compile('#')
	try:
		if debug == 1:
			print "Reading configuration file: ", file
		f = open(file)
		for line in f:
			line = line.rstrip('\r\n')
			item = line.split('=')
			if findComment.match(item[0]):
				continue
			else:
				config.update({item[0]: item[1]})
		f.close
	except IOError as e:
		if debug == 1:
			raise logErrors("IOError: %s"  %e)
			exit(1)
		else:
			print "Error reading configuration file: ", file
			exit(1)
	return config
			
## getservers(domain name) - get servers for specific domain from instance listing
def getservers(environ):
	command = "/opt/aws/ec2-describe-instances --hide-tags -F 'instance-state-name=running' -F 'tag:domain=" + environ + "'"
	servers = list()
	try:
		# run the aws command to get server listings
		cmd = subprocess.Popen(command, shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		out,err = cmd.communicate()
		# regex and parse
		internal = re.compile('.internal$')
		s = out.split('\t')
		for item in s:
			if internal.match(item):
				servers.append(item)
		return servers		
	except:
		if debug == 1:
			error = command, "failed to run with output: ", err
			raise logErrors(error)
			exit(1)
		else:
			print "Unable to run", command
			exit(1)
## setdate() - set the date to prior date.
def setdate():
	yesterday = date.today() - timedelta(days=1)
	dayToStr = yesterday.strftime('%Y.%m.%d')
	if debug == 1:
		print "Setting date to", daytoStr, ".  Original date: ", yesterday
	return dayToStr	
## checkdir(directory) - make sure the log dirs exist.  If not create
def checkdir(directory):
	if os.path.isdir(directory):
		print directory, "found.  Continuing."
	else:	
		try:
			print "Creating ", directory
			os.mkdir(directory,0755)
			return
		except OSError as e:
			if debug == 1:
				raise logErrors("OSError: " % e)
				exit(1)
			else:
				print "Unable to create directory."
				exit(1)
## getlogs(servers,date) - get logs for the date specified from passed servers.
def getlogs(servers,logdate):
	# some basic stuff
	port = 22
	key = paramiko.DSSKey.from_private_key_file(cfgItems['sshKey'])
	logname = "/access." + logdate
	accesslog = cfgItems['weblogdir'] + logname
	loglist = list()
	try:
		for server in servers:
			print "Getting logs for ", server
			sshlog = cfgItems['logDir'] + server + ".ssh.log"
			localog = cfgItems['weblogdir'] + logname + "." + server
			paramiko.util.log_to_file(sshlog)
			if debug == 1:
				print "Connection: ", cfgItems['sshUser'], "@", server, "."
				print "Using key: ", key, "."
			transport = paramiko.SSHClient()
			transport.set_missing_host_key_policy(paramiko.AutoAddPolicy())		
			transport.connect(server,username = cfgItems['sshUser'], pkey = key)
			sftp = transport.open_sftp()
			sftp.get(accesslog,localog)
			sftp.close
			transport.close
			loglist.append(localog)
			return loglist
	except IOError as e:
		if debug == 1:
			raise logErrors("SSH Error: %s" % e)
			exit(1)
		else:
			print "SSH Error: ", e 
			exit(1)
	except paramiko.AuthenticationException as e:
		if debug == 1:
			raise logErrors("SSH Error: %s" % e)
			exit(1)
		else:	
			print "SSH Error: ", e
			exit(1)
## parselogs(loglist) - parse the passed logs into awstats
def parselogs(logs,domain):
	for log in logs:
		if os.path.isFile(log):
			print "Will merge ", log
			l.append(log)
		else:
			print "Warning: ", log, "does not exist.  Skipping."
	# log merge command		
	merge = '/usr/local/awstats/tools/logresolve.pl' + logs
	# log parse command
	logparse = '/usr/local/awstats/wwwroot/cgi-bin/awstats.pl -update -config=' + domain
	# merge logs
	cmd = subprocess.Popen(merge,shell=True, stdout=cfgItems['mergeLog'])
	# parse logs 
	pcmd = subprocess.Popen(logparse,shell=True, stdout=cfgItems['parseLog'], stderr=['parseErr'])
	ret_code = pcmd.wait()
	return ret_code
	
### do stuff
parser = argprase.ArgumentParser()
parser.add_argument("-c","--config",help="<file> to load for runtime configuration",required=True)
parser.add_argument("-d","--date",help="Date to parse.  YYYYMMMDD.  Default is previous day",required=False)
parser.add_argument("-v","--version",help="Print out version",action="store_true")
args = parser.parse_args()

## output version
if arg.version:
	print "Version:", __version__
	exit(0)

## read in configuration file	
if args.config:
	if os.path.isFile(args.config):
		cfgItems = readconfig(args.config)
	else:
		error = "Cannot find", args.config, "for reading."
		exit(1)
## set date
if args.date:
	runday = args.date 
else:
	runday = setdate()

# now run what we need	
serverList = getservers(cfgItems['domain'])	
checkdir(cfgItems['logdir'])
getlogs(serverList,runday)
#parselogs(loglist)
print "Log parsing completed for domain: ", cfgItems['domain']
print "The following servers were parsed: ", serverList
exit(0)
