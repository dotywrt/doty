# DOTYCAT TUNNEL

## Default Ports

| Service  | Transport |   TLS    |    NTLS      |
|----------|-----------|----------|--------------|
| VLESS    | gRPC      | 443      | -            |
| VLESS    | WebSocket | 443      | 80           |
| VMESS    | gRPC      | 443      | -            |
| VMESS    | WebSocket | 443      | 80           |
| Trojan   | gRPC      | 443      | -            |
| Trojan   | WebSocket | 443      | 80           |
| SOCKS    | gRPC      | 443      | -            |
| SOCKS    | WebSocket | 443      | 80           |
| SSH      | WebSocket | 443      | 80           |

## Protocols & Multi-Path Support (WebSocket TLS & Non-TLS)

| Protocol       | Example Path       | Multi-Path Support |
|----------------|--------------------|--------------------|
| **VMess (WS)** | `/<anypath>/vmess` | ✅ Yes            |
| **VLESS (WS)** | `/<anypath>/vless` | ✅ Yes            |
| **Trojan (WS)**| `/<anypath>/trws`  | ✅ Yes            |
| **Socks (WS)** | `/<anypath>/ssws`  | ✅ Yes            |
| **SSH (WS)**   | `/<anypath>`       | ✅ Yes            |



## Info:  
- ✅ All working: The tunnel works fully without issues.  
- ⚠️ Partial: Some features (e.g., SSH over WebSocket) may not work properly.  

## Ubuntu:
- 20 ✅ All working
- 22 ✅ All working
- 24 ⚠️ Partial (⚠️ SSH not working)

## Debian:
- 10 ✅ All working
- 11 ✅ All working
- 12 ⚠️ Partial (⚠️ SSH not working)

## Installation
 
<pre>
<code>wget -O /root/doty.sh https://raw.githubusercontent.com/dotywrt/doty/1.0/doty.sh && chmod +x /root/doty.sh && /root/doty.sh</code>
</pre>

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

