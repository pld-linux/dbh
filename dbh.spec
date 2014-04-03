#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	Disk based hash library
Summary(pl.UTF-8):	Biblioteka obsługująca tablice haszujące na dysku
Name:		dbh
Version:	5.0.7
Release:	2
License:	LGPL
Group:		Libraries
Source0:	http://downloads.sourceforge.net/dbh/%{name}-%{version}.tar.gz
# Source0-md5:	15e1bd22aca735415dfb5ec60f48181b
Patch0:		am.patch
Patch1:		%{name}-bsd.patch
URL:		http://dbh.sourceforge.net/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	gtk-doc >= 1.15
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
rekordu jest minimalny (używając zasady punktów krytycznych), co daje
środki do tworzenia zoptymalizowanych baz danych dla aplikacji.

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

%package apidocs
Summary:	API documentation for dbh library
Summary(pl.UTF-8):	Dokumentacja API biblioteki dbh
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for dbh library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki dbh.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static} \
	--without-examples

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p examples/{filesystem,simple_hash}.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# belongs to man3
%{__mv} $RPM_BUILD_ROOT%{_mandir}/man1/dbh.h.1 $RPM_BUILD_ROOT%{_mandir}/man3/dbh.h.3
# just a copy of dbh.h.1, useless
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/dbh.1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS
%attr(755,root,root) %{_libdir}/libdbh2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdbh2.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdbh2.so
%{_libdir}/libdbh2.la
%{_includedir}/dbh
%{_pkgconfigdir}/dbh2.pc
%{_examplesdir}/%{name}-%{version}
%{_mandir}/man3/dbh.h.3*
%{_mandir}/man3/dbh_*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdbh2.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/dbh
