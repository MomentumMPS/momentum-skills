# Skills

Reusable agent skills for coordination, development, requirements, ticket creation,
review, and work reporting. Codex is the primary installation and documented
experience; Claude Code and Cursor can use the same shared collection. Maintained in
[pfonsecamoncada/Skills](https://github.com/pfonsecamoncada/Skills).
Skills maintained in
[Momentum Standard Skills](https://github.com/MomentumMPS/standards-momentum-skills)
belong there and are excluded here. Third-party skills are included only when
one of these custom skills depends on them.

## Collection

| Skill | Ownership | Purpose |
| --- | --- | --- |
| [coordinator](skills/coordinator) | Custom | Coordinate the overall outcome across specialist skills and bounded agents. |
| [project-manager](skills/project-manager) | Custom | Recover pending work and maintain private continuity for the current user. |
| [skill-improver](skills/skill-improver) | Custom | Review and improve skill intent, strategy, and instructions. |
| [mad-senior](skills/mad-senior) | Custom | Review consequential non-code decisions and evidence. |
| [development-orchestrator](skills/development-orchestrator) | Custom | Coordinate skills, reviews, approvals, and delivery. |
| [development-supporter](skills/development-supporter) | Custom | Resolve Jira work through code, branch setup, or a no-code outcome. |
| [jira-ticket-supporter](skills/jira-ticket-supporter) | Custom | Draft and create Jira tickets with reusable templates and verified context. |
| [requirement-collector](skills/requirement-collector) | Custom | Consolidate requirements and prepare approved ticket drafts. |
| [progress-summary](skills/progress-summary) | Custom | Write a weekly spoken leadership update from work evidence. |
| [slack-message-drafter](skills/slack-message-drafter) | Custom | Draft Slack messages using the current user’s evidenced voice. |
| [work-detective](skills/work-detective) | Custom | Reconstruct work across connected sources with supporting evidence. |
| [ponytail](skills/ponytail) | Third-party dependency | Apply the smallest complete implementation in development workflows. |
| [ponytail-review](skills/ponytail-review) | Third-party dependency | Review proposals and results for the development workflows. |
| [find-skills](skills/find-skills) | Third-party dependency | Discover missing capabilities for development-orchestrator. |
| [skill-creator](skills/skill-creator) | Third-party dependency | Author and validate capabilities when Coordinator needs them. |
| [openai-docs](skills/openai-docs) | Third-party dependency | Verify Codex configuration and client guidance for capability creation. |

Everything lives directly under `skills/<skill-name>/`. Supporting files stay
with their skill. There are no product-specific copies or category directories.
[SOURCES.md](SOURCES.md) records origins, dependencies, exclusions, and packaging
changes. [AGENTS.md](AGENTS.md) defines mandatory maintenance policies, with
privacy first. [CLAUDE.md](CLAUDE.md) imports that same policy for Claude Code.
Common workflows stay in SKILL.md; substantial host-specific details live
alongside them in host references. There is one source for each skill.

## Download and install

1. [Download the ZIP](https://github.com/pfonsecamoncada/Skills/archive/refs/heads/main.zip)
   from the reviewed `main` branch, or download a specific tag/commit archive
   when you need a fixed version. Extract it anywhere convenient.
2. Open a terminal in the extracted folder and run:

   ```sh
   python3 install.py
   ```

   On native Windows, use `py -3 install.py`. Python 3 is the only installer
   prerequisite. Git, administrator access and symlink permissions are not needed.
3. Start a fresh Codex session in any project. After successful installation,
   you can delete the downloaded ZIP and extracted folder.

Installation is **global for the current operating-system user**, across local
projects. It copies the complete skill folders and required dependencies into
Codex's user-level discovery location. Installed files do not depend on the
location of the download, and editing them does not edit this repository.
Use `python3 install.py --dry-run` to preview destinations without writing.

### Optional hosts

Codex is the default. Select other hosts explicitly:

| Command | Destination | Documentation |
| --- | --- | --- |
| `python3 install.py` | `~/.agents/skills/` | [Codex skill locations](https://learn.chatgpt.com/docs/build-skills) |
| `python3 install.py --host claude` | `~/.claude/skills/` | [Claude Code personal skills](https://code.claude.com/docs/en/skills) |
| `python3 install.py --host cursor` | `~/.agents/skills/` | [Cursor skill locations](https://cursor.com/help/customization/skills) |
| `python3 install.py --host all` | Both distinct roots above | Same discovery rules |

On Windows, replace `python3` with `py -3`; `~` means your Windows user profile.
For WSL, run the Linux command inside the WSL account. Codex and Cursor share
one destination. Selecting Claude as well creates an independent installed copy
for that host, while this repository maintains one shared collection. Unselected
host roots are left untouched. No custom directory tree or permanent checkout
is required on recipients' machines.

### Existing installations and updates

The installer never replaces existing content. Identical installed folders are
accepted on reruns. A different folder, an existing symlink (including one from
the old installer), or an obstructing path stops installation before copying.
Generated caches and private runtime files are excluded from distribution.

For an update, download the new ZIP and run with `--dry-run` first. If it reports
conflicts, compare those folders and move the affected installations to a backup
**outside all skill discovery roots**, preserving local customizations. Rerun the
installer after resolving the conflicts. There is no automatic overwrite,
update service or background synchronization.

For an old symlink installation, preserve the link's source and any edits, then
remove only the confirmed link before installing a copy. Do not delete its
source checkout as part of migration. Check older roots such as
`~/.codex/skills/`, `~/.cursor/skills/` and enabled plugins for duplicate skills;
the installer does not remove unrelated installations.

Keep private runtime state outside installed skills. For an older
`jira-ticket-supporter` with `references/project-memory.json`, preserve it under
`$XDG_STATE_HOME/jira-ticket-supporter/project-memory.json`, or
`~/.local/state/jira-ticket-supporter/project-memory.json` when unset, before
retiring the old installation. Reconcile existing state instead of overwriting it.

If a disk or permission error occurs after installation begins, read the reported
path before retrying. Completed copies remain installed; a partial destination
is preserved for inspection rather than overwritten. Resolve it as a conflict.

To uninstall, back up local edits and remove only the skill folders installed
from this collection in your selected destination. Keep unrelated skills and
private state. This repository does not install a background process or service.

### Verify and use

Start a fresh session in a selected client from an unrelated project and ask it
to list available skills. The collection has eleven custom skills and five
required dependencies. For example: "Use requirement-collector to organize these
requirements." Codex also supports `$skill-name`; Claude Code and Cursor support
`/skill-name`. Host tools and permissions remain specific to the selected client.

The installer provides skills, not service access. Install and authenticate
prerequisites only when a selected workflow needs them: `acli` for Jira, Git and
`gh` for repository delivery, Node.js/npm for skill discovery, and appropriate
connectors or authorized local tools for research. Skill validation uses Python
with PyYAML; OpenAI Docs helpers use Node.js and network access. No executables,
credentials, accounts or whole vendor plugins are bundled.

Identity, audience, accounts and timezone come from the current user's context.
No maintainer work contacts, private reporting preferences or professional
context belongs in the collection. `SKILL.md` is the common entrypoint;
`agents/openai.yaml` is optional Codex metadata. Installing locally does not
install into cloud agents, remote machines or other operating-system accounts.

## Maintaining the collection

Back up separately maintained installed skills by comparing their active sources
and sanitizing repository copies only. Review the full proposed content and diff
before publishing. Preserve installed originals and private state, and do not
copy entire installation or plugin-cache directories into this repository.

Before merging an update, run:

```sh
python3 -m unittest -v test_install.py
python3 -m unittest discover -s skills/work-detective/scripts -p 'test_*.py'
git diff --check
```

Tests use temporary directories. Also verify the inventory, dependency closure,
frontmatter, local references, provenance and privacy of the publication. Test
installation from an archive and confirm it still works after removing the
extracted source. Native Windows execution must be reported separately from
portable-code or simulated-filesystem tests. Per-skill license scope is recorded
in [SOURCES.md](SOURCES.md).
