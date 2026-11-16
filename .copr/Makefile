# COPR "make_srpm" entry point. COPR runs:
#   make -f .copr/Makefile srpm outdir=<dir> spec=<path>
spec ?= t3code-nightly.spec

srpm:
	dnf -y install rpmdevtools rpm-build
	spectool -g -C $(outdir) $(spec)
	rpmbuild -bs \
		--define "_sourcedir $(outdir)" \
		--define "_srcrpmdir $(outdir)" \
		$(spec)

.PHONY: srpm
