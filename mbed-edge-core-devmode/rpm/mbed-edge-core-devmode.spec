%global forgeurl https://github.com/ARMmbed/mbed-edge
%global tag      0.13.0
%global debug_package %{nil}
%forgemeta

Name:           mbed-edge-core-devmode
Version:        0.0.1
Release:        1%{?dist}
Summary:        The core of Device Management Edge (developer version)
License:        Apache-2.0
URL:            %{forgeurl}
Source0:        %{forgesource}
Conflicts:      mbed-edge-core
BuildRequires:  cmake doxygen graphviz mosquitto-devel systemd systemd-rpm-macros
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Patch0: fix-calculation-of-remaining-buffer-size-when-callin.patch
Patch1: fix-bug-dynamic-resources-should-be-updatable-by-the.patch
Patch2: Fixed-edge-cloud-write-errors.patch
Patch3: Broadcast-gateway-stats-to-LWM2M-resources.patch
Patch4: allow-resources-to-be-named.patch
Patch5: patch-mbed-edge-with-the-ability-to-override-pelion-.patch
Patch6: Remove-Version.patch
Patch7: Fix-CPU-Temp-Path.patch

%description
Device Management Edge (from now on, just Edge) is a product that
enables you to connect a variety of devices to Device
Management. Examples of such devices are:

1. Existing legacy devices that use a protocol, such as BACNet, Modbus and
   Zigbee.
2. Non-IP based devices, such as Bluetooth LE.
3. Devices with a limited memory footprint that cannot host a full Device
   Management Client.

Edge lets you connect all these devices to Device Management, so you
can manage them and their resources remotely and locally. The Edge
Protocol Translator API is protocol agnostic, so anything your gateway
connects with can be connected to Edge. Use the Edge Management API to
create local management applications that can manage connected devices
with and without Device Management connectivity.

%prep
%setup -q %{forgesetupargs}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
cmake . -DCMAKE_POSITION_INDEPENDENT_CODE=ON -DDEVELOPER_MODE=ON \
		-DFIRMWARE_UPDATE=OFF -DCMAKE_BUILD_TYPE=RelWithDebInfo \
		-DTRACE_LEVEL=WARN -DMBED_CLOUD_DEV_UPDATE_ID=ON

%make_build

%install
install -vdm 0755				                    %{buildroot}/var/lib/pelion/mbed/

install -vdm 0755				                    %{buildroot}/usr/lib/pelion/scripts/
install -vpm 0755 %{_filesdir}/arm*                 %{buildroot}/usr/lib/pelion/scripts/

install -vdm 0755                                   %{buildroot}/%{_bindir}
install -vpm 0755 bin/edge-core                     %{buildroot}/%{_bindir}

install -vdm 0755				                    %{buildroot}/%{_unitdir}
install -vpm 0755 %{_filesdir}/edge-core.service    %{buildroot}/%{_unitdir}

install -vdm 0755 %{buildroot}/%{_sysconfdir}/logrotate.d
install -vpm 0755 %{_filesdir}/edge-core.logrotate	%{buildroot}/%{_sysconfdir}/logrotate.d/edge-core

%files
%{_bindir}/edge-core
%{_unitdir}/edge-core.service
%{_sysconfdir}/logrotate.d/edge-core
/usr/lib/pelion/scripts/*

%dir
/var/lib/pelion/mbed/

%post
%systemd_post edge-core.service

%preun
%systemd_preun edge-core.service

%postun
%systemd_postun_with_restart edge-core.service

%changelog
* Mon May 18 2020 Vasily Smirnov <vasilii.smirnov@globallogic.com> - 0.0.1-1
- Initial release.
