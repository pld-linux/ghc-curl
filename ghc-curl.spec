#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	curl
Summary:	Haskell binding to libcurl
Summary(pl.UTF-8):	Wiązanie Haskella do biblioteki libcurl
Name:		ghc-%{pkgname}
Version:	1.3.8
Release:	3
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/curl
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	853113e2ac933e203894a4588150821d
URL:		http://hackage.haskell.org/package/curl
BuildRequires:	curl-devel
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.9
BuildRequires:	ghc-containers
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-bytestring-prof >= 0.9
BuildRequires:	ghc-containers-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base >= 3
Requires:	ghc-base < 5
Requires:	ghc-bytestring >= 0.9
Requires:	ghc-containers
%requires_releq	ghc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
libcurl is a client-side URL transfer library, supporting FTP, FTPS,
HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS and FILE.
libcurl supports SSL certificates, HTTP POST, HTTP PUT, FTP uploading,
HTTP form based upload, proxies, cookies, user+password authentication
(Basic, Digest, NTLM, Negotiate, Kerberos4), file transfer resume,
http proxy tunneling and more!

This package provides a Haskell binding to libcurl.

%description -l pl.UTF-8
libcurl to biblioteka kliencka do przesyłania danych wskazanych przez
URL-e, obsługująca protokoły FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP,
TELNET, DICT, LDAP, LDAPS oraz FILE. libcurl obsługuje certyfikaty
SSL, wysyłanie danych przez HTTP POST, HTTP PUT i FTP, pobieranie
danych w oparciu o formularze HTTP, a także serwery proxy, ciasteczka,
uwierzytelnianie nazwą użytkownika i hasłem (metody Basic, Digest,
NTLM, Negotiate, Kerberos4), wznawianie transmisji plików, tunelowanie
proxy HTTP itd.

Ten pakiet zapewnia wiązanie Haskella do biblioteki libcurl.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
%configure
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGES %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HScurl-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHScurl-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Curl.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Curl
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Curl/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHScurl-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Curl.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Curl/*.p_hi
%endif
