"""
Claude Code plugin tree for Askalot AI skills, profiles, and MCP wiring.

This package marker exists so Python imports resolve cleanly against the
installed wheel (e.g. ``from askalot_ai.plugin.profiles import ...``). The
``skills/`` sibling is markdown-only and is not a Python sub-package;
``__all__`` is empty to discourage importing it as one. The research-lifecycle
flows are skills, not installed agents, so there is no ``agents/`` directory.

The directory is loaded by Claude Code via
``ClaudeAgentOptions(plugins=[{"type": "local", "path": <site-packages>/askalot_ai/plugin}])``
in SaaS execution, and via ``/plugin install`` from the public marketplace
mirror at github.com/askalot-io/askalot-plugin for CLI users.
"""

__all__: list[str] = []
