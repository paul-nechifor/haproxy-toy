from fabric.api import local, task


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
    """ % (n_balancers, n_apps))
