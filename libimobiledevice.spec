%global commit b314f04bd791b263cf43fadc6ac0756e67ab4ed0
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:          libimobiledevice
Version:       1.3.0^20220904git%{shortcommit}
Release:       8%{?dist}
Summary:       Library for connecting to mobile devices

License:       LGPLv2+
URL:           http://www.libimobiledevice.org/
Source:        https://github.com/libimobiledevice/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
Patch:         libimobiledevice-configure-use-static-version.patch

BuildRequires: openssl-devel
BuildRequires: libgcrypt-devel
BuildRequires: libtasn1-devel
BuildRequires: pkgconfig
BuildRequires: pkgconfig(libplist-2.0) >= 2.2.0
BuildRequires: pkgconfig(libimobiledevice-glue-1.0) >= 1.0.0
BuildRequires: pkgconfig(libusbmuxd-2.0) >= 2.0.2
BuildRequires: git-core
BuildRequires: autoconf automake libtool
BuildRequires: make
Requires: usbmuxd

%description
libimobiledevice is a library for connecting to mobile devices including phones 
and music players

%package devel
Summary: Development package for libimobiledevice
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with libimobiledevice.

%package utils
Summary: Utilites for libimobiledevice
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
Utilites for use with libimobiledevice.

%prep
%autosetup -n %{name}-%{commit}

./autogen.sh

%build
%configure --disable-static --enable-openssl --enable-dev-tools --without-cython --disable-wireless-pairing
# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install


