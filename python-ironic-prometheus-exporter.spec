%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2ef3fe0ec2b075ab7458b5f8b702b20b13df2318

%global library ironic-prometheus-exporter
%global module ironic_prometheus_exporter

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order


Name:       python-%{library}
Version:    4.3.0
Release:    1%{?dist}
Summary:    ironic-prometheus-exporter provides a way to export hardware sensor data from ironic project in OpenStack to Prometheus
License:    Apache-2.0
URL:        https://opendev.org/openstack/ironic-prometheus-exporter

Source0:    https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-oslo-messaging-tests

%description
ironic-prometheus-exporter provides a way to export hardware sensor data from
ironic project in OpenStack to Prometheus. It's implemented as an
oslo-messaging notification driver to get the sensor data and a Flask
Application to export the metrics to Prometheus. It can be used not only in
metal3 but in any OpenStack deployment which includes Ironic service.

%package -n  python3-%{library}
Summary:    ironic-prometheus-exporter provides a way to export hardware sensor data from ironic project in openstack to Prometheus

%description -n python3-%{library}
ironic-prometheus-exporter provides a way to export hardware sensor data from
ironic project in OpenStack to Prometheus. It's implemented as an
oslo-messaging notification driver to get the sensor data and a Flask
Application to export the metrics to Prometheus. It can be used not only in
metal3 but in any OpenStack deployment which includes Ironic service.

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{library}-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv}

%build
%pyproject_wheel

%install
%pyproject_install

%check
export OS_TEST_PATH='./ironic_prometheus_exporter/tests'
%if 0%{?rhel} >= 7
%tox -e %{default_toxenv}
%endif

%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.dist-info
%exclude %{python3_sitelib}/%{module}/tests

%changelog
* Thu Mar 14 2024 RDO <dev@lists.rdoproject.org> 4.3.0-1
- Update to 4.3.0

