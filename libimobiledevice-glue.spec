%global commit 7eaa28ea9529b69da6b1721ba3e791e7ea5e950b
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           libimobiledevice-glue
Version:        1.0.0^20220905git%{shortcommit}
Release:        3%{?dist}
Summary:        Glue library for libimobiledevice projects

License:       LGPLv2+
URL:           http://www.libimobiledevice.org/
Source:        https://github.com/libimobiledevice/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires: pkgconfig
BuildRequires: pkgconfig(libplist-2.0) >= 2.2.0
BuildRequires: git-core
BuildRequires: autoconf automake libtool

%description
Library with common code used by the libraries and tools around the
libimobiledevice project

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -S git_am -n %{name}-%{commit}

NOCONFIGURE=1 ./autogen.sh

%build
%configure --disable-static
# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sat Sep 17 2022 Tommy Nguyen <remyabel@gmail.com> - 1.0.0^20220905git7eaa28e-3
- Fix lint errors and warnings

* Mon Sep 05 2022 Tommy Nguyen <remyabel@gmail.com> - 1.0.0^20220905git7eaa28e-2
- Update to latest master

* Thu Aug 04 2022 Tommy Nguyen <remyabel@gmail.com> - 1.0.0^20220523gitd2ff796-1
- Fix versioning scheme
- Use pkgconfig for dependencies

* Mon Aug 01 2022 Tommy Nguyen <remyabel@gmail.com> - 0^20220523gitd2ff796-1
- Fix versioning scheme

* Sat Jul 30 2022 Tommy Nguyen <remyabel@gmail.com> - 20220523gitd2ff796
- Initial commit
