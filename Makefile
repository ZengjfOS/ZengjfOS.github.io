all:
	pip3 uninstall -y SphinxPages
	python3 setup.py sdist bdist_wheel
	pip3 install dist/SphinxPages-*-py3-none-any.whl

clean:
	pip3 uninstall -y SphinxPages
