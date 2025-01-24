# tests/utils/test_versions.py
from importlib.metadata import version
import sys

# Updated dependencies based on your Makefile and requirements
dependencies = [
    ("llama-index-core", "0.12.13"),
    ("llama-index-llms-ollama", "0.5.0"),
    ("torch", "2.5.0+cu124"),
    ("ollama", "0.4.7"),
    ("transformers", "4.48.1"),
    ("numpy", "2.2.2")
]

def test_versions():
    print("\nTesting dependency versions:")
    all_ok = True
    for pkg, expected in dependencies:
        try:
            installed = version(pkg)
            status = "✓" if installed == expected else "✗"
            print(f"  {status} {pkg:<25} Expected: {expected:<12} Installed: {installed}")
            if installed != expected:
                all_ok = False
        except Exception as e:
            print(f"  ✗ {pkg:<25} Not installed ({str(e)})")
            all_ok = False
    
    assert all_ok, "Version mismatches detected"
    print("\nAll versions match expected values!")

if __name__ == "__main__":
    try:
        test_versions()
    except AssertionError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    sys.exit(0)