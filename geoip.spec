%define oname GeoIP
%define major 1
%define updatemajor 0

%define libname %mklibname geoip %{major}
%define libupdate %mklibname geoipupdate %{updatemajor}
%define devname %mklibname geoip -d

Summary:	Find what country an IP address or hostname originates from
Name:		geoip
Version:	1.5.1
Release:	3
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.maxmind.com/app/c
Source0:	http://www.maxmind.com/download/geoip/api/c/%{oname}-%{version}.tar.gz
Source1:	http://www.maxmind.com/download/geoip/database/%{oname}.dat.gz
Source2:	http://www.maxmind.com/download/geoip/database/LICENSE.txt
Source3:	http://www.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
Source4:	http://www.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz
Source5:	geoip.contrab
BuildRequires:	libtool
BuildRequires:	pkgconfig(zlib)

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

%package -n	%{libupdate}
Summary:	Shared library parts of GeoIP
Group:		System/Libraries

%description -n	%{libupdate}
This package contains a shared library for %{name}.

%package -n	%{devname}
Summary:	Headers and libraries needed for GeoIP development
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Requires:	%{libupdate} = %{version}-%{release}
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

%build
rm -rf configure autom4te.cache
libtoolize --copy --force; aclocal; automake --gnu --add-missing --copy; autoconf

%configure2_5x \
	--disable-static

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

%files -n %{libupdate}
%{_libdir}/libGeoIPUpdate.so.%{updatemajor}*

%files -n %{devname}
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

