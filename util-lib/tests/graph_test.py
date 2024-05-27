import logging
import unittest

from util_lib import graph

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class TestGraphHelp(unittest.TestCase):

    def test_get_named_plotly_colours(self) -> None:
        df = graph.show_named_plotly_colours()
        assert df.size == 147
        assert df.columns.size == 1


if __name__ == "__main__":
    unittest.main()
