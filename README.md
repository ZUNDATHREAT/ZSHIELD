# ZSHIELD

ZSHIELD is a local-first Raspberry Pi network privacy dashboard for AdGuard Home. It gives a home or small business a simple branded view of DNS activity, blocked trackers, threat protection, device status, and system health without sending dashboard data to the cloud.

## Included

- Responsive dashboard for `http://192.168.68.80:8080`
- Live AdGuard Home statistics through its local API
- Pi temperature, memory, disk, uptime, hostname, and IP
- Graceful offline state
- No Docker requirement
- systemd service and installer
- Python standard library only

## Install

```bash
git clone https://github.com/ZUNDATHREAT/ZSHIELD.git
cd ZSHIELD
sudo bash scripts/install.sh
```

Open `http://192.168.68.80:8080` or `http://zshield.local:8080`.

If AdGuard Home requires authentication, edit `/etc/zshield/zshield.env`, then run `sudo systemctl restart zshield`.

## Development

```bash
python3 app.py
```

## Security

Do not expose port 8080 directly to the public internet. Use Tailscale or WireGuard for remote access.

## Roadmap

Per-device summaries, plain-language block explanations, encrypted SSD history, optional WireGuard administration, ZundaThreat safety checks, and local AI summaries.

## License

Copyright © 2026 ZundaThreat. See [LICENSE](LICENSE).
