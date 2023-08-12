# cephlab
ceph storage cluster lab

# step
- vagrant up
- vagrant ssh storage01
- sudo cephadm bootstrap --mon-ip 192.168.56.4
```log
Ceph Dashboard is now available at:

	     URL: https://cephadmn1:8443/
	    User: admin
	Password: iwpiu6ylo6
    Enabling client.admin keyring and conf on hosts with "admin" label
Enabling autotune for osd_memory_target
You can access the Ceph CLI as following in case of multi-cluster or non-default config:

	sudo /usr/sbin/cephadm shell --fsid 059e4c44-3907-11ee-b143-957635158a07 -c /etc/ceph/ceph.conf -k /etc/ceph/ceph.client.admin.keyring

Or, if you are only running a single cluster on this host:

	sudo /usr/sbin/cephadm shell

Please consider enabling telemetry to help improve Ceph:

	ceph telemetry on

For more information see:

	https://docs.ceph.com/en/pacific/mgr/telemetry/

```
- change to : admin123
- # save passwd to file
- vagrant@cephadmn1:~$ vi password

- cp /etc/ceph/ceph.pub /vagrant/
- vagrant ssh storage02
- vagrant@cephadmn2:~$ sudo su -
- cat /vagrant/ceph.pub >> .ssh/authorized_keys
- same to storage03

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