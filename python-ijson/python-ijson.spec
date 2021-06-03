%global srcname ijson

Name:           python-%{srcname}
Version:        3.0
Release:        1%{?dist}
Summary:        Iterative JSON parser with a standard Python iterator interface

License:        BSD-3-Clause
URL:            https://github.com/ICRAR/ijson
Source0:        https://files.pythonhosted.org/packages/source/i/ijson/ijson-%{version}.tar.gz
# https://github.com/ICRAR/ijson/pull/26
Source1:        https://raw.githubusercontent.com/ICRAR/ijson/3eec07f9eb1fb383c9986904fb23f83786333653/tests_asyncio.py

BuildArch:      noarch

%global _description %{expand:
Iterative JSON parser with a standard Python iterator interface.}

%description %_description

%package -n     python3-%{srcname}
Summary:        %{summary}
# BuildRequires:  yajl
BuildRequires:  pkgconfig(python3)
BuildRequires:  python3dist(setuptools)
# BuildRequires:  python3dist(cffi)
# BuildRequires:  fdupes
# BuildRequires:  python3-asyncio
# BuildRequires:  pkgconfig(yajl)

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}
cp %{SOURCE1} .

%build
%py3_build

%install
%py3_install

%check
%{python3} tests.py

%files -n python3-%{srcname}
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}/

%changelog
* Thu Apr  9 2020 Marketa Calabkova <mcalabkova@suse.com>
- update to 3.0
  * Exposing backend's name under ``<backend>.backend``,
  and default backend's name under ``ijson.backend``.
  * Exposing ``ijson.sendable_list`` to users in case it comes in handy.
  * Improved the protocol for user-facing coroutines,
  where instead of having to send a final, empty bytes string
  to finish the parsing process
  users can simply call ``.close()`` on the coroutine.
  * Including C code in coverage measurements,
  and increased overall code coverage up to 99%%.
  * Full re-design of ijson.
  * Initial support for ``asyncio`` in python 3.5+.
  * Exposure of underlying infrastructure implementing the push model.
  * C extension broken down into separate source files
  for easier understanding and maintenance.
  * Fixed a deprecation warning in the C backend
  present in python 3.8 when parsing Decimal values.
  * New `kvitems` method in all backends.
  Like `items`, it takes a prefix,
  and iterates over the key/value pairs of matching objects
  (instead of iterating over objects themselves, like in `items`).
  * When using python 2, all backends now return
  `map_key` values as `unicode` objects, not `str`.
  * Including more files in source distributions (#14).
  * Adjusting python backend to avoid reading off the input stream
  too eagerly (#15).
* Fri Oct 18 2019 John Vandenberg <jayvdb@gmail.com>
- Use libyajl
- Update URL to new maintainer https://github.com/ICRAR/ijson
- Update to v2.5.1
* Wed Mar 27 2019 John Vandenberg <jayvdb@gmail.com>
- Initial spec for v2.3
