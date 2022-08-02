# Motivation

The current downstream release of Firejail is over a year old, with the latest
version fixing a high severity CVE. So, until the package gets a new
maintainer, this is a stopgap measure.

libimobiledevice does not have a new upstream release yet, but the git snapshot
has compatibility for newer iOS devices.

I also cleaned up the specs for cruft and added some additional stuff I
considered necessary (like hardening the Firejail permissions.)

# Instructions

```
dnf copr enable remyabel/firejail

# Dependencies.
dnf copr enable remyabel/libplist
dnf copr enable remyabel/libimobiledevice-glue

dnf copr enable remyabel/usbmuxd
dnf copr enable remyabel/libusbmuxd
dnf copr enable remyabel/libimobiledevice

sudo dnf install firejail libplist-devel libimobiledevice-glue usbmuxd libusbmuxd libimobiledevice

sudo usermod -a -G firejail $USER
```

Alternatively, add yourself to `firejail.users`. See `man firejail.users`.

# Development

To test locally in mock:

```
# Defaults to $PWD if unset
env RPMBUILD_ROOT="some_path" ./mock-build.sh
```

To build in batches for COPR:

```
# Defaults to $PWD if unset
env RPMBUILD_ROOT="some_path" ./copr-build.sh
```
