# Motivation

The current downstream release of Firejail is over a year old, with the latest
version fixing a high severity CVE. So, until the package gets a new
maintainer, this is a stopgap measure. **UPDATE**: Firejail should now be
updated for Fedora 37, thus this is no longer needed.

libimobiledevice does not have a new upstream release yet, but the git snapshot
has compatibility for newer iOS devices. Further, I've packaged usbmuxd2 which
should help with upcoming changes to [Fedora's crypto
policies](https://fedoraproject.org/wiki/Changes/StrongCryptoSettings3).

I also cleaned up the specs for cruft and added some additional stuff I
considered necessary (like hardening the Firejail permissions.)

# Instructions

```
dnf copr enable remyabel/firejail
dnf copr enable remyabel/libimobiledevice
dnf copr enable remyabel/usbmuxd2

sudo dnf install libplist-devel libimobiledevice-glue usbmuxd libusbmuxd libimobiledevice
# or
sudo dnf install libgeneral libplist-devel libimobiledevice-glue usbmuxd2 libusbmuxd libimobiledevice

sudo dnf install firejail
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
env RPMBUILD_ROOT="some_path" ./copr-build.sh [--firejail]|[--libimobiledevice]|[--usbmuxd2]
```
