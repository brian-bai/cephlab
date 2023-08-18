## vms setup
### set /etc/hosts for all hosts
```
192.168.56.4    cephnode1

192.168.56.5    cephnode2

192.168.56.6    cephnode3

192.168.56.7    cephapp1

192.168.56.8    cephapp2
```

### enable ssh access
```
[root@cephnode1 ~]# ssh-keygen
[root@cephnode1 ~]# ssh-copy-id cephnode2
[root@cephnode1 ~]# ssh-copy-id cephnode3

```
### change repos
```
sudo rm /etc/yum.repos.d/*.repo
sudo wget -O /etc/yum.repos.d/CentOS-Linux-BaseOS.repo https://mirrors.aliyun.com/repo/Centos-8.repo
sudo sed -i -e '/mirrors.cloud.aliyuncs.com/d' -e '/mirrors.aliyuncs.com/d' /etc/yum.repos.d/CentOS-Linux-BaseOS.repo
```
Or with ansible playbook:
```
ansible-playbook -i inventory.yaml replace-repo-playbook.yml -K -u vagrant
```

### preflight packages on all cephnodes
```
yum -y install python3
yum -y install podman
yum -y install lvm2
```
Or with ansible playbook:
```
# repos replace and packages install
 ansible-playbook -i inventory.yaml myceph-preflight.yml -K -u vagrant
```


## cephadm install
(On [root@cephnode1 ~]$)

### step1 check ntp service is on
```
timedatectl
```
### step2 check centos version
```
cat /etc/centos-release
```
### step3 cephadm install
```
curl --silent --remote-name --location https://github.com/ceph/ceph/raw/quincy/src/cephadm/cephadm
chmod +x cephadm
./cephadm add-repo --release quincy
./cephadm install
```

### step4 bootstrap
```
cephadm bootstrap --mon-ip 192.168.56.4
```

output:
```
[root@cephnode1 ~]# cephadm bootstrap --mon-ip 192.168.56.4
Creating directory /etc/ceph for ceph.conf
Verifying podman|docker is present...
Verifying lvm2 is present...
Verifying time synchronization is in place...
Unit chronyd.service is enabled and running
Repeating the final host check...
podman (/usr/bin/podman) version 3.3.1 is present
systemctl is present
lvcreate is present
Unit chronyd.service is enabled and running
Host looks OK
Cluster fsid: 54bf5dbc-3cfa-11ee-a8d9-080027f1cae4
Verifying IP 192.168.56.4 port 3300 ...
Verifying IP 192.168.56.4 port 6789 ...
Mon IP `192.168.56.4` is in CIDR network `192.168.56.0/24`
Mon IP `192.168.56.4` is in CIDR network `192.168.56.0/24`
Internal network (--cluster-network) has not been provided, OSD replication will default to the public_network
Pulling container image quay.io/ceph/ceph:v17...
Ceph version: ceph version 17.2.6 (d7ff0d10654d2280e08f1ab989c7cdf3064446a5) quincy (stable)
Extracting ceph user uid/gid from container image...
Creating initial keys...
Creating initial monmap...
Creating mon...
Waiting for mon to start...
Waiting for mon...
mon is available
Assimilating anything we can from ceph.conf...
Generating new minimal ceph.conf...
Restarting the monitor...
Setting mon public_network to 192.168.56.0/24
Wrote config to /etc/ceph/ceph.conf
Wrote keyring to /etc/ceph/ceph.client.admin.keyring
Creating mgr...
Verifying port 9283 ...
Waiting for mgr to start...
Waiting for mgr...
mgr not available, waiting (1/15)...
mgr not available, waiting (2/15)...
mgr not available, waiting (3/15)...
mgr not available, waiting (4/15)...
mgr is available
Enabling cephadm module...
Waiting for the mgr to restart...
Waiting for mgr epoch 5...
mgr epoch 5 is available
Setting orchestrator backend to cephadm...
Generating ssh key...
Wrote public SSH key to /etc/ceph/ceph.pub
Adding key to root@localhost authorized_keys...
Adding host cephnode1...
Deploying mon service with default placement...
Deploying mgr service with default placement...
Deploying crash service with default placement...
Deploying ceph-exporter service with default placement...
Deploying prometheus service with default placement...
Deploying grafana service with default placement...
Deploying node-exporter service with default placement...
Deploying alertmanager service with default placement...
Enabling the dashboard module...
Waiting for the mgr to restart...
Waiting for mgr epoch 9...
mgr epoch 9 is available
Generating a dashboard self-signed certificate...
Creating initial admin user...
Fetching dashboard port number...
Ceph Dashboard is now available at:

             URL: https://cephnode1:8443/
            User: admin
        Password: ofc0r59hu5

Enabling client.admin keyring and conf on hosts with "admin" label
Saving cluster configuration to /var/lib/ceph/54bf5dbc-3cfa-11ee-a8d9-080027f1cae4/config directory
Enabling autotune for osd_memory_target
You can access the Ceph CLI as following in case of multi-cluster or non-default config:

        sudo /usr/sbin/cephadm shell --fsid 54bf5dbc-3cfa-11ee-a8d9-080027f1cae4 -c /etc/ceph/ceph.conf -k /etc/ceph/ceph.client.admin.keyring

Or, if you are only running a single cluster on this host:

        sudo /usr/sbin/cephadm shell

Please consider enabling telemetry to help improve Ceph:

        ceph telemetry on

For more information see:

        https://docs.ceph.com/docs/master/mgr/telemetry/

Bootstrap complete.
```

