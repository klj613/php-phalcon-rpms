%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global _name       phalcon
%global subdir build/%{__isa_bits}bits

# nuke private-shared-object-provides
%global __provides_exclude %{_name}.so*

Name:           php53u-%{_name}13
Version:        1.3.1
Release:        1
Summary:        A web framework implemented as a C extension

License:        BSD and MIT and Zend and PHP
URL:            http://phalconphp.com/
Source0:        https://github.com/phalcon/cphalcon/archive/%{version}.tar.gz#/%{_name}-%{version}.tar.gz

BuildRequires:  php53u-devel
BuildRequires:  chrpath
#BuildRequires:  php53u-phpunit-PHPUnit
BuildRequires:  php53u-mcrypt
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires:       php53u-pdo

%description
A web framework implemented as a C extension; offering high performance and
lower resource consumption. Several database backends are supported via
additional packages.

%prep
%setup -q -n cphalcon-%{version}

%build
cd %{subdir}
phpize
%configure --enable-phalcon

make %{?_smp_mflags}

%install
cd %{subdir}
%{__mkdir_p} %{buildroot}%{php_extdir}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d

make install INSTALL_ROOT=%{buildroot}

echo "; comment out next line to disable %{_name} extension in php" > %{buildroot}/%{_sysconfdir}/php.d/%{_name}.ini
echo "extension=%{_name}.so" >> %{buildroot}/%{_sysconfdir}/php.d/%{_name}.ini

#%check
# TODO - Run all non-database tests
#TEMPDIR=$(mktemp -d)
#echo $TEMPDIR
#find %{php_extdir} -name '*.so' -exec ln -s {} $TEMPDIR \;
#ln -s %{buildroot}/%{php_extdir}/%{_name}.so $TEMPDIR
#php -d extension_dir=$TEMPDIR -d extension=%{_name}.so /usr/bin/phpunit --debug -c unit-tests/phpunit.xml
#rm -rf $TEMPDIR

%files
%doc CHANGELOG CONTRIBUTING.md README.md docs/DOCUMENTATION.txt docs/LICENSE.md  docs/LICENSE.txt
%{php_extdir}/%{_name}.so
%config(noreplace) %{_sysconfdir}/php.d/phalcon.ini

%changelog
