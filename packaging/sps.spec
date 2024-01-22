%global cuda_version 12-2

# build options		.rpmmacros options	change to default action
# ====================  ====================	========================
# --with nvml		%_with_nvml path	require nvml support

%bcond_with nvml

%global pkgname sps
%if %{with nvml}
%global extra_name _cuda
%else
%global extra_name %{nil}
%endif

Name: %{pkgname}%{extra_name}
Version: 4.0
Release: 1%{?dist}
Summary: The Slurm Profiling Service

License: Copyright University of Oxford
Source0: %{pkgname}_%{version}.tar.gz

Provides: %{pkgname} = %{version}-%{release}

BuildRequires: make
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: slurm-devel
Requires: python3-pandas

%if %{with nvml}
BuildRequires: cuda-nvml-devel-%{cuda_version}
BuildRequires: cuda-nvcc-%{cuda_version}
BuildRequires: cuda-cudart-devel-%{cuda_version}
%undefine _hardened_build
%endif

%description
The Slurm (or Simple) Profiling Service sps is a lightweight job profiler which bridges the gap between numerical job stats and full-blown application profiling.

%prep
%setup -q -n %{pkgname}-%{version}

%build
%cmake \
    %{?_with_nvml:-DCMAKE_CUDA_COMPILER=/usr/local/cuda-$(echo %{cuda_version} | tr - .)/bin/nvcc}
%cmake_build

%install
%cmake_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/ckill
%{_bindir}/sps
%{_bindir}/sps-pyplot
%{_bindir}/sps-stop
%{_libdir}/slurm/launch_sps.so

%changelog
