%define oname GeoIP

%define major 1
%define updatemajor 0

%define libname %mklibname geoip %{major}
%define libname1 %mklibname geoipupdate %{updatemajor}

Summary:	Find what country an IP address or hostname originates from
Name:		geoip
Version:	1.4.1
Release:	%mkrel 3
License:	LGPL
Group:		System/Libraries
URL:		http://www.maxmind.com/app/c
Source0:	http://www.maxmind.com/download/geoip/api/c/%{oname}-%{version}.tar.bz2
Source1:	http://www.maxmind.com/download/geoip/database/GeoIP.dat.bz2
Source2:	http://www.maxmind.com/download/geoip/database/LICENSE.txt
BuildRequires:	zlib-devel
BuildRequires:	libtool
BuildRequires:	autoconf2.5
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
Requires:	%{name} >= %{version}

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

%package -n	%{libname}-devel
Summary:	Headers and libraries needed for GeoIP development
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	%{libname1} = %{version}
Provides:	lib%{name}-devel = %{version}
Provides:	%{oname}-devel = %{version}

%description -n	%{libname}-devel
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

%setup -q -n %oname-%{version}

bzip2 -cd %{SOURCE1} > data/GeoIP.dat
cp %{SOURCE2} LICENSE.txt

%build
rm -rf configure autom4te.cache
libtoolize --copy --force; aclocal; automake --gnu --add-missing --copy; autoconf

%configure2_5x

%make

%check
#gw disable tests if there's no network
if ping -c 1 svn.mandriva.com; then
make check
fi

%install
rm -rf %{buildroot}

%makeinstall
#gw path fix man page
perl -pi -e "s^%buildroot^^" %buildroot%_mandir/man1/geoipupdate.1

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libname1} -p /sbin/ldconfig

%postun -n %{libname1} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README TODO LICENSE.txt
%config(noreplace) %{_sysconfdir}/GeoIP.conf
%config(noreplace) %{_sysconfdir}/GeoIP.conf.default
%{_bindir}/geoiplookup
%{_bindir}/geoipupdate
%dir %{_datadir}/GeoIP/
%{_datadir}/GeoIP/GeoIP.dat
%{_mandir}/man1/geoiplookup.1*
%{_mandir}/man1/geoipupdate.1*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libGeoIP.so.%{major}*

%files -n %{libname1}
%defattr(-,root,root)
%{_libdir}/libGeoIPUpdate.so.%{updatemajor}*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/lib*.a
%{_includedir}/*


