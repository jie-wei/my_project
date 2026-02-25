#!/usr/bin/env python3
"""
Desktop Notification Hook for Claude Code

Sends a desktop notification when Claude needs attention.
Cross-platform: macOS (osascript), Linux (notify-send), Windows (PowerShell).

Hook Event: Notification
"""

import json
import platform
import subprocess
import sys


def notify(title: str, message: str) -> None:
    """Send a desktop notification. Fails silently on all platforms."""
    system = platform.system()

    try:
        if system == "Darwin":
            subprocess.run(
                ["osascript", "-e",
                 f'display notification "{message}" with title "{title}"'],
                capture_output=True, timeout=5
            )
        elif system == "Linux":
            subprocess.run(
                ["notify-send", title, message],
                capture_output=True, timeout=5
            )
        elif system == "Windows":
            ps_script = (
                f"[Windows.UI.Notifications.ToastNotificationManager, "
                f"Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null; "
                f"$template = [Windows.UI.Notifications.ToastNotificationManager]::"
                f"GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::"
                f"ToastText02); "
                f"$text = $template.GetElementsByTagName('text'); "
                f"$text.Item(0).AppendChild($template.CreateTextNode('{title}')) | Out-Null; "
                f"$text.Item(1).AppendChild($template.CreateTextNode('{message}')) | Out-Null; "
                f"$toast = [Windows.UI.Notifications.ToastNotification]::new($template); "
                f"[Windows.UI.Notifications.ToastNotificationManager]::"
                f"CreateToastNotifier('Claude Code').Show($toast)"
            )
            subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True, timeout=5
            )
    except Exception:
        pass  # Fail silently — notifications are best-effort


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    message = hook_input.get("message", "Claude needs attention")
    title = hook_input.get("title", "Claude Code")

    notify(title, message)
    sys.exit(0)


if __name__ == "__main__":
    main()
