from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in rest_webform/__init__.py
from rest_webform import __version__ as version

setup(
	name="rest_webform",
	version=version,
	description="Webform ",
	author="Alimerdan Rahimov",
	author_email="alimerdanrahimov@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
