README.txt: README.md
	pandoc --from=markdown --to=rst --output=README.txt README.md

install:
	sudo python setup.py install

.PHONY: install
