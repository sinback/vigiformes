# vigiformes
Personal home-monitoring toy. Not a safety tool.

## Setup

On a fresh Raspberry Pi, install system dependencies before running the application:

```bash
./setup/install_deps.sh
```

## Python environment

This project uses Python 3.14 via [pyenv](https://github.com/pyenv/pyenv).

```bash
pyenv install 3.14
python -m venv .venv
source .venv/bin/activate
```

The `.python-version` file in the repo root will make pyenv select 3.14 automatically once it's installed.

Then install dev tools and git hooks:

```bash
pip install -r requirements-dev.txt
hooks/autohook.sh install
```

## Linting and type checking

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and import sorting, and [mypy](https://mypy.readthedocs.io/) for type checking. Ruff's isort integration enforces alphabetical imports with trailing commas (configured in `pyproject.toml`).

```bash
ruff check .
mypy .
```

To auto-fix import ordering and other fixable issues:

```bash
ruff check --fix .
```

## Audio device detection and initial mic check

PiOS uses ALSA for audio. You'll need to take note of its ALSA device name to get this project working.

Example:
```bash
sinback@raspberrypi:~ $ arecord -l
**** List of CAPTURE Hardware Devices ****
card 2: H2 [HyperX SoloCast 2], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

The hardware device name in this example is `hw:2,0`. The `2` comes from `card 2` being reported, and the `0` comes from `device 0` being reported. Depending on your platform, this may be different, especially if you're trying to make this project work on a non-PiOS device.

Verify the interface is working:
```bash
arecord -D hw:2,0 -d 5 -f S24_3LE -c 2 -r 44100 test.wav
```

Make sure to replace `hw:2,0` with the device name you just learned using `arecord -l`. Depending on your device, you may need to use different flags. For example, for a mono-channel mic, you want `-c 1`. Read `arecord --help` if you're stuck or see errors. Listen to `test.wav` to confirm your mic is functioning.

## Recording service

Once the mic is confirmed working, install the recording pipeline as a systemd user service:

```bash
./setup/install_recording_service.sh
```

Assuming you haven't overriden recording/config.toml, this installs and starts a service that
continuously records 5-second clips to `recording/samples/`, and configures systemd to automatically
delete clips older than 1 day. The service restarts automatically on failure and starts on boot
without requiring an active login session.

Check recording/config.toml for some tweakable settings (such as clip duration and destination for
recordings on the filesystem). If you want to change the 1 day retention rule, you'll need to update
`setup/install_recording_service.sh`.

Useful commands:

```bash
systemctl --user status vigiformes-recording   # check service status
systemctl --user stop vigiformes-recording     # stop recording
systemctl --user start vigiformes-recording    # start recording
journalctl --user -u vigiformes-recording      # view logs
```
