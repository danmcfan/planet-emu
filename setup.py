from distutils.core import setup

setup(
    name="planet_emu",
    version="1.0.0",
    description="Planet Emu",
    author="Danny OBrien",
    author_email="danmcfan33@gmail.com",
    packages=["planet_emu"],
    install_requires=[
        "earthengine-api",
        "eeconvert",
        "geopandas",
        "awswrangler",
        "fastapi",
        "mangum",
    ],
)
