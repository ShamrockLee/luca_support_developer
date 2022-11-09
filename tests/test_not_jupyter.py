from support_developer import support_luca
from support_developer.utils import is_directly_imported_in_jupyter_notebook


def test_not_jupyter():
    support_luca("support_developer")
    assert not is_directly_imported_in_jupyter_notebook()