import os
import tempfile

from fabric.api import local, task, sudo, env, put, lcd

env.key_filename = '~/.vagrant.d/insecure_private_key'
env.user = 'vagrant'

root = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')


class Test(object):

    def __init__(self, n_balancers, n_apps, n_services=1):
        self.n_balancers = n_balancers
        self.n_apps = n_apps
        self.n_services = n_services
        self.server_list = self.get_server_list()

    def get_server_list(self):
        list = []
        format = '    server app%ds%d 172.17.2.%d:%d check'
        for i in xrange(self.n_apps):
            for j in xrange(self.n_services):
                list.append(format % (i, j, 10 + i + 1, 8000 + j + 1))
        return '\n'.join(list) + '\n'

    def run(self):
        self.bring_up()
        self.setup_test()
        self.run_test()

    def destroy(self):
        with lcd(root):
            local("""
                export n_balancers=%s
                export n_apps=%s
                vagrant destroy -f
                rm -fr .vagrant
            """ % (self.n_balancers, self.n_apps))

    def bring_up(self):
        with lcd(root):
            local("""
                export n_balancers=%s
                export n_apps=%s
                vagrant up
            """ % (self.n_balancers, self.n_apps))

    def setup_test(self):
        for i in xrange(self.n_apps):
            for j in xrange(self.n_services):
                self.setup_service(i + 1, j + 1)
        for i in xrange(self.n_balancers):
            self.setup_balancer(i + 1)

    def run_test(self):
        pass

    def setup_service(self, i_app, i_service):
        env.host_string = '172.17.2.%d' % (10 + i_app)
        with lcd(root):
            sudo("""
                [ -d /opt/app%(is)d ] || mkdir /opt/app%(is)d
                [ -d /var/run/app%(is)d ] || mkdir /var/run/app%(is)d
                service app%(is)d stop 2>/dev/null || true
                chown vagrant:vagrant /opt/app%(is)d /var/run/app%(is)d
                sudo -u vagrant rsync -a --del /vagrant/app/ /opt/app%(is)d/

                cp /vagrant/provision/service /etc/init.d/app%(is)d
                sed -i.bak 's/{number}/%(is)d/g' /etc/init.d/app%(is)d
                sed -i.bak 's/{port}/%(port)s/g' /etc/init.d/app%(is)d
                sed -i.bak 's/{host}/%(host)s/g' /etc/init.d/app%(is)d
                chkconfig --add app%(is)d
                service app%(is)d start
            """ % {
                'host': env.host_string,
                'port': 8000 + i_service,
                'is': i_service,
            })

    def setup_balancer(self, i_balancer):
        env.host_string = '172.17.1.%d' % (10 + i_balancer)
        template = open(root + '/provision/haproxy.cfg').read() % {
            'servers': self.server_list
        }
        tmp = tempfile.mkstemp()[1]
        file(tmp, 'w').write(template)
        with lcd(root):
            put(local_path=tmp, remote_path='/tmp/haproxy.cfg')
            sudo("""
                service haproxy stop >/dev/null || true
                cp /tmp/haproxy.cfg /etc/haproxy/haproxy.cfg
                service haproxy start
                chkconfig haproxy on
            """)
        os.remove(tmp)


@task
def setup(n_balancers='1', n_apps='1', n_services='1'):
    """
    Brings up a certain server configuration. Don't forget to destroy the same
    configuration.
    """
    test = Test(int(n_balancers), int(n_apps), int(n_services))
    test.run()


@task
def destroy(n_balancers='1', n_apps='1'):
    """Destroys a certain server configuration."""
    test = Test(int(n_balancers), int(n_apps))
    test.destroy()
