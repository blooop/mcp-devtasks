from unittest import TestCase
from mcp_devtasks.basic_class import BasicClass


class TestBasicClass(TestCase):
    def test_init(self):
        instance = BasicClass()

        self.assertEqual(instance.int_var, 0)
