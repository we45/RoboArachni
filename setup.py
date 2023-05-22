from setuptools import setup

install_dependencies = (
    'requests==2.31.0',
    'robotframework==3.1.2',
    'docker==4.1.0',
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
    'requests==2.31.0', 'robotframework==3.1.2', 'docker==4.1.0',
    ],
    description='Robot Framework Library for Arachni Scanner'
)