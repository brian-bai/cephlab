# cephlab
ceph storage cluster lab

# step
- vagrant plugin install vagrant-persistent-storage
- vagrant up
- vagrant ssh cephnode1
- sudo cephadm bootstrap --mon-ip 192.168.56.11
```log
Ceph Dashboard is now available at:

	     URL: https://cephadmn1:8443/
	    User: admin
	Password: ch9txat658

Enabling client.admin keyring and conf on hosts with "admin" label
Saving cluster configuration to /var/lib/ceph/6c358b6a-3ab1-11ee-a3f3-aba1e693ae90/config directory
Enabling autotune for osd_memory_target
You can access the Ceph CLI as following in case of multi-cluster or non-default config:

	sudo /usr/sbin/cephadm shell --fsid 6c358b6a-3ab1-11ee-a3f3-aba1e693ae90 -c /etc/ceph/ceph.conf -k /etc/ceph/ceph.client.admin.keyring

Or, if you are only running a single cluster on this host:

	sudo /usr/sbin/cephadm shell

```
- change to : admin123
- # save passwd to file
- vagrant@cephadmn1:~$ vi password

- cp /etc/ceph/ceph.pub /vagrant/
- vagrant ssh cephnode2
- vagrant@cephadmn2:~$ sudo su -
- cat /vagrant/ceph.pub >> .ssh/authorized_keys
- same to cephnode3

- add hosts on dashboard
- add osds on dashboard
- add mds services on dashboard
- # wait for osds to up
- vagrant@cephadmn1:~$ sudo cephadm shell
```
root@cephadmn1:/# ceph osd pool create cephfs
pool 'cephfs' created
root@cephadmn1:/# ceph osd pool create cephfs_metadata
pool 'cephfs_metadata' created
root@cephadmn1:/# ceph fs new cephfs cephfs_metadata cephfs
new fs with metadata pool 3 and data pool 2
```
- # check pools on dashboard

- # suspend and resume
- vagrant suspend
- vagrant resume

root@cephadmn1:/# ceph mds stat
cephfs:1 {0=mds.cephadmn2.uxstvp=up:active} 2 up:standby

root@cephadmn1:/# ceph fs authorize cephfs client.fsuser / rw
[client.fsuser]
	key = AQBtudhk45uUIhAASYG8QJkLLVwAa0Xab+40rg==



dd if=/dev/zero of=1g.img bs=1 count=0 seek=1G 

# rados
sudo /usr/sbin/cephadm shell
root@cephadmn1:/# rados df
root@cephadmn1:/# rados -p cephfs ls 



# API
https://docs.ceph.com/en/pacific/rados/api/librados-intro/

client config:
vagrant@cephadmn1:~$ sudo cp /etc/ceph/ceph.client.admin.keyring /vagrant/
vagrant@cephclient:~$ sudo mkdir /etc/ceph/
vagrant@cephclient:~$ sudo cp /vagrant/ceph.client.admin.keyring /etc/ceph/
vagrant@cephclient:~$ sudo vi /etc/ceph/ceph.conf
[global]
mon host = 192.168.56.11
keyring = /etc/ceph/ceph.client.admin.keyring

vagrant@cephclient:~$ cp /vagrant/c-client-example.c ./
vagrant@cephclient:~$ gcc c-client-example.c -lrados -o c-client-example
vagrant@cephclient:~$ ./c-client-example
root@cephadmn1:/# rados -p cephfs ls




root@cephadmn1:/# rados bench -p cephfs 10 write -b 1M --no-cleanup
hints = 1
Maintaining 16 concurrent writes of 1048576 bytes to objects of size 1048576 for up to 10 seconds or 0 objects
Object prefix: benchmark_data_cephadmn1_202
  sec Cur ops   started  finished  avg MB/s  cur MB/s last lat(s)  avg lat(s)
    0       0         0         0         0         0           -           0
    1      16        32        16   15.8597        16    0.993707    0.528696
    2      16        56        40   19.8854        24    0.940467    0.620996
    3      16        71        55   18.2509        15     1.25059    0.716954
    4      16        96        80   19.9185        25     0.66672    0.737981
    5      16       117       101   20.1222        21    0.696608    0.733174
    6      16       143       127   21.0921        26    0.443357    0.731064
    7      16       163       147   20.9266        20    0.711145    0.725032
    8      16       182       166   20.6662        19       0.246    0.731547
    9      16       207       191    21.139        25    0.821806    0.729734
   10      15       229       214   21.3201        23    0.262785    0.722071
