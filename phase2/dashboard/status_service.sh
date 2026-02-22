#!/usr/bin/env bash
set -euo pipefail

LABEL="com.quiznat.tothf.dashboard"

launchctl print "gui/$(id -u)/${LABEL}" | sed -n '1,120p'
echo
echo "HTTP check:"
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8787/ || true
