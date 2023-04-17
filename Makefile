generate:
	@echo "Generating requirements.txt"
	@poetry export -f requirements.txt --without-hashes -o requirements.txt
	@echo "Generating requirements-test.txt"
	@poetry export -f requirements.txt --with test --without-hashes -o requirements-test.txt