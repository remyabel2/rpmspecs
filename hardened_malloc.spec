%global commit 2250130c537fda373a4362cf7727562287eb1168
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global toolchain clang
%global debug_package %{nil}

Name:           hardened_malloc
Version:        13^20220917git%{shortcommit}
Release:        1%{?dist}
Summary:        Hardened allocator designed for modern systems

License:        MIT
URL:            https://github.com/GrapheneOS/hardened_malloc
Source0:        https://github.com/GrapheneOS/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
ExclusiveArch:  x86_64

BuildRequires: make
BuildRequires: clang >= 11.0.1
BuildRequires: glibc >= 2.31
BuildRequires: python3 >= 3.8.0
Requires:      kernel >= 5.10.0

%description
Hardened allocator designed for modern systems. It has integration into
Android's Bionic libc and can be used externally with musl and glibc as a
dynamic library for use on other Linux-based platforms.

%prep
%autosetup -n %{name}-%{commit}


%build
%{__make} VARIANT=light
echo %{_libdir}/libhardened_malloc-light.so > out-light/libhardened-malloc.conf

%install
%{__install} -Dm 0755 out-light/libhardened_malloc-light.so %{buildroot}%{_libdir}/libhardened-malloc/libhardened_malloc-light.so
%{__install} -Dm 0644 out-light/libhardened-malloc.conf %{buildroot}%{_sysconfdir}/ld.so.preload.d/libhardened-malloc.conf
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysctl.d
echo 'vm.max_map_count = 1048576' > %{buildroot}%{_sysconfdir}/sysctl.d/hardened_malloc.conf


%files
%license LICENSE
%doc README.md
%config(noreplace) %{_sysconfdir}/sysctl.d/hardened_malloc.conf
%config(noreplace) %{_sysconfdir}/ld.so.preload.d/libhardened-malloc.conf
%{_libdir}/libhardened-malloc/libhardened_malloc-light.so


%changelog
* Sat Sep 17 2022 Tommy Nguyen <remyabel@gmail.com> - 13^20220917git2250130-1
- Initial package
