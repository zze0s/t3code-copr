# Managed by scripts/update.sh. Do not edit these four lines by hand.
%global base_version 0.1.14
%global nightly_tag 20261128.5372
%global deb_sha256 ada83b8c7991fe04889fd163b70c33b11098856e1ffae1dd72b9f2e03fdc1bab
%global pkg_rel 1

%global upstream_version %{base_version}-nightly.%{nightly_tag}
%global upstream_dir T3 Code (Nightly)
%global install_dir /opt/%{name}

# Prebuilt Electron app: no debuginfo, no stripping, no brp rewrites.
%global debug_package %{nil}
%global __os_install_post %{nil}
%define _build_id_links none

Name:           t3code-nightly
Version:        %{base_version}
Release:        0.nightly.%{nightly_tag}.%{pkg_rel}%{?dist}
Summary:        Minimal GUI for coding agents (nightly build)
License:        MIT
URL:            https://github.com/pingdotgg/t3code
Source0:        %{url}/releases/download/v%{upstream_version}/T3-Code-%{upstream_version}-amd64.deb

ExclusiveArch:  x86_64

BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  desktop-file-utils
BuildRequires:  tar
BuildRequires:  xz

# The bundle ships its own Chromium, Node and native modules. Skip automatic
# dependency scanning and list the system libraries the upstream .deb depends on.
AutoReqProv:    no
Requires:       alsa-lib
Requires:       at-spi2-core
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libnotify
Requires:       libsecret
Requires:       libuuid
Requires:       libXScrnSaver
Requires:       libXtst
Requires:       mesa-libgbm
Requires:       nss
Requires:       xdg-utils
Recommends:     libappindicator-gtk3

%description
T3 Code is a minimal GUI for coding agents. This unofficial package
repackages the upstream x86_64 nightly .deb (%{upstream_version}).

%prep
echo "%{deb_sha256}  %{SOURCE0}" | sha256sum -c -
%setup -q -c -T
ar x %{SOURCE0}
tar -xf data.tar.*

%build
# Nothing to build.

%install
install -d %{buildroot}%{install_dir}
cp -a "opt/%{upstream_dir}/." %{buildroot}%{install_dir}/

# electron-updater reads this marker. Anything other than "deb" (with no
# APPIMAGE env) makes T3 Code disable in-app updates; dnf handles them instead.
echo rpm > %{buildroot}%{install_dir}/resources/package-type

# Fedora has unprivileged user namespaces, so the SUID sandbox helper is not needed.
chmod 0755 %{buildroot}%{install_dir}/chrome-sandbox

install -d %{buildroot}%{_bindir}
ln -s %{install_dir}/t3code %{buildroot}%{_bindir}/t3code

install -d %{buildroot}%{_datadir}/icons
cp -a usr/share/icons/hicolor %{buildroot}%{_datadir}/icons/
install -Dpm 0644 usr/share/metainfo/com.t3tools.t3code.metainfo.xml \
    %{buildroot}%{_metainfodir}/com.t3tools.t3code.metainfo.xml
install -Dpm 0644 usr/share/applications/t3code.desktop \
    %{buildroot}%{_datadir}/applications/t3code.desktop
sed -i 's|^Exec=.*|Exec=%{install_dir}/t3code %U|' \
    %{buildroot}%{_datadir}/applications/t3code.desktop

install -d %{buildroot}%{_licensedir}/%{name}
cp -p usr/share/doc/t3code/copyright %{buildroot}%{_licensedir}/%{name}/LICENSE

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/t3code.desktop

%files
%license %{_licensedir}/%{name}/LICENSE
%{install_dir}
%{_bindir}/t3code
%{_datadir}/applications/t3code.desktop
%{_datadir}/icons/hicolor/*/apps/t3code.png
%{_metainfodir}/com.t3tools.t3code.metainfo.xml

%changelog
* Mon Nov 16 2026 ze0s - 0.1.10-0.nightly.20261116.4774.1
- Repackage upstream nightly .deb; changelog tracks the spec, not upstream
