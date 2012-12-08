%define oname GeoIP

%define major 1
%define updatemajor 0

%define libname %mklibname geoip %{major}
%define libname1 %mklibname geoipupdate %{updatemajor}
%define develname %mklibname geoip -d

Summary:	Find what country an IP address or hostname originates from
Name:		geoip
Version:	1.4.8
Release:	3
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.maxmind.com/app/c
Source0:	http://www.maxmind.com/download/geoip/api/c/%{oname}-%{version}.tar.gz
Source1:	http://www.maxmind.com/download/geoip/database/%{oname}.dat.gz
Source2:	http://www.maxmind.com/download/geoip/database/LICENSE.txt
Source3:	http://www.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
Source4:	http://www.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz
Source5:	geoip.contrab
BuildRequires:	zlib-devel
BuildRequires:	autoconf automake libtool

%description
GeoIP is a C library that enables the user to find the country that any IP
address or hostname originates from. It uses a file based database that is
accurate as of March 2003. This database simply contains IP blocks as keys,
and countries as values. This database should be more complete and accurate
than using reverse DNS lookups. Commercial databases and automatic update
services are available from http://www.maxmind.com/

This module can be used to automatically select the geographically closest
mirror, to analyze your web server logs to determine the countries of your
visitors, for credit card fraud detection, and for software export controls.

%package -n	%{libname}
Summary:	Shared library part of GeoIP
Group:		System/Libraries
Requires:	%{name} >= %{version}-%{release}

%description -n	%{libname}
GeoIP is a C library that enables the user to find the country that any IP
address or hostname originates from. It uses a file based database that is
accurate as of March 2003. This database simply contains IP blocks as keys,
and countries as values. This database should be more complete and accurate
than using reverse DNS lookups. Commercial databases and automatic update
services are available from http://www.maxmind.com/

This module can be used to automatically select the geographically closest
mirror, to analyze your web server logs to determine the countries of your
visitors, for credit card fraud detection, and for software export controls.

%package -n	%{libname1}
Summary:	Shared library parts of GeoIP
Group:		System/Libraries

%description -n	%{libname1}
GeoIP is a C library that enables the user to find the country that any IP
address or hostname originates from. It uses a file based database that is
accurate as of March 2003. This database simply contains IP blocks as keys,
and countries as values. This database should be more complete and accurate
than using reverse DNS lookups. Commercial databases and automatic update
services are available from http://www.maxmind.com/

This module can be used to automatically select the geographically closest
mirror, to analyze your web server logs to determine the countries of your
visitors, for credit card fraud detection, and for software export controls.

%package -n	%{develname}
Summary:	Headers and libraries needed for GeoIP development
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Requires:	%{libname1} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{oname}-devel = %{version}-%{release}

%description -n	%{develname}
GeoIP is a C library that enables the user to find the country that any IP
address or hostname originates from. It uses a file based database that is
accurate as of March 2003. This database simply contains IP blocks as keys,
and countries as values. This database should be more complete and accurate
than using reverse DNS lookups. Commercial databases and automatic update
services are available from http://www.maxmind.com/

This module can be used to automatically select the geographically closest
mirror, to analyze your web server logs to determine the countries of your
visitors, for credit card fraud detection, and for software export controls.

%prep
%setup -q -n %{oname}-%{version}

zcat %{SOURCE1} > data/GeoIP.dat
cp %{SOURCE2} LICENSE.txt
zcat %{SOURCE3} > data/GeoLiteCity.dat
zcat %{SOURCE4} > data/GeoIPASNum.dat

%build
rm -rf configure autom4te.cache
libtoolize --copy --force; aclocal; automake --gnu --add-missing --copy; autoconf

%configure2_5x --disable-static

%make

%check
#gw disable tests if there's no network
if ping -c 1 svn.mandriva.com; then
make check
fi

%install
%makeinstall_std
#gw path fix man page
perl -pi -e "s^%{buildroot}^^" %{buildroot}%{_mandir}/man1/geoipupdate.1

mkdir -p %{buildroot}%{_sysconfdir}/cron.monthly
install -m755 %{SOURCE5} %{buildroot}%{_sysconfdir}/cron.monthly/geoip
install -m0644 data/GeoLiteCity.dat %{buildroot}%{_datadir}/GeoIP/
install -m0644 data/GeoIPASNum.dat %{buildroot}%{_datadir}/GeoIP/

