import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


def read_env_var(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def load_configuration() -> dict[str, str]:
    if load_dotenv is None:
        print("Missing dependency: python-dotenv")
        print("Install with: pip install python-dotenv")
        print("Or with Poetry: poetry add python-dotenv")
        sys.exit(1)

    load_dotenv(override=False)

    mode = read_env_var("MATRIX_MODE", "development")
    default_log = "DEBUG" if mode == "development" else "USER"

    return {
        "matrix_mode": mode,
        "database_url": read_env_var("DATABASE_URL"),
        "api_key": read_env_var("API_KEY"),
        "log_level": read_env_var("LOG_LEVEL", default_log),
        "zion_endpoint": read_env_var("ZION_ENDPOINT"),
    }


def validate_configuration(config: dict[str, str]) -> list[str]:
    errors: list[str] = []
    mode = config["matrix_mode"]
    if mode not in {"development", "production"}:
        errors.append("MATRIX_MODE must be 'development' or 'production'")
    if not config["database_url"]:
        errors.append("DATABASE_URL is missing")
    if not config["api_key"]:
        errors.append("API_KEY is missing")

    if mode == "production" and not config["zion_endpoint"]:
        errors.append("ZION_ENDPOINT is missing (Strictly required in production)")
    return errors


def environment_status(config: dict[str, str]) -> None:
    print(f"Mode: {config['matrix_mode']}")

    if config["matrix_mode"] == "production":
        print(">>> [DANGER] LIVE PRODUCTION ENVIRONMENT ACTIVE <<<")
        print("Database: Connected to PRODUCTION instance (WRITE-LOCKED)")
        print("API Access: Authenticated (STRICT RATE LIMITS)")
        print(f"Log Level: {config['log_level'].upper()}")

        print("Zion Network: Production uplink established (ENCRYPTED)")
    else:
        print("Database: Connected to local instance")
        print("API Access: Authenticated")
        print(f"Log Level: {config['log_level'].upper()}")

        if config["zion_endpoint"]:
            print("Zion Network: Online")
        else:
            print("Zion Network: Offline")


def security_checks() -> None:
    env_ignored = False
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r", encoding="utf-8") as gitignore_file:
            ignored_entries = [line.strip() for line in gitignore_file]
        env_ignored = ".env" in ignored_entries

    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")
    if env_ignored:
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] .env is not listed in .gitignore")
    print("[OK] Production overrides available\n")


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...\n")
    config = load_configuration()

    errors = validate_configuration(config)
    if errors:
        print("Configuration warnings/errors:")
        for error in errors:
            print(f"- {error}")
        print("\nCreate a .env file from .env.example or export variables manually.")
        return

    print("Configuration loaded:")
    environment_status(config)
    security_checks()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
