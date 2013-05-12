#!/usr/bin/env python3
#
# ggit is a simple tool for seeing what git projects you have
#
# (c) benjamin.naecker@gmail.com 2013
'''ggit version 0.1
know thy git
(C) 2013 benjamin.naecker@gmail.com
'''
# printing constants
bold = '\033[1m'
under = '\033[4m'
norm = '\033[0m'

def findRepos(startpath):
	'''initialize ggit, finding the location of all git
	repos and putting them into ~/.ggit/repolist.txt'''

	# for a modicum of safety, let's check that the input is actually a path!
	if not pathSafe(startpath):
		print('sorry that ain\'t gonna work')
		sys.exit()

	# check if startpath is parent of ~, ask if require sudo
	if not fileOwner(startpath):
		print('you don\'t own the requested start path.')
		print('can\'t deal with this yet')
		sys.exit()
		
	# open the repolist file, just overwrite for now
	repolist = open(path.expanduser('~/.ggit/repolist.txt'), 'w')

	# notify
	sys.stdout.write('\rfinding all your git repos. this may take a second ... ')
	sys.stdout.flush()

	# execute find command as explicity shell function
	proc = sp.call(['find', startpath, '(', '(', '-path', '*.git', 
		')', '-and', '!', '(', '-path', '*Mail*', ')', ')'], stdout=repolist)

	# close and notify
	repolist.close()
	sys.stdout.write('done\n')

def pathSafe(p):
	'''sanitize user input'''
	# check that it's actually a path!
	# for now...may want to sanitize more in future
	return path.exists(p)

def fileOwner(f):
	'''check if the file f is owned by the user'''
	from os import stat, getuid
	return stat(startpath).st_uid == getuid()

def listRepos(abbrev=False):
	'''list all found git repos

	input:
		abbrev - print short pathor absolute path
	output:
		prints some repos
	'''

	print('\nyou have git repos in the following locations:\n')
	repolist = open(path.expanduser('~/.ggit/repolist.txt'), 'r')
	for line in repolist.readlines():
		if abbrev:
			repoStr = line.split('/')[-3] + '/' + line.split('/')[-2]
			print(repoStr)
		else:
			print(line.rstrip('.git\n'), end='\n')
	repolist.close()
	print('')

def getObjects(repodir):
	'''gets all the objects in the git repository

	input: repodir - the absolute path of the git repository
	output: a list with the hash value for each object
	'''
	# this should be fucking illegal
	objects = [si + oi for si in listdir(path.join(repodir, 'objects'))
			for oi in listdir(path.join(repodir, 'objects', si)) 
			if si not in ['pack', 'refs']]
	return objects

def countObjects(otype):
	'''count objects of the given type'''
	# load repolist, needed for erthang
	fid = open(path.expanduser('~/.ggit/repolist.txt'), 'r')

	# make a list of the repos
	repolist = [r.rstrip('\n') for r in fid.readlines()]

	# close that ish
	fid.close()

	if otype == 'repo':
		# just count number of repos
		print('you have {c} git repositories in your system'.format(
			c=len(repolist)))

	elif otype in ['commit', 'tree', 'blob']:

		# print some top-level stuff
		print('\n' + under + 'repo' + norm.ljust(40) + under + '# ' + otype + 's' + norm.ljust(40))

		# loop over repositories
		totalObjects = 0
		originalDir = path.curdir
		for repo in repolist:
			# change dir to this repo, so I can call 'git cat-file'
			chdir(repo)
			
			# get the objects in this repository
			objects = getObjects(repo)

			# use 'git cat-file' to determine the object type
			objecttypes = [sp.Popen(['git', 'cat-file', '-t', obj], 
				stdout=sp.PIPE).stdout.readline().decode().rstrip('\n') 
				for obj in objects]

			# count the number of commits
			numObjects = objecttypes.count(otype)
			totalObjects += numObjects

			# print
			repoStr = repo.split('/')[-3] + '/' + repo.split('/')[-2]
			print(repoStr.ljust(40), numObjects)

		# print the total number of objects
		print('\n' + bold + 'total' + norm.ljust(40) + bold + 
				str(totalObjects) + norm.ljust(40) + '\n')
		
		# change dir back
		chdir(originalDir)

	elif otype in ['branch', 'tag']:
		# print some top-level stuff
		if otype == 'branch': 
			ex = 'e' 
			dirname = 'heads'
		else: 
			ex = ''
			dirname = 'tags'
		print('\n' + under + 'repo' + norm.ljust(40) + under + '# ' + 
				otype + ex + 's' + norm.ljust(40))

		# loop over repositories
		totalObjects = 0
		for repo in repolist:
			# just get the number of files in .git/refs/heads
			numObjects = len(listdir(path.join(repo, 'refs', dirname)))

			# update total objects
			totalObjects += numObjects

			# print
			repoStr = repo.split('/')[-3] + '/' + repo.split('/')[-2]
			print(repoStr.ljust(40), numObjects)

		# print the total number of objects
		print('\n' + bold + 'total' + norm.ljust(40) + bold + 
				str(totalObjects) + norm.ljust(40) + '\n')
		
