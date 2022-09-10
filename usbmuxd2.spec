%global commit 753b79eaf317c56df6c8b1fb6da5847cc54a0bb0
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           usbmuxd2
Version:        0^20220909git%{shortcommit}
Release:        1%{?dist}
Summary:        A reimplementation of usbmuxd in C++ 

License:        GPLv3 
URL:            https://github.com/tihmstar/%{name}
Source0:        https://github.com/tihmstar/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
Patch0:         usbmuxd2-configure-use-static-version.patch

BuildRequires: make
BuildRequires: clang gcc
BuildRequires: pkgconfig
BuildRequires: pkgconfig(libgeneral) >= 39
BuildRequires: pkgconfig(libplist-2.0) >= 2.2.0
BuildRequires: pkgconfig(libimobiledevice-glue-1.0) >= 1.0.0
BuildRequires: pkgconfig(libusb-1.0) >= 1.0.9
BuildRequires: pkgconfig(libimobiledevice-1.0) >= 1.3.0
BuildRequires: pkgconfig(avahi-client) >= 0.7
BuildRequires: systemd
BuildRequires: autoconf libtool automake git-core
Conflicts: usbmuxd

Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
A socket daemon written in C++ to multiplex connections from and to iOS devices over USB and WIFI.

%prep
%autosetup -n %{name}-%{commit}

mkdir -p m4
NOCONFIGURE=1 ./autogen.sh

# Set the owner of the device node to be usbmuxd
sed -i.owner 's/OWNER="usbmux"/OWNER="usbmuxd"/' udev/39-usbmuxd.rules.in
sed -i.user 's/--user usbmux/--user usbmuxd/' systemd/usbmuxd.service.in

%build
%configure CC=clang CXX=clang++ --disable-static
# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%{?ldconfig_scriptlets}

%pre
getent group usbmuxd >/dev/null || groupadd -r usbmuxd -g 113
getent passwd usbmuxd >/dev/null || \
useradd -r -g usbmuxd -d / -s /sbin/nologin \
    -c "usbmuxd user" -u 113 usbmuxd
exit 0

%post
%systemd_post usbmuxd.service

%preun
%systemd_preun usbmuxd.service

%postun
%systemd_postun_with_restart usbmuxd.service 


%files
%license LICENSE
%doc README.md
%{_unitdir}/usbmuxd.service
%{_udevrulesdir}/39-usbmuxd.rules
%{_sbindir}/usbmuxd


%changelog
* Sat Sep 10 2022 Tommy Nguyen <remyabel@gmail.com>
- Initial package
