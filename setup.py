from setuptools import (
    setup,
    find_packages,
)

setup(
    name='pre_commit_dummy_package',
    version='0.0.0',
    install_requires=['pdm', 'semantic-version==2.10.0'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": "change_version=change_version.change_version:main",
    },
)
