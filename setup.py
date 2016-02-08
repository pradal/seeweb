from setuptools import setup, find_packages

with open('README.rst') as f:
    README = f.read()
with open('CHANGES.rst') as f:
    CHANGES = f.read()


def parse_requirements(fname):
    with open(fname, 'r') as f:
        txt = f.read()

    reqs = []
    for line in txt.splitlines():
        line = line.strip()
        if len(line) > 0 and not line.startswith("#"):
            reqs.append(line)

    return reqs


setup(name='seeweb',
      version='0.8',
      description='SEE website',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='revesansparole',
      author_email='revesansparole@gmail.com',
      url='',
      keywords='web pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='seeweb',
      install_requires=[],  # parse_requirements("requirements.txt"),
      entry_points={
          "paste.app_factory": ["main = seeweb:main"],
          "console_scripts": [
              "initialize_seeweb_db = seeweb.scripts.initializedb:main",
              "clean_seeweb = seeweb.scripts.clean_package_data:main"]
                    },
      )
