from fabric.api import task, env, local, lcd

from testing import HardwareMaker, root

env.key_filename = '~/.vagrant.d/insecure_private_key'
env.user = 'vagrant'


@task
def setup(n_balancers='1', n_apps='1', n_services='1'):
    """
    Brings up a certain server configuration. Don't forget to destroy the same
    configuration.
    """
    make_sure_requrements_are_installed()
    HardwareMaker(int(n_balancers), int(n_apps), int(n_services)).run()


@task
def destroy(n_balancers='1', n_apps='1'):
    """Destroys a certain server configuration."""
    make_sure_requrements_are_installed()
    HardwareMaker(int(n_balancers), int(n_apps)).destroy()


def make_sure_requrements_are_installed():
    with lcd(root):
        local("""
            virtualenv env
            . env/bin/activate
            pip install -r requirements.txt
        """)
