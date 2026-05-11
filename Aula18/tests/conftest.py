from pathlib import Path
import sys


AULA18_ROOT = Path(__file__).resolve().parents[1]
if str(AULA18_ROOT) not in sys.path:
    sys.path.insert(0, str(AULA18_ROOT))
