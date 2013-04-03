from setuptools import find_packages
from distutils.core import setup
from distutils.extension import Extension
import os

version = '0.5.6'

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

cmdclass = {}
ext_modules = [ ]
pyjsbsim_srcs = []

if use_cython:
    pyjsbsim_srcs.append("cython/fgfdmexec.pyx")
    cmdclass.update({'build_ext':build_ext})
else:
    pyjsbsim_srcs.append("cython/fgfdmexec.cpp")
    for src in pyjsbsim_srcs:
        if not os.path.isfile(src):
            raise IOError("Must install Cython >= 0.18 to build from git")

ext_modules += [ Extension('pyjsbsim.jsbsim_cython',
    sources= pyjsbsim_srcs,
    libraries=['JSBSim'],
    include_dirs=[
        '/usr/local/include/JSBSim'
    ],
    language='c++'),
]

setup(name='PyJSBSim',
      version=version,
      description='A python interface for JSBSim using Cython.',
      long_description='''\
      Interfaces to JSBSim using Cython.
      ''',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Topic :: Scientific/Engineering',
          'Topic :: Text Processing :: General',
      ],
      # Get strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='James Goppert',
      author_email='james.goppert@gmail.com',
      url='https://github.com/arktools/pyjsbsim',
      license='GPLv3',
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True,
      install_requires=['numpy'],
      ext_modules= ext_modules,
      cmdclass = cmdclass,
      test_suite='test',
      #package_data={'pyjsbsim': ['templates/*']},
      #entry_points={
      #  'console_scripts': [
      #      'pydatcom-export = pydatcom:DatcomExporter.command_line',
      #      'pydatcom-plot = pydatcom:DatcomPlotter.command_line'
      #  ]},
      )
