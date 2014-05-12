import os
from collections import namedtuple

disk_ntuple = namedtuple('partition',  'device mountpoint fstype')
usage_ntuple = namedtuple('usage',  'total used free percent')
stat_ntuple = namedtuple('w', 'x y z')

def disk_partitions(all=False):
    """Return all mountd partitions as a nameduple.
    If all == False return phyisical partitions only.
    """
    phydevs = []
    f = open("/proc/filesystems", "r")
    for line in f:
        if not line.startswith("nodev"):
            phydevs.append(line.strip())

    retlist = []
    f = open('/etc/mtab', "r")
    for line in f:
        if not all and line.startswith('none'):
            continue
        fields = line.split()
        device = fields[0]
        mountpoint = fields[1]
        fstype = fields[2]
        if not all and fstype not in phydevs:
            continue
        if device == 'none':
            device = ''
        ntuple = disk_ntuple(device, mountpoint, fstype)
        retlist.append(ntuple)
    return retlist

def disk_usage(path):
    """Return disk usage associated with path."""
    st = os.statvfs(path)
    free = (st.f_bavail * st.f_frsize) / 1073741824
    total = (st.f_blocks * st.f_frsize) / 1073741824
    used = ((st.f_blocks - st.f_bfree) * st.f_frsize) / 1073741824
    try:
        percent = ret = (float(used) / total) * 100
    except ZeroDivisionError:
        percent = 0
    # NB: the percentage is -5% than what shown by df due to
    # reserved blocks that we are currently not considering:
    # http://goo.gl/sWGbH
    # return usage_ntuple(total, used, free, round(percent, 1))
    
    return stat_ntuple(path,total,(round(percent,0)))

if __name__ == '__main__':
    for part in disk_partitions():
    #   print part
        pt1 = disk_usage(part.mountpoint)
    #   print "    %s\n" % str(disk_usage(part.mountpoint))
        print pt1.x
 	print pt1.y
	print pt1.z


