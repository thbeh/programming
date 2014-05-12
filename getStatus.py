import getDiskUsage

for part in getDiskUsage.disk_partitions():
    pt1 = getDiskUsage.disk_usage(part.mountpoint)
    print pt1.x
    print pt1.y
    print pt1.z

