%global debug_package %{nil}

Name: 		dptf
Version: 	8.4.10401
Release: 	1%{?dist}.pp3345
License:	Apache 2.0
URL:		https://github.com/intel/dptf
Source0:	https://github.com/intel/dptf/archive/%{version}.tar.gz
Source1:        dracut-module-setup.sh
Source2:	75-dptf.preset
Source3:	00-dptf.conf
Summary:	Intel (R) Dynamic Platform and Thermal Framework

BuildRequires:	git
BuildRequires:	make
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	cmake
BuildRequires:	glibc-devel
BuildRequires:	readline-devel

Requires:	readline
Requires:	dracut
Requires:	systemd

# patch systemd service for Fedora and early loading
Patch0: systemd-service.patch

# fixes required to allow DPTF to correctly build on Fedora
Patch1: build-fixes.patch

%description
This is a solution to help enable thin, quiet, and cool platform designs. Intel
DPTF hosts various platform level power and thermal management technologies that
help with this goal.  Intel DPTF provides mechanisms for platform components and
devices to be exposed to individual technologies in a consistent and modular
fashion thus enabling a coordinated control of the platform to achieve the power
and thermal management goals.

%prep
%autosetup -S git

%build
%cmake -S DPTF/Linux -B DPTF/Linux/build
%make_build -C DPTF/Linux/build
%make_build -C ESIF/Products/ESIF_UF/Linux
%make_build -C ESIF/Products/ESIF_CMP/Linux
%make_build -C ESIF/Products/ESIF_WS/Linux

%install
install -s -m 0755 -D DPTF/Linux/build/x64/release/Dptf.so %{buildroot}%{_datadir}/dptf/ufx64/Dptf.so
install -s -m 0755 -D DPTF/Linux/build/x64/release/DptfPolicyActive.so %{buildroot}%{_datadir}/dptf/ufx64/DptfPolicyActive.so
install -s -m 0755 -D DPTF/Linux/build/x64/release/DptfPolicyCritical.so %{buildroot}%{_datadir}/dptf/ufx64/DptfPolicyCritical.so
install -s -m 0755 -D DPTF/Linux/build/x64/release/DptfPolicyPassive.so %{buildroot}%{_datadir}/dptf/ufx64/DptfPolicyPassive.so
install -s -m 0755 -D ESIF/Products/ESIF_UF/Linux/esif_ufd %{buildroot}%{_sbindir}/esif_ufd
install -s -m 0755 -D ESIF/Products/ESIF_CMP/Linux/esif_cmp.so %{buildroot}%{_datadir}/dptf/ufx64/esif_cmp.so
install -s -m 0755 -D ESIF/Products/ESIF_WS/Linux/esif_ws.so %{buildroot}%{_datadir}/dptf/ufx64/esif_ws.so
install -m 0644 -D ESIF/Packages/DSP/dsp.dv %{buildroot}%{_sysconfdir}/dptf/dsp.dv
install -m 0644 -D ESIF/Packages/Installers/linux/dptf.service %{buildroot}%{_prefix}/lib/systemd/system/dptf.service
install -m 0755 -D %{_sourcedir}/dracut-module-setup.sh %{buildroot}%{_prefix}/lib/dracut/modules.d/09dptf/module-setup.sh
install -m 0644 -D %{_sourcedir}/75-dptf.preset %{buildroot}%{_prefix}/lib/systemd/system-preset/75-dptf.preset
install -m 0644 -D %{_sourcedir}/00-dptf.conf %{buildroot}%{_sysconfdir}/dracut.conf.d/00-dptf.conf

%post
%systemd_post dptf.service
dracut -f

%postun
%systemd_postun dptf.service
dracut -f

%files
%license LICENSE.txt
%doc README.txt
%{_sbindir}/esif_ufd
%dir %{_datadir}/dptf/ufx64/
%{_datadir}/dptf/ufx64/Dptf.so
%{_datadir}/dptf/ufx64/DptfPolicyActive.so
%{_datadir}/dptf/ufx64/DptfPolicyCritical.so
%{_datadir}/dptf/ufx64/DptfPolicyPassive.so
%{_datadir}/dptf/ufx64/esif_cmp.so
%{_datadir}/dptf/ufx64/esif_ws.so
%dir %{_sysconfdir}/dptf/
%{_sysconfdir}/dptf/dsp.dv
%dir %{_prefix}/lib/dracut/modules.d/09dptf/
%{_prefix}/lib/dracut/modules.d/09dptf/module-setup.sh
%{_prefix}/lib/systemd/system/dptf.service
%{_prefix}/lib/systemd/system-preset/75-dptf.preset
%{_sysconfdir}/dracut.conf.d/00-dptf.conf

%changelog
* Sun Jul 07 2019 Yussuf Khalil <dev@pp3345.net> - 8.4.10401-1
- Initial release
