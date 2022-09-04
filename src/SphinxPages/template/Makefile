# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
HTTPPORT      = 8080
SERVERSTATUS  = $(strip $(shell ps x | grep http.server | grep -v grep | wc -l))
SERVERPID     = $(strip $(shell ps x | grep http.server | grep -v grep | cut -d " " -f 1))

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

server:
ifeq ($(SERVERSTATUS),1)
	@echo server started, pid: $(SERVERPID)
	kill -9 $(SERVERPID)
	@echo server restarting
endif
	python3 -m http.server -d `pwd`/$(BUILDDIR)/html $(HTTPPORT) &
	@sleep 1
	@echo server started

docs:
	rm -rf docs
	cp -rf _build/html/ docs
	touch docs/.nojekyll
	cp -rf CNAME docs/

.PHONY: help Makefile docs

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	cp README.md index.md
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	rm index.md