%files
%{!?_licensedir:%global license %%doc}
%license COPYING.LESSER
%doc AUTHORS README.md
%{_libdir}/*.so.*

%files utils
%doc %{_datadir}/man/man1/idevice*
%{_bindir}/idevice*

%files devel
%doc docs/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/*

%changelog
* Thu Oct 06 2022 Tommy Nguyen <remyabel@gmail.com> - 1.3.0^20220904gitb314f04-8
- Update to latest snapshot

* Sat Sep 17 2022 Tommy Nguyen <remyabel@gmail.com> - 1.3.0^20220904gitef7cf8e-7
- Fix lint errors and warnings

* Fri Sep 16 2022 Tommy Nguyen <remyabel@gmail.com> - 1.3.0^20220904gitef7cf8e-6
- bump

* Fri Sep 16 2022 Tommy Nguyen <remyabel@gmail.com> - 1.3.0^20220904gitb5ce444-5
- Don't build third party libraries

* Fri Sep 16 2022 Tommy Nguyen <remyabel@gmail.com> - 1.3.0^20220904gitb5ce444-4
- Disabled wireless pairing for compatibility with new crypto policy

* Mon Sep 05 2022 Tommy Nguyen <remyabel@gmail.com> - 1.3.0^20220904gitb5ce444-3
- Update to latest master

* Mon Aug 01 2022 Tommy Nguyen <remyabel@gmail.com> - 1.3.0^20220702git2eec1b9-2
- Remove Obsolete tags

* Mon Aug 01 2022 Tommy Nguyen <remyabel@gmail.com> - 1.3.0^20220702git2eec1b9-1
- Fix versioning scheme

* Sat Jul 30 2022 Tommy Nguyen <remyabel@gmail.com> - 20220702git2eec1b9
- Update to latest master version

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.3.0-5
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 16 2020 Bastien Nocera <bnocera@redhat.com> - 1.3.0-1
+ libimobiledevice-1.3.0-1
- Update to 1.3.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Bastien Nocera <bnocera@redhat.com> - 1.2.1-0.2
+ libimobiledevice-1.2.1-0.2
- Use openssl instead of gnutls, as the gnutls backend keeps breaking

* Mon Nov 25 2019 Bastien Nocera <bnocera@redhat.com> - 1.2.1-0.1
+ libimobiledevice-1.2.1-0.1
- Add support for newer devices
- This is a snapshot of the in-development 1.2.1 version

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 07 2018 Bastien Nocera <bnocera@redhat.com> - 1.2.0-16
+ libimobiledevice-1.2.0-16
- Remove python2 subpackage, it hasn't been generated since F21

* Thu Mar 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.2.0-15
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 15 2017 Bastien Nocera <bnocera@redhat.com> - 1.2.0-13
+ libimobiledevice-1.2.0-13
- GNUTLS 3.6.0 compatibility bug fixes

* Fri Sep 15 2017 Bastien Nocera <bnocera@redhat.com> - 1.2.0-12
+ libimobiledevice-1.2.0-12
- Replace patches with a single mega-patch
- Fixes usbmuxd for iOS 11 devices

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 09 2016 Bastien Nocera <bnocera@redhat.com> - 1.2.0-8
+ libimobiledevice-1.2.0-8
- Fix usage with iOS 10
- Use upstream commit for GNUTLS3 support

* Fri May 27 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.0-7
- Fix CVE-2016-5104

* Mon Mar 14 2016 Bastien Nocera <bnocera@redhat.com> 1.2.0-6
- Add fix for potential security issue

* Mon Mar 14 2016 Bastien Nocera <bnocera@redhat.com> 1.2.0-5
- Fix installation proxy usage

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Aug 26 2015 Kalev Lember <klember@redhat.com> - 1.2.0-3
- Fix the build with gnutls 3.4

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 11 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.0-1
- New 1.2.0 release
- Use %%license

* Wed Oct 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.7-1
- New 1.1.7 release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May  5 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.6-1
- New 1.1.6 release

* Thu Apr 24 2014 Rex Dieter <rdieter@fedoraproject.org> 1.1.5-5
- disable broken -python on rawhide

* Wed Apr 23 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.5-4
- Rebuild

* Sat Aug  3 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.5-3
- Add dep on libgcrypt-devel to fix FTBFS

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.5-1
- New 1.1.5 release

* Thu Feb 21 2013 Bastien Nocera <bnocera@redhat.com> 1.1.4-6
- Add patch to avoid multi-byte characters from being stripped
  from the device name

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 05 2012 Bastien Nocera <bnocera@redhat.com> 1.1.4-4
- Don't make upowerd crash when run under systemd (#834359)

* Fri Aug 10 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.1.4-3
- disable broken python/cython bindings (for now, currently FTBFS)
- track soname
- tighten  subpkg deps

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 10 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.1.4-1
- New 1.1.4 release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 08 2011 Bastien Nocera <bnocera@redhat.com> 1.1.1-4
- All the version of Fedora are > 13 now

* Thu Dec 01 2011 Bastien Nocera <bnocera@redhat.com> 1.1.1-3
- Add iOS 5 support patches from upstream

* Wed Sep 21 2011 Bastien Nocera <bnocera@redhat.com> 1.1.1-2
- Fix compilation against recent version of gnutls

* Fri Apr 29 2011 Peter Robinson <pbrobinson@gmail.com> 1.1.1-1
- New 1.1.1 release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 26 2010 Bastien Nocera <bnocera@redhat.com> 1.1.0-1
- Update to 1.1.0

* Sun Nov 28 2010 Peter Robinson <pbrobinson@gmail.com> 1.0.4-1
- New 1.0.4 release

* Mon Oct  4 2010 Peter Robinson <pbrobinson@gmail.com> 1.0.3-1
- New 1.0.3 release

* Sun Aug 01 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.2-3
- Allow build against swig-2.0.0

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jun 20 2010 Peter Robinson <pbrobinson@gmail.com> 1.0.2-1
- New upstream stable 1.0.2 release

* Wed May 12 2010 Peter Robinson <pbrobinson@gmail.com> 1.0.1-1
- New upstream stable 1.0.1 release

* Sun Mar 21 2010 Peter Robinson <pbrobinson@gmail.com> 1.0.0-1
- New upstream stable 1.0.0 release

* Mon Feb 15 2010 Peter Robinson <pbrobinson@gmail.com> 0.9.7-3
- Add patch to fix DSO linking. Fixes bug 565084

* Wed Feb  3 2010 Peter Robinson <pbrobinson@gmail.com> 0.9.7-2
- Package review updates, add developer docs

* Wed Jan 27 2010 Peter Robinson <pbrobinson@gmail.com> 0.9.7-1
- New package for new library name. Update to 0.9.7

* Sun Jan 24 2010 Peter Robinson <pbrobinson@gmail.com> 0.9.6-1
- Update to 0.9.6 release

* Sat Jan  9 2010 Peter Robinson <pbrobinson@gmail.com> 0.9.5-3
- Updated to the new python sysarch spec file reqs

* Tue Dec 15 2009 Peter Robinson <pbrobinson@gmail.com> 0.9.5-2
- Update python bindings

* Sat Dec 12 2009 Peter Robinson <pbrobinson@gmail.com> 0.9.5-1
- Update to 0.9.5 release for new usbmuxd/libplist 1.0.0 final

* Sat Dec 12 2009 Peter Robinson <pbrobinson@gmail.com> 0.9.4-3
- Rebuild for libplist .so bump

* Wed Oct 28 2009 Peter Robinson <pbrobinson@gmail.com> 0.9.4-2
- Update from libusb to libusb1

* Wed Oct 28 2009 Peter Robinson <pbrobinson@gmail.com> 0.9.4-1
- Update to 0.9.4 release for new usbmuxd 1.0.0-rc1

* Mon Aug 10 2009 Peter Robinson <pbrobinson@gmail.com> 0.9.3-1
- Update to 0.9.3 release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 13 2009 Peter Robinson <pbrobinson@gmail.com> 0.9.1-2
- Add new build reqs

* Tue May 12 2009 Peter Robinson <pbrobinson@gmail.com> 0.9.1-1
- Update to official 0.9.1 release

* Fri Apr 03 2009 - Bastien Nocera <bnocera@redhat.com> - 0.1.0-11.20090325git443edc8
- Update to latest master version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-10.20090103git5cde554
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 3 2009 Peter Robinson <pbrobinson@gmail.com> 0.1.0-9.git5cde554
- Add back gnutls version patch

* Sat Jan 3 2009 Peter Robinson <pbrobinson@gmail.com> 0.1.0-8.git5cde554
- Upload bzipped source file

* Sat Jan 3 2009 Peter Robinson <pbrobinson@gmail.com> 0.1.0-7.git5cde554
- New git snapshot

* Mon Dec 8 2008 Peter Robinson <pbrobinson@gmail.com> 0.1.0-6.git8c3a01e
- Fix devel dependency 

* Mon Dec 8 2008 Peter Robinson <pbrobinson@gmail.com> 0.1.0-5.git8c3a01e
- Fix gnutls check for new rawhide version

* Mon Dec 8 2008 Peter Robinson <pbrobinson@gmail.com> 0.1.0-4.git8c3a01e
- Rebuild for pkgconfig

* Tue Dec 2 2008 Peter Robinson <pbrobinson@gmail.com> 0.1.0-3.git8c3a01e
- Fix git file generation

* Mon Dec 1 2008 Peter Robinson <pbrobinson@gmail.com> 0.1.0-2.git8c3a01e
- Updates for package review

* Sat Nov 29 2008 Peter Robinson <pbrobinson@gmail.com> 0.1.0-1
- Initial package
