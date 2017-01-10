.PHONY: default
default: dist

.PHONY: test
test: $(wildcard **/*.py)
	find jiraexport -name '*.py' -exec python -m py_compile {} \;

dist: $(wildcard **/*.py) setup.py | test
	rm -rf dist
	# sdist means "source distribution"
	python setup.py sdist
	rm -r jiraexport.egg-info

clean:
	rm -rf build dist jiraexport.egg-info devenv

install: dist
	# python2 setup.py install # setuptools bad. no way to uninstall
	# could also do `pip install .` but using the egg seems more fancy
	pip install dist/jiraexport-$(shell cat jiraexport/VERSION).tar.gz

uninstall:
	pip uninstall -y jiraexport

devenv: setup.py requirements.txt
	virtualenv -p python2.7 devenv
	devenv/bin/pip install . # production deps
	devenv/bin/pip install -r requirements.txt # developer deps

upload: devenv dist
	# Make sure there are no uncommitted changes
	git diff-index --quiet HEAD --
	git tag "v$(shell cat jiraexport/VERSION)"
	git push origin "v$(shell cat jiraexport/VERSION)"
	devenv/bin/twine upload dist/jiraexport-$(shell cat jiraexport/VERSION).tar.gz
