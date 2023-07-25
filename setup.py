from setuptools import setup


if __name__ == "__main__":
    setup(
        install_requires=[
            'Click',
        ],
        entry_points={
            'console_scripts': [
                'scanproject = scanproject:main'
            ],
        },
    )
