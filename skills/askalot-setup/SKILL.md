---
name: askalot-setup
description: Install-time configuration for the Askalot Claude Code plugin. Use when a user has just installed the askalot plugin from the marketplace and needs to point it at their tenant, sign in via the browser OAuth flow, verify the connection, or revoke an approved client. Covers the OAuth 2.1 flow and the alternate API-token path for non-interactive use.
---

# Askalot Plugin Setup

You've installed the Askalot plugin. The only thing you need to configure
yourself is the tenant URL — authentication is handled by an OAuth 2.1
browser handshake on first use, not by pasting a token.

## 1. Point the plugin at your tenant

Set `ASKALOT_MCP_URL` in the shell that launches Claude Code:

```sh
# Paying customers, universities and community organizations (EU production):
export ASKALOT_MCP_URL=https://portor.eu1.askalot.io/mcp

# Free trial and demo:
export ASKALOT_MCP_URL=https://portor.dev.askalot.io/mcp
```

Left unset, the plugin connects to `dev`. If you don't know which tenant
your account is on, check the URL of the Askalot UI you sign in to —
`eu1` and `dev` are the two tenants today. Pointing at the wrong one is
recoverable: sign-in succeeds and then ends with `user_not_in_tenant`,
whose message gives the `ASKALOT_MCP_URL` value for the tenant your
account is on. Set it and start Claude Code again; the variable is read
at launch.

### Security — verify the URL source

`ASKALOT_MCP_URL` must be an `askalot.io` subdomain. The OAuth flow
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
Portor /authorize → platform-OIDC /login → you sign in → tokens
issued back to Claude Code
```

What happens, step by step:

1. Claude Code calls (for example) `mcp__plugin_askalot_askalot__list_projects`.
2. Portor responds with `401 Unauthorized` and a `WWW-Authenticate`
   header pointing at its OAuth metadata.
3. Claude Code reads `/.well-known/oauth-authorization-server`,
   registers itself dynamically with Portor, and opens your default
   browser to Portor's `/authorize` endpoint.
4. Portor redirects you to the platform OIDC provider's login page
   (`oidc.platform.askalot.io`). Above the form it names the
   application asking to connect and the address your sign-in sends
   access to; for Claude Code that address is on your own machine
   (`localhost`). There is no separate consent screen: signing in is
   the approval, so stop if the application or address is not what you
   expect.
5. The browser redirects back to a local Claude Code callback URL
   with an authorization code.
6. Claude Code exchanges the code for an access token + refresh
   token at Portor's `/token` endpoint and stores both.

The plugin then retries the original tool call with the new bearer
token in the `Authorization` header. From here on, the refresh token
is exchanged transparently when the access token expires.

You see the browser handshake once, and again only after the sign-in
has ended (section 5).

## 3. Verify the connection

After the browser flow completes, run any read-only MCP tool to confirm:

```
@mcp__plugin_askalot_askalot__list_projects
```

A successful call lists your accessible projects (or returns an empty
list if you haven't created any). A 401 here means the OAuth handshake
didn't complete or the refresh token was rejected — see Troubleshooting.

## 4. Which organization are you working in?

Your session is always in exactly **one** organization at a time — its
*active organization* — and every tool call resolves against it. Projects,
questionnaires, campaigns and datasets are all organization-scoped, so this
is the single most important thing to know about where a tool is looking.

**Where you start.** A fresh session lands in your home organization: the
one your account belongs to. You are never asked to choose during sign-in.

**How to see it.** `list_organizations` shows every organization this session
may act in, marks which one is active, and flags any that are read-only:

```
@mcp__plugin_askalot_askalot__list_organizations
```

If you belong to one organization, that is the whole list and there is
nothing to manage. If you are a multi-organization member — or an operator —
the list is longer, and it matches exactly what the **Switch Organization**
menu offers you in the browser.

**How to change it.** `switch_organization` moves the session:

```
@mcp__plugin_askalot_askalot__switch_organization organization_id=<id from the list>
```

Every later call resolves in the new organization, and the change **sticks**:
restart Claude Code and you resume where you left off. Switch back the same
way. The tenant is fixed when you sign in and never changes — switching moves
you between organizations inside one tenant.

**When you are in the wrong one.** A not-found now tells you where it looked:

```
Project 6f2a… not found (searched organization: ACME Corp)
```

That is the signal to run `list_organizations` and switch, rather than
concluding the project does not exist.

**Sealed organizations.** Some organizations are sealed — a curated demo,
or a former customer's data kept for its retention window. You can switch
into one and read everything; any attempt to write is refused with
`org_sealed`. `list_organizations` marks them (`sealed: true`), so you can tell before you
try.

## 5. End the plugin's sign-in

The plugin's OAuth sign-in is not an API token and does not appear in
Profile Settings, whose token list holds API tokens only. It ends in one
of these ways:

- **From the machine that holds it**: sign out of the Askalot server in
  Claude Code (its `/mcp` menu). The next MCP call gets a 401 and the
  browser handshake runs again.
- **By losing the organization**: when an administrator removes you from
  the organization the session acts in, its tokens are revoked.
- **By disuse**: the access token lasts 1 hour and the refresh token
  30 days, so a sign-in nothing uses for 30 days is dead.

There is no self-service way to end the sign-in of a machine you no
longer have. For a lost or stolen machine, contact Askalot
(`info@askalot.io`), and say so plainly to a user who asks: revoking
API tokens in Profile Settings does not touch it.

## Non-interactive use: API tokens for REST / CI

The OAuth flow above is for the Claude Code plugin's MCP transport.
For non-interactive REST API consumers (CI scripts, server-to-server,
spreadsheet-style data pulls), Askalot also issues classic API tokens:

1. Sign in to Profile Settings on your tenant
   (`https://roundtable.eu1.askalot.io/profile` or
   `https://roundtable.dev.askalot.io/profile`) and click
   **Generate New Token**.
