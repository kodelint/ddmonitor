from setuptools import setup, find_packages

setup(
    name='ddmonitor',
    version='0.2.0',
    packages=find_packages(),
    url='',
    license='MIT',
    author='Satyajit Roy',
    author_email='satyajit@adobe.com',
    description='Handy tool for datadog monitoring',
    install_requires=[
          'datadog','argparse','configparser'
    ],
    entry_points = {
        'console_scripts': ['ddmonitor=ddmonitor:main']
    }
)
