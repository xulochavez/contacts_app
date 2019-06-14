from setuptools import setup, find_packages

setup(
    name='contacts',
    version='1.0',
    packages=find_packages(),
    scripts=['scripts/init_db.sh', 'scripts/run.sh']
)