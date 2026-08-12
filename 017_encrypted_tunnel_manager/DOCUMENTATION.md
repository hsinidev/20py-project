# Technical Documentation: Encrypted Communication Tunnel Manager

## 1. Tunneling Architecture
The system uses a **Decoupled Asynchronous Network Service** architecture. The `SSHManager` handles the persistent connection to the gateway, while local proxy threads handle the multiplexing of application traffic through the established SSH transport.

### Forwarding Modes
- **Dynamic (-D)**: Creates a SOCKS5 proxy locally.
- **Local (-L)**: Maps a local port to a specific remote host/port.
- **Remote (-R)**: Maps a remote port on the gateway back to a local resource.

## 2. Kill-Switch Mechanism
The `FirewallShield` module interacts with the OS kernel to manage outbound traffic rules.
- **Windows**: Uses `netsh` or direct WFP API calls to modify the active firewall profile.
- **Linux**: Uses `iptables` to set a `DROP` policy on the `OUTPUT` chain for all non-tunnel-endpoint traffic.

## 3. UI Rendering Engine
**Dear PyGui** was selected for its direct integration with GPU backends (DirectX11/OpenGL). This allows the application to render high-density traffic plots without consuming CPU cycles that should be dedicated to packet processing.
- **Theming**: Custom color palette "Matrix-Industrial" (#00FF41 on #0D0208).
- **Optimization**: Uses `add_line_series` with dynamic value buffering for smooth 60 FPS telemetry.

## 4. Security Protocols
- **Config Encryption**: Sensitive gateway credentials are stored on disk using Fernet symmetric encryption.
- **Elevation**: The application requires administrative/root privileges to modify kernel-level firewall rules.

## 5. Audit & Telemetry
- **Byte-Stream Analyzer**: Deque-based buffer for real-time throughput calculation.
- **Immutable Logs**: Encrypted session logs for compliance auditing.

---
**Developer**: HSINI MOHAMED
**Version**: 3.1.0
