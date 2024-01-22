%global cuda_version 12-2

# build options		.rpmmacros options	change to default action
# ====================  ====================	========================
# --with nvml		%_with_nvml path	require nvml support

%bcond_with nvml

Name: sps
Version: 4.0
Release: 1%{?dist}
Summary: The Slurm Profiling Service

License: Copyright University of Oxford
Source0: %{name}_%{version}.tar.gz

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
%setup -q

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
