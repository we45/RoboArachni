from setuptools import setup

install_dependencies = (
    'certifi==2018.1.18',
    'chardet==3.0.4',
    'decorator==4.2.1',
    'idna==2.6',
    'pkg-resources==0.0.0',
    'psutil==5.4.3',
    'requests==2.18.4',
    'robotframework==3.0.2',
    'robotframework-selenium2library==1.8.0',
    'selenium==3.9.0',
    'urllib3==1.22'
)

setup(
    name='RoboArachni',
    version='0.1',
    packages=[''],
    package_dir={'': 'roboarachni'},
    url='www.we45.com',
    license='MIT License',
    author='Abhay Bhargav',
    author_email='Twitter: @abhaybhargav',
    install_requires = [
    'certifi==2018.1.18', 'chardet==3.0.4', 'decorator==4.2.1', 'idna==2.6',
    'pkg-resources==0.0.0', 'psutil==5.4.3', 'requests==2.18.4', 'robotframework==3.0.2',
    'robotframework-selenium2library==1.8.0', 'selenium==3.9.0','urllib3==1.22'
    ],
    description='Robot Framework Library for Arachni Scanner'
)