srpm:
	dnf install -y python2
	sed "s/name='requests-gssapi'/name='python-requests-gssapi'/" setup.py > .copr/setup.py
	python .copr/setup.py bdist_rpm --source-only --dist-dir "$(outdir)" --build-requires=python-setuptools
