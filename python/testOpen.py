import os

def get_info():
	distinfo = {}
	if os.path.exists('/etc/lsb-release'):
		try:
		   with open('/etc/lsb-release') as lsb_release_file:
                	for line in lsb_release_file:
                    		line = line.strip()
                    		if not line:
                        		continue
                    		# Skip invalid lines
                    		if not '=' in line:
                        		continue
                    		var, arg = line.split('=', 1)
                    		if var.startswith('DISTRIB_'):
                        		var = var[8:]
                        		if arg.startswith('"') and arg.endswith('"'):
                            			arg = arg[1:-1]
                        		if arg: # Ignore empty arguments
                            			distinfo[var] = arg
		except IOError as msg:
			print('Unable to open /etc/lsb-release:')
	return distinfo

if __name__ == '__main__':
    info = get_info()
    print info['DESCRIPTION']

