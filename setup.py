from setuptools import setup, find_packages

setup(
    name='eventscraper_bot',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = secondscrapy.settings']}, install_requires=['simplejson', 'stem', 'scrapy']
)
