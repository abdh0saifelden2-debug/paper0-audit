#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
target="${1:-${PAPER0_ROOT:-$script_dir/../../../K1-two-clocks-theory}}"

if [[ ! -f "$target/tools/check_claim_map.py" ]]; then
  echo "not a target checkout: $target" >&2
  echo "usage: $0 /path/to/K1-two-clocks-theory" >&2
  exit 2
fi

PAPER0_ROOT="$target" exec python3 "$script_dir/check_claim_map.py"
