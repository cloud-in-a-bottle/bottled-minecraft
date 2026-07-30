import shlex

_HEAP_MAX_PREFIXES = ("-Xmx", "-XX:MaxHeapSize")


def parse_jvm_args(raw: str) -> list[str]:
    """Tokenize user-supplied JVM args, splitting on whitespace/newlines and honoring quotes."""
    return shlex.split(raw)


def heap_flags(memory_mb: int, jvm_args: list[str]) -> list[str]:
    """Return -Xmx/-Xms from memory_mb, or [] when memory_mb <= 0 or jvm_args already sets a max heap."""
    if memory_mb <= 0 or any(a.startswith(_HEAP_MAX_PREFIXES) for a in jvm_args):
        return []
    return [f"-Xmx{memory_mb}M", f"-Xms{memory_mb}M"]
