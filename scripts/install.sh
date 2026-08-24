#!/usr/bin/env bash
set -euo pipefail
if [[ $EUID -ne 0 ]]; then echo "Run with sudo: sudo bash scripts/install.sh"; exit 1; fi
SOURCE_DIR="$(pwd)"
INSTALL_DIR="/opt/zshield"
install -d -m 0755 "$INSTALL_DIR" /etc/zshield
cp -R "$SOURCE_DIR/app.py" "$SOURCE_DIR/static" "$INSTALL_DIR/"
chmod 0755 "$INSTALL_DIR/app.py"
if [[ ! -f /etc/zshield/zshield.env ]]; then install -m 0600 "$SOURCE_DIR/zshield.env.example" /etc/zshield/zshield.env; fi
install -m 0644 "$SOURCE_DIR/systemd/zshield.service" /etc/systemd/system/zshield.service
systemctl daemon-reload
systemctl enable --now zshield.service
echo "ZSHIELD installed on port 8080"
