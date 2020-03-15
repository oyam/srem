import setuptools


def read_requirements(dev=False):
    reqs = 'requirements-dev.txt' if dev else 'requirements.txt'
    with open(reqs, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements


setuptools.setup(
    name="srem",
    version="0.1.1",
    description="A Simplified and Robust Surface Reflectance Estimation Method",
    packages=setuptools.find_packages(),
    install_requires=read_requirements(),
    extras_require={
        'test': read_requirements(dev=True)
    }
)
