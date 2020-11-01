from unittest import TestCase

from .plugins.mockplugin import MockPlugin
from .plugins.test1 import Test1
from .plugins.test2 import Test2
from .plugins2.test3 import Test3

class TestPlugin(TestCase):
	def setUp(self):
		self.plugins = MockPlugin()

	def test_plugins_can_be_found(self):
		self.assertTrue(self.plugins.plugins)

	def test_plugins_can_be_instantiated(self):
		test1 = self.plugins.instance('Test1')
		self.assertIsInstance(test1, Test1)

	def test_plugins_can_be_instantiated_from_custom_parameters(self):
		test2 = self.plugins.byFoo('bar')
		self.assertIsInstance(test2, Test2)

	def test_plugins_can_be_instantiated_with_a_configuration(self):
		config = { 'foo': 'bar' }
		test2 = self.plugins.instance('Test2', config)
		self.assertEqual("bar", test2.foo)

	def test_plugins_can_be_found_in_dynamically_added_directories(self):
		self.plugins.addPath('tests.plugins2')
		test3 = self.plugins.instance('Test3')
		self.assertIsInstance(test3, Test3)
