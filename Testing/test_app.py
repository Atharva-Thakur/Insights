from streamlit.testing.v1 import AppTest
# import sys
# sys.path.append("..")

def test_smoke():
    """Basic smoke test"""
    at = AppTest.from_file("../app.py", default_timeout=10).run()
    # Supported elements are primarily exposed as properties on the script
    # results object, which returns a sequence of that element.
    assert not at.exception

