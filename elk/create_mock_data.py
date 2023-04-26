import sys
import pathlib

sys.path[0] = str(pathlib.Path(sys.path[0]).parent.absolute())

from test.utils import create_mock_es_data

if __name__ == "__main__":
    # Create mock data manually
    try:
        create_mock_es_data()
        print("CREATE MOCK ES DATA SUCCESSFULLY!")
    except Exception as e:
        print(f"ERROR: {e}")
