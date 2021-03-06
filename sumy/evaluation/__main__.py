# -*- coding: utf8 -*-

"""
Sumy - evaluation of automatic text summary.

Usage:
    sumy_eval (random | luhn | edmundson | lsa) <reference_summary> [--length=<length>]
    sumy_eval (random | luhn | edmundson | lsa) <reference_summary> [--length=<length>] --url=<url>
    sumy_eval (random | luhn | edmundson | lsa) <reference_summary> [--length=<length>] --file=<file_path> --format=<file_format>
    sumy_eval --version
    sumy_eval --help

Options:
    <reference_summary>  Path to the file with reference summary.
    --url=<url>          URL address of summarizied message.
    --file=<file>        Path to file with summarizied text.
    --format=<format>    Format of input file. [default: plaintext]
    --length=<length>    Length of summarizied text. It may be count of sentences
                         or percentage of input text. [default: 20%]
    --version            Displays version of application.
    --help               Displays this text.

"""

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import sys

from itertools import chain
from docopt import docopt
from .. import __version__
from ..utils import ItemsCount, get_stop_words
from ..models import TfDocumentModel
from .._compat import urllib, to_string
from ..nlp.tokenizers import Tokenizer
from ..parsers.html import HtmlParser
from ..parsers.plaintext import PlaintextParser
from ..summarizers.random import RandomSummarizer
from ..summarizers.luhn import LuhnSummarizer
from ..summarizers.edmundson import EdmundsonSummarizer
from ..summarizers.lsa import LsaSummarizer
from ..nlp.stemmers.cs import stem_word
from . import precision, recall, f_score, cosine_similarity, unit_overlap


HEADERS = {
    "User-Agent": "Sumy (Automatic text summarizer) Version/%s" % __version__,
}
PARSERS = {
    "html": HtmlParser,
    "plaintext": PlaintextParser,
}


def build_random(parser):
    return RandomSummarizer()


def build_luhn(parser):
    summarizer = LuhnSummarizer(stem_word)
    summarizer.stop_words = get_stop_words("cs")

    return summarizer


def build_edmundson(parser):
    summarizer = EdmundsonSummarizer(stem_word)
    summarizer.null_words = get_stop_words("cs")
    summarizer.bonus_words = parser.significant_words
    summarizer.stigma_words = parser.stigma_words

    return summarizer


def build_lsa(parser):
    summarizer = LsaSummarizer(stem_word)
    summarizer.stop_words = get_stop_words("cs")

    return summarizer


def evaluate_cosine_similarity(evaluated_sentences, reference_sentences):
    evaluated_words = tuple(chain(*(s.words for s in evaluated_sentences)))
    reference_words = tuple(chain(*(s.words for s in reference_sentences)))
    evaluated_model = TfDocumentModel(evaluated_words)
    reference_model = TfDocumentModel(reference_words)

    return cosine_similarity(evaluated_model, reference_model)


def evaluate_unit_overlap(evaluated_sentences, reference_sentences):
    evaluated_words = tuple(chain(*(s.words for s in evaluated_sentences)))
    reference_words = tuple(chain(*(s.words for s in reference_sentences)))
    evaluated_model = TfDocumentModel(evaluated_words)
    reference_model = TfDocumentModel(reference_words)

    return unit_overlap(evaluated_model, reference_model)


AVAILABLE_METHODS = {
    "random": build_random,
    "luhn": build_luhn,
    "edmundson": build_edmundson,
    "lsa": build_lsa,
}
AVAILABLE_EVALUATIONS = (
    ("Precision", False, precision),
    ("Recall", False, recall),
    ("F-score", False, f_score),
    ("Cosine similarity", False, evaluate_cosine_similarity),
    ("Cosine similarity (document)", True, evaluate_cosine_similarity),
    ("Unit overlap", False, evaluate_unit_overlap),
    ("Unit overlap (document)", True, evaluate_unit_overlap),
)


def main(args=None):
    args = docopt(to_string(__doc__), args, version=__version__)
    summarizer, document, items_count, reference_summary = handle_arguments(args)

    evaluated_sentences = summarizer(document, items_count)
    reference_document = PlaintextParser.from_string(reference_summary, Tokenizer("czech"))
    reference_sentences = reference_document.document.sentences

    for name, evaluate_document, evaluate in AVAILABLE_EVALUATIONS:
        if evaluate_document:
            result = evaluate(evaluated_sentences, document.sentences)
        else:
            result = evaluate(evaluated_sentences, reference_sentences)
        print("%s: %f" % (name, result))


def handle_arguments(args):
    parser = PARSERS["plaintext"]
    input_stream = sys.stdin

    if args["--url"] is not None:
        parser = PARSERS["html"]
        request = urllib.Request(args["--url"], headers=HEADERS)
        input_stream = urllib.urlopen(request)
    elif args["--file"] is not None:
        parser = PARSERS.get(args["--format"], PlaintextParser)
        input_stream = open(args["--file"], "rb")

    summarizer_builder = AVAILABLE_METHODS["luhn"]
    for method, builder in AVAILABLE_METHODS.items():
        if args[method]:
            summarizer_builder = builder
            break

    items_count = ItemsCount(args["--length"])

    parser = parser(input_stream.read(), Tokenizer("czech"))
    if input_stream is not sys.stdin:
        input_stream.close()

    with open(args["<reference_summary>"], "rb") as file:
        reference_summmary = file.read().decode("utf8")

    return summarizer_builder(parser), parser.document, items_count, reference_summmary


if __name__ == "__main__":
    try:
        exit_code = main()
        exit(exit_code)
    except KeyboardInterrupt:
        exit(1)
    except Exception as e:
        print(e)
        exit(1)
