# Phase 2 Dashboard

Lightweight local dashboard for monitoring experiment execution and result artifacts.

## URL
- `http://127.0.0.1:8787`

## Features
- protocol-v3.1 and protocol-v3.2 block/pair progress tracking (`done/partial/not started`)
- runtime process status from PID/log files
- protocol-v3 directional snapshot (ToT vs ReAct)
- protocol-v3.1/v3.2 series explorer with filters (including version) and click-through detail (`task x model x profile`)
- latest analysis artifacts table
- log-tail viewer for runtime logs

## Install As Persistent macOS Service (launchd)
```bash
bash /Users/quiznat/Desktop/Tree_of_Thought/phase2/dashboard/install_service.sh
```

## Verify Service
```bash
launchctl print gui/$(id -u)/com.quiznat.tothf.dashboard | sed -n '1,80p'
curl -I http://127.0.0.1:8787/
```

## Privacy Note (macOS)
If service mode shows empty data while manual mode works, macOS Desktop privacy controls are blocking LaunchAgent file reads.

Open the privacy panel and print the exact interpreter path used by launchd:
```bash
bash /Users/quiznat/Desktop/Tree_of_Thought/phase2/dashboard/repair_permissions.sh
```

After granting Full Disk Access to that interpreter, reinstall:
```bash
bash /Users/quiznat/Desktop/Tree_of_Thought/phase2/dashboard/install_service.sh
```

## Uninstall Service
```bash
bash /Users/quiznat/Desktop/Tree_of_Thought/phase2/dashboard/uninstall_service.sh
```

## Run Manually
```bash
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/dashboard/server.py --host 127.0.0.1 --port 8787
```

## Session-Resilient Manual Service (Fallback)
Use this if macOS privacy blocks LaunchAgent data access from Desktop paths.

Start:
```bash
bash /Users/quiznat/Desktop/Tree_of_Thought/phase2/dashboard/start_manual_service.sh 8891
```

Stop:
```bash
bash /Users/quiznat/Desktop/Tree_of_Thought/phase2/dashboard/stop_manual_service.sh 8891
```
