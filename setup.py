from setuptools import find_packages, setup

setup(
    name="pmoai",
    version="0.1.0",
    description="Project Management Office AI Agents - A framework for orchestrating PM-focused AI agents",
    author="PMOAI Team",
    author_email="info@pmoai.org",
    url="https://github.com/pmoai/pmoai",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "crewai>=0.119.0",
        "pydantic>=2.4.2",
        "openai>=1.13.3",
        "python-dotenv>=1.0.0",
        "tiktoken>=0.7.0",
        "pyyaml>=6.0",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "pmoai=pmoai.cli:main",
        ],
    },
    package_data={
        "pmoai": ["config/templates/*.yaml"],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
