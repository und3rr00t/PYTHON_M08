import os
import sys
import site


def is_virtual_environment() -> bool:
    return bool(
        getattr(sys, "real_prefix", None)
        or (hasattr(sys, "base_prefix") and sys.prefix != sys.base_prefix)
    )


def print_outside_matrix() -> None:
    print("MATRIX STATUS: You're still plugged in\n")
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected\n")
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.\n")
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print(r"matrix_env\Scripts\activate # On Windows")
    print("\nThen run this program again.")


def print_inside_construct() -> None:
    print("MATRIX STATUS: Welcome to the construct\n")
    print(f"Current Python: {sys.executable}")

    env_name = os.path.basename(os.path.normpath(sys.prefix))
    print(f"Virtual Environment: {env_name}")
    print(f"Environment Path: {sys.prefix}\n")

    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.\n")
    print("Package installation path:")
    print(site.getsitepackages()[0])


def main() -> None:
    try:
        if is_virtual_environment():
            print_inside_construct()
        else:
            print_outside_matrix()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