def printUsage(verb):
	'''print usage info'''
	if verb == 'general':
		print('\nusage: ggit <verb> [options]\n')
		print('verbs:')
		print('  help\t\tprint this help and exit')
		print('  find\t\tfind all git repositories')
		print('  list\t\tlist all git repositories')
		print('  count <type>\tcount git objects of the given type\n')
	elif verb == 'find':
		print('\nfind all git repositories')
		print('usage: ggit find [startpath]')
		print('{u}startpath{n} is the location at which to start searching\n'.format(
			u=under, n=norm))
		print('requires sudo if below ~')
	elif verb == 'list':
		print('\nlist all found git repos\n')
	elif verb == 'count':
		print('\ncount up git objects of the given type')
		print('usage: ggit count [type]')
		print('{u}type{n} can be any of {u}repo{n}, \
{u}branch{n}, {u}tag{n}, {u}commit{n}, {u}tree{n}, or {u}blob{n}. defaults to {u}repo{n}\n'.format(
			u=under, n=norm))
		
if __name__ == '__main__':
	from os import path, sys, listdir, chdir
	import subprocess as sp

	# parse commands!
	if len(sys.argv) == 1:
		printUsage('general')
		sys.exit()
	else:
		nargs = len(sys.argv)
		verb = sys.argv[1]
		opts = sys.argv[2:]
	
	if verb in ['-v', '--version']:
		print('')
		print(__doc__)

	elif verb == 'help':
		if nargs == 2:
			helpVerb = 'general'
		else:
			helpVerb = opts[0]
		printUsage(helpVerb)

	elif verb == 'find':
		# parse startpath
		if nargs == 2:
			# no startpath given, assume ~
			startpath = path.expanduser('~')
		else:
			startpath = path.expanduser(opts[0])

		# make sure it exists
		if not path.exists(startpath):
			print('sorry. requested startpath {p} doesn\'t exist'.format(
				p=startpath))
			sys.exit()

		# find
		findRepos(startpath)

	elif verb == 'list':
		# check for repolist
		if not path.exists(path.expanduser('~/.ggit/repolist.txt')):
			print('repolist doesn\'t exist. call \'ggit find\' first')
			sys.exit()

		# check for abbrev
		if len(opts) == 0:
			abbrev = False
		else:
			if opts[0] in ['-a', '--abbrev']:
				abbrev = True
			else:
				abbrev = False
		
		# list em
		listRepos(abbrev)

	elif verb == 'count':
		if len(opts) == 0:
			otype = 'repo'
		else:
			otype = opts[0]
		countObjects(otype)

	elif verb == 'stats':
		# wil compute some stats, maybe? like what?
		'''compute stats'''
	else:
		print('unknown command: ' + sys.argv[1])

	# exit
	sys.exit()
