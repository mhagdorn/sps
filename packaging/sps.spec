%global cuda_version 12-2

%bcond_with nvml
%bcond_with rsmi

%global pkgname sps
%global extra_name %{nil}
%if %{with nvml}
%global extra_name _cuda
%endif
%if %{with rsmi}
%global extra_name _rocm
%endif

Name: %{pkgname}%{extra_name}
Version: 4.1
Release: 1%{?dist}
Summary: The Slurm Profiling Service

License: Copyright University of Oxford
Source0: %{pkgname}_%{version}.tar.gz

# build options		.rpmmacros options	change to default action
# ====================  ====================	========================
# --with nvml		%_with_nvml path	require nvml support
# --with rsmi           %_with_rsmi path        require rsmi support
#

Provides: %{pkgname} = %{version}-%{release}

BuildRequires: make
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: slurm-devel
BuildRequires: boost-devel
Requires: python3-pandas

%if %{with nvml}
BuildRequires: cuda-nvml-devel-%{cuda_version}
BuildRequires: cuda-nvcc-%{cuda_version}
BuildRequires: cuda-cudart-devel-%{cuda_version}
%undefine _hardened_build
%endif

%if %{with rsmi}
BuildRequires: rocm-smi-lib
%endif

%description
The Slurm (or Simple) Profiling Service sps is a lightweight job profiler which bridges the gap between numerical job stats and full-blown application profiling.

%prep
%setup -q -n %{pkgname}_%{version}

%build
%cmake \
    %{?_with_nvml:-DCMAKE_CUDA_COMPILER=/usr/local/cuda-$(echo %{cuda_version} | tr - .)/bin/nvcc} \
    %{?_with_rsmi:-DCMAKE_PREFIX_PATH=/opt/rocm}
%cmake_build

%install
%cmake_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README.md
%license LICENSE
%{_bindir}/ckill
%{_bindir}/sps
%{_bindir}/sps-pyplot
%{_bindir}/sps-stop
%{_libdir}/slurm/launch_sps.so

%changelog