Total time run:         10.2509
Total writes made:      229
Write size:             1048576
Object size:            1048576
Bandwidth (MB/sec):     22.3395
Stddev Bandwidth:       3.86437
Max bandwidth (MB/sec): 26
Min bandwidth (MB/sec): 15
Average IOPS:           22
Stddev IOPS:            3.86437
Max IOPS:               26
Min IOPS:               15
Average Latency(s):     0.709479
Stddev Latency(s):      0.249555
Max latency(s):         1.52738
Min latency(s):         0.171154

root@cephadmn1:/# rados bench -p cephfs 10 write -b 3M --no-cleanup
hints = 1
Maintaining 16 concurrent writes of 3145728 bytes to objects of size 3145728 for up to 10 seconds or 0 objects
Object prefix: benchmark_data_cephadmn1_223
  sec Cur ops   started  finished  avg MB/s  cur MB/s last lat(s)  avg lat(s)
    0      16        16         0         0         0           -           0
    1      16        19         3   8.94104         9        0.64    0.527112
    2      16        25         9   13.4539        18     1.84201     1.06059
    3      16        28        12   11.9545         9     1.86667      1.1749
    4      16        32        16   11.9597        12    0.603741     1.52546
    5      16        39        23   13.7618        21     4.76442     2.16879
    6      16        46        30   14.9635        21     3.39258     2.24313
    7      16        54        38   16.2398        24     3.15693     2.42701
    8      16        60        44   16.4477        18     3.51704     2.44073
    9      16        67        51    16.945        21     3.45757     2.40873
   10      15        73        58   17.3337        21     1.84875     2.41009
Total time run:         10.6939
Total writes made:      73
Write size:             3145728
Object size:            3145728
Bandwidth (MB/sec):     20.4791
Stddev Bandwidth:       5.44059
Max bandwidth (MB/sec): 24
Min bandwidth (MB/sec): 9
Average IOPS:           6
Stddev IOPS:            1.81353
Max IOPS:               8
Min IOPS:               3
Average Latency(s):     2.27567
Stddev Latency(s):      1.33922
Max latency(s):         5.69941
Min latency(s):         0.470573


# Ceph File System mount
root@cephadmn1:/# ceph fs volume create myvol

root@cephadmn1:/# ceph fs flag set enable_multiple true

root@cephadmn1:/# ceph fs authorize cephfs client.foo / rw
[client.foo]
	key = AQCzGdtk9kVoDRAAZlqEturSncnBY/5aKHCRbQ==

vagrant@cephclient:~$ sudo vi /etc/ceph/ceph.client.foo.keyring
root@cephadmn1:/# sudo ceph config generate-minimal-conf
vagrant@cephclient:~$ sudo vi /etc/ceph/ceph.conf
vagrant@cephclient:~$ sudo chmod 644 /etc/ceph/ceph.conf

vagrant@cephclient:~$ sudo mkdir /mnt/mycephfs
vagrant@cephclient:~$ sudo apt-get -y install ceph-fuse
vagrant@cephclient:~$ sudo ceph-fuse --id foo /mnt/mycephfs

## create file
sudo dd if=/dev/zero of=1g.img bs=1 count=0 seek=100M

root@cephadmn1:/# ceph auth ls
root@cephadmn1:/# ceph auth get client.foo


sudo ceph fs authorize cephfs client.foo / rw
cephadmn1:6789,cephadmn2:6789,cephadmn3:6789:/ /cephfs ceph name=foo,secret=AQC8Kdtk2JMjChAAuDx45yofHxO12EtrCBZ7bg==,noatime,_netdev 0 2



vagrant@cephclient:~$ sudo cephfs-shell
CephFS:~/>>> mkdir mydir2
CephFS:~/>>> put 1g.img mydir/1g.img
CephFS:~/>>> ls -la mydir
drwxr-xr-x    104857600 0 0 2023-08-15 13:36:14 ./
drwxr-xr-x    104857600 0 0 2023-08-15 13:35:45 ../
-rw-rw-rw-    104857600 0 0 2023-08-15 13:36:17 1g.img
CephFS:~/>>> quit
vagrant@cephclient:~$ ls /cehpfs/
mydir  mydir2


vagrant up cephclient2

# pytorch deep learning sample

```
vagrant@cephclient:~$ sudo cp -r /vagrant/pytorch/data /cephfs/mydir2/
vagrant@cephclient:~$ ls /cephfs/mydir2/
vagrant@cephclient2:~$ ls /cephfs/mydir2/
vagrant@cephclient2:~$ sudo pip3 install torch torchvision --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple

```

