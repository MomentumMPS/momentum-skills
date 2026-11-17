# Repository instructions

## Required policy: privacy first

These policies are mandatory for every improvement, backup, synchronization,
review, installation change and publication in this repository. Apply them before
editing and again to the complete proposed tree and diff before delivery. They
are not optional recommendations. Within project policy, privacy takes priority
over convenience, fidelity to installed sources and publication speed.

- Never add the maintainer's personal information, professionally sensitive
  information, work contacts or identifiable real work evidence to repository
  files, examples, tests, metadata, commit messages or pull request content.
  This includes names of colleagues, private organizations/accounts, internal
  project details, private tracker links and identifiers, contact details,
  approval records, personal preferences, credentials, runtime memory and
  machine-specific paths. Keep private tracker identifiers out of public branch
  names and commit/PR metadata too; refer to the work by its reusable outcome.
- Check Git author and committer metadata before publication. Do not expose a
  private or work email: use the verified account's public noreply identity for
  that commit and read back both fields. Preserve accurate attribution and the
  user's global Git configuration; never invent an account or contact address.
- Resolve identity, audience, accounts, team conventions and timezone from the
  current user's authorized context at execution time. Use fictional examples.
  Public upstream source links and legally required third-party notices are
  provenance; preserve them without importing private profile information.
- Sanitize repository copies only. Do not strip personal context from installed
  originals, migrate their private state or replace installations without an
  explicit request covering that action.
- Review all publishable text and supporting resources, including scripts,
  fixtures, assets and UI metadata. Pattern scans supplement content review;
  they cannot establish the absence of sensitive information by themselves.
  Fix violations before committing or publishing. If a required check cannot
  be completed, keep the affected delivery pending and state the limitation.

## Required policy: preserve explicit requirements

Apply the current user's explicit project requirements on every task. When a
new durable rule is supplied, record it here during that task, reconcile any
contradictory older wording and apply it to the actual changes. Do not defer
recording or enforcement as optional follow-up work. Recover prior decisions
from their requests, corrections and outcomes when history is in scope; titles
and earlier assistant claims alone are not proof of acceptance.

The newest explicit user instruction supersedes an older conflicting one.
Rejected attempts are not accepted implementations or validation evidence.
Preserve independent verified requirements, but reassess the implementation
against the current request. Never revive the superseded Codex-only scope:
this collection is Codex-first, with shared workflows and optional compatible
hosts. These repository instructions remain subject to higher-priority host
instructions and do not claim technical enforcement over every AI system.

## Scope and ownership

This repository backs up the maintainer's custom skills that are not maintained
in `MomentumMPS/standards-momentum-skills`. Compare that repository's actual
inventory before adding or moving a skill; do not classify solely by its name.
Do not duplicate its audit/audit-authoring skills here; verify the live inventory
rather than relying on a fixed count.

Include a third-party skill only when a retained custom skill requires it,
including a conditional workflow dependency. Record the consuming skill,
upstream source, known revision, license, and local modifications in SOURCES.md.
Follow dependencies transitively. Generic optional host capabilities (browser,
document, or spreadsheet support) do not justify copying entire vendor plugins.
Do not treat local installation as evidence of the maintainer's authorship.

External executables and services are prerequisites, not vendored skills.
Document required tools (such as Git, gh, acli, Python, and Node.js) and guide
their installation only when the selected workflow needs them. Do not bundle
binaries, package caches, credentials, or an entire plugin for one skill.
Suggest optional capabilities when relevant rather than installing them all.

## Layout

- Keep one flat `skills/<skill-name>/` collection for custom skills and required
  third-party dependencies. Mark ownership in the README and SOURCES tables.
- Keep each SKILL.md and its necessary references, scripts, assets, and optional
  agent metadata together. Preserve folder names used by dependency links.
- Keep repository documentation and the installer at the root. Add directories
  only for a real resource need; no per-product copies, category trees, generated
  bundles, or duplicated installation guides.
