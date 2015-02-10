#!/bin/bash

set -e

common_packages=(
  expect
)
balancer_packages=(
  haproxy
)
app_packages=(
  python-devel
  python-pip
)

main() {
  install_packages "$1"
  if [[ "$1" == "balancer" ]]; then
    setup_haproxy
  elif [[ "$1" == "app" ]]; then
    setup_app
  fi
}

install_packages() {
  local other=
  if [[ "$1" == "balancer" ]]; then
    other="${balancer_packages[@]}"
  elif [[ "$1" == "app" ]]; then
    other="${app_packages[@]}"
  fi
  yum -y shell <<END
    update
    install ${common_packages[@]} $other
    run
END
}

setup_haproxy() {
  cp /vagrant/provision/haproxy.cfg /etc/haproxy/haproxy.cfg
  service haproxy start
  chkconfig haproxy on
}

setup_app() {
  [ -d /opt/app ] || mkdir /opt/app
  [ -d /var/run/app ] || mkdir /var/run/app
  service app stop 2>/dev/null || true
  chown vagrant:vagrant /opt/app /var/run/app
  sudo -u vagrant rsync -a --del /vagrant/app/ /opt/app/

  pip install virtualenv
  pip install flask

  cp /vagrant/provision/service /etc/init.d/app
  chkconfig --add app
  service app start
}

main "$@"
