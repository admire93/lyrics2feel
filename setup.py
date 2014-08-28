#! -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(name='lyrics2feel',
      version='0.0.1',
      author='Kang Hyojun',
      author_email='admire9@gmail.com',
      packages=find_packages(),
      install_requires=[
          'flask==0.10.1', 'flask-script==2.0.5', 'sqlalchemy==0.9.7',
          'pytest==2.6.0', 'alembic', 'sphinx'
      ],
      entry_points={
          'console_scripts': 'lyrics = lyrics2feel.script:main'
      })
