# Generic GNU Makefile for python projects
# Tom Söderlund <tom.soderlund@iki.fi> 2021-04-10
#
# - make lint to generate lint reports (default)
# - make clean to remove generated files
# - make test to run tests
# - make run to run

.PHONY: lint
lint: $(patsubst %.py,%.pylint,$(wildcard *.py))

%.pylint: %.py
	pylint $^
	touch $@

.PHONY: test
test: test.py
	python3 $^

.PHONY: run
run: main.py
	python3 $^

.PHONY: clean
clean:
	-rm -fr __pycache__ *.pylint *~
