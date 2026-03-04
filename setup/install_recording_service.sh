#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
SAMPLES_DIR="$PROJECT_ROOT/recording/samples"

mkdir -p ~/.config/systemd/user ~/.config/user-tmpfiles.d

cat > ~/.config/systemd/user/vigiformes-recording.service <<EOF
[Unit]
Description=vigiformes recording pipeline
After=default.target
StartLimitIntervalSec=300
StartLimitBurst=5

[Service]
Type=simple
WorkingDirectory=$PROJECT_ROOT
ExecStart=$PROJECT_ROOT/.venv/bin/python -m recording.record
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=default.target
EOF

# d: create directory if missing, and clean files older than 1 day
cat > ~/.config/user-tmpfiles.d/vigiformes.conf <<EOF
d $SAMPLES_DIR 0755 - - 1d
EOF

# allow the user service to run without an active login session
loginctl enable-linger "$(whoami)"

systemctl --user daemon-reload
systemctl --user enable --now vigiformes-recording.service
systemd-tmpfiles --user --create

echo "Done."
echo "  Status : systemctl --user status vigiformes-recording"
echo "  Logs   : journalctl --user -u vigiformes-recording"
