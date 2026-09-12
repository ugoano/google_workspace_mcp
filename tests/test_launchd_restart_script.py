import os
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "restart_launchd_jobs.sh"
PLIST = ROOT / "launchd" / "com.arno.google-workspace-mcp-nightly-restart.plist"


def test_restart_script_dry_run_lists_both_google_workspace_jobs():
    result = subprocess.run(
        [str(SCRIPT)],
        check=True,
        capture_output=True,
        text=True,
        env={**os.environ, "DRY_RUN": "1"},
    )

    lines = result.stdout.strip().splitlines()
    assert lines == [
        f"launchctl kickstart -k gui/{os.getuid()}/com.arno.google-workspace-mcp",
        f"launchctl kickstart -k gui/{os.getuid()}/com.arno.google-workspace-mcp-personal",
    ]


def test_restart_script_accepts_explicit_labels_for_targeted_checks():
    result = subprocess.run(
        [str(SCRIPT), "com.example.test"],
        check=True,
        capture_output=True,
        text=True,
        env={**os.environ, "DRY_RUN": "1"},
    )

    assert result.stdout.strip() == (
        f"launchctl kickstart -k gui/{os.getuid()}/com.example.test"
    )


def test_launchd_plist_schedules_nightly_restart_and_uses_script():
    parsed = subprocess.run(
        ["plutil", "-convert", "json", "-o", "-", str(PLIST)],
        check=True,
        capture_output=True,
        text=True,
    )

    plist = json.loads(parsed.stdout)
    assert plist["Label"] == "com.arno.google-workspace-mcp-nightly-restart"
    assert plist["ProgramArguments"] == [str(SCRIPT)]
    assert plist["StartCalendarInterval"] == {"Hour": 4, "Minute": 15}
