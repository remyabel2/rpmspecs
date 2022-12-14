%global commit 2250130c537fda373a4362cf7727562287eb1168
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global toolchain clang
%global debug_package %{nil}

Name:           hardened_malloc
Version:        13^20220917git%{shortcommit}
Release:        4%{?dist}
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
%{__make} CC=clang CXX=clang++ VARIANT=light
echo %{_libdir}/libhardened-malloc/libhardened_malloc-light.so > out-light/ld.so.preload

%install
%{__install} -Dm 0755 out-light/libhardened_malloc-light.so %{buildroot}%{_libdir}/libhardened-malloc/libhardened_malloc-light.so
%{__install} -Dm 0644 out-light/ld.so.preload %{buildroot}%{_sysconfdir}/ld.so.preload
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysctl.d
echo 'vm.max_map_count = 1048576' > %{buildroot}%{_sysconfdir}/sysctl.d/hardened_malloc.conf

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README.md
%config(noreplace) %{_sysconfdir}/sysctl.d/hardened_malloc.conf
%config(noreplace) %{_sysconfdir}/ld.so.preload
%{_libdir}/libhardened-malloc/libhardened_malloc-light.so


%changelog
* Mon Sep 19 2022 Tommy Nguyen <remyabel@gmail.com> - 13^20220917git2250130-4
- ld.so.preload.d doesn't work; need to edit ld.so.preload directly

* Mon Sep 19 2022 Tommy Nguyen <remyabel@gmail.com> - 13^20220917git2250130-3
- ldconfig needs to be called when using ld.so.preload.d

* Sat Sep 17 2022 Tommy Nguyen <remyabel@gmail.com> - 13^20220917git2250130-2
- Fix typo

* Sat Sep 17 2022 Tommy Nguyen <remyabel@gmail.com> - 13^20220917git2250130-1
- Initial package
