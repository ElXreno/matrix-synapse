%global srcname authlib
%global pypi_name Authlib

Name:           python-%{srcname}
Version:        0.15.2
Release:        1%{?dist}
Summary:        Build OAuth and OpenID Connect servers in Python

License:        BSD
URL:            https://github.com/lepture/authlib
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3dist(setuptools)

%global _description %{expand:
Python library for building OAuth and OpenID Connect servers. JWS, JWK, JWA,
JWT are included.}

%description %_description

%package -n     python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel

# Test dependencies
BuildRequires:  python3dist(coverage)
BuildRequires:  python3dist(mock)
BuildRequires:  python3dist(pytest)

BuildRequires:  python3dist(flask)
BuildRequires:  python3dist(flask-sqlalchemy)

# BuildRequires:  python3dist(httpx)
# BuildRequires:  python3dist(pytest-asyncio)
# BuildRequires:  python3dist(starlette)
# BuildRequires:  python3dist(itsdangerous)

BuildRequires:  python3dist(django)
BuildRequires:  python3dist(pytest-django)

# Runtime dependencies
BuildRequires:  python3dist(cryptography)
BuildRequires:  python3dist(requests)

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
# Do multiple pytest runs as environment gets dirty.
%{python3} -m pytest tests/core
#%{python3} -m pytest tests/starlette
%{python3} -m pytest tests/flask
%{python3} -m pytest tests/django

%files -n python3-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
* Tue Oct 27 14:35:50 +03 2020 ElXreno <elxreno@gmail.com> - 0.15.2-1
- Update to version 0.15.2

* Sun Oct 11 2020 Kai A. Hiller <V02460@gmail.com> - 0.15.0-1
- Update to v1.15.0

* Fri May 29 2020 Kai A. Hiller <V02460@gmail.com> - 0.14.3-1
- Initial package.
