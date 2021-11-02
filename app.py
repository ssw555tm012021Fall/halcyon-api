import unittest

from server import app

if __name__ == '__main__':
    app.run(debug=True, port=4000)


def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1
