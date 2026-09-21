#!/usr/bin/env bash
# Checks every http(s) URL found in data/*.yaml. Exit 1 if any fails.
# Some sites block non-browser clients (Unreal Engine returns 403); they are allow-listed below.
set -uo pipefail
cd "$(dirname "$0")/.."
ALLOW_403='unrealengine.com|linkedin.com'
fail=0
grep -ohE 'https?://[^ "'"'"'<>)]+' data/*.yaml | sort -u | while read -r url; do
  code=$(curl -sS -o /dev/null -L -m 25 -A "Mozilla/5.0 (link-check)" -w "%{http_code}" "$url" || echo "000")
  if [[ "$code" =~ ^(200|301|302)$ ]]; then
    printf "ok   %s %s\n" "$code" "$url"
  elif [[ "$code" == "403" && "$url" =~ $ALLOW_403 ]]; then
    printf "skip %s %s (bot-blocked)\n" "$code" "$url"
  else
    printf "FAIL %s %s\n" "$code" "$url"
    echo "$url" >> .links.failed
  fi
done
if [[ -f .links.failed ]]; then fail=1; echo; echo "Broken links:"; cat .links.failed; rm -f .links.failed; fi
exit $fail
