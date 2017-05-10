.. image:: https://img.shields.io/badge/stdlib--only-yes-green.svg
    :target: https://img.shields.io/badge/stdlib--only-yes-green.svg

mucro
=====

Wouldn't it be nice to use your python apps without activating a virtualenv?

Imagine you have a python app ``blah.py``. This is what you do:

.. code:: bash

   $ source env/bin/activate
   (env) $ mucro --pyfile blah.py --bindir ~/bin

This will create an executable in the dir: ``~/bin/blah``. Now you can call
that executable from anywhere (it's on your ``$PATH`` right?).  And you don't
have to active a virtualenv. You can even continue to hack on ``blah.py`` in
one shell (with your dev virtualenv activated), and run it inside another shell
window in another path, with no virtualenv actived! YES!

Install
-------

This will create a ``mucro`` executable on your ``$PATH``:

.. code:: bash

   $ git clone git@github.com:cjrh/mucro.git
   $ cd mucro
   $ python3 mucro.py --pyfile mucro.py --bindir ~/bin

Be sure to replace ``~/bin`` with your own folder for such things that is
on your ``$PATH``.

Uninstall
---------

.. code:: bash

   $ cd mucro
   $ ./mucro-uninstall

This will remove the symlink that was created in ``~/bin`` in the *install* step.

How does it work?
-----------------

The answer is super boring, I'm afraid: ``mucro`` creates a new shell script
alongside the original py file, makes that shell script executable, and then
symlinks that into your target bin directory.

So if it's putting all this stuff all over the place, how do I clean it up?
Glad you asked! in addition to creating the ``blah`` executable, it will
also create a ``blah-uninstall`` executable that will delete the symlink,
the executable and the uninstaller itself!

What's in a name?
-----------------

The name *mucro* means *a short sharp point at the end of a part or organ*. In
this analogy, the organ is your python application, and the sharp point is the
executable entry point that can be accessed via ``$PATH``. Yes, I know it's
a stretch but coming up with good, unused names on GitHub is hard.
