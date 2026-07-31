#!/usr/bin/env python3
"""
=============================================================================
Phase 7 - k6 Output Parser
=============================================================================
Parses k6 CSV (per-second aggregates) + k6 JSON streaming output (per-request)
to compute Tier-1 academic metrics and append one master row.

Inputs:
  --csv      Path to k6 CSV output (k6 run --out csv=...)
  --json     Path to k6 JSON streaming output (k6 run --out json=...)
  --master   Path to master_runs.csv (created if not exists, appended if exists)
  --platform Platform ID (e.g., 03_django_gunicorn)
  --scenario Scenario ID (e.g., A_browse)
  --rep      Replication number (1..8)
  --start    Run start timestamp (ISO 8601)
  --end      Run end timestamp (ISO 8601)

Output: One row appended to master_runs.csv with ~22 Tier-1 metrics.

Author: Chapk Rzgar Mohammed Abdalla, MSc Computer Science, U. Sulaimani
Thesis: Benchmarking Traditional vs Serverless Web Platforms (Phase 7)
=============================================================================
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from datetime import datetime


def percentile(values, p):
    """Compute the p-th percentile (linear interpolation, NumPy-compatible)."""
    if not values:
        return float('nan')
    s = sorted(values)
    n = len(s)
    if n == 1:
        return s[0]
    rank = (p / 100.0) * (n - 1)
    lo = int(rank)
    hi = min(lo + 1, n - 1)
    frac = rank - lo
    return s[lo] + frac * (s[hi] - s[lo])


def mean(values):
    return sum(values) / len(values) if values else float('nan')


def stddev(values):
    if len(values) < 2:
        return float('nan')
    m = mean(values)
    return (sum((x - m) ** 2 for x in values) / (len(values) - 1)) ** 0.5


def parse_k6_json(json_path):
    """Parse k6 JSON streaming output.

    Returns:
        dict with keys:
          durations_ms: list[float]   - all http_req_duration values
          dns_ms:       list[float]   - http_req_dns
          tcp_ms:       list[float]   - http_req_connecting (TCP handshake)
          tls_ms:       list[float]   - http_req_tls_handshaking
          waiting_ms:   list[float]   - http_req_waiting (TTFB server)
          sending_ms:   list[float]   - http_req_sending
          receiving_ms: list[float]   - http_req_receiving
          statuses:     list[int]     - HTTP status codes
          errors:       int           - count of http_req_failed=1
          total_requests: int
          total_iterations: int
          per_second_rps: list[(ts, rps)]
          data_received_bytes: int
          data_sent_bytes:     int
    """
    out = {
        'durations_ms': [],
        'dns_ms': [],
        'tcp_ms': [],
        'tls_ms': [],
        'waiting_ms': [],
        'sending_ms': [],
        'receiving_ms': [],
        'statuses': [],
        'errors': 0,
        'total_requests': 0,
        'total_iterations': 0,
        'data_received_bytes': 0,
        'data_sent_bytes': 0,
        'first_ts': None,
        'last_ts': None,
    }

    if not Path(json_path).exists():
        sys.stderr.write(f"WARNING: JSON file not found: {json_path}\n")
        return out

    with open(json_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue

            t = rec.get('type')
            if t != 'Point':
                continue

            metric = rec.get('metric', '')
            data = rec.get('data', {})
            val = data.get('value')
            ts = data.get('time')
            tags = data.get('tags', {})

            if val is None:
                continue

            # Track first/last timestamps
            if ts:
                if out['first_ts'] is None:
                    out['first_ts'] = ts
                out['last_ts'] = ts

            if metric == 'http_req_duration':
                out['durations_ms'].append(val)
                out['total_requests'] += 1
                # Status from tags
                status_str = tags.get('status', '0')
                try:
                    out['statuses'].append(int(status_str))
                except (ValueError, TypeError):
                    pass
            elif metric == 'http_req_dns':
                out['dns_ms'].append(val)
            elif metric == 'http_req_connecting':
                out['tcp_ms'].append(val)
            elif metric == 'http_req_tls_handshaking':
                out['tls_ms'].append(val)
            elif metric == 'http_req_waiting':
                out['waiting_ms'].append(val)
            elif metric == 'http_req_sending':
                out['sending_ms'].append(val)
            elif metric == 'http_req_receiving':
                out['receiving_ms'].append(val)
            elif metric == 'http_req_failed':
                if val == 1:
                    out['errors'] += 1
            elif metric == 'iterations':
                out['total_iterations'] += int(val) if val else 0
            elif metric == 'data_received':
                out['data_received_bytes'] += int(val) if val else 0
            elif metric == 'data_sent':
                out['data_sent_bytes'] += int(val) if val else 0

    return out


def apdex(durations_ms, t_satisfied_ms=500, f_tolerable_ms=2000):
    """Apdex score (Apdex Alliance 2007).
    T = 500ms (satisfied), F = 2000ms (tolerable, 4*T per standard).
    Apdex = (satisfied + tolerated/2) / total
    """
    if not durations_ms:
        return float('nan')
    satisfied = sum(1 for d in durations_ms if d <= t_satisfied_ms)
    tolerated = sum(1 for d in durations_ms if t_satisfied_ms < d <= f_tolerable_ms)
    total = len(durations_ms)
    return (satisfied + tolerated / 2.0) / total


def main():
    parser = argparse.ArgumentParser(description='Parse k6 output and append master row')
    parser.add_argument('--csv',       required=True,  help='k6 CSV output path')
    parser.add_argument('--json',      required=True,  help='k6 JSON streaming output path')
    parser.add_argument('--master',    required=True,  help='master_runs.csv path (created/appended)')
    parser.add_argument('--platform',  required=True,  help='Platform ID')
    parser.add_argument('--scenario',  required=True,  help='Scenario ID')
    parser.add_argument('--rep',       required=True,  type=int, help='Replication number')
    parser.add_argument('--start',     required=True,  help='Run start timestamp ISO')
    parser.add_argument('--end',       required=True,  help='Run end timestamp ISO')
    parser.add_argument('--target_rps', default='',    help='Target RPS (for verification)')
    args = parser.parse_args()

    # Parse JSON streaming output (primary source of raw per-request data)
    sys.stderr.write(f"Parsing k6 JSON: {args.json}\n")
    j = parse_k6_json(args.json)
    sys.stderr.write(f"  Parsed {j['total_requests']} requests, {j['errors']} errors\n")

    # Compute Tier-1 metrics
    durations = j['durations_ms']
    waiting   = j['waiting_ms']

    n_req = j['total_requests']
    n_err = j['errors']

    # Compute test duration in seconds (from first to last point timestamp)
    test_duration_sec = 0.0
    try:
        if j['first_ts'] and j['last_ts']:
            t0 = datetime.fromisoformat(j['first_ts'].replace('Z', '+00:00'))
            t1 = datetime.fromisoformat(j['last_ts'].replace('Z', '+00:00'))
            test_duration_sec = (t1 - t0).total_seconds()
    except Exception:
        pass

    rps_actual = (n_req / test_duration_sec) if test_duration_sec > 0 else float('nan')
    goodput_rps = ((n_req - n_err) / test_duration_sec) if test_duration_sec > 0 else float('nan')

    # Compose row
    row = {
        'run_id':           f"{args.platform}__{args.scenario}__rep{args.rep:02d}",
        'platform':         args.platform,
        'scenario':         args.scenario,
        'replication':      args.rep,
        'start_time':       args.start,
        'end_time':         args.end,
        'test_duration_s':  round(test_duration_sec, 2),
        'target_rps':       args.target_rps,
        'rps_actual':       round(rps_actual, 3) if rps_actual == rps_actual else '',
        'goodput_rps':      round(goodput_rps, 3) if goodput_rps == goodput_rps else '',
        'total_requests':   n_req,
        'total_errors':     n_err,
        'error_rate':       round(n_err / n_req, 6) if n_req else 0,
        # Latency distribution (ms)
        'latency_p50':      round(percentile(durations, 50), 3),
        'latency_p90':      round(percentile(durations, 90), 3),
        'latency_p95':      round(percentile(durations, 95), 3),
        'latency_p99':      round(percentile(durations, 99), 3),
        'latency_p999':     round(percentile(durations, 99.9), 3),
        'latency_mean':     round(mean(durations), 3) if durations else '',
        'latency_min':      round(min(durations), 3) if durations else '',
        'latency_max':      round(max(durations), 3) if durations else '',
        'latency_stddev':   round(stddev(durations), 3) if len(durations) > 1 else '',
        'latency_cv':       round(stddev(durations) / mean(durations), 6) if durations and mean(durations) > 0 else '',
        # TTFB decomposition (ms)
        'dns_p50':          round(percentile(j['dns_ms'], 50), 3) if j['dns_ms'] else '',
        'dns_p95':          round(percentile(j['dns_ms'], 95), 3) if j['dns_ms'] else '',
        'tcp_p50':          round(percentile(j['tcp_ms'], 50), 3) if j['tcp_ms'] else '',
        'tcp_p95':          round(percentile(j['tcp_ms'], 95), 3) if j['tcp_ms'] else '',
        'tls_p50':          round(percentile(j['tls_ms'], 50), 3) if j['tls_ms'] else '',
        'tls_p95':          round(percentile(j['tls_ms'], 95), 3) if j['tls_ms'] else '',
        'waiting_p50':      round(percentile(waiting, 50), 3) if waiting else '',
        'waiting_p95':      round(percentile(waiting, 95), 3) if waiting else '',
        'waiting_p99':      round(percentile(waiting, 99), 3) if waiting else '',
        # Quality of service
        'apdex_t500_f2000': round(apdex(durations, 500, 2000), 4),
        # Bandwidth
        'bytes_received':   j['data_received_bytes'],
        'bytes_sent':       j['data_sent_bytes'],
        'bandwidth_rx_bps': round(j['data_received_bytes'] / test_duration_sec, 1) if test_duration_sec > 0 else '',
        # Sanity tags
        'k6_iterations':    j['total_iterations'],
        'first_ts':         j['first_ts'] or '',
        'last_ts':          j['last_ts'] or '',
    }

    # Append to master CSV (write header if file doesn't exist)
    master_path = Path(args.master)
    write_header = not master_path.exists()
    with open(master_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    # Print summary to stdout for orchestrator log
    print(f"=== Parse Summary ===")
    print(f"  Run:          {row['run_id']}")
    print(f"  Requests:     {row['total_requests']}")
    print(f"  Errors:       {row['total_errors']}  (rate={row['error_rate']})")
    print(f"  RPS actual:   {row['rps_actual']} (target {row['target_rps']})")
    print(f"  Latency p50:  {row['latency_p50']} ms")
    print(f"  Latency p95:  {row['latency_p95']} ms")
    print(f"  Latency p99:  {row['latency_p99']} ms")
    print(f"  Apdex:        {row['apdex_t500_f2000']}")
    print(f"  CV:           {row['latency_cv']}")
    print(f"  Master row appended to: {master_path}")


if __name__ == '__main__':
    main()