- Back up real files, not links into one machine's installed skill directories.
- Use AGENTS.md as the canonical repository policy. A small CLAUDE.md imports
  it for Claude Code; do not maintain a second, diverging policy copy.
- Keep common workflows in SKILL.md. Put substantial host-specific details in
  the skill's own `references/hosts/` only when needed, with Codex first.

## Installation and portability

Document and support global user-level installation only, across projects.
Use home-relative or resolved paths, never one person's concrete home path.
Codex is the default installation target, using `~/.agents/skills`. Claude Code
is an explicit option using `~/.claude/skills`; Cursor can use the shared
`~/.agents/skills` root. Distribute a downloadable archive and copy complete
skill folders into selected discovery roots. Recipients must be able to delete
the extracted download after installation; do not require a permanent checkout,
symlinks, Git or administrator permissions for installation. Keep one maintained
repository collection; selected hosts with different discovery roots receive
independent installed copies, while shared roots are installed only once.
Verify official documentation before changing product discovery guidance.
Do not silently overwrite or remove existing installations, and do not change
unselected host roots. Test installation only in temporary user directories.
Accept identical reruns and report conflicting folders or legacy links before
writing. Preserve customizations during explicit update/migration steps and keep
backups outside discovery roots. Exclude caches, private state and source links
from distribution. Verify installed resources after deleting the source archive
and extracted folder; report native-platform testing limits honestly.

Keep required skills as siblings. Resolve supporting resources relative to the
skill's real directory. Allow standalone dependency names as well as a plugin
namespace when applicable. Do not assume a tool, connector, account, or plugin
exists in every agent product. Preserve invocation policies and workflow gates.

## Backups and changes

Read installed skills as source artifacts when backing them up; copying a
workflow does not activate it or authorize its Jira, messaging, or deployment
actions. Prefer the active, user-selected version when copies differ. Preserve
installed originals unless the user requests installation or migration.

Publish reusable workflows without the maintainer's personal information or
private defaults. Resolve identity, accounts, audience, timezone, and team
preferences from the current user's context. Keep private runtime memory, account
identifiers, credentials, approval records, and real work evidence out of this
public repository. Use fictional examples and user-state directories outside
the checkout for mutable memory. Apply sanitization only to repository copies;
never remove personal data from the maintainer's installed originals. Record
packaging and portability changes in SOURCES.md.

Do not apply a blanket license to third-party or unlicensed skills. Preserve
existing notices and obtain actual provenance rather than inventing authorship,
versions, or permission. Add only dependencies required by the retained skills.

Before delivery, verify the skill inventory, dependency closure, frontmatter,
local references, absence of private state, and `git diff --check`. Run installer
tests when installation behavior changes. Test in temporary directories, never
by replacing the user's installed skills. Report actual validation limits.

Keep README.md and SOURCES.md aligned with the final collection. Publish to the
personal original repository through a feature branch and pull request targeting
its `main` branch when authorized. Never publish implementation directly to
`main`, merge without authorization, or target the organization fork by mistake.
The organization repository remains a separately synchronized fork; syncing it
is a separate action and is not automatic. Historical approvals do not approve
new merges or publications.

## Conversation titles

Apply this permanent preference whenever title tools are available, without asking for confirmation. For ticket work, the leading label reflects the ticket's last verified tracker status, not the chat's progress or the agent's runtime state. This replaces the former OPEN/WAITING/PAUSED chat-state convention.

