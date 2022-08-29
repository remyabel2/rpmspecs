#
# spec file for package btrfsmaintenance
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

%global commit be42cb6267055d125994abd6927cf3a26deab74c
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           btrfsmaintenance
Version:        0.5^20200730%{shortcommit}
Release:        1%{?dist}
Summary:        Scripts for btrfs periodic maintenance tasks

License:        GPL-2.0-only
Url:            https://github.com/kdave/btrfsmaintenance
Source:         https://github.com/kdave/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
BuildRequires:  pkgconfig(systemd)
Requires:       btrfs-progs
Supplements:    btrfs-progs
BuildRequires:  systemd
BuildArch:      noarch

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd


%description
Scripts for btrfs maintenance tasks like periodic scrub, balance, trim or defrag
on selected mountpoints or directories. Hints for periodic snapshot tuning (eg.
for snapper).

%prep
%autosetup -n %{name}-%{commit}

%build

%install
# scripts
install -m 755 -d %{buildroot}%{_datadir}/%{name}
install -m 755 btrfs-defrag.sh %{buildroot}%{_datadir}/%{name}
install -m 755 btrfs-balance.sh %{buildroot}%{_datadir}/%{name}
install -m 755 btrfs-scrub.sh %{buildroot}%{_datadir}/%{name}
install -m 755 btrfs-trim.sh %{buildroot}%{_datadir}/%{name}
install -m 755 btrfsmaintenance-refresh-cron.sh %{buildroot}%{_datadir}/%{name}
install -m 644 btrfsmaintenance-functions %{buildroot}%{_datadir}/%{name}

# systemd services and timers
install -m 755 -d %{buildroot}%{_unitdir}
install -m 644 -D btrfsmaintenance-refresh.service %{buildroot}%{_unitdir}
install -m 644 -D btrfsmaintenance-refresh.path %{buildroot}%{_unitdir}
install -m 644 -D btrfs-balance.service %{buildroot}%{_unitdir}
install -m 644 -D btrfs-defrag.service %{buildroot}%{_unitdir}
install -m 644 -D btrfs-scrub.service %{buildroot}%{_unitdir}
install -m 644 -D btrfs-trim.service %{buildroot}%{_unitdir}
install -m 644 -D btrfs-balance.timer %{buildroot}%{_unitdir}
install -m 644 -D btrfs-defrag.timer %{buildroot}%{_unitdir}
install -m 644 -D btrfs-scrub.timer %{buildroot}%{_unitdir}
install -m 644 -D btrfs-trim.timer %{buildroot}%{_unitdir}
install -m 755 -d %{buildroot}%{_sbindir}
ln -s %{_sbindir}/service %{buildroot}%{_sbindir}/rcbtrfsmaintenance-refresh

# config
install -m 0755 -d %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 -D sysconfig.btrfsmaintenance %{buildroot}%{_sysconfdir}/%{name}

%pre
# if the new service files don't exist, we migrate from
# old version with old script, remove cron symlinks
if [ ! -f %{_unitdir}/btrfs-balance.timer -a -f %{_datadir}/%{name}/btrfsmaintenance-refresh-cron.sh ] ; then
    %{_datadir}/%{name}/btrfsmaintenance-refresh-cron.sh uninstall
fi

%post
%systemd_post btrfsmaintenance-refresh.service btrfsmaintenance-refresh.path btrfs-balance.service btrfs-balance.timer btrfs-scrub.service btrfs-scrub.timer

%preun
%systemd_preun btrfsmaintenance-refresh.service btrfsmaintenance-refresh.path btrfs-balance.service btrfs-balance.timer btrfs-scrub.service btrfs-scrub.timer

%postun
%systemd_postun_with_restart btrfsmaintenance-refresh.service btrfsmaintenance-refresh.path btrfs-balance.service btrfs-balance.timer btrfs-scrub.service btrfs-scrub.timer

%files
%license COPYING
%doc README.md
%config(noreplace) %{_sysconfdir}/%{name}/sysconfig.btrfsmaintenance
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/btrfs-balance.sh
%{_datadir}/%{name}/btrfs-defrag.sh
%{_datadir}/%{name}/btrfs-scrub.sh
%{_datadir}/%{name}/btrfs-trim.sh
%{_datadir}/%{name}/btrfsmaintenance-refresh-cron.sh
%{_datadir}/%{name}/btrfsmaintenance-functions
%{_unitdir}/btrfsmaintenance-refresh.path
%{_unitdir}/btrfsmaintenance-refresh.service
%{_unitdir}/btrfs-balance.service
%{_unitdir}/btrfs-defrag.service
%{_unitdir}/btrfs-scrub.service
%{_unitdir}/btrfs-trim.service
%{_unitdir}/btrfs-balance.timer
%{_unitdir}/btrfs-defrag.timer
%{_unitdir}/btrfs-scrub.timer
%{_unitdir}/btrfs-trim.timer
%{_sbindir}/rcbtrfsmaintenance-refresh

%changelog
* Mon Aug 29 2022 Tommy Nguyen <remyabel@gmail.com> 0.5^20200730be42cb6-1
- Initial package
- Cleanup spec to use Fedora macros and conventions
- Explicitly list files
