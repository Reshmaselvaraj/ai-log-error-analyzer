import re

LOG_PATTERN = re.compile(
    r"""
    (?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d+)
    \s+
    (?P<level>INFO|WARN|ERROR|DEBUG)
    \s+
    \[(?P<component>[^\]]+)\]
    .*?
    (?P<message>.+)
    """,
    re.VERBOSE,
)


def clean_line(line: str) -> str:
    """
    Remove ANSI color codes and trim whitespace
    """
    ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", line).strip()


def parse_logs(file_path: str):
    """
    Parse WildFly / JBoss style logs into structured entries
    """
    parsed = []

    with open(file_path, "r", errors="ignore") as f:
        for line in f:
            line = clean_line(line)
            if not line:
                continue

            match = LOG_PATTERN.search(line)
            if not match:
                continue  # ignore non-log lines (build output, noise)

            data = match.groupdict()

            parsed.append(
                {
                    "timestamp": data["timestamp"],
                    "level": data["level"],
                    "component": data["component"],
                    "message": data["message"],
                }
            )

    return parsed
