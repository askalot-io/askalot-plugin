---
name: askalot-setup
description: Install-time configuration for the Askalot Claude Code plugin. Use when a user has just installed the askalot plugin from the marketplace and needs to sign in via the browser OAuth flow, verify the connection, see or switch the organization the session works in, or end a sign-in. Covers the single connection address, the OAuth 2.1 flow and the alternate API-token path for non-interactive use.
---

# Askalot Plugin Setup

You've installed the Askalot plugin. There is nothing to configure: the
plugin connects to Askalot's one MCP address, `https://askalot.io/mcp`, and
authentication is an OAuth 2.1 browser sign-in on first use, not a pasted
token. You do not need to know which tenant holds your account; the sign-in
finds it.

## 1. The connection address

The plugin's address is fixed at `https://askalot.io/mcp`. The same address
works for every Askalot account, whether it is a free trial, a paying
customer, a university or a community organization.

### Security — verify where you sign in

The sign-in opens pages on `askalot.io` and on the platform's sign-in
service, `oidc.platform.askalot.io`. Enter your Askalot password only
there. If a browser window asking for it shows any other host, close it.
For a connector you add by hand (Claude Desktop, claude.ai), take the
address from official Askalot documentation (`https://docs.askalot.io`)
or direct askalot.io operator communication.

## 2. Sign in via OAuth on first use

The first time Claude Code calls an Askalot MCP tool after install,
the server answers 401 with an OAuth discovery hint and Claude Code
opens your browser to Askalot's sign-in:

```
askalot.io/authorize → platform-OIDC sign-in → you sign in → your tenant
issues tokens back to Claude Code
```

What happens, step by step:

1. Claude Code calls (for example) `mcp__plugin_askalot_askalot__list_projects`.
2. `askalot.io` responds with `401 Unauthorized` and a `WWW-Authenticate`
   header pointing at its OAuth metadata.
3. Claude Code reads that metadata and opens your default browser to
   `https://askalot.io/authorize`. There is no registration step.
4. The browser lands on the usual Askalot sign-in page
   (`oidc.platform.askalot.io`): you enter your email and then sign in
   the way you do on the web. Only if your email has an account on more
   than one Askalot tenant are you asked which one to use. Above the
   form the page names the application asking to connect and the
   address your sign-in sends access to; for Claude Code that address
   is on your own machine (`localhost`). There is no separate consent
   screen: signing in is the approval, so stop if the application or
   address is not what you expect.
5. The browser passes through your tenant and then back to a local
   Claude Code callback URL with an authorization code.
6. Claude Code exchanges the code for an access token + refresh
   token at `https://askalot.io/token` and stores both.

The plugin then retries the original tool call with the new bearer
token in the `Authorization` header. From here on, the refresh token
is exchanged transparently when the access token expires, and every
call is served by the tenant you signed in to.

You see the browser handshake once, and again only after the sign-in
has ended (section 5). A connection made before Askalot moved to the
single address needs one new sign-in.

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
you between organizations inside one tenant. To work on another tenant your
email has an account on, end the sign-in (section 5) and sign in again,
choosing that tenant.

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
- **`invalid_redirect_uri` in the browser:** the callback address the
  client used is not one its client metadata document lists. Reinstalling
  changes nothing, since there is no registration: end the sign-in
  (section 5), restart Claude Code and connect again. If it persists,
  the client's metadata document is out of date; report it.
- **Sign-in succeeds, then `user_not_in_tenant`:** the connection was
  made at one tenant's own address rather than the single one. Connect to
  `https://askalot.io/mcp` instead; its sign-in finds the tenant that holds
  your account.
- **Tool calls hang or refuse to connect:** check that `askalot.io` is
  reachable from your network.
