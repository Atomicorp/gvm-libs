%define _prefix /usr
%define _default_patch_fuzz 2

Summary: Support libraries for Open Vulnerability Assessment (OpenVAS) Server
Name:    gvm-libs
Version: 20.8.0
Release: RELEASE-AUTO%{?dist}.art
Source0: https://github.com/greenbone/gvm-libs/archive/v%{version}.tar.gz
Patch0:  openvas-libraries-strncpy.patch

License: GNU LGPLv2
Group: System Environment/Libraries
URL: http://www.openvas.org
Vendor: Greenbone https://www.greenbone.net
Packager: https://www.atomicorp.com
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix: %{_prefix}
Provides: openvas-libraries
Obsoletes: openvas-libraries


BuildRequires:  libxml2-devel
BuildRequires: git
BuildRequires: libssh-devel
BuildRequires: zlib-devel
BuildRequires: libtool
BuildRequires: openldap-devel
BuildRequires: openvas-smb
BuildRequires: hiredis-devel
BuildRequires: xmltoman
BuildRequires: net-snmp-devel
BuildRequires: libksba-devel
BuildRequires: graphviz

# El7
%if  0%{?rhel} == 7
BuildRequires: atomic-libgcrypt-libgcrypt atomic-libgcrypt-libgcrypt-devel atomic-libgcrypt-libgcrypt-runtime atomic-libgpg-error-libgpg-error-devel atomic-libgpg-error-libgpg-error-runtime
BuildRequires: cmake3
BuildRequires: atomic-zlib, atomic-zlib-devel
BuildRequires: atomic-gpgme, atomic-gpgme-devel

Requires: atomic-gpgme

%else
BuildRequires: libgcrypt-devel
%endif



%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
BuildRequires: libuuid libuuid-devel
#%else
#BuildRequires: e2fsprogs e2fsprogs-devel
%endif


# OV-8
%if  0%{?rhel} == 6
BuildRequires: atomic-gnutls3-gnutls-devel
BuildConflicts: gnutls gnutls-devel
BuildRequires: atomic-glib2-glib2-devel
Requires: atomic-gnutls3-gnutls atomic-glib2-glib2
%else
BuildRequires: gnutls-devel
BuildRequires: glib2 >= 2.6.0, glib2-devel >= 2.6.0,
%endif


BuildRequires: doxygen 
BuildRequires: graphviz

# 3.0
BuildRequires: gpgme gpgme-devel bison flex pkgconfig 
BuildRequires: cmake
Requires: gpgme
Obsoletes: openvas-libnasl


BuildRequires: libpcap-devel

%description
openvas-libraries is the base library for the OpenVAS network
security scanner.

%package devel
Summary: Development files for openvas-libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}


%description devel
This package contains the development files (mainly C header files)
for openvas-libraries.

%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.


%prep

#%setup -q
%autosetup -n gvm-libs-%{version} -p1


%build
export CFLAGS="$RPM_OPT_FLAGS -Werror=unused-but-set-variable -lgpg-error -lgnutls -Wno-format-truncation  -Wno-maybe-uninitialized -Wno-error=stringop-truncation"

%if  0%{?rhel} == 7
	source /opt/atomicorp/atomic/enable
        export CC="gcc -Wl,-rpath,/opt/atomicorp/atomic/root/usr/lib64/,-rpath,/opt/atomicorp/atomic/root/usr/lib64/heimdal/"
	export PATH="/opt/atomicorp/atomic/root/usr/bin:$PATH"
	export LDFLAGS="-L/opt/atomicorp/atomic/root/usr/lib64/heimdal -L/opt/atomicorp/atomic/root/usr/lib64/ -lkrb5"
	export CFLAGS="$CFLAGS -I/opt/atomicorp/atomic/root/usr/include/"
	export PKG_CONFIG_PATH="/opt/atomicorp/atomic/root/usr/lib64/pkgconfig:/opt/atomicorp/atomic/root/usr/lib64/heimdal/pkgconfig/"
	export CMAKE_PREFIX_PATH="/opt/atomicorp/atomic/root/"

%endif




%if  0%{?rhel} == 7
cmake3 \
%else 
%cmake \
%endif 
	-DCMAKE_VERBOSE_MAKEFILE=ON \
        -DCMAKE_INSTALL_PREFIX=%{_prefix} \
        -DSYSCONFDIR=%{_sysconfdir} \
	-DLIBDIR=%{_libdir} \
        -DLOCALSTATEDIR=%{_localstatedir} \
	-DBUILD_WITH_LDAP=ON

%make_build
%{__make} doc-full

%install
make install  DESTDIR=$RPM_BUILD_ROOT


%post 
/sbin/ldconfig

