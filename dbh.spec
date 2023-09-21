#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	Disk based hash library
Summary(pl.UTF-8):	Biblioteka obsługująca tablice haszujące na dysku
Name:		dbh
Version:	5.0.22
Release:	1
License:	GPL v3+
Group:		Libraries
Source0:	https://downloads.sourceforge.net/dbh/libdbh2-%{version}.tar.gz
# Source0-md5:	f8c592f6fd4d336cbb5529dc52177e4f
Patch0:		am.patch
URL:		http://www.gnu.org/software/libdbh/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.11
BuildRequires:	gtk-doc >= 1.18
BuildRequires:	libtool >= 2:2
BuildRequires:	rpm-build >= 4.6
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
Obsoletes:	dbh-examples < 1.0.14-1

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
BuildArch:	noarch

%description apidocs
API documentation for dbh library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki dbh.

%prep
%setup -q -n libdbh2-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--without-examples

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libdbh.la

cp -p examples/{filesystem,simple_hash}.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libdbh.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdbh.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdbh.so
%{_includedir}/dbh
%{_pkgconfigdir}/dbh2.pc
%{_examplesdir}/%{name}-%{version}
%{_mandir}/man3/dbh.3*
%{_mandir}/man3/dbh.h.3*
%{_mandir}/man3/dbh_*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdbh.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/dbh
