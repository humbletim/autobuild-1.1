#!/usr/bin/make -f

all: deb

listpackages:
	@echo python-autobuild

build:
	cd ../../; python setup.py --command-packages=stdeb.command bdist_deb

deb: build
	mv ../../deb_dist/*.deb ..

clean:
	rm -rf ../../deb_dist
	rm -rf ../../autobuild.egg-info
	rm -f ../*.deb

