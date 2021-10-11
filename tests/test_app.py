import unittest

import server


def test_test():
    assert server.test() == "Works!"


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4
