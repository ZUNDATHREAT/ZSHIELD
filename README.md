# ZSHIELD

**A local-first network privacy and threat-filtering appliance built on Raspberry Pi.**

ZSHIELD filters DNS requests for a home or small-office network before known advertising, tracking, analytics, malware, and phishing domains can be reached. It provides a branded dashboard on the operator's local network.

> Project status: working prototype. ZSHIELD complements—but does not replace—endpoint protection, software updates, a firewall, and safe browsing practices.

## Privacy guarantee for this public build

This repository contains **no telemetry or heartbeat service**.

- No remote reporting or node registration
- No external analytics SDK
- No cloud dashboard connection
- No raw DNS-log upload
- No client names, MAC addresses, private-IP inventory, or browsing-history transmission
- No automatic outbound connection from the dashboard

The browser requests `/api/status` from the Raspberry Pi. The local ZSHIELD service reads system health and aggregate counters from the local AdGuard Home API. That exchange remains inside the local network. Normal DNS resolution still uses the upstream resolver selected by the operator.

See [docs/architecture.md](docs/architecture.md).

## Dashboard

It shows current AdGuard Home queries, blocked requests, threat-list counters, block rate, Pi temperature, memory, storage, uptime, hostname, and local IP. Counts are DNS events—not confirmed cyberattacks, unique people, or unique devices.

## Install from a Windows PC

Do **not** run the Linux installation commands directly in ordinary Windows Command Prompt. Use Command Prompt only to connect to the Raspberry Pi:

```powershell
ssh <PI_USERNAME>@<PI_IP>
```

Replace the placeholders with the Raspberry Pi username and local IP. Enter the Pi account password when prompted. After the prompt changes to the Pi, run:

```bash
git clone https://github.com/ZUNDATHREAT/ZSHIELD.git
cd ZSHIELD
sudo bash scripts/install.sh
```

Then open:

```text
http://<PI_IP>:8080
```

If the folder already exists:

```bash
cd ZSHIELD
git pull
sudo bash scripts/install.sh
```

## What installation does

The installer copies the dashboard to `/opt/zshield`, creates private configuration at `/etc/zshield/zshield.env`, installs a systemd service, starts it immediately, and enables automatic startup after reboot. It does not install or activate telemetry.

## Useful checks

```bash
sudo systemctl status zshield --no-pager
curl http://127.0.0.1:8080/health
sudo journalctl -u zshield -n 50 --no-pager
```

## Security boundaries

Keep port 8080 behind the router/firewall. Do not expose it with public port forwarding. Use Tailscale or WireGuard for future remote access.

ZSHIELD filters DNS. It does not decrypt HTTPS, scan file contents, stop direct-to-IP connections, or replace endpoint security.

## Repository layout

```text
ZSHIELD/
├── app.py
├── static/
├── scripts/install.sh
├── systemd/zshield.service
├── docs/architecture.md
├── SECURITY.md
└── zshield.env.example
```

## License

Copyright © 2026 ZundaThreat. See [LICENSE](LICENSE).
