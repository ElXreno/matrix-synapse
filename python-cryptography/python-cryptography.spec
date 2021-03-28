%bcond_without tests

%{!?python3_pkgversion:%global python3_pkgversion 3}

%global srcname cryptography
%global pyo3_version 0.13.1

Name:           python-%{srcname}
Version:        3.4.7
Release:        1%{?dist}
Summary:        PyCA's cryptography library

License:        ASL 2.0 or BSD
URL:            https://cryptography.io/en/latest/
Source0:        %{pypi_source}
Source1:        %{pypi_source}.asc
# key ids of upstream authors are published in the AUTHORS file:
#    https://github.com/pyca/cryptography/blob/master/AUTHORS.rst
# gpg2 --recv-keys "05FD 9FA1 6CF7 5735 0D91 A560 235A E5F1 29F9 ED98"
# gpg2 --export --export-options export-minimal "05FD 9FA1 6CF7 5735 0D91 A560 235A E5F1 29F9 ED98" > gpgkey-05FD_9FA1_6CF7_5735_0D91_A560_235A_E5F1_29F9_ED98.gpg
Source2:        gpgkey-05FD_9FA1_6CF7_5735_0D91_A560_235A_E5F1_29F9_ED98.gpg
%if 0%{?rhel}
                # created by ./vendor_rust.py helper script
Source3:        cryptography-%{version}-vendor.tar.bz2
Source4:        conftest-skipper.py
%endif

ExclusiveArch:  %{rust_arches}

BuildRequires:  openssl-devel
BuildRequires:  gcc
BuildRequires:  gnupg2
%if 0%{?fedora}
BuildRequires:  rust-packaging
%else
BuildRequires:  rust-toolset
%endif

BuildRequires:  python%{python3_pkgversion}-cffi >= 1.7
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-setuptools-rust >= 0.11.3
BuildRequires:  python%{python3_pkgversion}-six >= 1.4.1

%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-cryptography-vectors = %{version}
%if 0%{?fedora}
BuildRequires:  python%{python3_pkgversion}-hypothesis >= 1.11.4
BuildRequires:  python%{python3_pkgversion}-iso8601
BuildRequires:  python%{python3_pkgversion}-pretend
BuildRequires:  python%{python3_pkgversion}-pytest-xdist
%endif
BuildRequires:  python%{python3_pkgversion}-pytest >= 6.0
BuildRequires:  python%{python3_pkgversion}-pytest-subtests >= 0.3.2
BuildRequires:  python%{python3_pkgversion}-pytz
%endif

%description
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%package -n  python%{python3_pkgversion}-%{srcname}
Summary:        PyCA's cryptography library
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

Requires:       openssl-libs
Requires:       python%{python3_pkgversion}-six >= 1.4.1
Requires:       python%{python3_pkgversion}-cffi >= 1.7

%description -n python%{python3_pkgversion}-%{srcname}
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1 -n %{srcname}-%{version}

%generate_buildrequires

%if 0%{?fedora}
# Fedora: use cargo macros to make use of RPMified crates
%cargo_prep
cd src/rust
rm -f Cargo.lock
%cargo_generate_buildrequires
cd ../..
%else
# RHEL: use vendored Rust crates
%cargo_prep -V 3
%endif

%build
%py3_build

%install
# Actually other *.c and *.h are appropriate
# see https://github.com/pyca/cryptography/issues/1463
find . -name .keep -print -delete
%py3_install

%check
%if %{with tests}
%if 0%{?rhel}
# skip hypothesis tests on RHEL
rm -rf tests/hypothesis
# append skipper to skip iso8601 and pretend tests
cat < %{SOURCE4} >> tests/conftest.py
%endif

# see https://github.com/pyca/cryptography/issues/4885 and
# see https://bugzilla.redhat.com/show_bug.cgi?id=1761194 for deselected tests
PYTHONPATH=%{buildroot}%{python3_sitearch} %{__python3} -m pytest -k "not (test_buffer_protocol_alternate_modes or test_dh_parameters_supported or test_load_ecdsa_no_named_curve)"
%endif

%files -n python%{python3_pkgversion}-%{srcname}
%doc README.rst docs
%license LICENSE LICENSE.APACHE LICENSE.BSD
%{python3_sitearch}/%{srcname}
%{python3_sitearch}/%{srcname}-%{version}-py*.egg-info

%changelog
* Sun Mar 28 2021 ElXreno <elxreno@gmail.com> - 3.4.7-1
- Update to 3.4.7

