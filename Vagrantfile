# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "bento/centos-8"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Disable the default share of the current code directory. Doing this
  # provides improved isolation between the vagrant box and your host
  # by making sure your Vagrantfile isn't accessable to the vagrant box.
  # If you use this you may want to enable additional shared subfolders as
  # shown above.
  # config.vm.synced_folder ".", "/vagrant", disabled: true

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    #vb.gui = true
  
    # Customize the amount of memory on the VM:
    vb.memory = "2048"
  end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL

  config.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: false, mount_options: ["dmode=770,fmode=664"]


  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true
  config.hostmanager.ignore_private_ip = false
  config.hostmanager.include_offline = true
 

 
  config.vm.define "cephnode1" do |s1|
    s1.vm.hostname = "cephnode1"
	  storage = "storage01.vdi"

	  s1.persistent_storage.enabled = true
	  s1.persistent_storage.location = "./storage01.vdi"
	  s1.persistent_storage.size = 10000
	  s1.persistent_storage.partition = false
	  s1.persistent_storage.volgroupname = 'storage01'
	  s1.persistent_storage.diskdevice = '/dev/sdc'
	
	  s1.persistent_storage.use_lvm = false

	  s1.vm.network "private_network", ip: "192.168.56.4"
    s1.vm.network :forwarded_port, guest: 8443, host:8443
    # s1.vm.provision "shell", path: "cephadm_install.sh"
  end
  config.vm.define "cephnode2" do |s2|
    s2.vm.hostname = "cephnode2"
  	s2.persistent_storage.enabled = true
	  s2.persistent_storage.location = "./storage02.vdi"
	  s2.persistent_storage.size = 10000
	  s2.persistent_storage.partition = false
	  s2.persistent_storage.volgroupname = 'storage02'
	  s2.persistent_storage.diskdevice = '/dev/sdc'
	  s2.persistent_storage.use_lvm = false
	  s2.vm.network "private_network", ip: "192.168.56.5"
    # s2.vm.provision "shell", inline: "apt install -y chrony"
    # s2.vm.provision "shell", path: "docker_install.sh"
  end
  config.vm.define "cephnode3" do |s3|
    s3.vm.hostname = "cephnode3"
  	s3.persistent_storage.enabled = true
	  s3.persistent_storage.location = "./storage03.vdi"
	  s3.persistent_storage.size = 10000
	  s3.persistent_storage.partition = false
	  s3.persistent_storage.volgroupname = 'storage01'
	  s3.persistent_storage.diskdevice = '/dev/sdc'
	  s3.persistent_storage.use_lvm = false
	  s3.vm.network "private_network", ip: "192.168.56.6"
    # s3.vm.provision "shell", inline: "apt install -y chrony"
    # s3.vm.provision "shell", path: "docker_install.sh"
  end
  config.vm.define "cephapp1" do |s4|
    s4.vm.hostname = "cephapp1"
    s4.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
    end
	  s4.vm.network "private_network", ip: "192.168.56.7"
    # s4.vm.provision "shell", inline: "apt install -y chrony"
  end
  config.vm.define "cephapp2" do |s5|
    s5.vm.hostname = "cephapp2"
    s5.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
    end
	  s5.vm.network "private_network", ip: "192.168.56.8"
    # s4.vm.provision "shell", inline: "apt install -y chrony"
  end
end
