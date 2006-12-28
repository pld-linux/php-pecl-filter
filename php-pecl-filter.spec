%define		_modname	filter
%define		_status		beta
Summary:	%{_modname} - extension for safely dealing with input parameters
Summary(pl):	%{_modname} - rozszerzenie do bezpiecznej obs³ugi danych wej¶ciowych
Name:		php-pecl-%{_modname}
Version:	0.11.0
Release:	2
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	0255df6106eb36f1bc35e102ce505d9e
URL:		http://pecl.php.net/package/filter/
BuildRequires:	pcre-devel
BuildRequires:	php-devel >= 3:5.1.5-2
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Provides:	php(filter)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
We all know that you should always check input variables, but PHP does
not offer really good functionality for doing this in a safe way. The
Input Filter extension is meant to address this issue by implementing
a set of filters and mechanisms that users can use to safely access
their input data.

In PECL status of this extension is: %{_status}.

%description -l pl
Wiadomo, ¿e trzeba zawsze sprawdzaæ zmienne wej¶ciowe, ale PHP nie
oferuje naprawdê dobrej funkcjonalno¶ci do robienia tego w sposób
bezpieczny. Rozszerzenie Input Filter ma rozwi±zaæ ten problem poprzez
zaimplementowanie zestawu filtrów i mechanizmów, których u¿ytkownicy
mog± bezpiecznie u¿ywaæ do dostêpu do danych.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure \
	--with-libdir=%{_lib}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
