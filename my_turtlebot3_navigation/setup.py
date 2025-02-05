from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'my_turtlebot3_navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='davyjones',
    maintainer_email='davyjones7731@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_turtlebot3_navigation = my_turtlebot3_navigation.my_turtlebot3_navigation:main',
        ],
    },
)
