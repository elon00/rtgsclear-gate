"""Legacy command shim: execute real offline tests, never claim 100/100."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.discover("tests", pattern="test_*.py")
    )
    sys.exit(0 if result.wasSuccessful() else 1)
