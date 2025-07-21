#!venv/bin/python3
import os
import re
from pathlib import Path
from multiprocessing import Pool, cpu_count
import argparse

# Compile once
user_re = re.compile(r'user="(?:.*?\()?(?P<username>[a-zA-Z0-9._-]+)\s*(?:\))?"')

def extract_username(line):
    match = user_re.search(line)
    if match:
        return match.group("username").strip()
    return None

def process_file(args):
    file_path, output_dir = args
    output_dir = Path(output_dir)

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
            user_buffers = {}

            for line in infile:
                username = extract_username(line)
                if username:
                    user_buffers.setdefault(username, []).append(line)

        # Write all user buffers to their log files
        for username, lines in user_buffers.items():
            out_path = output_dir / f"{username}.log"
            with open(out_path, 'a') as f:
                f.writelines(lines)

        print(f"Processed: {file_path}")
    except Exception as e:
        print(f"Error: {file_path}: {e}")

def main(input_dir, output_dir, processes):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = sorted([f for f in input_dir.glob("**/*") if f.is_file()])
    tasks = [(str(f), str(output_dir)) for f in files]

    print(f"Starting pool with {processes} processes...")
    with Pool(processes) as pool:
        pool.map(process_file, tasks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help="Directory with input log files")
    parser.add_argument("output_dir", help="Directory to store per-user logs")
    parser.add_argument("--processes", type=int, default=cpu_count(), help="Number of worker processes (default: all CPUs)")
    args = parser.parse_args()

    main(args.input_dir, args.output_dir, args.processes)