- Use `[TODO]`, `[IN-PROGRESS]`, `[ON-HOLD]`, `[REVIEW/QA]`, `[DONE]`, or `[CANCELED]` for ticket work. Normalize the actual workflow status using its evidenced meaning: queued/not started, active work, explicitly on hold, review or QA, completed, or canceled respectively. Preserve the distinction between completed and canceled; a generic closed category alone does not establish which applies.
- Use `[STATUS] KEY-123: Short faithful topic` for one identified work ticket. Derive the key and topic from the real ticket or trusted context; never invent keys or infer ownership from incidental mentions. Verify status through the ticket owner workflow or explicit current user-provided status. If status or its mapping is unknown, retain the existing title and report the uncertainty rather than guessing; `[NO-TICKET]` is not an unknown-status fallback.
- For work without a specific ticket, use `[NO-TICKET] Subject — Specific task` with no additional status prefix. General discovery, reporting, audits and administration can remain NO-TICKET despite incidental ticket mentions. Replace this form when a specific ticket becomes the actual scope.
- A finished assistant turn, delivered PR, user pause, pending approval, resumed chat, or additional request does not itself change the ticket-status label. Update it only when the underlying status is verified to have changed. Renaming does not authorize a tracker transition. Track unfinished chat commitments and dependencies in the response or handoff even when the ticket label is `[DONE]` or `[CANCELED]`.
- Keep one ticket per session unless explicitly approved otherwise. For approved multi-ticket work or read-only reporting, retain every key and the ticket count. If all statuses agree, use `[STATUS] [2 TICKETS][KEY-123 & KEY-456]: Shared topic`. If statuses differ, show each verified status beside its key, for example `[TODO] KEY-123 & [REVIEW/QA] KEY-456: Topic (2 tickets)`; do not invent one aggregate status. Multi-ticket formatting never authorizes additional ticket work.
- Keep the ticket/subject core stable and distinctive words early. Use a short purpose or verified dependency suffix only when useful. Use explicit reporting dates for dated recaps. Respect the title tool's saved-length limit and verify the saved title for truncation. Shorten wording first; use unambiguous shared-prefix key compression where statuses remain clear, without silently dropping keys, statuses or the ticket count.
- Reassess on start/resume, a scope change, newly verified ticket status, and before ending. Reuse reliable status evidence; inspect the tracker through its owner workflow when a refresh is needed. Titles, age, archive state and earlier assistant claims alone do not prove current status. A title is a last-known state, not background monitoring.
- Rename only the current chat by default. An explicit request to update other chats authorizes that bounded batch; inspect each chat and its ticket evidence, preserve archive/project placement, record old and new titles, and verify saved titles. Do not message or resume other chats merely to enforce titles.

## Skill use and ownership

The primary agent loads Coordinator as the default entry point before
substantial work, unless the user opts out or selects another workflow. Small
requests remain small. Delegated agents retain their assigned roles and do not
restart Coordinator. If a required skill is unavailable, report that limitation
and continue independent authorized work; do not invent its instructions.

When using a skill, begin each user-facing commentary and final message with
one bold label on its own line: `**[SKILL NAME · PURPOSE]**`. Use uppercase names,
spaces instead of hyphens in names, omit plugin prefixes, and name the skill
performing the reported work. Use Coordinator for combined results. Explain
meaningful role changes and distinguish skill switches from separate agents.
Do not add labels to published artifacts or tool calls without a request.

Load the installed `jira-ticket-supporter` before every Jira operation or acli
invocation. Only that owner may prepare, execute and verify authorized Jira
mutations, including when another skill requested the outcome. Other skills
hand over facts, target, requested delta, constraints and existing authorization;
they never bypass the owner with APIs, scripts, browser actions, connectors or
Smart Commits. Merely loading its instructions does not make another workflow
the writer. A same-agent explicit switch to its full workflow is allowed.
Other acli products remain read-only. Missing owner access leaves Jira work
pending and does not authorize a fallback writer.

## Jira authentication

Follow the current host's sandbox and approval rules. If a sandbox prevents
access to the authenticated CLI session or network, retry in an authorized
execution context before asking for login. All Jira write authorization
requirements still apply.

## Shared critical-action gates

Apply these conventions across skills and delegated agents, subject to higher-priority host instructions. They supersede older conflicting workflow defaults, without adding routine approval stages.

