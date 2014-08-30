from setuptools import setup, find_packages

setup(name="robots-scanner",
      version="0.2.0a",
      description="robots.txt scanner",
      author="Yeuk Hon Wong",
      classifiers=[
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
        'Topic :: Security',
      ],
      author_email="yeukhon@acm.org",
      packages=find_packages(),
      include_package_data=True,
)
