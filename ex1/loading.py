import importlib
from typing import Any


def check_dependencies() -> bool:
    packages = [
        ("pandas", "Data manipulation ready"),
        ("numpy", "Numerical computation ready"),
        ("matplotlib", "Visualization ready")
    ]

    print("\nChecking dependencies:")
    missing = []

    for pkg, desc in packages:
        try:
            module = importlib.import_module(pkg)
            version = getattr(module, "__version__", "unknown")
            print(f"[OK] {pkg} ({version}) - {desc}")
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"\nMissing required dependencies: {', '.join(missing)}")
        print("\nDependency Management Instructions:")
        print("  [pip]    Run: pip install -r requirements.txt")
        print("  [Poetry] Run: poetry install")
        return False

    return True


def generate_matrix_dataset(np_module: Any, data_points: int = 1000) -> Any:
    random = np_module.random.default_rng(seed=42)
    time_axis = np_module.linspace(0.0, 30.0, data_points)
    base_signal = np_module.sin(time_axis)
    noise = random.normal(0.0, 0.2, data_points)
    energy = np_module.abs(base_signal + noise) * 100.0
    return np_module.column_stack((time_axis, energy))


def analyze_and_plot() -> None:
    try:
        np_module = importlib.import_module("numpy")
        pd_module = importlib.import_module("pandas")
        matplotlib = importlib.import_module("matplotlib")

        if hasattr(matplotlib, "use"):
            matplotlib.use("Agg")

        plt_module = importlib.import_module("matplotlib.pyplot")
    except ImportError:
        return

    print("\nAnalyzing Matrix data...")
    dataset = generate_matrix_dataset(np_module)
    print(f"Processing {dataset.shape[0]} data points...")

    dataframe = pd_module.DataFrame(
        dataset, columns=["time", "signal_strength"]
    )
    rolling = dataframe[
        "signal_strength"
        ].rolling(window=25, min_periods=1).mean()

    print("Generating visualization...")
    plt_module.figure(figsize=(10, 5))
    plt_module.plot(
        dataframe["time"],
        dataframe["signal_strength"],
        label="Signal strength",
        alpha=0.6,
    )
    plt_module.plot(
        dataframe["time"], rolling, label="Rolling mean", linewidth=2.0
    )
    plt_module.title("Matrix Signal Analysis")
    plt_module.xlabel("Time")
    plt_module.ylabel("Signal strength")
    plt_module.legend()
    plt_module.tight_layout()

    output_path = "matrix_analysis.png"
    plt_module.savefig(output_path)
    plt_module.close()

    print("\nAnalysis complete!")
    print(f"Results saved to: {output_path}")


def main() -> None:
    try:
        print("LOADING STATUS: Loading programs...")
        if check_dependencies():
            analyze_and_plot()
    except Exception as e:
        print(f"An error occurred during loading: {e}")
    except KeyboardInterrupt:
        print("\nLoading interrupted by user.")


if __name__ == "__main__":
    main()
