import unittest
from walle.web.views.demo_view import WalleDemoView


class TestDemo(unittest.TestCase):
    def test_demo(self):
        demo = WalleDemoView()
        demo.get()
