# Security Policy

## Reporting a vulnerability

Do not disclose credentials, raw DNS logs, private network details, or personal data in a public GitHub issue. Report concerns through the contact form at [zundathreat.ca](https://zundathreat.ca).

Include the affected component, concise reproduction steps, and potential impact. Remove secrets and personal data from evidence.

## Supported versions

ZSHIELD is currently a prototype. No production release is supported.

## Data handling

This public build does not send telemetry, heartbeat data, analytics, raw DNS logs, device identifiers, or browsing history to ZundaThreat or another remote dashboard.

Dashboard data is generated locally and served to a browser on the same network. Operators should keep port 8080 behind the router/firewall and use strong AdGuard Home and Raspberry Pi credentials.
