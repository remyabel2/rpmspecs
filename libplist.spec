%global commit c3af449543795ad4d3ab178120ff69e90fdd2cc8
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%{!?python3_sitearch: %global python_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:     libplist
Version:  2.2.0^20220904git%{shortcommit}
Release:  4%{?dist}
Summary:  Library for manipulating Apple Binary and XML Property Lists

License:  LGPLv2+
URL:      http://www.libimobiledevice.org/
Source:   https://github.com/libimobiledevice/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
Patch:    libplist-configure-use-static-version.patch

BuildRequires: gcc gcc-c++
BuildRequires: python3-Cython
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: automake autoconf libtool
BuildRequires: make
BuildRequires: doxygen

%description
libplist is a library for manipulating Apple Binary and XML Property Lists

%package  devel
Summary:  Development package for libplist
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
%{name}, development headers and libraries.

%package  -n python3-libplist
%{?python_provide:%python_provide python3-libplist}
# Remove before F30
Provides: %{name}-python = %{version}-%{release}
Provides: %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}
Provides: python2-%{name} = %{version}-%{release}
Provides: python2-%{name}%{?_isa} = %{version}-%{release}
Obsoletes: python2-%{name} < %{version}-%{release}
Summary:  Python3 bindings for libplist
%{?python_provide:%python_provide python3-libplist}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: python3

%description -n python3-libplist
%{name}, python2 libraries and bindings.

%prep
%autosetup -n %{name}-%{commit}

NOCONFIGURE=1 ./autogen.sh

%build
export CC=%{__cc}
export CXX=%{__cxx}
export CFLAGS='%optflags'
export CXXFLAGS='%optflags'
export PYTHON='python3'
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build V=1
%{__make} docs

%install
%make_install

%check
make check


