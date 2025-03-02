from dataclasses import dataclass, field
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

@dataclass
class Paths:
    """Paths for the scripture search."""

    data_dir: Path = PROJECT_ROOT / "data"
    dhamma_talks_suttas_data_file: Path = data_dir / "dhamma_talks_suttas.csv"

    def __post_init__(self):
        """Create directories if they don't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)

@dataclass
class Config:
    """Configuration for the scripture search."""

    paths: Paths = field(default_factory=Paths)