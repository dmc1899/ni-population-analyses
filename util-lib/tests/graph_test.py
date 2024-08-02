"""
Tests for the graph module.
"""

import logging
import unittest

from util_lib import graph

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def test_get_named_plotly_colours() -> None:
    df = graph.get_named_plotly_colours()
    assert df.size == 147
    assert df.columns.size == 1

