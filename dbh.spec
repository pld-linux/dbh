%define		ver		1.0
%define		rel		14

Summary:	Disk based hash library
Name:		dbh
Version: 	%{ver}.%{rel}
Release: 	0.1
License:	QPL
Group:		Libraries
Source0:	http://belnet.dl.sourceforge.net/sourceforge/dbh/%{name}_%{ver}-%{rel}.tgz
# Source0-md5:	11352e539a3e40f23d539a52f2153b95
URL:		http://dbh.sourceforge.net
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description 
Disk based hashes is a method to create multidimensional binary trees on disk.
This library permits the extension of database concept to a plethora of 
electronic data, such as graphic information. With the multidimensional binary 
tree it is possible to mathematically prove that access time to any 
particular record is minimized (using the concept of critical points from 
calculus), which provides the means to construct optimized databases for 
particular applications.  

%package devel
Summary:	Disk based hash library development files
Group:		Libraries
Requires:	%{name} = %{version}

%description devel
Disk based hash library development files

%package static
Summary:	Disk based hash static libraries
Group:		Libraries
Requires:	%{name}-devel = %{version}

%description static
Disk based hash static libraries

%package examples
Summary:	Disk based hash library examples
Group:		Libraries

%description examples
Disk based hash library examples

%prep
%setup  -q -n %{name}_%{ver}-%{rel}

%build
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/src/examples/%{name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT 

cd examples
install -m 644 simple_hash.c $RPM_BUILD_ROOT/usr/src/examples/%{name}-%{version}
install -m 644 trafico.c $RPM_BUILD_ROOT/usr/src/examples/%{name}-%{version}
install -m 644 Makefile $RPM_BUILD_ROOT/usr/src/examples/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc  AUTHORS COPYING ChangeLog NEWS README TODO doc/*.html
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libdbh.a

%files examples
%defattr(644,root,root,755)
%dir /usr/src/examples/%{name}-%{version}
/usr/src/examples/%{name}-%{version}/*
