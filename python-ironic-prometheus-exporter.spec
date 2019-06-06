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

%global library ironic-prometheus-exporter
%global module ironic_prometheus_exporter

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}


Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    ironic-prometheus-exporter provides a way to export hardware sensor data from ironic project in OpenStack to Prometheus
License:    ASL 2.0
URL:        https://github.com/metal3-io/ironic-prometheus-exporter

Source0:    https://github.com/metal3-io/ironic-prometheus-exporter/archive/%{commit}/%{library}-%{shortcommit}.tar.gz

BuildArch:  noarch

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
# test dependencies
BuildRequires: python%{pyver}-pbr
BuildRequires: python%{pyver}-oslotest
BuildRequires: python%{pyver}-stestr
BuildRequires: python%{pyver}-oslo-config
BuildRequires: python%{pyver}-prometheus_client >= 0.6.0
BuildRequires: python%{pyver}-oslo-messaging >= 9.4.0
BuildRequires: python%{pyver}-oslo-messaging-tests

%description
ironic-prometheus-exporter provides a way to export hardware sensor data from
ironic project in OpenStack to Prometheus. It's implemented as an
oslo-messaging notification driver to get the sensor data and a Flask
Application to export the metrics to Prometheus. It can be used not only in
metal3 but in any OpenStack deployment which includes Ironic service.

%package -n  python%{pyver}-%{library}
Summary:    ironic-prometheus-exporter provides a way to export hardware sensor data from ironic project in openstack to Prometheus
%{?python_provide:%python_provide python%{pyver}-%{library}}

Requires: python%{pyver}-pbr
Requires: python%{pyver}-stevedore >= 1.20.0
Requires: python%{pyver}-oslo-messaging >= 9.4.0
Requires: python%{pyver}-flask >= 0.12.3
Requires: python%{pyver}-prometheus_client >= 0.6.0
Requires: python%{pyver}-oslo-config


%description -n python%{pyver}-%{library}
ironic-prometheus-exporter provides a way to export hardware sensor data from
ironic project in OpenStack to Prometheus. It's implemented as an
oslo-messaging notification driver to get the sensor data and a Flask
Application to export the metrics to Prometheus. It can be used not only in
metal3 but in any OpenStack deployment which includes Ironic service.

%prep
%autosetup -n %{module}-%{upstream_version} -S git

%build
%{pyver_build}

%install
%{pyver_install}

# Remove setuptools installed data_files
rm -rf %{buildroot}%{_datadir}/%{library}/LICENSE
rm -rf %{buildroot}%{_datadir}/%{library}/README.rst

%check
export OS_TEST_PATH='./ironic_prometheus_exporter/tests'
%if 0%{?rhel} >= 7
PYTHON=%{pyver_bin} stestr-%{pyver} --test-path $OS_TEST_PATH run
%endif

%files -n python%{pyver}-%{library}
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/%{module}-*.egg-info
%exclude %{pyver_sitelib}/%{module}/tests

%changelog
