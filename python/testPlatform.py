import getPlatform
import platform

lsbinfo = getPlatform.get_lsb_information()
print lsbinfo['DESCRIPTION']
os = platform.uname()

print os[2]

