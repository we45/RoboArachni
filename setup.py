from setuptools import setup

install_dependencies = (
    'requests==2.18.4',
    'robotframework==3.0.4',
    'docker',
)

setup(
    name='RoboArachni',
    version='0.9',
    packages=[''],
    package_dir={'': 'roboarachni'},
    url='www.we45.com',
    license='MIT License',
    author='Abhay Bhargav',
    author_email='Twitter: @abhaybhargav',
    install_requires = [
    'requests==2.18.4', 'robotframework==3.0.4', 'docker',
    ],
    description='Robot Framework Library for Arachni Scanner'
)