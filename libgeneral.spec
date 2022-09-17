Name:           libgeneral
Version:        63
Release:        2%{?dist}
Summary:        A collection of macros used in tihmstar projects.

License:        LGPLv2
URL:            https://github.com/tihmstar/libgeneral
Source0:        https://github.com/tihmstar/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         libgeneral-pkgconfig-version.patch
Patch1:         libgeneral-configure-use-static-version.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig

%description
A collection of macros used in tihmstar projects.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup

mkdir -p m4
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
%license LICENSE
%doc README.md
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sat Sep 17 2022 Tommy Nguyen <remyabel@gmail.com> - 63-2
- Fix lint errors and warnings

* Sat Sep 10 2022 Tommy Nguyen <remyabel@gmail.com>
- Initial package
