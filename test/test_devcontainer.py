import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEVCONTAINER = REPO / ".devcontainer"


def host_bind_sources() -> list[str]:
    config = (DEVCONTAINER / "devcontainer.json").read_text(encoding="utf-8")
    return re.findall(r"source=\$\{localEnv:HOME\}/([^,]+),[^\"]*type=bind", config)


def test_init_host_creates_every_home_bind_source(tmp_path):
    """docker refuses to create the container when a bind source is missing."""
    sources = host_bind_sources()
    assert sources, "found no ${localEnv:HOME} bind mounts in devcontainer.json"

    subprocess.run(
        [str(DEVCONTAINER / "claude-code" / "init-host.sh")],
        env={"HOME": str(tmp_path), "PATH": "/usr/bin:/bin"},
        check=True,
    )

    missing = [s for s in sources if not (tmp_path / s).is_dir()]
    assert not missing
