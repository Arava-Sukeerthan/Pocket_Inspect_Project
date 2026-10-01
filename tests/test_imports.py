"""
Basic package import test using standard unittest.
"""
import unittest

class TestPackageImports(unittest.TestCase):
    def test_imports(self):
        import src
        import src.acquisition
        import src.quality
        import src.inference
        import src.adaptation
        import src.inspection
        import src.uncertainty
        import src.monitoring

        self.assertEqual(src.__version__, "0.1.0")

if __name__ == "__main__":
    unittest.main()
