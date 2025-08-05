from setuptools import setup, find_packages

setup(
    name="ai-code-agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask>=2.0.1',
        'streamlit>=1.10.0',
        'torch>=2.0.0',
        'transformers>=4.40.0',
        'pyyaml>=6.0',
    ],
    python_requires='>=3.8',
)
