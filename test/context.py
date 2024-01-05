# pylint: disable=missing-module-docstring
import sys
from pathlib import Path


sys.path.insert(0, str(Path(Path(__file__).parent.parent).resolve()))

# pylint: disable=wrong-import-position, unused-import
import blocky       # noqa: F401, E402
