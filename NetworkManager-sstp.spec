%if 0%{?fedora} < 28 && 0%{?rhel} < 8
%bcond_without libnm_glib
%else
# Disable the legacy version by default
%bcond_with libnm_glib
%endif

%global snapshot %{nil}
%global ppp_version %(rpm -q ppp --queryformat '%{VERSION}')

Summary:   NetworkManager VPN plugin for SSTP
Name:      NetworkManager-sstp
Epoch:     1
Version:   1.2.6
Release:   1%{snapshot}%{?dist}
License:   GPLv2+
URL:       https://github.com/enaess/network-manager-sstp/
Source:    https://downloads.sourceforge.net/project/sstp-client/network-manager-sstp/%{name}-%{version}%{snapshot}.tar.bz2

BuildRequires: gtk3-devel
BuildRequires: dbus-devel
%if %{with libnm_glib}
BuildRequires: NetworkManager-glib-devel >= 1.2.0
BuildRequires: libnm-gtk-devel >= 1.2.0
%else
BuildRequires: NetworkManager-libnm-devel >= 1.2.0
%endif
BuildRequires: sstp-client-devel
BuildRequires: glib2-devel
BuildRequires: ppp-devel >= 2.4.6
BuildRequires: libtool intltool gettext
BuildRequires: libsecret-devel
BuildRequires: libnma-devel >= 1.2.0

Requires: dbus
Requires: NetworkManager >= 1.2.0
Requires: sstp-client
Requires: ppp = %{ppp_version}

%global __provides_exclude ^libnm-.*\\.so

%description
This package contains software for integrating VPN capabilities using
the SSTP server with NetworkManager.

%package -n NetworkManager-sstp-gnome
Summary: NetworkManager VPN plugin for SSTP - GNOME files
Group:   System Environment/Base

Requires: NetworkManager-sstp%{?_isa} = %{epoch}:%{version}-%{release}
Requires: nm-connection-editor

%description -n NetworkManager-sstp-gnome
This package contains software for integrating VPN capabilities with
the SSTP server with NetworkManager (GNOME files).

%prep
%setup -q

%build
%configure \
    --disable-static \
%if %without libnm_glib
    --without-libnm-glib \
%endif
    --enable-more-warnings=yes \
    --with-pppd-plugin-dir=%{_libdir}/pppd/%{ppp_version}
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la
rm -f %{buildroot}%{_libdir}/pppd/%{ppp_version}/*.la

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS README ChangeLog
%license COPYING
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/nm-sstp-service.conf
%{_libexecdir}/nm-sstp-service
%{_libexecdir}/nm-sstp-auth-dialog
%{_libdir}/pppd/%{ppp_version}/nm-sstp-pppd-plugin.so
%{_prefix}/lib/NetworkManager/VPN/nm-sstp-service.name

%files -n NetworkManager-sstp-gnome
%doc AUTHORS README ChangeLog
%license COPYING
%{_libdir}/NetworkManager/lib*.so*
%{_datadir}/appdata/network-manager-sstp.metainfo.xml

%if %with libnm_glib
%{_sysconfdir}/NetworkManager/VPN/nm-sstp-service.name
%endif

%changelog
* Sun Apr 15 2018 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 1:1.2.6.1
- Update to 1.2.6

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 30 2017 Lubomir Rintel <lkundrak@v3.sk> - 1.2.0-5
- Drop libnm-glib for Fedora 28

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 16 2016 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 1:1.2.0-1
- Switch to 1.2.0 tarball

* Thu Jun 30 2016 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 1:1.2.0-0.20160529git72e50bf2
- Fix issue with broken dependency due to missing epoch
- Update to Git commit with 1.2.0 final

* Fri Jun 24 2016 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 1:1.2.0-0.20160514git86c2737d
- Upgrade to Git snapshot from 1.2.0 branch
- Specification enhancements by Lubomir Rintel

* Thu Feb 04 2016 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 1:0.9.10-6
- Apply remarks after package review by Christopher Meng
- Specify minimal required ppp version to >= 2.4.6

* Wed Jun 24 2015 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 1:0.9.10-5
- Change doc macro to license macro for COPYING file
- Change URL to plugin project page instead if NetworkManager itself

* Thu Jun 11 2015 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 1:0.9.10-4
- Specify minimum required NetworkManager version - 0.9.10

* Mon Jun 08 2015 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 1:0.9.10-3
- Minor changes to adjust configuration to Fedora requirements
- Remove redundant Obsoletes tag 

* Tue Jun 02 2015 Eivind Naess <eivnaes@yahoo.com> - 1:0.9.10-2
- Taking suggested changes for Gateway validation from George Joseph

* Fri May 29 2015 Eivind Naess <eivnaes@yahoo.com> - 1:0.9.10-1
- Upgraded the network-manager-sstp package to reflect mainstream 
  changes made to the network-manager-pptp counter part.

* Fri Oct 12 2012 Eivind Naess <eivnaes@yahoo.com> - 1:0.9.4-2
- Fixed a bug that caused connection to be aborted with the message:
  "Connection was aborted, value of attribute is incorrect"

* Sat May 05 2012 Eivind Naess <eivnaes@yahoo.com> - 1:0.9.4-1
- Compiled against the latest network manager 0.9.4 sources.

* Sat Mar 03 2012 Eivind Naess <eivnaes@yahoo.com> - 1:0.9.1-4
- Added back the 'refuese-eap=yes' by default in the configuration.

* Wed Feb 08 2012 Eivind Naess <eivnaes@yahoo.com> - 1:0.9.1-3
- Changed the pppd plugin to send MPPE keys on ip-up

* Sun Nov 20 2011 Eivind Naess <eivnaes@yahoo.com> - 1:0.9.1-2
- Added proxy support

* Sun Oct 02 2011 Eivind Naess <eivnaes@yahoo.com> - 1:0.9.0-1
- Initial release
