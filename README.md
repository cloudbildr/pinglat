# pinglat

A lightweight network ping latency logger for Windows, macOS, and Linux.

Use it to ping a list of hosts or IPs, then display the results on screen or log them to a CSV file for historical analysis. Pair it with cron (Linux/macOS) or Task Scheduler (Windows) to build a latency record over time — useful for diagnosing intermittent network issues, tracking WAP performance, or monitoring key devices on your LAN.

## Usage

```bash
python3 pinglat.py
```

The script will prompt you for:

1. **How to provide hosts** — load from a file or enter manually
2. **What to do with results** — display on screen, save to CSV, or both

### Option 1: Load from a file

Create a text file with one host per line. Each line can be:

```
LABEL,ip_or_hostname
ip_or_hostname
```

If no label is provided, the host value is used as the label. Lines starting with `#` are treated as comments.

**Example `hosts.txt`:**
```
# My network devices
WAP,192.168.1.1
IOT_Device,192.168.1.50
GOOGLE,8.8.8.8
cloudflare.com
```

### Option 2: Enter manually

Enter a comma-separated list of IPs or hostnames at the prompt:

```
8.8.8.8, 1.1.1.1, google.com
```

## Output

### Screen display

Results are printed in a clean, aligned table:

```
HOST        RESULT                                              TIMESTAMP
--------------------------------------------------------------------------
WAP         64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=3.21 ms   2026-03-22 10:04:21.123456
GOOGLE      64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=12.44 ms     2026-03-22 10:04:22.456789
```

### CSV logging

Results are appended to `pinglatstore.csv` in the same directory:

```
LABEL,ping result,timestamp
```

Run on a schedule to build a historical latency dataset you can analyze in Excel, Python, or any tool that reads CSV files.

## Requirements

- Python 3
- `ping` available on the system (standard on all platforms)
- No third-party packages required