2. Give it a descriptive name, choose an expiry (30 days, 90 days or
   1 year), and copy the `aslat_...` value (shown once).
3. Use it in REST calls as the `X-Api-Token: aslat_...` header. Portor's
   `Authorization: Bearer` path is OAuth-only and will 401 on an API
   token — API tokens travel exclusively via `X-Api-Token`.

The expiry defaults to 90 days, and Profile Settings flags a token
within 14 days of expiring. A token does not renew: generate a
replacement, switch to it, then revoke the old one in the same list.
A token acts in the organization you were working in when you
generated it; it is not accepted on the MCP endpoint.

This is also the credential to use when you (the agent) generate
sandboxed code that drives the REST API directly for a mass operation —
see the `gateway-routing` skill's code-execution guidance for why a
minted API token, not your live MCP OAuth session token, is the right
credential for that lane.

Don't paste an API token into the plugin's environment — the OAuth
flow is the supported path for Claude Code. The token mechanism
exists for use cases where a browser handshake isn't possible.

**Security warning:** do not add `aslat_...` tokens to your
`.zshrc`, `.bashrc`, or any other shell startup file: those files are
often readable by other users and end up in dotfile repositories by
accident. Store API tokens in a secrets manager (e.g. macOS Keychain,
1Password, HashiCorp Vault) or a `.env` file that is listed in
`.gitignore`.

## Troubleshooting

- **Browser doesn't open during install:** Claude Code may have
  printed the `/authorize` URL to the terminal — open it manually.
- **`401 Unauthorized` after a successful sign-in:** the refresh
  token may have been revoked. Try a new MCP tool call to re-trigger
  the OAuth handshake.
- **`invalid_redirect_uri` in the browser:** Claude Code's localhost
  callback URL changed between install and use. Re-running
  `/plugin install` registers a fresh client.
- **Sign-in succeeds, then `user_not_in_tenant`:** your account is on
  the other tenant. Set `ASKALOT_MCP_URL` to the URL the message gives
  and start Claude Code again.
- **Tool calls hang or refuse to connect:** check `ASKALOT_MCP_URL`
  resolves and the tenant is reachable from your network.
