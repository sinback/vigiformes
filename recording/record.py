import sys
from datetime import datetime
from pathlib import Path

import sounddevice as sd
import soundfile as sf

from recording.config import Config, load_config

PROJECT_ROOT = Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "recording" / "config.toml"


def record_clip(output_dir: Path, config: Config) -> None:
    frames = config.recording.duration_seconds * config.recording.sample_rate
    audio = sd.rec(
        frames=frames,
        samplerate=config.recording.sample_rate,
        channels=config.recording.channels,
        # always float32 regardless of hardware format; float16 has less dynamic range than int16
        # and downstream DSP expects float32
        dtype="float32",
        device=config.recording.device,
    )
    sd.wait()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sf.write(output_dir / f"{timestamp}.wav", audio, config.recording.sample_rate)


def run(config: Config) -> None:
    output_dir = config.output.directory
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Recording to {output_dir}")
    print(
        f"Device: {config.recording.device} | "
        f"{config.recording.sample_rate} Hz | "
        f"{config.recording.channels} ch | "
        f"{config.recording.duration_seconds}s clips"
    )
    print("Ctrl+C to stop.")

    while True:
        record_clip(output_dir, config)


def main() -> None:
    config = load_config(DEFAULT_CONFIG_PATH)
    try:
        run(config)
    except KeyboardInterrupt:
        print("\nStopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
