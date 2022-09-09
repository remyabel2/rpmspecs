#!/bin/bash

# SPDX-FileCopyrightText: 2022 Tommy Nguyen
#
# SPDX-License-Identifier: MIT

packages=("libplist" "libimobiledevice-glue" "libusbmuxd" "libimobiledevice" "usbmuxd")
srpms=()

for package in "${packages[@]}"; do
    version=$(rpmspec -P "$package".spec | grep "Version:" | tr -s ' ' | cut -f2 -d' ')
    release=$(rpmspec -P "$package".spec | grep "Release:" | tr -s ' ' | cut -f2 -d' ')
    filename="$package-$version-$release.src.rpm"
    srpms+=("SRPMS/$filename")
done

pushd "${RPMBUILD_ROOT:-$PWD}"
if [ ! -d "SRPMS" ]; then
    echo "Doesn't look like you're in the rpmbuild root. Exiting."
    exit 1
fi
rm SRPMS/*.src.rpm
mock -r fedora-36-x86_64 --clean
mock -r fedora-36-x86_64 --init
for spec in SPECS/*.spec; do
    mock -r fedora-36-x86_64 --buildsrpm --spec "$spec" --sources SOURCES/ --resultdir SRPMS/
done
mock -r fedora-36-x86_64 --rebuild --chain "${srpms[@]}"
mock -r fedora-35-x86_64 --clean
mock -r fedora-35-x86_64 --init
for spec in SPECS/*.spec; do
    mock -r fedora-35-x86_64 --buildsrpm --spec "$spec" --sources SOURCES/ --resultdir SRPMS/
done
mock -r fedora-35-x86_64 --rebuild --chain "${srpms[@]}"
popd
