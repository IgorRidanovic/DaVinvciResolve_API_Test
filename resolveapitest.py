#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This script tests Resolve 15 scripting API on MacOS.
# We suspect an issue with import of fusionscript.so.
# To test launch Resolve Studio first and then run this script.
# The script will save a text report.
# igor@hdhead.com

from datetime import datetime
import os
import sys
import imp

# Exit if not MacOS
if 'darwin' not in sys.platform:
	sys.exit('This script is for use on Mac only.')

eol = '\n'
pathLib = '/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so'

# Create initial report file. It will overwrite existing!
reportName = 'Resolve_API_Report.txt'
reportPath = os.path.join('.', reportName)
reportfile = open(reportPath, 'w')
reportfile.close()

def report(entry):
	# Print to console
	print entry

	# Write a report entry
	reportfile = open(reportPath, 'a')
	reportfile.write(entry)
	reportfile.write(eol)
	reportfile.close()

# These are the values we'll discover and save
report('Time: ' + str(datetime.now()))
report('Hostname: ' + os.uname()[1])
report('Python Version: ' + sys.version)
report('Interpreter Path: ' + sys.executable)
report('___________________________________' + eol)

report('If no lines follow we have likely experienced a Fatal Python Error.')

try:
	# Will the API library import? Does it exist?
	smodule = imp.load_dynamic('fusionscript', pathLib)
	report('Imported fusionscript.so')

	# It looks like the library imported. Can we create a resolve instance now?
	try:
		resolve = smodule.scriptapp('Resolve')
		if 'None' in str(type(resolve)):
			report('Resolve instance is created, but Resolve is not found.')
			sys.exit()
		if 'PyRemoteObject' in str(type(resolve)):
			report('Resolve instance is created and Resolve is responsive.')
	except Exception, e:
		report(str(e))

	# Let's go nuts and count how many projects are in the Project Manager
	try:
		projman  = resolve.GetProjectManager()
		projects = projman.GetProjectsInCurrentFolder()
		report('Project Count: ' + str(len(projects)))
		report('All is well!')
	except Exception, e:
		report(str(e))

except Exception, e:
	report(str(e))
