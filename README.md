# To use version 1.4 and above, you need to reinstall. Updating will not work because I changed too much code and added new features.

# DOTYCAT TUNNEL
- dotycat tunnel.is — Free Script
This script is provided free of charge and may be used without a license or domain/IP registration. It is intended for testing purposes only. The author and distributor accept no responsibility for losses, damages, or legal issues arising from its use. Use at your own risk.

### TELEGRAM
- https://t.me/dotycatV2

## Default Ports

| Service  | Transport |   TLS       |   NTLS      |
|----------|-----------|-------------|-------------|
| VLESS    | gRPC      | 443         | -           |
| VLESS    | WebSocket | 443         | 80          |
| VLESS    | HttpUpgrade   | 443         | 80          |
| VLESS    | xHTTP     | 443         | 80          |
| VMESS    | gRPC      | 443         | -           |
| VMESS    | WebSocket | 443         | 80          |
| VMESS    | HttpUpgrade   | 443         | 80          |
| VMESS    | xHTTP     | 443         | 80          |
| Trojan   | gRPC      | 443         | -           |
| Trojan   | WebSocket | 443         | 80          |
| Trojan   | HttpUpgrade   | 443         | 80          |
| Trojan   | xHTTP     | 443         | 80          |
| SSH      | WebSocket | 443         | 80          |
| SQUID    | -         | 3128  | -           |
| OpenVPN  | TCP/UDP   | 1194        | 2200        |
| OHP      | TCP       | -           | 8000        |


## Custom path or NO path info 
- Allow configuration of custom paths or no path only for the following ports:
  
| Protocol | Type | Port |     Custom Path    |   Multi-Path Support   |
| -------- | ---- | ---- | ------------------ | -----------------------|
| VMESS    | TLS  | 2083 | / or `/<anytext>`  |  ✅ Yes `/<any>/<any>`   |
| VMESS    | NTLS | 2082 | / or `/<anytext>`  |  ✅ Yes `/<any>/<any>`   |
| VLESS    | TLS  | 2087 | / or `/<anytext>`  |  ✅ Yes `/<any>/<any>`   |
| VLESS    | NTLS | 2086 | / or `/<anytext>`  |  ✅ Yes `/<any>/<any>`   |

## Protocols & Multi-Path Support (WebSocket TLS & Non-TLS)

| Protocol       | Example Path       | Port TLS/NTLS  |   Multi-Path Support    |
|----------------|--------------------|----------------|-------------------------|
| **VMess (WS)** |      `/vmess`      |   443/80       | ⚠️ Partial (some port) |
| **VLESS (WS)** |      `/vless`      |   443/80       | ⚠️ Partial (some port) |
| **Trojan (WS)**|      `/trws`       |   443/80       | ⚠️ Partial (some port) |
| **Socks (WS)** |      `/ssws`       |   443/80       | ⚠️ Partial (some port) |
| **SSH (WS)**   |      `/<anypath>`  |   443/80       | ✅ Yes                 |



## Info:  
- ✅ All working: The tunnel works fully without issues.  
- ⚠️ Partial: Some features (e.g., SSH over WebSocket) may not work properly.  

## Ubuntu:
- 20 ✅ All working
- 22 ✅ All working
- 24 ✅ All working

## Debian:
- 10 ✅ All working
- 11 ✅ All working
- 12 ✅ All working

## Installation
 
<pre>
<code>apt update && apt upgrade -y && apt install -y git wget curl unzip && \
wget -O /root/install.sh https://raw.githubusercontent.com/dotywrt/doty/main/install.sh && \
chmod +x /root/install.sh && \
/root/install.sh</code>
</pre>

## Install a Specific Version

To install a specific version, pass the version as an argument:

<pre>
<code>apt update && apt upgrade -y && apt install -y git wget curl unzip && \
wget -O /root/install.sh https://raw.githubusercontent.com/dotywrt/doty/main/install.sh && \
chmod +x /root/install.sh && \
/root/install.sh VERSION HERE</code>
</pre>

Change VERSION HERE  to Script version  eg V1.4.1

## OS REINSTALL
<pre><code>curl -O https://raw.githubusercontent.com/dotywrt/reOS/main/reinstall.sh && bash reinstall.sh Debian 10</code></pre>

### Known Bugs (will fix later, too lazy now 😅)
- Active user count for Xray (VLESS, VMess, Trojan, SOCKS) not displayed correctly
- Automatic deletion of expired accounts not working
 
## Changelog

### 📅 [2025-09-03]
- Initial script release
  
### 📅 [2025-09-04]
- Added support for custom multipath
- Fixed gRPC connection issues
- Updated Nginx configuration (single file)
- Fixed issue where user data could not be saved to JSON file

### 📅 [2025-09-06]  
- Added automatic blocking of torrent sites (BitTorrent traffic, trackers, etc.)  
- Added automatic blocking of adult (pornographic) sites  
- Added ad-blocking functionality (ads, popups, tracking scripts)

### 📅 [2025-09-10]  
- Add new ports for VMESS & VLESS.
- Support custom paths or no path for a specific port.
- Remove NetGuard, Use Default host blocker
- Remove Xray multi-path on ports 443 and 80

### 📅 2025-09-11
- Added OpenVPN support (TCP / UDP / SSL)
- Added Squid Proxy (3128 / 8080)
- Added OHP (Open HTTP Puncher) over TCP

### 📅 2025-09-12
- Added support for ZIVPN panel
- Added support for SlowDNS

### 📅 2025-09-13
- Fixed bug in SSH WebSocket
- Fixed bug in SlowDNS
- Added support for UDP Custom
- Added auto delete expiry account

### 📅 2025-09-16
- Updated from stunnel4 to stunnel5

### 📅 2026-3-10
- Fix Stunnel5
- Fix Dropbear
- Fix ZiVpn
- Upgrade XRAY (Xray-Core-v25.10.15.3)
- Debugging My Lazy Brain.😄

### 📅 2026-3-11
- Fix SSH WebSocket (support lates os)
- Remove ZIVPN, UDP CUSTOM, SLOWDNS
