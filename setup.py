# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='NetworkTraceScripts',
    version='0.1.5',
    description='Network Trace Scripts from reactive-firewall',
    long_description=readme,
    author='reactive-firewall',
    author_email='reactive-firewall@users.noreply.github.com',
    url='https://github.com/reactive-firewall/NetworkTrace.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

