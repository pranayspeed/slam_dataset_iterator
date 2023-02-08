editable:
	SETUPTOOLS_ENABLE_FEATURES="legacy-editable" pip install --verbose --prefix=$(shell python3 -m site --user-base) --editable .

install:
	@pip install --verbose .

uninstall:
	@pip -v uninstall slam-dataset-sdk

license:
	@addlicense -f LICENSE -v -ignore **/*.yaml -v .
