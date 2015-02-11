from fabric.api import local, task, sudo, env, execute

env.key_filename = '~/.vagrant.d/insecure_private_key'
env.user = 'vagrant'


@task
def vagrant_up(n_balancers='1', n_apps='1'):
    """
    Brings up a certain server configuration. Don't forget to destroy the same
    configuration.
    """
    local("""
        export n_balancers=%s
        export n_apps=%s
        vagrant up
    """ % (n_balancers, n_apps))


@task
def vagrant_destroy(n_balancers='1', n_apps='1'):
    """Destroys a certain server configuration."""
    local("""
        export n_balancers=%s
        export n_apps=%s
        vagrant destroy -f
        rm -fr .vagrant
    """ % (n_balancers, n_apps))


@task
def setup_service(i_app, i_service):
    env.host_string = '172.17.2.%d' % (10 + int(i_app))
    sudo("""
        [ -d /opt/app%(is)s ] || mkdir /opt/app%(is)s
        [ -d /var/run/app%(is)s ] || mkdir /var/run/app%(is)s
        service app%(is)s stop 2>/dev/null || true
        chown vagrant:vagrant /opt/app%(is)s /var/run/app%(is)s
        sudo -u vagrant rsync -a --del /vagrant/app/ /opt/app%(is)s/

        cp /vagrant/provision/service /etc/init.d/app%(is)s
        sed -i.bak 's/{NUMBER}/%(is)s/g' /etc/init.d/app%(is)s
        sed -i.bak 's/{PORT}/%(port)s/g' /etc/init.d/app%(is)s
        chkconfig --add app%(is)s
        service app%(is)s start
    """ % {'is': i_service, 'port': 8000 + int(i_service)})


@task
def run_test(n_balancers='1', n_apps='1', n_services='1'):
    vagrant_up(n_balancers, n_apps)
    for i in xrange(int(n_apps)):
        for j in xrange(int(n_services)):
            setup_service(str(i), str(j))
    vagrant_destroy(n_balancers, n_apps)
