=====
Usage
=====


Generating test files
---------------------

Execute ``pact-testgen`` as follows:

::

    pact-testgen /path/to/pactfile.json /output/dir

The output directory should be in your tests directory, where your
test runner will pick it up.

This will create two files in the output directory:

1. A file named ``provider_states.py``. This will contain empty setup functions for each
   combination of provider states defined in the given pact file.

   Developers must edit this file, filling in the function bodies with whatever code is
   necessary to create the necessary states required by each function.

2. A file named ``test_pact.py``. This file contains unit tests which call out to the functions
   defined in ``provider_states.py`` in their ``setUp`` methods. Each interaction defined in the pact
   file will get a corresponding test method.

   This file is 100% ready to go, and does not need to be edited.


Updating test files
-------------------

Currently, ``pact-testgen`` will not overwrite an existing ``provider_states.py`` file.

To update tests after an update to the pact file which does not
add new provider states, simply re-run ``pact-testgen``.

If provider states have changed, rename your ``provider_states.py`` before running
``pact-testgen``. Copy provider states from the renamed file to the new ``provider_states.py``
file, and fill in any new states as required.

In the future, ``pact-testgen`` will intelligently update the ``provider_states.py`` file,
which should make updates simpler, as well as simplify support for provider code bases
with multiple consumers.


Help
----

::

    usage: pact-testgen [-h] [--base-class BASE_CLASS] [--debug]
                        pact_file output_dir

    positional arguments:
    pact_file             Path to a Pact file.
    output_dir            Output for generated Python files.

    optional arguments:
    -h, --help            show this help message and exit
    --base-class BASE_CLASS
                            Python path to the TestCase which generated test cases
                            will subclass.
    --debug
