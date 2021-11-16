import setuptools

setuptools.setup(
    python_requires='>=3.6',
    name='k2chain',
    version='0.0.1',
    author='Alex Hung',
    author_email='hung_alex@icloud.com',
    keywords='chain-model',
    description="Chain-model",
    url='https://github.com/alex-ht/k2chain',
    package_dir={
        'k2chain': 'k2chain',
    },
    packages=['k2chain'],
    install_requires='k2',
    data_files=[('', ['LICENSE'])],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
