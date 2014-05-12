import platform
import sys
import os
import re
import subprocess

def get_lsb_information():
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
            print('Unable to open /etc/lsb-release:', str(msg))
            
    return distinfo

def get_distro_information():
    lsbinfo = get_lsb_information()
    # OS is only used inside guess_debian_release anyway
    for key in ('ID', 'RELEASE', 'CODENAME', 'DESCRIPTION',):
        if key not in lsbinfo:
            distinfo = guess_debian_release()
            distinfo.update(lsbinfo)
            return distinfo
    else:
        return lsbinfo


def linux_distribution():
  try:
    return platform.linux_distribution()
  except:
    return "N/A"

if __name__ == '__main__':
	os = platform.uname()
	dist = platform.dist()
	print(get_distro_information())
	print dist[0]+' '+dist[1]
	print os[2]

	print("""Python version: %s
	dist: %s
	linux_distribution: %s
	system: %s
	machine: %s
	platform: %s
	uname: %s
	version: %s
	mac_ver: %s
	""" % (
	sys.version.split('\n'),
	str(platform.dist()),
	linux_distribution(),
	platform.system(),
	platform.machine(),
	platform.platform(),
	platform.uname(),
	platform.version(),
	platform.mac_ver(),
	))
