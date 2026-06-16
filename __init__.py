"""
Claude Code plugin tree for Askalot AI agents, skills, profiles, and MCP wiring.

This package marker exists so Python imports resolve cleanly against the
installed wheel (e.g. ``from askalot_ai.plugin.profiles import ...``). The
``agents/`` and ``skills/`` siblings are markdown-only and are not Python
sub-packages; ``__all__`` is empty to discourage importing them as such.

The directory is loaded by Claude Code via
``ClaudeAgentOptions(plugins=[{"type": "local", "path": <site-packages>/askalot_ai/plugin}])``
in SaaS execution, and via ``/plugin install`` from the public marketplace
mirror at github.com/askalot-io/askalot-plugin for CLI users.
"""

__all__: list[str] = []
