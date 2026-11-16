# t3code-copr

Unofficial Fedora RPM of the [T3 Code](https://github.com/pingdotgg/t3code) nightly desktop app, built on [COPR](https://copr.fedorainfracloud.org).

The package repackages the upstream x86_64 nightly `.deb` into `/opt/t3code-nightly`. In-app updates are disabled; dnf handles updates.

## How it stays current

1. `.github/workflows/update.yml` runs every 30 minutes and calls `scripts/update.sh`.
2. The script finds the newest `v*-nightly.*` release upstream. Once the `.deb` has finished uploading, it writes the version and the asset's sha256 into `t3code-nightly.spec`.
3. The workflow commits and pushes the change. The push hits the COPR webhook.
4. COPR clones the repo, runs `.copr/Makefile` to download the `.deb` and build the SRPM, then builds the RPMs.

A new upstream nightly usually reaches the repo within about 45 minutes.

## Install

```sh
sudo dnf copr enable <copr-user>/t3code-nightly
sudo dnf install t3code-nightly
```

## Manual runs

```sh
./scripts/update.sh                                 # newest nightly
./scripts/update.sh v0.1.10-nightly.20261116.4774   # a specific tag
```

To package a specific tag, run the workflow from the Actions tab with the `tag` input.

To change the packaging without a new upstream version, edit the spec and bump `pkg_rel`.

## Local build

```sh
spectool -g -C ~/rpmbuild/SOURCES t3code-nightly.spec
rpmbuild -bb t3code-nightly.spec
```
