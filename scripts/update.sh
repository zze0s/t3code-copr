#!/usr/bin/env bash
# Point t3code-nightly.spec at the newest upstream nightly (or the tag given as $1).
# Prints the new version and writes changed=true|false to $GITHUB_OUTPUT when set.
set -euo pipefail

upstream=pingdotgg/t3code
spec="$(dirname "$0")/../t3code-nightly.spec"
nightly_re='^v([0-9]+\.[0-9]+\.[0-9]+)-nightly\.([0-9]{8}\.[0-9]+)$'

output() {
	if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
		echo "$1" >>"$GITHUB_OUTPUT"
	fi
}

tag="${1:-}"
if [[ -z "$tag" ]]; then
	tag=$(gh release list -R "$upstream" --limit 30 --json tagName \
		--jq '[.[].tagName | select(test("^v[0-9]+\\.[0-9]+\\.[0-9]+-nightly\\.[0-9]{8}\\.[0-9]+$"))][0] // ""')
fi
if [[ ! "$tag" =~ $nightly_re ]]; then
	echo "no nightly tag found (got '$tag')" >&2
	exit 1
fi
base_version="${BASH_REMATCH[1]}"
nightly_tag="${BASH_REMATCH[2]}"
deb="T3-Code-${base_version}-nightly.${nightly_tag}-amd64.deb"

# Upstream publishes the release before every asset finishes uploading.
digest=$(gh release view "$tag" -R "$upstream" --json assets \
	--jq ".assets[] | select(.name == \"$deb\" and .state == \"uploaded\") | .digest")
if [[ ! "$digest" =~ ^sha256:([0-9a-f]{64})$ ]]; then
	echo "$tag: $deb not uploaded yet, try again later"
	output changed=false
	exit 0
fi
sha256="${BASH_REMATCH[1]}"

current_tag=$(sed -n 's/^%global nightly_tag //p' "$spec")
current_base=$(sed -n 's/^%global base_version //p' "$spec")
if [[ "$current_base" == "$base_version" && "$current_tag" == "$nightly_tag" ]]; then
	echo "already at $tag"
	output changed=false
	exit 0
fi

sed -i \
	-e "s/^%global base_version .*/%global base_version ${base_version}/" \
	-e "s/^%global nightly_tag .*/%global nightly_tag ${nightly_tag}/" \
	-e "s/^%global deb_sha256 .*/%global deb_sha256 ${sha256}/" \
	-e "s/^%global pkg_rel .*/%global pkg_rel 1/" \
	"$spec"

echo "updated to $tag"
output changed=true
output version="${base_version}-nightly.${nightly_tag}"
