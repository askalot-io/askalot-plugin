---
name: askalot-setup
description: Install-time configuration for the Askalot Claude Code plugin. Use when a user has just installed the askalot plugin from the marketplace and needs to point it at their tenant, sign in via the browser OAuth flow, verify the connection, or revoke an approved client. Covers the OAuth 2.1 flow and the alternate API-token path for non-interactive use.
disable-model-invocation: false
---

# Askalot Plugin Setup

You've installed the Askalot plugin. The only thing you need to configure
yourself is the tenant URL — authentication is handled by an OAuth 2.1
browser handshake on first use, not by pasting a token.

## 1. Point the plugin at your tenant

Set `ASKALOT_MCP_URL` in the shell that launches Claude Code:

```sh
# Paying Professional / Business customers (EU data residency):
export ASKALOT_MCP_URL=https://portor.eu1.askalot.io/mcp

# Free tier / universities / community organizations:
export ASKALOT_MCP_URL=https://portor.dev.askalot.io/mcp
```

If you don't know which tenant your account is on, check the URL of
the Askalot UI you sign in to — `eu1` and `dev` are the two production
tenants today.

### Security — verify the URL source

`ASKALOT_MCP_URL` MUST be an `askalot.io` subdomain. The OAuth flow
opens a browser to the URL you've set; a phishing-supplied URL routes
you to an attacker-controlled login page that captures your
credentials. Only use URLs from official Askalot documentation
(`https://docs.askalot.io`) or direct askalot.io operator
communication.

## 2. Sign in via OAuth on first use

The first time Claude Code calls an Askalot MCP tool after install,
Portor returns a 401 with an OAuth discovery hint and Claude Code
opens your browser to Askalot's authorization endpoint:

```
Portor /authorize → platform-OIDC /login → you sign in → consent
screen → tokens issued back to Claude Code
```

What happens, step by step:

1. Claude Code calls (for example) `mcp__plugin_askalot_askalot__list_projects`.
2. Portor responds with `401 Unauthorized` and a `WWW-Authenticate`
   header pointing at its OAuth metadata.
3. Claude Code reads `/.well-known/oauth-authorization-server`,
   registers itself dynamically with Portor, and opens your default
   browser to Portor's `/authorize` endpoint.
4. Portor redirects you to the platform OIDC provider's login page.
   If you're already signed in to Askalot in the browser, the login
   step is skipped; otherwise enter your credentials.
5. You see a consent screen showing "Claude Code is requesting access
   to your Askalot account" — click Approve.
6. The browser redirects back to a local Claude Code callback URL
   with an authorization code.
7. Claude Code exchanges the code for an access token + refresh
   token at Portor's `/token` endpoint, and stores both in its
   plugin-scoped secrets vault.

The plugin then retries the original tool call with the new bearer
token in the `Authorization` header. From here on, the refresh token
is exchanged transparently when the access token expires.

You only see the browser handshake once (or after revocation).

## 3. Verify the connection

After the browser flow completes, run any read-only MCP tool to confirm:

```
@mcp__plugin_askalot_askalot__list_projects
```

A successful call lists your accessible projects (or returns an empty
list if you haven't created any). A 401 here means the OAuth handshake
didn't complete or the refresh token was rejected — see Troubleshooting.

## 4. Revoke an approved client

If a machine is lost, stolen, or you want to revoke Claude Code's
access without affecting other API consumers:

1. Sign in to Profile Settings on the appropriate tenant
   - eu1 → `https://roundtable.eu1.askalot.io/profile/api-tokens`
   - dev → `https://roundtable.dev.askalot.io/profile/api-tokens`
2. Look for the OAuth-granted entry labeled "Claude Code"
   (registered_via=oauth) and click **Revoke**.
3. Claude Code's next MCP call will receive a 401; the OAuth
   handshake re-runs and you sign in again on the affected machine.

Revoking via Roundtable invalidates BOTH the access token and the
refresh token, so a stolen laptop's grant is dead immediately.

## Non-interactive use: API tokens for REST / CI

The OAuth flow above is for the Claude Code plugin's MCP transport.
For non-interactive REST API consumers (CI scripts, server-to-server,
spreadsheet-style data pulls), Askalot also issues classic API tokens:

1. Sign in to Profile Settings (links above), click **New API token**.
2. Give it a descriptive name, copy the `aslat_...` value (shown once).
3. Use it in REST calls as `Authorization: Bearer aslat_...` or
   `X-Api-Token: aslat_...`.

API tokens default to a 90-day lifetime (post-U13 cutover) — Profile
Settings flags tokens nearing 14 days from expiry with a "rotate
before <date>" warning. Pre-U13 tokens retain indefinite lifetime
and can be rotated voluntarily.

Don't paste an API token into the plugin's environment — the OAuth
flow is the supported path for Claude Code. The token mechanism
exists for use cases where a browser handshake isn't possible.

**Security warning:** do NOT add `aslat_...` tokens to your
`.zshrc`, `.bashrc`, or any other shell startup file that is
readable by other processes or committed to a repository. Shell RC
files are world-readable by default on many systems and are
frequently included in dotfile repos by accident. Store API tokens
in a secrets manager (e.g. macOS Keychain, 1Password, HashiCorp
Vault) or a `.env` file that is listed in `.gitignore`.

## Troubleshooting

- **Browser doesn't open during install:** Claude Code may have
  printed the `/authorize` URL to the terminal — open it manually.
- **`401 Unauthorized` after a successful sign-in:** the refresh
  token may have been revoked. Try a new MCP tool call to re-trigger
  the OAuth handshake.
- **`invalid_redirect_uri` in the browser:** Claude Code's localhost
  callback URL changed between install and use. Re-running
  `/plugin install` registers a fresh client; the prior one can be
  revoked via Profile Settings.
- **Tool calls hang or refuse to connect:** check `ASKALOT_MCP_URL`
  resolves and the tenant is reachable from your network.
