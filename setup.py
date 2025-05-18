from setuptools import setup, find_packages

setup(
    name="car_sales_dashboard",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "reflex",
        "pandas",
        "numpy",
        "scikit-learn",
        "plotly",
    ],
)