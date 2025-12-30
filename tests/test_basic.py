import importlib


def test_import_module():
    # import should not raise on import; it should define `app`
    m = importlib.import_module('testppy')
    assert hasattr(m, 'app')
