# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global library ironic-prometheus-exporter
%global module ironic_prometheus_exporter

%global common_desc ironic-prometheus-exporter provides a way to export hardware sensor data from ironic project in openstack to Prometheus. It's implemented as an oslo-messaging notification driver to get the sensor data and a Flask Application to export the metrics to Prometheus. It can be used not only in metal3 but in any OpenStack deployment which includes Ironic service.


Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    ironic-prometheus-exporter provides a way to export hardware sensor data from ironic project in openstack to Prometheus.
License:    ASL 2.0
URL:        https://github.com/metal3-io/ironic-prometheus-exporter

Source0:    https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n  python%{pyver}-%{library}
Summary:    ironic-prometheus-exporter provides a way to export hardware sensor data from ironic project in openstack to Prometheus.
%{?python_provide:%python_provide python%{pyver}-%{library}}
# Required for tests
BuildRequires: python%{pyver}-oslotest
BuildRequires: python%{pyver}-stestr

Requires: python%{pyver}-pbr
Requires: python-stevedore >=1.20.0
Requires: python-oslo-messaging >=9.4.0
Requires: uwsgi
Requires: python-flask >= 0.12.3
Requires: python-prometheus_client >= 0.6.0


%description -n python%{pyver}-%{library}
%{common_desc}


%package -n python%{pyver}-%{library}-tests
Summary:    ironic-prometheus-exporter tests
%{?python_provide:%python_provide python%{pyver}-%{library}-tests}
Requires:   python%{pyver}-%{library} = %{version}-%{release}

%description -n python%{pyver}-%{library}-tests
%{common_desc}

This package contains the ironic-prometheus-exporter test files.

%if 0%{?with_doc}
%package doc
Summary:    ironic-prometheus-exporter documentation

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme

%description doc
%{common_desc}

This package contains the documentation.
%endif

%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

# Remove setuptools installed data_files
rm -rf %{buildroot}%{_datadir}/%{library}/LICENSE
rm -rf %{buildroot}%{_datadir}/%{library}/README.rst

%check
export OS_TEST_PATH='./ironic_prometheus_exporter/tests'
export PATH=$PATH:%{buildroot}/usr/bin
export PYTHONPATH=$PWD
stestr-%{pyver} --test-path $OS_TEST_PATH run

%files -n python%{pyver}-%{library}
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/%{module}-*.egg-info
%exclude %{pyver_sitelib}/%{module}/tests

%files -n python%{pyver}-%{library}-tests
%license LICENSE
%{pyver_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
