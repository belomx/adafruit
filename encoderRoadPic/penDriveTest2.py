import os

path = os.path.abspath("/media/")

for dirname, dirnames, filenames in os.walk("/media"):
	isMountFounded = False
	for subdirname in dirnames:
		path = os.path.join(dirname, subdirname)
		if os.path.ismount(os.path.join(dirname, subdirname)):
			isMountFounded = True
			break
	if isMountFounded :
		break
	
print "the path = %s" %  path 
