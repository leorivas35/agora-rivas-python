import os
import sys

from django.core.management import execute_from_command_line

DEFAULT_SETTINGS_MODULE = "agora_rivas.infrastructure.config.settings"


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)
    argv = list(sys.argv)
    if len(argv) == 1:
        argv += ["runserver", "0.0.0.0:8000"]
    execute_from_command_line(argv)


if __name__ == "__main__":
    main()