%postun 
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%license COPYING
%doc CHANGELOG.md README.md
#%{_bindir}/openvas-nasl
#%{_bindir}/openvas-nasl-lint
%{_libdir}/libgvm_*
#%{_mandir}/man1/openvas-nasl.1.gz
#%{_mandir}/man1/openvas-nasl-lint.1.gz
#/usr/share/openvas/openvas-services
#/usr/share/openvas/openvas-lsc-rpm-creator.sh


%files devel
%defattr(-,root,root,-)
#{_bindir}/libopenvas-config
#{_mandir}/man1/libopenvas-config.1.gz
%{_libdir}/pkgconfig/libgvm*.pc
%{_includedir}/gvm/

%if 0%{!?el5}
%files doc
%defattr(-,root,root,-)
%doc doc/generated/html
%doc doc/example.auth.conf
%doc doc/example.target.locators
%doc doc/signatures-howto.txt
%doc doc/test_ipv6_packet_forgery.nasl
%doc doc/wmi-howto.txt
%endif



%changelog
* Sat Aug 15 2020 Scott R. Shinn <scott@atomicorp.com> - 20.8.0-RELEASE-AUTO
- Update to 20.8.0

* Fri Oct 25 2019 Scott R. Shinn <scott@atomicorp.com> - 11.0.0-RELEASE-AUTO
- Update to 11.0.0

* Fri Apr 5 2019 Scott R. Shinn <scott@atomicorp.com> - 10.0.0-RELEASE-AUTO
- Update to 10.0.0

* Wed Aug 31 2016 Scott R. Shinn <scott@atomicorp.com> - 8.0.8-25
- Update to 8.0.8

* Fri Mar 18 2016 Scott R. Shinn <scott@atomicorp.com> - 8.0.7-24
- Update to 8.0.7

* Wed Jan 13 2016 Scott R. Shinn <scott@atomicorp.com> - 8.0.6-23
- Backport r24104 (Patch originally from Guillaume Castagnino)
  * misc/openvas_server.c: Replace 'SECURE' with 'NORMAL'.

* Mon Dec 21 2015 Scott R. Shinn <scott@atomicorp.com> - 8.0.6-22
- Update to 8.0.6

* Mon Jul 13 2015 Scott R. Shinn <scott@atomicorp.com> - 8.0.4-20
- Update to 8.0.4

* Sat May 23 2015 Scott R. Shinn <scott@atomicorp.com> - 8.0.3-19
- Update to 8.0.3

* Tue Mar 17 2015 Scott R. Shinn <scott@atomicorp.com> - 7.0.9-18
- Update to 7.0.9

* Fri Jan 30 2015 Scott R. Shinn <scott@atomicorp.com> - 7.0.7-17
- UPdate to 7.0.7

* Mon Dec 15 2014 Scott R. Shinn <scott@atomicorp.com> - 7.0.6-16
- Fedora 21 updates

* Thu Nov 27 2014 Scott R. Shinn <scott@atomicorp.com> - 7.0.6-15
- Update to 7.0.6

* Mon Nov 17 2014 Scott R. Shinn <scott@atomicorp.com> - 7.0.5-14
- Update to 7.0.5

* Tue Sep 9 2014 Scott R. Shinn <scott@atomicorp.com> - 7.0.4-13
- Update to 7.0.4

* Fri Aug 1 2014 Scott R. Shinn <scott@atomicorp.com> - 7.0.3-12
- Update to 7.0.3

* Wed Jul 2 2014 Scott R. Shinn <scott@atomicorp.com> - 7.0.2-11
- Add libssh support

* Mon Jun 16 2014 Scott R. Shinn <scott@atomicorp.com> - 7.0.2-10
- Update to 7.0.2

* Sat May 3 2014 Scott R. Shinn <scott@atomicorp.com> - 7.0.1-9
- Update to 7.0.1

* Fri Feb 28 2014 Scott R. Shinn <scott@atomicorp.com> - 6.0.2-8
- Update to 6.0.2

* Fri Oct 25 2013 Scott R. Shinn <scott@atomicorp.com> - 6.0.1-7
- Update to 6.0.1

* Thu Apr 18 2013 Scott R. Shinn <scott@atomicorp.com> - 6.0.0-6
- Update to 6.0.0
- Remove el4 references 

* Wed Nov 07 2012 Scott R. Shinn <scott@atomicorp.com> - 5.0.4-5
- Update to 5.0.4

* Mon Aug 20 2012 Scott R. Shinn <scott@atomicorp.com> - 5.0.3-4
- Update to 5.0.3 

* Wed Jul 25 2012 Scott R. Shinn <scott@atomicorp.com> - 5.0.1-3
- Backport fix for gnutls 2.17 support

