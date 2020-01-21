%global srcname Mopidy-MPD

Name:           mopidy-mpd
Version:        3.0.0
Release:        1%{?dist}
Summary:        Mopidy extension for controlling Mopidy from MPD clients

License:        ASL 2.0
URL:            https://mopidy.com/ext/mpd/
Source0:        %{pypi_source}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  mopidy
Requires:       mopidy

%description
Frontend that provides a full MPD server implementation to make Mopidy
available from MPD clients.


%prep
%autosetup -n %{srcname}-%{version}
rm MANIFEST.in

%build
%py3_build

%install
%py3_install

%check
%{__python3} setup.py test
 
%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/Mopidy_MPD-*.egg-info/
%{python3_sitelib}/mopidy_mpd/


%changelog
* Mon Dec 23 2019 Tobias Girstmair <t-rpmfusion@girst.at> - 3.0.0-1
- Initial RPM Release

