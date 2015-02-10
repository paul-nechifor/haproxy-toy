required_plugins = %w( vagrant-proxyconf vagrant-vbguest vagrant-cachier )
required_plugins.each do |plugin|
  system "vagrant plugin install #{plugin}" unless Vagrant.has_plugin? plugin
end

nBalancers = ENV['n_balancers'].to_i
nApps = ENV['n_apps'].to_i

Vagrant.configure('2') do |config|
  config.vm.box = 'centos-6.6'
  config.ssh.insert_key = false
  config.proxy.http = ENV['http_proxy']
  config.proxy.https = ENV['https_proxy']
  config.cache.scope = :box

  (1..nBalancers).each do |i|
    vmname = "balancer#{i}"
    config.vm.define vmname.to_sym do |box|
      box.vm.host_name = vmname
      box.vm.network 'private_network', ip: "172.17.1.#{10+i}"
      box.vm.provider 'virtualbox' do |v|
        v.name = vmname
        v.memory = 1024
        v.cpus = 1
      end
      box.vm.provision 'shell', path: 'provision/provision.sh',
          args: 'balancer'
    end
  end

  (1..nApps).each do |i|
    vmname = "app#{i}"
    config.vm.define vmname.to_sym do |box|
      box.vm.host_name = vmname
      box.vm.network 'private_network', ip: "172.17.2.#{10+i}"
      box.vm.provider 'virtualbox' do |v|
        v.name = vmname
        v.memory = 512
        v.cpus = 1
      end
      box.vm.provision 'shell', path: 'provision/provision.sh',
          args: 'app'
    end
  end
end
