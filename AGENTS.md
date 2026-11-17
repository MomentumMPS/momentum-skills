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

When title tools are available, apply this title convention without asking:

- Begin with exactly one status: `[OPEN]` for work that can continue,
  `[WAITING]` for a verified dependency, `[PAUSED]` only for an explicit user
  deferral, or `[DONE]` only when the requested endpoint is verified complete.
- Follow with `KEY-123: Short faithful topic` for one real ticket, or
  `[2 TICKETS][KEY-123 & KEY-456]: Shared topic` for several. Preserve all ticket
  numbers, using an unambiguous shared prefix if space is tight.
- Otherwise use `[NO-TICKET] Subject — Specific task`. Incidental ticket mentions
  do not turn general discovery, audits or administration into ticket work.
- Keep the subject stable, describe the requested outcome and last verified
  state, and include a short verified dependency in every `[WAITING]` title.
  Reassess on start/resume, scope or dependency changes, explicit pause and
  before ending. A finished turn, age or archive state is not completion.
- Rename only the current chat unless a bounded batch is explicitly requested.
  Inspect requests and outcomes before classifying history; preserve unresolved
  titles rather than guessing. Verify saved titles are not truncated. Renaming
  never authorizes messaging, resuming or monitoring other chats.
- For authorized batches, preserve archive/project placement and record old
  and new titles. Use explicit reporting dates for dated recaps. Reopen a done
  title when more work is requested, and replace NO-TICKET when a specific
  ticket becomes the actual scope; never infer ownership from a mention.

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
