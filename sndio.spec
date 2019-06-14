%define		libname %mklibname sndio %{major}
%define		devel	%mklibname sndio -d
%define		major	7.0

Name:		sndio
Version:	1.5.0
Release:	1
Summary:	A sound library
Group:		Sound/Utilities

License:	ISC
URL:		http://www.sndio.org
Source0:	http://www.sndio.org/%{name}-%{version}.tar.gz

BuildRequires:	pkgconfig(alsa)
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires:	%{libname} = %{version}-%{release}

%description
sndio is a sound library

%package -n	%{libname}
Summary:	Libraries for %{name}

%description -n	%{libname}
These are libraries for %{name}

%package -n	%{devel}
Summary:	This includes the development files for %{name}
Provides:	%{name}-devel
Requires:	%{libname}

%description -n	%{devel}
Here are the development files for %{name}

%prep
%autosetup

%build
%setup_compile_flags
./configure \
--prefix=%{_prefix} \
--libdir=%{_libdir} \
--mandir=%{_mandir}

%make_build

%install
%make_install

# Install sndiod systemd service file
%__install -Dm 755 contrib/%{name}d.service %{buildroot}%{_unitdir}/%{name}d.service
%__install -Dm 644 contrib/default.%{name}d %{buildroot}%{_sysconfdir}/default/%{name}d

%pre
%_pre_useradd %{name}d /dev/null /bin/false
/usr/sbin/usermod -a -G audio %{name}d

%post
%_post_service	%{name}d

%preun
%preun_service	%{name}d

%postun
/usr/sbin/usermod -G %{name}d %{name}d
%_postun_userdel %{name}d

%files
%{_bindir}/aucat
%{_bindir}/midicat
%{_bindir}/sndiod
%{_mandir}/man*/*
%{_unitdir}/%{name}d.service
%{_sysconfdir}/default/%{name}d

%files -n	%{libname}
%{_libdir}/libsndio.so.%{major}

%files -n	%{devel}
%{_libdir}/libsndio.so
%{_includedir}/sndio.h

