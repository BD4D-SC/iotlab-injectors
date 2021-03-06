from setuptools import setup, find_packages

PACKAGE = "embers.injectors"
VERSION = "0.1"


setup(
    name           = PACKAGE,
    version        = VERSION,
    author         = "The EMBERS consortium",
    author_email   = "dev@embers.city",
    description    = "Injectors for EMBERS",
    url            = "http://www.embers.city/",
    keywords       = ["Open Data", "Smart City"],
    license        = "=== TBD ===",
    packages       = find_packages("src"),
    package_dir    = {"": "src"},
    entry_points   = {
        "console_scripts": [
            "injectors = "+PACKAGE+".injectors_cli:main",
            "registry = "+PACKAGE+".registry_cli:main",
            "subscriber = "+PACKAGE+".subscriber:main",
            "datasets = "+PACKAGE+".datasets_cli:main",
        ],
    },
    namespace_packages = ["embers", PACKAGE],

    install_requires = [
        "embers.meshblu",
        "embers.datasets",
    ],
)