- Use a human GATE before a consequential action when an important judgment or authorization remains unresolved: destructive or hard-to-reverse changes to valuable data, production releases or changes with material outage/data risk, significant access/security/privacy changes, substantial spending or external commitments, or a business-policy choice with material consequences. Judge the actual target, impact, reversibility and uncertainty; an ordinary local edit or routine authorized update does not become critical merely because a tool can write.
- Complete the authorized investigation, preparation and safe validation first. Present one concrete decision: the proposed action and exact target/environment, material impact and tradeoffs, relevant verification, recovery limits, and the approval needed. Explain why the gate applies. Do not perform the gated action while preparing it; continue independent authorized work.
- Reuse explicit human approval that covers the same action, target, scope and material risks, including an adequately specific instruction in the current conversation. A broad goal such as “fix it,” a reviewer verdict, tool availability, sandbox approval or agent recommendation is not human approval of an uncovered critical decision. If the proposed scope or risk changes materially, obtain approval of that change. Silence and elapsed time never count as approval.
- Keep approvals attached to their scope in session context and handoffs; do not require an extra approval document. Combine related decisions when they are ready for review. Do not ask again for unchanged approved work or gate routine reads, reversible local preparation, tests, or already authorized low-impact actions. Preserve any explicit user hold or narrower approval condition.

## Tool-selection fallback and context economy

Honor an explicit user tool choice, a tool prescribed by the active skill, or an already established suitable tool for the operation. Do not replace a clear authorized tool route merely to prefer a CLI. When no such route is established, use this strict fallback order, both while executing tasks and when designing skills:

1. **CLI tools and lightweight skills first.** Check an available local CLI (for example `gh`, `aws`, `psql`, `curl`) or a lightweight script-based skill/plugin that can perform the operation.
2. **Scoped MCP servers.** If no suitable CLI or lightweight skill exists, use a narrowly scoped MCP server configured for the task.
3. **Built-in connectors and app-backed plugins.** Use these when neither preceding option can handle the operation.
4. **Chrome Codex extension.** When no suitable programmatic interface exists, use the extension if supported by the current host, targeting specific selectors instead of full-page dumps.
5. **Computer Use, last resort.** Use it only when the earlier programmatic and browser-extension routes have failed or are unsupported for the target application.

Suitability includes the operation's capabilities, authorized access, required fidelity and active host constraints. Use known capability evidence to skip unsupported routes; do not exhaustively probe every tier or install tools, change authentication, copy credentials, or broaden access merely to force an earlier tier. Preserve specialist ownership, approval rules and the user's control of their active browser/profile; a fallback is not new authority. Higher-priority mandatory tools still apply.

Regardless of route, request only necessary fields, dates and records. Filter large outputs at the source or with `jq`, `rg`/`grep`, `head`, or `--limit`; load focused excerpts and reuse verified results. Use limits for discovery, then paginate or fetch the required detail when completeness matters. Never present a truncated sample as complete evidence or suppress failures to save tokens.

## One ticket per session

- Default to one work ticket per Codex chat or Claude session. Keep implementation, ticket-specific investigation, drafting and mutations focused on that ticket; delegated agents inherit the same boundary. Completing it does not silently authorize picking up another ticket in the same session.
- Working on multiple tickets in the same session requires explicit user approval. A clear request to handle a named or bounded set of tickets is that approval; do not ask for it twice. An explicit instruction to switch tickets authorizes that switch, not continued work on both. Record the approved exception and its scope in session context and handoffs, and keep each ticket's outcome distinct. Merely listing tickets, spotting a dependency or receiving a worker recommendation is not an exception.
- Related-ticket reads needed to understand the primary ticket, incidental references, historical reporting and cross-ticket discovery/triage may remain read-only without opening a second ticket workflow. Do not use those exceptions to implement, draft changes for, or mutate additional tickets. A necessary follow-up ticket is additional ticket work and needs the same explicit exception.
- If a second ticket needs work without that approval, finish independent work on the current ticket and present the concrete choice: authorize the additional scope here or use a separate session. Prepare a brief handoff from existing facts when useful; do not begin the second ticket's work or create/resume another user-owned chat without an explicit request. Multi-ticket title conventions describe approved scope or read-only reporting; they do not authorize execution.
