"""gwsignal4gwsurr package initialization."""

import re
import sys
import logging
import platform
import os
import subprocess

try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown (not installed, run pip install -e .)"

def _get_dirty_files():
    """Return list of uncommitted changes."""
    try:
        result = subprocess.check_output(
            ["git", "-C", os.path.dirname(__file__), "status", "--porcelain"],
            text=True,
            stderr=subprocess.DEVNULL
        )
        return [line.strip() for line in result.strip().splitlines() if line.strip()]
    except Exception:
        return []
logger = logging.getLogger(__name__)



def _parse_version(version_str):
    """Parse a setuptools-scm version string into components."""
    match = re.match(
        r"(?P<tag>\d+\.\d+\.\d+)"
        r"(?:\.dev(?P<commits>\d+)"
        r"\+g(?P<hash>[0-9a-f]+)"
        r"(?:\.d(?P<date>\d+))?)?",
        version_str,
    )
    if not match:
        return version_str, None, None, False

    tag     = match.group("tag")
    commits = match.group("commits")
    githash = match.group("hash")
    dirty   = match.group("date") is not None
    return tag, commits, githash, dirty

def diagnostics_dict():
    """Return diagnostic info as a dict, useful for logging to files or experiment metadata."""
    tag, commits, githash, dirty = _parse_version(__version__)
    return {
        "package":        "gwsignal4gwsurr",
        "version":        __version__,
        "tag":            tag,
        "commits_since":  commits,
        "git_hash":       githash,
        "dirty":          dirty,
        "python":         sys.version,
        "platform":       platform.platform(),
    }


def diagnostics():
    """Print full diagnostic info."""
    d = diagnostics_dict()
    print(f"  package  : {d['package']}")
    print(f"  version  : {d['version']}")
    print(f"  tag      : {d['tag']}")
    print(f"  commits  : {d['commits_since']}")
    print(f"  git hash : {d['git_hash']}")
    print(f"  dirty    : {d['dirty']}")
    print(f"  python   : {d['python']}")
    print(f"  platform : {d['platform']}")



def _print_diagnostics():
    tag, commits, githash, dirty = _parse_version(__version__)

    if commits:
        version_str = f"{tag} +{commits} commits [{githash}]"
    else:
        version_str = tag

    if dirty:
        dirty_files = _get_dirty_files()
        version_str += f" (dirty: {len(dirty_files)} files)"

    print(
        f"gwsignal4gwsurr {version_str} | "
        f"python {sys.version.split()[0]} | "
        f"{platform.platform()}"
    )
    
    if dirty:
        for f in dirty_files:
            print(f"  {f}")

_print_diagnostics()
