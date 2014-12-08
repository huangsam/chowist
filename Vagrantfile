# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "ubuntu/trusty64"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine.
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 3000, host: 3000
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.network "forwarded_port", guest: 8080, host: 18080

  # Install Docker and some images
  config.vm.provision "docker" do |d|
    d.pull_images "ubuntu:14.04"
    d.pull_images "mongo:2.6.5"
  end

  # Setup sudo-less Docker and pip artifacts
  config.vm.provision :shell, :path => "installer.sh"

  # Bring source code into home directory
  config.vm.synced_folder "./", "/home/vagrant/ciscochef", type: "rsync", rsync__exclude: ".git/"

  # Bring Git credentials into home directory
  config.vm.provision "file", source: "~/.gitconfig", destination: ".gitconfig"
  config.vm.provision "file", source: "~/.ssh/id_rsa", destination: ".ssh/id_rsa"
  config.vm.provision "file", source: "~/.ssh/id_rsa.pub", destination: ".ssh/id_rsa.pub"

  # Name for the guest instance
  config.vm.hostname = "ciscochef-dev"

end
