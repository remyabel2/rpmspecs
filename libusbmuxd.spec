%global commit 36ffb7ab6e2a7e33bd1b56398a88895b7b8c615a
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:          libusbmuxd
Version:       2.0.2^20220504git%{shortcommit}
Release:       1%{?dist}
Summary:       Client library USB multiplex daemon for Apple's iOS devices

License:       LGPLv2+
URL:           http://www.libimobiledevice.org/
Source:        https://github.com/libimobiledevice/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
Patch:         libusbmuxd-configure-use-static-version.patch

BuildRequires: gcc
BuildRequires: libplist-devel
BuildRequires: autoconf automake libtool
BuildRequires: make
BuildRequires: libimobiledevice-glue-devel
Requires: usbmuxd
Obsoletes: libusbmuxd < %{version}-%{release} 
Obsoletes: libusbmuxd-devel < %{version}-%{release}

%description
libusbmuxd is the client library used for communicating with Apple's iPod Touch,
iPhone, iPad and Apple TV devices. It allows multiple services on the device 
to be accessed simultaneously.

%package utils
Summary: Utilities for communicating with Apple's iOS devices
License: GPLv2+
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
Utilities for Apple's iOS devices

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: usbmuxd-devel < 1.0.9

%description devel
Files for development with %{name}.

%prep
%autosetup -n %{name}-%{commit}

NOCONFIGURE=1 ./autogen.sh

%build
%configure --disable-static
# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%check
make check

%{?ldconfig_scriptlets}

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md AUTHORS
%{_libdir}/*.so.*

%files utils
%{_bindir}/iproxy
%{_bindir}/inetcat
%{_mandir}/man1/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%changelog
* Mon Aug 01 2022 Tommy Nguyen <remyabel@gmail.com> - 2.0.2^20220504git36ffb7a-1
- Update to latest master version

* Sat Jul 30 2022 Tommy Nguyen <remyabel@gmail.com> - 20220504git36ffb7a
- Update to latest master version

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 2.0.2-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jun 16 2020 Bastien Nocera <bnocera@redhat.com> - 2.0.2-1
+ libusbmuxd-2.0.2-1
- Update to 2.0.2

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 23 2019 Bastien Nocera <bnocera@redhat.com> - 2.0.0-1
+ libusbmuxd-2.0.0-1
- Update to 2.0.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri May 27 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.10-5
- Fix CVE-2016-5104

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb  3 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.10-2
- Use %%license

* Wed Oct 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.10-1
- Update to 1.0.10

* Tue Sep 09 2014 Rex Dieter <rdieter@fedoraproject.org> 1.0.9-4
- -devel: Obsoletes: usbmuxd-devel

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 22 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.9-1
- Initial package
