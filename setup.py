from setuptools import setup, find_packages


setup(
    name='cli-notify-slack',
    description='Fetches the most recent aws spot prices, plots them, and sends them to you',
    url='https://github.com/EntilZha/cli-notify-slack',
    author='Pedro Rodriguez',
    author_email='ski.rodriguez@gmail.com',
    maintainer='Pedro Rodriguez',
    maintainer_email='ski.rodriguez@gmail.com',
    license='Apache License 2.0',
    keywords='cli notify slack watch',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*', 'test']),
    version='0.0.0',
    install_requires=['click', 'slacker'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={
        'console_scripts': ['notify = slacknotify.cli:cli']
    }
)