* Thu May 10 2012 Scott R. Shinn <scott@atomicorp.com> - 5.0.1-2
- Update to 5.0.1

* Tue Apr 24 2012 Scott R. Shinn <scott@atomicorp.com> - 5.0.0-1
- Update to 5.0.0
- Add in documentation package

* Mon Nov 7 2011 Scott R. Shinn <scott@atomicorp.com> - 4.0.6-3
- Bugfix #XXX, correct md5sum for the lsc rpm creation script

* Fri Nov 4 2011 Scott R. Shinn <scott@atomicorp.com> - 4.0.6-1
- Update to 4.0.6

* Wed Jun 1 2011 Scott R. Shinn <scott@atomicorp.com> - 4.0.5-1
- Update to 4.0.5

* Wed May 4 2011 Scott R. Shinn <scott@atomicorp.com> - 4.0.4-1
- Update to 4.0.4

* Mon Mar 7 2011 Scott R. Shinn <scott@atomicorp.com> - 4.0.3-1
- Update to 4.0.3

* Wed Feb 23 2011 Scott R. Shinn <scott@atomicorp.com> - 4.0.2-1
- Update to 4.0.2
- Happy 40th Mike!

* Tue Feb 22 2011 Scott R. Shinn <scott@atomicorp.com> - 4.0.1-1
- Update to 4.0.1

* Thu Feb 3 2011 Scott R. Shinn <scott@atomicorp.com> - 4.0.0-1
- Update to 4.0 final

* Wed Jan 19 2011 Scott R. Shinn <scott@atomicorp.com> - 4.0-0.3
- Update to 4.0-rc2

* Wed Dec 29 2010 Scott R. Shinn <scott@atomicorp.com> - 4.0-0.2
- Update to 4.0-rc1

* Fri Dec 3 2010 Scott R. Shinn <scott@atomicorp.com> - 4.0-beta2 
- Update to 4.0-beta2

* Sun Oct 17 2010 Scott R. Shinn <scott@atomicorp.com> - 3.1.3-2
- Rebuild libraries with wmi support

* Fri Sep 10 2010 Scott R. Shinn <scott@atomicorp.com> - 3.1.3-1
- Update to 3.1.3

* Thu Aug 26 2010 Scott R. Shinn <scott@atomicorp.com> - 3.1.2-1
- Update to 3.1.2

* Thu Jul 1 2010 Scott R. Shinn <scott@atomicorp.com> - 3.1.0-3
- Update to 3.1.0rc3

* Mon Jun 28 2010 Scott R. Shinn <scott@atomicorp.com> - 3.1.0-2
- Update to 3.1.0rc2

* Wed May 19 2010 Scott R. Shinn <scott@atomicorp.com> - 3.1.0-1
- Update to 3.1.0rc1

* Sun Apr 11 2010 Scott R. Shinn <scott@atomicorp.com> - 3.0.5-1
- Update to 3.0.5

* Wed Mar 3 2010 Scott R. Shinn <scott@atomicorp.com> - 3.0.4-1
- Update to 3.0.4

* Thu Feb 4 2010 Scott R. Shinn <scott@atomicorp.com> - 3.0.3-1
- Update to 3.0.3

* Mon Jan 11 2010 Scott R. Shinn <scott@atomicorp.com> - 3.0.1-1
- Update to 3.0.1

* Fri Dec 18 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 3.0.0-1
- Update to 3.0.0

* Tue Aug 18 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0.4-1
- Update to 2.0.4

* Thu Jun 11 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0.3-1
- Update to 2.0.3

* Fri Mar 6 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0.2-1
- Update to 2.0.2

* Mon Feb 9 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0.1-1
- Update to 2.0.1

* Tue Dec 30 2008 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0.0-2
- Bugfix #XXX, added libtoolize before configure

* Mon Dec 22 2008 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0.0
- Update to 2.0.0

* Thu Dec 11 2008 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0.0.rc1
- Update to 2.0.0.rc1

* Mon Nov 17 2008 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0.0.beta2-1
- Update to 2.0.0.beta2
 
* Fri Nov 7 2008 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0.0.beta1-1
- Update to 2.0.0.beta1

* Wed Nov 5 2008 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.0.2-1
- Update to 1.0.2
- Merge into Atomic

* Fri Apr 18 2008 Jan-Oliver Wagner <jan-oliver.wagner@intevation.de>
  - Adapated for Fedora 8 (naming)
  - %post and %postrun changed to apply ldconfig directly instead of using
    a (SUSE specific?) scriplet.
  - extended BuildRequires with libpcap-devel
* Tue Apr 15 2008 Jan-Oliver Wagner <jan-oliver.wagner@intevation.de>
  Initial SUSE 10.2 spec file, tested for i586
