#!/bin/bash

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

main "$@"
