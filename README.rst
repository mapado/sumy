=========================
Automatic text summarizer
=========================
.. image:: https://api.travis-ci.org/miso-belica/sumy.png?branch=master
   :target: https://travis-ci.org/miso-belica/sumy

Here are some other summarizers:

- https://github.com/thavelick/summarize/ - Python, TF (very simple)
- `Sumtract: Second project for UW LING 572 <https://github.com/stefanbehr/sumtract>`_ - Python
- `Simple program that summarize text <https://github.com/xhresko/text-summarizer>`_ - Python, TF without normalization
- `Open Text Summarizer <http://libots.sourceforge.net/>`_ - C, TF without normalization

- `Automatic Document Summarizer <https://github.com/himanshujindal/Automatic-Text-Summarizer>`_ - Java, Bipartite HITS (no sources)
- `Pythia <https://github.com/giorgosera/pythia/blob/dev/analysis/summarization/summarization.py>`_ - Python, LexRank & Centroid
- `Reduction <https://github.com/adamfabish/Reduction>`_ - Python, some graph method
- `SWING <https://github.com/WING-NUS/SWING>`_ - Ruby
- `Topic Networks <https://github.com/bobflagg/Topic-Networks>`_ - R, topic models & bipartite graphs
- `Almus: Automatic Text Summarizer <http://textmining.zcu.cz/?lang=en&section=download>`_ - Java, LSA (without source code)
- `Musutelsa <http://www.musutelsa.jamstudio.eu/>`_ - Java, LSA (always freezes)
- http://mff.bajecni.cz/index.php - C++
- `MEAD <http://www.summarization.com/mead/>`_ - Perl, various methods + evaluation framework


Installation
------------
Currently only from git repo (make sure you have
`Python installed <https://python-guide.readthedocs.org/en/latest/#getting-started>`_)

.. code-block:: bash

    $ wget https://github.com/miso-belica/sumy/archive/master.zip # download the sources
    $ unzip master.zip # extract the downloaded file
    $ cd sumy-master/
    $ [sudo] python setup.py install # install the package

Or simply run:

.. code-block:: bash

    $ [sudo] pip install git+git://github.com/miso-belica/sumy.git


Usage
-----
Sumy contains command line utility for quick summarization of documents.

.. code-block:: bash

    $ sumy luhn --url=http://www.zdrojak.cz/clanky/automaticke-zabezpeceni/
    $ sumy edmundson --length=3% --url=http://cs.wikipedia.org/wiki/Bitva_u_Lipan
    $ sumy --help # for more info

Various evaluation methods for some summarization method can be executed by
commands below:

.. code-block:: bash

    $ sumy_eval lsa reference_summary.txt --url=http://www.zdrojak.cz/clanky/automaticke-zabezpeceni/
    $ sumy_eval edmundson reference_summary.txt --url=http://cs.wikipedia.org/wiki/Bitva_u_Lipan
    $ sumy_eval --help # for more info


Python API
----------
Or you can use sumy like a library in your project.

.. code-block:: python

    # -*- coding: utf8 -*-

    from __future__ import absolute_import
    from __future__ import division, print_function, unicode_literals

    from sumy.parsers.html import HtmlParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lsa import LsaSummarizer
    from sumy.nlp.stemmers.cs import stem_word
    from sumy.utils import get_stop_words


    if __name__ == "__main__":
        url = "http://www.zsstritezuct.estranky.cz/clanky/predmety/cteni/jak-naucit-dite-spravne-cist.html"
        parser = HtmlParser.from_url(url, Tokenizer("czech"))

        summarizer = LsaSummarizer(stem_word)
        summarizer.stop_words = get_stop_words("cs")

        for sentence in summarizer(parser.document, 20):
            print(sentence)


Tests
-----
Run tests via

.. code-block:: bash

    $ nosetests --with-coverage --cover-package=sumy --cover-erase tests
    $ nosetests-3.3 --with-coverage --cover-package=sumy --cover-erase tests
