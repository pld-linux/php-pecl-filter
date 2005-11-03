%define		_modname	filter
%define		_status		beta
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	%{_modname} - extension for safely dealing with input parameters
Summary(pl):	%{_modname} - rozszerzenie do bezpiecznej obs³ugi danych wej¶ciowych
Name:		php-pecl-%{_modname}
Version:	0.9.2
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	cff766bc7b84d5e8a7d06e30505b0956
URL:		http://pecl.php.net/package/filter/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.254
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
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
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
