README.txt: README.md
	pandoc --from=markdown --to=rst --output=README.txt README.md
