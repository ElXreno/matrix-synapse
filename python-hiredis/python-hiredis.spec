# Created by pyp2rpm-3.3.4
%global pypi_name hiredis

Name:           python-%{pypi_name}
Version:        1.1.0
Release:        1%{?dist}
Summary:        Python wrapper for hiredis

License:        BSD
URL:            https://github.com/redis/hiredis-py
Source0:        %{pypi_source}

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  gcc

%global _description \
Python extension that wraps protocol parsing code in hiredis.\
It primarily speeds up parsing of multi bulk replies.

%description
%{_description}

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
%{_description}


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%doc README.md
%{python3_sitearch}/%{pypi_name}
%{python3_sitearch}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
* Sat Oct 31 2020 ElXreno <elxreno@gmail.com> - 1.1.0-1
- Initial package.
