#!/bin/bash

set -e

balancer_packages=(
  haproxy
)
app_packages=(
  python-devel
  python-pip
)

main() {
  install_packages "$1"
  if [[ "$1" == "app" ]]; then
    setup_app
  fi
}

install_packages() {
  local packages=
  if [[ "$1" == "balancer" ]]; then
    packages="${balancer_packages[@]}"
  elif [[ "$1" == "app" ]]; then
    packages="${app_packages[@]}"
  fi
  yum -y shell <<END
    update
    install $packages
    run
END
}

setup_app() {
  pip install virtualenv
  pip install flask
}

main "$@"
