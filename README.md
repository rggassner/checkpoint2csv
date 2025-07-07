# Checkpoint Log Parser

This script parses Check Point firewall log entries from standard input and outputs them in either:

* **CSV format** for further analysis or reporting.
* **Formatted field=value log format** compatible with other log processing tools.

## Features

* Extracts specific fields: `time`, `src`, `s_port`, `dst`, `service`, `service_id`, `action`, `xlatesrc`
* Converts UNIX timestamps to human-readable datetime
* Supports both CSV and Check Point formats

## Usage

```bash
cat log.txt | ./checkpoint_log_parser.py          # Output CSV (default)
cat log.txt | ./checkpoint_log_parser.py -c       # Output Check Point style
```

## Options

| Flag                 | Description                      |
| -------------------- | -------------------------------- |
| `-c`, `--checkpoint` | Output in Check Point log format |

## Example Input

```
time="1719752098" src="192.168.1.1" s_port="12345" dst="10.0.0.5" service="http" service_id="80" action="accept" xlatesrc="203.0.113.10"
```

## Example Output (CSV)

```
time_formatted,time,src,s_port,dst,service,service_id,action,xlatesrc
2024-06-30 12:34:58-03:00,1719752098,192.168.1.1,12345,10.0.0.5,http,80,accept,203.0.113.10
```

## Example Output (Checkpoint)

```
time_formatted="2024-06-30 12:34:58-03:00" time="1719752098" src="192.168.1.1" s_port="12345" dst="10.0.0.5" service="http" service_id="80" action="accept" xlatesrc="203.0.113.10"
```

## Requirements

* Python 3
* tzlocal

Install dependencies:

```bash
pip install tzlocal
```

## License

MIT