%files
%license COPYING.LESSER
%doc AUTHORS README.md
%{_bindir}/plistutil
%{_libdir}/libplist-2.0.so.3*
%{_libdir}/libplist++-2.0.so.3*
%{_mandir}/man1/*

%files devel
%doc docs/html
%{_libdir}/pkgconfig/libplist-2.0.pc
%{_libdir}/pkgconfig/libplist++-2.0.pc
%{_libdir}/libplist-2.0.so
%{_libdir}/libplist++-2.0.so
%{_includedir}/plist

%files -n python3-libplist
%{python3_sitearch}/plist*

%changelog
* Sat Sep 17 2022 Tommy Nguyen <remyabel@gmail.com> - 2.2.0^20220904gitc3af449-4
- Build docs and remove outdated practices

* Mon Sep 5 2022 Tommy Nguyen <remyabel@gmail.com> - 2.2.0^20220904gitc3af449-3
- Update to latest master, which contains strict aliasing fixes

* Mon Aug 01 2022 Tommy Nguyen <remyabel@gmail.com> - 2.2.0^20220405gitdb93bae-2
- Remove Obsoletes tags

* Mon Aug 01 2022 Tommy Nguyen <remyabel@gmail.com> - 2.2.0^20220405gitdb93bae-1
- Fix versioning scheme
- Add Obsoletes tag

* Mon Aug 01 2022 Tommy Nguyen <remyabel@gmail.com> - 20220405gitdb93bae
- Update to latest master

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.2.0-7
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.2.0-4
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 16 2020 Bastien Nocera <bnocera@redhat.com> - 2.2.0-1
+ libplist-2.2.0-1
- Update to 2.2.0, breaking the ABI
- Stop linking python module against libpython

* Tue May 26 2020 Miro Hron??ok <mhroncok@redhat.com> - 2.1.0-4
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Tom Stellard <tstellar@redhat.com> - 2.1.0-2
- Spec cleanup: Use make_build, make_install, __cc, and __cxx macros

* Sat Nov 23 2019 Bastien Nocera <bnocera@redhat.com> - 2.1.0-1
+ libplist-2.1.0-1
- Update to 2.1.0

* Mon Aug 19 2019 Miro Hron??ok <mhroncok@redhat.com> - 2.0.0-15
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 09 2019 Charalampos Stratakis <cstratak@redhat.com> - 2.0.0-13
- Add Python 3.8 compatibility

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hron??ok <mhroncok@redhat.com> - 2.0.0-10
- Rebuilt for Python 3.7

* Thu Jun 07 2018 Bastien Nocera <bnocera@redhat.com> - 2.0.0-9
+ libplist-2.0.0-9
- Fix libplist python2 sub-package obsolescence

* Thu Jun 07 2018 Bastien Nocera <bnocera@redhat.com> - 2.0.0-8
- Port to python3, and obsolete Python2 subpackage

* Wed Mar  7 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.0-8
- Add gcc BR

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.0.0-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sun Aug 20 2017 Zbigniew J??drzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.0-5
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew J??drzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.0-4
- Python 2 binary package renamed to python2-libplist
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 26 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.0-1
- Update to upstream 2.0.0
- Fixes the following CVEs plus others
- CVE-2017-6440 CVE-2017-6439 CVE-2017-6438 CVE-2017-6437 CVE-2017-6436
- CVE-2017-6435 CVE-2017-5836 CVE-2017-5835 CVE-2017-5834 CVE-2017-5545
- CVE-2017-5209

* Thu Mar 09 2017 Kalev Lember <klember@redhat.com> - 1.12-9
- Remove lib64 rpaths
- Disable strict aliasing as it's not strict-aliasing clean on ppc64el
- Don't redefine licensedir

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.12-4
- Rebuilt for GCC 5 C++11 ABI change

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.12-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Feb  3 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.12-2
- Use %%license

* Wed Oct 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.12-1
- New upstream 1.12 release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 22 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.11-1
- New upstream 1.11 release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.10-1
- New upstream 1.10 release

* Mon Mar 18 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.9-1
- New upstream 1.9 release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 11 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8-4
- Fix python bindings

* Wed Apr 11 2012 Rex Dieter <rdieter@fedoraproject.org> 1.8-3
- fix ftbfs, work harder to ensure CMAKE_INSTALL_LIBDIR macro is correct 

* Fri Mar 23 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8-2
- Fix RPATH issue with cmake, disable parallel build as it causes other problems

* Thu Jan 12 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8-1
- 1.8 release

* Mon Sep 26 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7-1
- 1.7 release

* Sat Jun 25 2011 Peter Robinson <pbrobinson@fedoraproject.org> 1.6-1
- 1.6 release

* Mon Jun 13 2011 Peter Robinson <pbrobinson@fedoraproject.org> 1.5-1
- 1.5 release

* Tue Mar 22 2011 Peter Robinson <pbrobinson@fedoraproject.org> 1.4-1
- stable 1.4 release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 20 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-1
- Upstream stable 1.3 release

* Sat Jan 23 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.2-1
- Upstream stable 1.2 release

* Sat Jan  9 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-5
- Updated to the new python sysarch spec file reqs

* Mon Dec  7 2009 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-4
- and once more with feeling

* Mon Dec  7 2009 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-3
- Further updated fixes for the spec file

* Mon Dec  7 2009 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-2
- Drop upstreamed patch

* Mon Dec  7 2009 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-1
- Upstream stable 1.0.0 release

* Thu Oct 29 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.16-3
- Actually add patch for python

* Thu Oct 29 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.16-2
- Add python patch and c++ bindings

* Thu Oct 29 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.16-1
- New upstream 0.16 release

* Tue Oct 20 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.15-1
- New upstream 0.15 release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 11 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.13-1
- New upstream 0.13 release

* Mon May 11 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12-2
- Further review updates

* Sun May 10 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12-1
- Update to official tarball release, some review fixes

* Sun May 10 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.0-0.1
- Initial package
