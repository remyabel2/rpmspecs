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
dnf copr enable remyabel/usbmuxd
dnf copr enable remyabel/libusbmuxd
dnf copr enable remyabel/libimobiledevice
dnf copr enable remyabel/libimobiledevice-glue

sudo dnf install firejail usbmuxd libusbmuxd libimobiledevice libimobiledevice-glue
```
