"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='komunitin-lite',
    version='0.0.1',
    description='Basic python GTK3 client for komunitin users',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/XaviP/komunitin-lite-gtk3',
    author='XaviP - Ecoxarxa del Bages',
    author_email='xavip@medusaweb.cat',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business :: Financial :: Accounting',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='komunitin, social currencies, mutual credit',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.7, <4',
    install_requires=['requests'],
    project_urls={
        'Bug Reports': 'https://github.com/XaviP/komunitin-lite-gtk3/issues',
        'Source': 'https://github.com/XaviP/komunitin-lite-gtk3',
    },
)