```
vagrant@cephclient2:~$ python3 quick_example.py
# PermissionError: [Errno 13] Permission denied: '/cephfs/mydir2/data/FashionMNIST'
vagrant@cephclient2:~$ sudo python3 quick_example.py
#Shape of X [N, C, H, W]: torch.Size([64, 1, 28, 28])
#Shape of y: torch.Size([64]) torch.int64
```

```
vagrant@cephclient2:~$ df -h
Filesystem                                                  Size  Used Avail Use% Mounted on
udev                                                        466M     0  466M   0% /dev
/dev/sda1                                                    39G  7.6G   32G  20% /
vagrant-root                                                234G  167G   67G  72% /vagrant
192.168.56.11:6789,192.168.56.12:6789,192.168.56.13:6789:/  9.3G  180M  9.1G   2% /cephfs
tmpfs                                                        97M     0   97M   0% /run/user/1000
```

# rgw
- create rgw service on dashboard
- check service status
```
root@cephadmn1:/# ceph orch ls
NAME                               PORTS        RUNNING  REFRESHED  AGE  PLACEMENT
alertmanager                       ?:9093,9094      1/1  7m ago     12h  count:1
ceph-exporter                                       3/3  7m ago     12h  *
crash                                               3/3  7m ago     12h  *
grafana                            ?:3000           1/1  7m ago     12h  count:1
mds.mds                                             3/3  7m ago     11h  count:3;label:mds
mds.myvol                                           2/2  7m ago     21h  count:2
mgr                                                 2/2  7m ago     12h  count:2
mon                                                 3/5  7m ago     12h  count:5
node-exporter                      ?:9100           3/3  7m ago     12h  *
osd.dashboard-admin-1692025056629                     3  7m ago     11h  *
prometheus                         ?:9095           1/1  7m ago     12h  count:1
rgw.myrgw                          ?:8000           3/3  7m ago     8m   count:3;label:rgw
root@cephadmn1:/#

root@cephadmn1:/# radosgw-admin zone get --rgw-zone=default

```
- validate rgw access
```
vagrant@cephclient2:~$ curl http://192.168.56.11:8000/
<?xml version="1.0" encoding="UTF-8"?><ListAllMyBucketsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>anonymous</ID><DisplayName></DisplayName></Owner><Buckets></Buckets></ListAllMyBucketsResult>
```

- create rgw user
```
root@cephadmn1:/# radosgw-admin user create --uid="wgs" --display-name="wgs"
{
    "user_id": "wgs",
    "display_name": "wgs",
    "email": "",
    "suspended": 0,
    "max_buckets": 1000,
    "subusers": [],
    "keys": [
        {
            "user": "wgs",
            "access_key": "867564SZSW7XZJ9XFT97",
            "secret_key": "XfeIBhDw3IZJGd67H3UjY8vYhdzFF9Ot4EJPABmM"
        }
    ],
    "swift_keys": [],
    "caps": [],
    "op_mask": "read, write, delete",
    "default_placement": "",
    "default_storage_class": "",
    "placement_tags": [],
    "bucket_quota": {
        "enabled": false,
        "check_on_raw": false,
        "max_size": -1,
        "max_size_kb": 0,
        "max_objects": -1
    },
    "user_quota": {
        "enabled": false,
        "check_on_raw": false,
        "max_size": -1,
        "max_size_kb": 0,
        "max_objects": -1
    },
    "temp_url_keys": [],
    "type": "rgw",
    "mfa_ids": []
}
```

### s3cmd refer to https://www.cnblogs.com/wangguishe/p/15666853.html
```
vagrant@cephclient2:~$ sudo apt -y install s3cmd

vagrant@cephclient2:~$ sudo vi /etc/hosts
# rgw
192.168.56.11 rgw.wgs.com

vagrant@cephclient2:~$ sudo s3cmd --configure
# S3 Endpoint [s3.amazonaws.com]: rgw.wgs.com:8000
vagrant@cephclient2:~$ sudo vi /root/.s3cfg
#host_base = rgw.wgs.com:8000
#host_bucket = rgw.wgs.com:8000/%(bucket)

vagrant@cephclient2:~$ sudo cat /root/.s3cfg
vagrant@cephclient2:~$ sudo s3cmd mb s3://wgsbucket
Bucket 's3://wgsbucket/' created

vagrant@cephclient2:~$ sudo s3cmd ls s3:/
2023-08-16 03:09  s3://wgsbucket

root@cephadmn1:/# radosgw-admin bucket list
[
    "wgsbucket"
]

vagrant@cephclient2:~$ sudo pip3 install boto3 --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple

```