* Wed Mar 03 2021 Christian Heimes <cheimes@redhat.com> - 3.4.6-1
- Update to 3.4.6 (#1927044)

* Mon Feb 15 2021 Christian Heimes <cheimes@redhat.com> - 3.4.5-1
- Update to 3.4.5 (#1927044)

* Fri Feb 12 2021 Christian Heimes <cheimes@redhat.com> - 3.4.4-3
- Skip iso8601 and pretend tests on RHEL

* Fri Feb 12 2021 Christian Heimes <cheimes@redhat.com> - 3.4.4-2
- Provide RHEL build infrastructure

* Wed Feb 10 2021 Christian Heimes <cheimes@redhat.com> - 3.4.4-1
- Update to 3.4.4 (#1927044)

* Mon Feb 08 2021 Christian Heimes <cheimes@redhat.com> - 3.4.2-1
- Update to 3.4.2 (#1926339)
- Package no longer depends on Rust (#1926181)

* Mon Feb 08 2021 Fabio Valentini <decathorpe@gmail.com> - 3.4.1-2
- Use dynamically generated BuildRequires for PyO3 Rust module.
- Drop unnecessary CARGO_NET_OFFLINE environment variable.

* Sun Feb 07 2021 Christian Heimes <cheimes@redhat.com> - 3.4.1-1
- Update to 3.4.1 (#1925953)

* Sun Feb 07 2021 Christian Heimes <cheimes@redhat.com> - 3.4-2
- Add missing abi3 and pytest dependencies

* Sun Feb 07 2021 Christian Heimes <cheimes@redhat.com> - 3.4-1
- Update to 3.4 (#1925953)
- Remove Python 2 support
- Remove unused python-idna dependency
- Add Rust support

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 10 2020 Christian Heimes <cheimes@redhat.com> - 3.3.1-1
- Update to 3.3.1 (#1905756)

* Wed Oct 28 2020 Christian Heimes <cheimes@redhat.com> - 3.2.1-1
- Update to 3.2.1 (#1892153)

* Mon Oct 26 2020 Christian Heimes <cheimes@redhat.com> - 3.2-1
- Update to 3.2 (#1891378)

* Mon Sep 07 2020 Christian Heimes <cheimes@redhat.com> - 3.1-1
- Update to 3.1 (#1872978)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Christian Heimes <cheimes@redhat.com> - 3.0-1
- Update to 3.0 (#185897)

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 2.9-3
- Rebuilt for Python 3.9

* Tue May 12 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 2.9-2
- add source file verification

* Fri Apr 03 2020 Christian Heimes <cheimes@redhat.com> - 2.9-1
- Update to 2.9 (#1820348)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Christian Heimes <cheimes@redhat.com> - 2.8-2
- cryptography 2.8+ no longer depends on python-asn1crypto

* Thu Oct 17 2019 Christian Heimes <cheimes@redhat.com> - 2.8-1
- Update to 2.8
- Resolves: rhbz#1762779

* Sun Oct 13 2019 Christian Heimes <cheimes@redhat.com> - 2.7-3
- Skip unit tests that fail with OpenSSL 1.1.1.d
- Resolves: rhbz#1761194
- Fix and simplify Python 3 packaging

* Sat Oct 12 2019 Christian Heimes <cheimes@redhat.com> - 2.7-2
- Drop Python 2 package
- Resolves: rhbz#1761081

* Tue Sep 03 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 2.7-1
- Update to 2.7 (#1715680).

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 28 2019 Christian Heimes <cheimes@redhat.com> - 2.6.1-1
- New upstream release 2.6.1, resolves RHBZ#1683691

* Wed Feb 13 2019 Alfredo Moralejo <amoralej@redhat.com> - 2.5-1
- Updated to 2.5.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 13 2018 Christian Heimes <cheimes@redhat.com> - 2.3-2
- Use TLSv1.2 in test as workaround for RHBZ#1615143

* Wed Jul 18 2018 Christian Heimes <cheimes@redhat.com> - 2.3-1
- New upstream release 2.3
- Fix AEAD tag truncation bug, RHBZ#1602752

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.2.1-2
- Rebuilt for Python 3.7

* Wed Mar 21 2018 Christian Heimes <cheimes@redhat.com> - 2.2.1-1
- New upstream release 2.2.1

* Sun Feb 18 2018 Christian Heimes <cheimes@redhat.com> - 2.1.4-1
- New upstream release 2.1.4

* Sun Feb 18 2018 Christian Heimes <cheimes@redhat.com> - 2.1.3-4
- Build requires gcc

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.1.3-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
