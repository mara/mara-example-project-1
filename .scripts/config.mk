# Ensure that databases and app/local_setup.py exist


ensure-config: app/local_setup.py

app/local_setup.py:
	cp -v app/local_setup.py.example app/local_setup.py
	@ >&2 echo '!!! copied app/local_setup.py.example to app/local_setup.py. Please check'

.cleanup-config:
	rm -f app/local_setup.py