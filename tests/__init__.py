# pylint: skip-file
# type: ignore
#
#       tests._init__.py is part of the docformatter project
#
# Copyright (C) 2012-2019 Steven Myint
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Standard Library Imports
import random
import string


def generate_random_docstring(
    max_indentation_length=32,
    max_word_length=20,
    max_words=50,
):
    """Generate single-line docstring."""
    if random.randint(0, 1):
        words = []
    else:
        words = [
            generate_random_word(random.randint(0, max_word_length))
            for _ in range(random.randint(0, max_words))
        ]

    indentation = random.randint(0, max_indentation_length) * " "
    quote = '"""' if random.randint(0, 1) else "'''"
    return quote + indentation + " ".join(words) + quote


def generate_random_word(word_length):
    return "".join(random.sample(string.ascii_letters, word_length))
