
%global library ironic-prometheus-exporter
%global module ironic_prometheus_exporter

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}


Name:       python-%{library}
Version:    2.1.1
Release:    1%{?dist}
Summary:    ironic-prometheus-exporter provides a way to export hardware sensor data from ironic project in OpenStack to Prometheus
License:    ASL 2.0
URL:        https://opendev.org/openstack/ironic-prometheus-exporter

Source0:    https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# test dependencies
BuildRequires: python3-pbr
BuildRequires: python3-oslotest
BuildRequires: python3-stestr
BuildRequires: python3-oslo-config
BuildRequires: python3-prometheus_client >= 0.6.0
BuildRequires: python3-oslo-messaging >= 9.4.0
BuildRequires: python3-oslo-messaging-tests

%description
ironic-prometheus-exporter provides a way to export hardware sensor data from
ironic project in OpenStack to Prometheus. It's implemented as an
oslo-messaging notification driver to get the sensor data and a Flask
Application to export the metrics to Prometheus. It can be used not only in
metal3 but in any OpenStack deployment which includes Ironic service.

%package -n  python3-%{library}
Summary:    ironic-prometheus-exporter provides a way to export hardware sensor data from ironic project in openstack to Prometheus
%{?python_provide:%python_provide python3-%{library}}

Requires: python3-flask >= 1.0.0
Requires: python3-oslo-messaging >= 9.4.0
Requires: python3-pbr >= 3.1.1
Requires: python3-prometheus_client >= 0.6.0
Requires: python3-stevedore >= 1.20.0

%description -n python3-%{library}
ironic-prometheus-exporter provides a way to export hardware sensor data from
ironic project in OpenStack to Prometheus. It's implemented as an
oslo-messaging notification driver to get the sensor data and a Flask
Application to export the metrics to Prometheus. It can be used not only in
metal3 but in any OpenStack deployment which includes Ironic service.

%prep
%autosetup -n %{library}-%{upstream_version} -S git

%build
%{py3_build}

%install
%{py3_install}

%check
export OS_TEST_PATH='./ironic_prometheus_exporter/tests'
%if 0%{?rhel} >= 7
PYTHON=%{__python3} stestr-3 --test-path $OS_TEST_PATH run
%endif

%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%changelog
* Thu Oct 01 2020 RDO <dev@lists.rdoproject.org> 2.1.1-1
- Update to 2.1.1

* Mon Sep 21 2020 RDO <dev@lists.rdoproject.org> 2.1.0-1
- Update to 2.1.0

