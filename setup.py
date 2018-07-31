import os
from setuptools import setup, find_packages


f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
readme = f.read()
f.close()

setup(
    name='django-tracer',
    version="0.9.2",
    description='django-tracer gives you an easy way to generate and use a UUID per request',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Frank Wiles',
    author_email='frank@revsys.com',
    url='https://github.com/revsys/django-tracer/',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    test_suite='runtests.runtests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
)
