%define oname GeoIP
%define major 1

%define libname %mklibname geoip %{major}
%define devname %mklibname geoip -d

Summary:	Find what country an IP address or hostname originates from
Name:		geoip
Version:	1.6.12
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.maxmind.com/app/c
Source0:	https://github.com/maxmind/geoip-api-c/releases/download/v%{version}/GeoIP-%{version}.tar.gz
Source1:	http://www.maxmind.com/download/geoip/database/%{oname}.dat.gz
Source2:	http://www.maxmind.com/download/geoip/database/LICENSE.txt
Source3:	http://www.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
Source4:	http://www.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz
Source5:	geoip.contrab
Source6:	http://geolite.maxmind.com/download/geoip/database/GeoIPv6.dat.gz

BuildRequires:	libtool
BuildRequires:	pkgconfig(zlib)
BuildRequires:	gzip-utils

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
Suggests:	%{name} >= %{version}-%{release}

%description -n	%{libname}
This package contains a shared library for %{name}.

%package -n	%{devname}
Summary:	Headers and libraries needed for GeoIP development
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{oname}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the development files for %{name}.

%prep
%setup -qn %{oname}-%{version}

zcat %{SOURCE1} > data/GeoIP.dat
cp %{SOURCE2} LICENSE.txt
zcat %{SOURCE3} > data/GeoLiteCity.dat
zcat %{SOURCE4} > data/GeoIPASNum.dat
zcat %{SOURCE6} > data/GeoIPv6.dat

%build
rm -rf configure autom4te.cache
libtoolize --copy --force; aclocal; automake --gnu --add-missing --copy; autoconf

%configure \
	--disable-static

%make

%check
#gw disable tests if there's no network
if ping -c 1 www.google.com; then
make check
fi

%install
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/cron.monthly
mkdir -p %{buildroot}%{_datadir}/GeoIP

install -m755 %{SOURCE5} %{buildroot}%{_sysconfdir}/cron.monthly/geoip
install -m0644 data/*.dat %{buildroot}%{_datadir}/GeoIP/

%files
%doc AUTHORS COPYING ChangeLog README.md LICENSE.txt
%{_bindir}/geoiplookup
%{_bindir}/geoiplookup6
%config(noreplace) %{_datadir}/GeoIP
%{_mandir}/man1/geoiplookup.1*
%{_mandir}/man1/geoiplookup6.1*
%{_sysconfdir}/cron.monthly/geoip

%files -n %{libname}
%{_libdir}/libGeoIP.so.%{major}*

%files -n %{devname}
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