### change dashboard password
```
         URL: https://cephnode1:8443/
        User: admin
        Password: ofc0r59hu5
    change to: admin123
```

## cluster setup
### step1 add hosts
- enable ssh access to hosts
```
[root@cephnode1 ~]# ssh-copy-id -f -i /etc/ceph/ceph.pub root@cephnode2
[root@cephnode1 ~]# ssh-copy-id -f -i /etc/ceph/ceph.pub root@cephnode3
```


- add hosts from dashboard
```
Hostname: cephnode2
Network address: 192.168.56.5
Labels: grafana mds mgr mon osd rgw

Hostname: cephnode3
Network address: 192.168.56.6
Labels: mds mgr mon osd rgw _admin
```
- add labels to centnode1
```
Labels: mds mgr mon osd rgw _admin 
```

```
[ceph: root@cephnode1 /]# ceph cephadm check-host cephnode2 192.168.56.5
cephnode2 (192.168.56.5) ok
podman (/usr/bin/podman) version 3.3.1 is present
systemctl is present
lvcreate is present
Unit chronyd.service is enabled and running
Hostname "cephnode2" matches what is expected.
Host looks OK

[ceph: root@cephnode1 /]# ceph orch ls --refresh
```

### step2 create osds

```
Primary devices +Add
Filter with type: hdd
```

### step3 create services
```
mds
rgw
```

### step4 create ceph file system
```
[vagrant@centnode1 ~]$ sudo cephadm shell
[ceph: root@centnode1 /]# ceph fs ls
No filesystems enabled
[ceph: root@centnode1 /]# ceph fs volume create mycephfs
[ceph: root@centnode1 /]# ceph fs ls
name: mycephfs, metadata pool: cephfs.mycephfs.meta, data pools: [cephfs.mycephfs.data ]
[vagrant@cephnode1 ~]$ sudo cephadm shell ceph fs authorize mycephfs client.foo / rw | sudo tee /etc/ceph/ceph.client.foo.keyring
```

### mount fs
```
# dispatch ceph.conf and ceph.client.foo.keyring
ansible-playbook -i inventory.yaml dispatch-conf-playbook.yml -K -u vagrant
# mount on app1 & app2
[vagrant@cephapp2 ~]$ sudo mkdir /mnt/mycephfs
[vagrant@cephapp2 ~]$ sudo mount -t ceph foo@.mycephfs=/ /mnt/mycephfs
```
## client setup on 
 
```
ansible-playbook -i inventory.yaml myceph-preflight.yml -K -u vagrant
```