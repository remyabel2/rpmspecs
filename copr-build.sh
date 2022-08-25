#!/bin/bash

# SPDX-FileCopyrightText: 2022 Tommy Nguyen
#
# SPDX-License-Identifier: MIT

packages=("libplist" "libimobiledevice-glue" "libusbmuxd" "libimobiledevice" "usbmuxd")
srpms=()

for package in "${packages[@]}";
do
    version=$(rpmspec -P "$package".spec | grep "Version:" | tr -s ' ' | cut -f2 -d' ')
    release=$(rpmspec -P "$package".spec | grep "Release:" | tr -s ' ' | cut -f2 -d' ')
    filename="$package-$version-$release.src.rpm"
    srpms+=("SRPMS/$filename")
done

pushd "${RPMBUILD_ROOT:-$PWD}"
    if [ ! -d "SRPMS" ];
    then
        echo "Doesn't look like you're in the rpmbuild root. Exiting."
        exit 1
    fi
    build_id=$(copr-cli build "libimobiledevice" "${srpms[0]}" --nowait)
    build_id=$(echo "$build_id" | grep "Created" | tr -d ' ' | cut -f2 -d':')
    for idx in "${!srpms[@]}";
    do
        # Skip first one
        if [ "$idx" -eq 0 ];
        then
            continue
        fi
        build_id=$(copr-cli build "libimobiledevice" "${srpms[$idx]}" --nowait --after-build-id="$build_id")
        build_id=$(echo "$build_id" | grep "Created" | tr -d ' ' | cut -f2 -d':')
    done
popd
