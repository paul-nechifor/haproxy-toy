from fabric.api import task, env

from testing import HardwareMaker

env.key_filename = '~/.vagrant.d/insecure_private_key'
env.user = 'vagrant'


@task
def setup(n_balancers='1', n_apps='1', n_services='1'):
    """
    Brings up a certain server configuration. Don't forget to destroy the same
    configuration.
    """
    HardwareMaker(int(n_balancers), int(n_apps), int(n_services)).run()


@task
def destroy(n_balancers='1', n_apps='1'):
    """Destroys a certain server configuration."""
    HardwareMaker(int(n_balancers), int(n_apps)).destroy()
