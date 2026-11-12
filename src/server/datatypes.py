import attr


# wherever possible, the developer version is used
# int rather than a string
@attr.s(auto_attribs=True, frozen=True)
class WorldInfo:
    version: int
    name: str
    port: int = 0
    mod_loader: str = "vanilla"
    mod_loader_version: str = ""


@attr.s(auto_attribs=True, frozen=True)
class JavaRequirement:
    java_version: int
    downloaded: bool


@attr.s(auto_attribs=True, frozen=True)
class ServerState:
    session_id: int
    version: int
    world: str
    port: int
    memory_mb: int
    running: bool
    status: str  # "running" | "stopping" | "saving" | "saved"


@attr.s(auto_attribs=True, frozen=True)
class StartRequest:
    world: str
    memory_mb: int
    jvm_args: str = ""


@attr.s(auto_attribs=True, frozen=True)
class RunRequest:
    """One-click launch of a config using its saved launch settings + active save."""

    world: str


@attr.s(auto_attribs=True, frozen=True)
class LaunchSettings:
    memory_mb: int = 4096
    jvm_args: str = ""
    flags_preset: str = "aikar"  # "aikar" | "custom" | "none"


@attr.s(auto_attribs=True, frozen=True)
class SaveInfo:
    name: str
    active: bool
    generated: bool  # has a level.dat on disk (vs. a pending name that generates on next launch)


@attr.s(auto_attribs=True, frozen=True)
class SaveRequest:
    save: str


@attr.s(auto_attribs=True, frozen=True)
class CommandRequest:
    session_id: int
    command: str


@attr.s(auto_attribs=True, frozen=True)
class WorldJarUpdate:
    version: int
    mod_loader: str
    mod_loader_version: str


@attr.s(auto_attribs=True, frozen=True)
class ServerPerfStats:
    pid: int
    cpu_percent: float
    memory_mb: float
    uptime_seconds: float
