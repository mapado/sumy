# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import unittest
import sumy.summarizers.lsa as lsa_module

from sumy.summarizers.lsa import LsaSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers.cs import stem_word
from sumy.utils import get_stop_words
from sumy._compat import to_unicode
from ..utils import build_document, load_resource


class TestLsa(unittest.TestCase):
    def test_numpy_not_installed(self):
        summarizer = LsaSummarizer()

        numpy = lsa_module.numpy
        lsa_module.numpy = None

        self.assertRaises(ValueError, summarizer, build_document(), 10)

        lsa_module.numpy = numpy

    def test_scipy_not_installed(self):
        summarizer = LsaSummarizer()

        scipy = lsa_module.singular_value_decomposition
        lsa_module.singular_value_decomposition = None

        self.assertRaises(ValueError, summarizer, build_document(), 10)

        lsa_module.singular_value_decomposition = scipy

    def test_empty_document(self):
        document = build_document()
        summarizer = LsaSummarizer()

        sentences = summarizer(document, 10)
        self.assertEqual(len(sentences), 0)

    def test_single_sentence(self):
        document = build_document(("I am the sentence you like",))
        summarizer = LsaSummarizer()
        summarizer.stopwords = ("I", "am", "the",)

        sentences = summarizer(document, 10)
        self.assertEqual(len(sentences), 1)
        self.assertEqual(to_unicode(sentences[0]), "I am the sentence you like")

    def test_document(self):
        document = build_document(
            ("I am the sentence you like", "Do you like me too",),
            ("This sentence is better than that above", "Are you kidding me",)
        )
        summarizer = LsaSummarizer()
        summarizer.stopwords = ("I", "am", "the", "you", "are", "me", "is", "than", "that", "this",)

        sentences = summarizer(document, 2)
        self.assertEqual(len(sentences), 2)
        self.assertEqual(to_unicode(sentences[0]), "I am the sentence you like")
        self.assertEqual(to_unicode(sentences[1]), "This sentence is better than that above")

    def test_real_example(self):
        """Source: http://www.prevko.cz/dite/skutecne-pribehy-deti"""
        parser = PlaintextParser.from_string(
            "Jednalo se o případ chlapce v 6. třídě, který měl problémy s učením. "
            "Přerostly až v reparát z jazyka na konci školního roku. "
            "Nedopadl bohužel dobře a tak musel opakovat 6. třídu, což se chlapci ani trochu nelíbilo. "
            "Připadal si, že je mezi malými dětmi a realizoval se tím, že si ve třídě "
            "o rok mladších dětí budoval vedoucí pozici. "
            "Dost razantně. Fyzickou převahu měl, takže to nedalo až tak moc práce.",
            Tokenizer("czech")
        )
        summarizer = LsaSummarizer(stem_word)
        summarizer.stop_words = get_stop_words("cs")

        sentences = summarizer(parser.document, 2)
        self.assertEqual(len(sentences), 2)
        self.assertEqual(to_unicode(sentences[0]),
            "Jednalo se o případ chlapce v 6. třídě, který měl problémy s učením.")
        self.assertEqual(to_unicode(sentences[1]),
            "Nedopadl bohužel dobře a tak musel opakovat 6. třídu, což se chlapci ani trochu nelíbilo.")

    def test_article_example(self):
        """Source: http://www.prevko.cz/dite/skutecne-pribehy-deti"""
        parser = PlaintextParser.from_string(
            load_resource("articles/prevko_cz_1.txt"),
            Tokenizer("czech")
        )
        summarizer = LsaSummarizer(stem_word)
        summarizer.stop_words = get_stop_words("cs")

        sentences = summarizer(parser.document, 20)
        self.assertEqual(len(sentences), 20)
