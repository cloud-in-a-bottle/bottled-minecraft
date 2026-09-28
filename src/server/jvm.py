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


def aikar_flags(memory_mb: int) -> list[str]:
    """Aikar's tuned G1GC flags (https://mcflags.emc.gs), sized for memory_mb. Includes -Xmx/-Xms."""
    flags = [
        f"-Xms{memory_mb}M",
        f"-Xmx{memory_mb}M",
        "-XX:+UseG1GC",
        "-XX:+ParallelRefProcEnabled",
        "-XX:MaxGCPauseMillis=200",
        "-XX:+UnlockExperimentalVMOptions",
        "-XX:+DisableExplicitGC",
        "-XX:+AlwaysPreTouch",
        "-XX:G1HeapWastePercent=5",
        "-XX:G1MixedGCCountTarget=4",
        "-XX:G1MixedGCLiveThresholdPercent=90",
        "-XX:G1RSetUpdatingPauseTimePercent=5",
        "-XX:SurvivorRatio=32",
        "-XX:+PerfDisableSharedMem",
        "-XX:MaxTenuringThreshold=1",
        "-Dusing.aikars.flags=https://mcflags.emc.gs",
        "-Daikars.new.flags=true",
    ]
    # Aikar recommends larger young-gen / region sizing at >= ~12 GB heaps.
    if memory_mb >= 12000:
        flags += [
            "-XX:G1NewSizePercent=40",
            "-XX:G1MaxNewSizePercent=50",
            "-XX:G1HeapRegionSize=16M",
            "-XX:G1ReservePercent=15",
            "-XX:InitiatingHeapOccupancyPercent=20",
        ]
    else:
        flags += [
            "-XX:G1NewSizePercent=30",
            "-XX:G1MaxNewSizePercent=40",
            "-XX:G1HeapRegionSize=8M",
            "-XX:G1ReservePercent=20",
            "-XX:InitiatingHeapOccupancyPercent=15",
        ]
    return flags


def effective_jvm_args(memory_mb: int, jvm_args: str, flags_preset: str) -> str:
    """Resolve a config's stored launch settings into the JVM-args string passed to a server.

    - "aikar": Aikar's flags generated from memory_mb (includes -Xmx/-Xms).
    - "custom": the user's raw jvm_args verbatim.
    - anything else ("none"/""): empty — heap_flags() will add -Xmx/-Xms from memory_mb.
    """
    if flags_preset == "aikar":
        return " ".join(aikar_flags(memory_mb))
    if flags_preset == "custom":
        return jvm_args
    return ""
