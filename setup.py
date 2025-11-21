from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sspm-engine",
    version="1.0.0",
    description="SaaS Security Posture Management Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="SSPM Builder",
    author_email="builder@example.com",
    url="https://github.com/Raoof128/SSPME",
    packages=find_packages(exclude=["tests*", "docs*"]),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "typer>=0.4.0",
        "pyyaml>=6.0",
        "jinja2>=3.0.0",
        "requests>=2.26.0",
        "pydantic>=1.8.2",
        "slack-sdk>=3.11.0",
        "PyGithub>=1.55",
        "google-api-python-client>=2.0.0",
        "google-auth-httplib2>=0.1.0",
        "google-auth-oauthlib>=0.4.0",
        "python-dotenv>=0.19.0",
        "rich>=10.0.0",
        "pandas>=1.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2",
            "black>=22.0",
            "isort>=5.0",
            "mypy>=0.910",
            "flake8>=3.9",
            "pre-commit>=2.17.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sspmctl=sspm_engine.cli.sspmctl:app",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="security sspm saas posture-management compliance",
)
