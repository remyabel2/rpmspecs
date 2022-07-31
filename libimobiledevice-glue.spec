%global commit d2ff7969dcd0a12e4f18f63dab03e6cd03054fcb
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           libimobiledevice-glue
Version:        0
Release:        20220523git%{shortcommit}%{?dist}
Summary:        Glue library for libimobiledevice projects.

License:       LGPLv2+
URL:           http://www.libimobiledevice.org/
Source:        https://github.com/libimobiledevice/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires: libplist-devel
BuildRequires: git-core
BuildRequires: autoconf automake libtool

%description
Library with common code used by the libraries and tools around the libimobiledevice project.

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
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%{?ldconfig_scriptlets}

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
* Sat Jul 30 2022 Tommy Nguyen <remyabel@gmail.com> - 20220523gitd2ff796
- Initial commit
