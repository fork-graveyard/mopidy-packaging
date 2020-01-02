%global srcname Mopidy
%global homedir %{_sharedstatedir}/%{name}

Name:           mopidy
Version:        3.0.1
Release:        1%{?dist}
Summary:        An extensible music server written in Python

License:        ASL 2.0
URL:            https://mopidy.com/
Source0:        %{pypi_source}
Source1:        mopidy.conf

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
BuildRequires:  python3-graphviz
BuildRequires:  python3-tornado
BuildRequires:  python3-Pykka >= 2.0.1
BuildRequires:  python3-requests
BuildRequires:  python3-pytest
BuildRequires:  python3-responses
BuildRequires:  python3-gstreamer1
BuildRequires:  gstreamer1-plugins-good
BuildRequires:  systemd-rpm-macros
Requires:       python3-gstreamer1
Requires:       gstreamer1-plugins-good
Requires:       python3-tornado
Requires:       python3-Pykka >= 2.0.1
Requires:       python3-requests
Requires(pre):  shadow-utils
Suggests:       mopidy-mpd

%description
Mopidy plays music from local disk, and a plethora of streaming services and
sources. You edit the playlist from any phone, tablet, or computer using a
variety of MPD and web clients.


%prep
%autosetup -n %{srcname}-%{version}
rm MANIFEST.in
# without this, mopidy must be installed for docs to be able to be built.
# Note: jodal promised to remove the necessity for this hack in a future version
sed -i 's/^__version__ = .*$/__version__ = "%{version}"/' mopidy/__init__.py

%build
%py3_build

cd docs
make SPHINXBUILD=sphinx-build-3 html man
rm _build/html/.buildinfo

%install
%py3_install

install -d -m 0755 %{buildroot}%{homedir}
install -d -m 0755 %{buildroot}%{_var}/cache/%{name}
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
touch %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -p -D extra/mopidyctl/mopidyctl %{buildroot}%{_sbindir}/mopidyctl
install -p -D -m 0644 docs/_build/man/mopidy.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -p -D -m 0644 extra/mopidyctl/mopidyctl.8 %{buildroot}%{_mandir}/man8/mopidyctl.8
install -p -D -m 0644 extra/systemd/mopidy.service %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/%{name}/conf.d/mopidy.conf

%check
%{__python3} setup.py test
 
%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{homedir} -s /sbin/nologin \
    -c "%{summary}" %{name}
exit 0

%post
%systemd_post %{name}.service
 
%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%license LICENSE
%doc README.rst docs/_build/html
# Note: this directory needs to be writable by the mopidy service
%attr(-,%name,%name) %dir %{_var}/cache/%{name}
%ghost               %dir %{homedir}
                     %dir %{_sysconfdir}/%{name}
                     %dir %{_datadir}/%{name}
                     %dir %{_datadir}/%{name}/conf.d
# Note: users are expected to put streaming service credentials here
%attr(0640,%name,%name) %ghost %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{name}/
%{_bindir}/%{name}
%{_sbindir}/mopidyctl
%{_unitdir}/%{name}.service
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man8/mopidyctl.8.gz
%{_datadir}/%{name}/conf.d/fedora.conf


%changelog
* Fri Dec 27 2019 Tobias Girstmair <t-rpmfusion@girst.at> - 3.0.1-1
- Initial RPM Release

