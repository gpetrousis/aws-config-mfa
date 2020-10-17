import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws_mfa_config",
    version="0.0.1",
    author="Georgios Petrousis",
    author_email="gpetrousis@gmail.com",
    description="An aws configure wrapper tha adds support for MFA protected profiles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gpetrousis/aws-config-mfa",
    packages=['aws_mfa_config'],
    license='MIT',
    keywords='aws config mfa session',
    zip_safe=False,
    install_requires=[
        'boto3'
    ],
    classifiers=[
		"Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
		"Intended Audience :: Developers"
    ],
    entry_points={
        'console_scripts': [
            'aws-mfa-config=aws_mfa_config.command_line:main',	
        ],
    },
    python_requires='>=3.6',
)