%files
%doc AUTHORS COPYING ChangeLog README TODO LICENSE.txt
%config(noreplace) %{_sysconfdir}/GeoIP.conf
%config(noreplace) %{_sysconfdir}/GeoIP.conf.default
%{_bindir}/geoiplookup
%{_bindir}/geoipupdate
%{_bindir}/geoiplookup6
%config(noreplace) %{_datadir}/GeoIP
%{_mandir}/man1/geoiplookup.1*
%{_mandir}/man1/geoiplookup6.1*
%{_mandir}/man1/geoipupdate.1*
%{_sysconfdir}/cron.monthly/geoip

%files -n %{libname}
%{_libdir}/libGeoIP.so.%{major}*

%files -n %{libname1}
%{_libdir}/libGeoIPUpdate.so.%{updatemajor}*

%files -n %{develname}
%{_libdir}/lib*.so
%{_includedir}/*


%changelog
* Thu Dec 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.8-2
+ Revision: 738982
- drop the static libs and the libtool *.la files
- various fixes

* Mon Jul 11 2011 Götz Waschk <waschk@mandriva.org> 1.4.8-1
+ Revision: 689501
- update to new version 1.4.8

* Wed Apr 20 2011 Götz Waschk <waschk@mandriva.org> 1.4.7-1
+ Revision: 656113
- update to new version 1.4.7

* Sun Aug 01 2010 Funda Wang <fwang@mandriva.org> 1.4.6-8mdv2011.0
+ Revision: 564253
- rebuild for perl 5.12.1

  + Sandro Cazzaniga <kharec@mandriva.org>
    - fix Source1

* Thu Feb 18 2010 Götz Waschk <waschk@mandriva.org> 1.4.6-6mdv2010.1
+ Revision: 507920
- use the right file for the cron job

* Thu Feb 18 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.4.6-5mdv2010.1
+ Revision: 507900
- New monthly crontab that lets update to non-payed suscriptors
- DataBase update to 20100201

* Wed Sep 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.6-2mdv2010.0
+ Revision: 435105
- added some additional data files

* Tue Mar 17 2009 Götz Waschk <waschk@mandriva.org> 1.4.6-1mdv2009.1
+ Revision: 356530
- new version
- update file list
- update license

* Fri Oct 17 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.5-1mdv2009.1
+ Revision: 294777
- new version

* Fri Jun 13 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.4-3mdv2009.0
+ Revision: 218736
- new database

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sat May 10 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.4-2mdv2009.0
+ Revision: 205387
- new database

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.4-1mdv2008.1
+ Revision: 162379
- 1.4.4
- newer database

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Sep 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-1mdv2008.0
+ Revision: 78623
- 1.4.3

  + Thierry Vignaud <tv@mandriva.org>
    - replace %%{_datadir}/man by %%{_mandir}!


* Wed Jan 17 2007 Götz Waschk <waschk@mandriva.org> 1.4.1-3mdv2007.0
+ Revision: 109845
- fix man page
- fix check

* Wed Jan 17 2007 Götz Waschk <waschk@mandriva.org> 1.4.1-2mdv2007.1
+ Revision: 109777
- add missing data file (bug #28257)

* Mon Jan 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.1-1mdv2007.1
+ Revision: 106089
- 1.4.1
- drop the upstream update vulnerability patch

* Fri Jan 05 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-3mdv2007.1
+ Revision: 104548
- plug a sec hole (P0)
- rebuild
- Import geoip

* Tue Aug 29 2006 G�tz Waschk <waschk@mandriva.org> 1.4.0-2mdv2007.0
- spec fix

* Thu Aug 24 2006 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-1mdv2007.0
- 1.4.0
- new S1

* Fri Jul 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1.3.17-1mdv2007.0
- 1.3.17
- new S1

* Fri Jul 21 2006 Götz Waschk <waschk@mandriva.org> 1.3.8-4mdk
- Rebuild

* Mon Jan 16 2006 G�tz Waschk <waschk@mandriva.org> 1.3.8-3mdk
- fix build without network

* Tue Jan 03 2006 Götz Waschk <waschk@mandriva.org> 1.3.8-2mdk
- Rebuild
- use mkrel

* Sun Jan 02 2005 Frederic Lepied <flepied@mandrakesoft.com> 1.3.8-1mdk
- New release 1.3.8

* Tue Sep 28 2004 Frederic Lepied <flepied@mandrakesoft.com> 1.3.6-2mdk
- updated data

* Wed Aug 18 2004 Frederic Lepied <flepied@mandrakesoft.com> 1.3.6-1mdk
- New release 1.3.6

* Tue May 11 2004 Goetz Waschk <waschk@linux-mandrake.com> 1.3.2-1mdk
- New release 1.3.2

* Thu Feb 19 2004 G�tz Waschk <waschk@linux-mandrake.com> 1.3.1-1mdk
- new version

