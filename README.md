# vigiformes
Personal home-monitoring toy. Not a safety tool.

## Setup

On a fresh Raspberry Pi, install system dependencies before running the application:

```bash
./setup/install_deps.sh
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
