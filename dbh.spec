#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Disk based hash library
Summary(pl.UTF-8):	Biblioteka obsługująca tablice haszujące na dysku
Name:		dbh
Version:	5.0.7
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/dbh/%{name}-%{version}.tar.gz
# Source0-md5:	15e1bd22aca735415dfb5ec60f48181b
Patch0:		am.patch
URL:		http://dbh.sourceforge.net/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Disk based hashes is a method to create multidimensional binary trees
on disk. This library permits the extension of database concept to a
plethora of electronic data, such as graphic information. With the
multidimensional binary tree it is possible to mathematically prove
that access time to any particular record is minimized (using the
concept of critical points from calculus), which provides the means to
construct optimized databases for particular applications.

%description -l pl.UTF-8
Hasze przechowywane na dysku to metoda tworzenia wielowymiarowych
drzew binarnych na dysku. Biblioteka pozwala rozszerzać pojęcie bazy
danych o bogactwo danych elektronicznych, takich jak informacje
graficzne. Można udowodnić matematycznie, że przy użyciu
wielowymiarowego drzewa binarnego czas dostępu do każdego konkretnego
rekordu jest minimalny (używając zasady punktów krytycznych), co
daje środki do tworzenia zoptymalizowanych baz danych dla aplikacji.

%package devel
Summary:	Disk based hash library development files
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki dbh
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	dbh-examples

%description devel
Disk based hash library development files.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki dbh.

%package static
Summary:	Disk based hash static library
Summary(pl.UTF-8):	Statyczna biblioteka dbh
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Disk based hash static library.

%description static -l pl.UTF-8
Statyczna biblioteka dbh.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd examples
install filesystem.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install simple_hash.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib*.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_gtkdocdir}/dbh
%{_libdir}/lib*.la
%{_includedir}/dbh
%{_pkgconfigdir}/*.pc
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
