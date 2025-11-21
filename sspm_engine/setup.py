from setuptools import find_packages, setup

setup(
    name="sspm-engine",
    version="1.0.0",
    description="SaaS Security Posture Management Engine",
    author="SSPM Builder",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "typer>=0.4.0",
        "pyyaml>=5.4.1",
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
    entry_points={
        "console_scripts": [
            "sspmctl=sspm_engine.cli.sspmctl:app",
        ],
    },
    python_requires=">=3.8",
)
