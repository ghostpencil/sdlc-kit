# SDLC Update

Bring this project's kit-owned files forward to a newer kit release without destroying
anything the project has recorded. Every installed file is classified against the
manifest of the version the project is **on**: files that provably match are safe to
overwrite, files that differ are the owner's call, and project-owned files are never
touched. Process reference: the ownership split below; the kit's home repository README
(*Updating an adopted project*) states this same procedure for humans — if this command
and that section disagree, the kit has a bug; trust the manifest math and report it.

Prime directive: **never overwrite what is not provably unmodified, and never touch what
the project owns.**

| Path in this project | Owner | Update behavior |
|---|---|---|
| `.claude/commands/*.md` (from the kit's `commands/` and `reference/REVIEW_LENSES.md` — and from `skills/` too on kits ≤ 0.13.0) | kit | overwrite when provably unmodified; owner decides when drifted |
| `.claude/skills/*/SKILL.md` (+ `tdd/tdd-references/`, from the kit's `skills/`; this mapping starts at 0.14.0) | kit | same rule; on a project coming from ≤ 0.13.0 these are *new* files and their `.claude/commands/` originals are *removed* |
| `.claude/agents/*.md` (from kits 0.6.0–0.9.0; the `agents/` mapping was retired in 0.10.0) | kit | classified for the transition — removed when provably unmodified; owner decides when drifted |
| `.github/skills/*/SKILL.md` (Copilot: the kit commands, packaged) | kit | same rule, but compared with the frontmatter block stripped — see step 3 |
| `.github/agents/explore.agent.md` (Copilot: the read-only sweep profile) | kit | same rule; compared against `templates/explore.agent.template.md`, which it copies verbatim |
| `CLAUDE.md`, `spec/*.md`, `.claude/settings.json`, `.github/hooks/*.json` | project | never overwritten — they hold the gate baseline, the project's own gate commands, owner decisions, backlog, gotchas |
| `.github/copilot-instructions.md`, `AGENTS.md` | project | never written, never overwritten, never removed. Setup does not create either (`reference/COPILOT.md`); if one is present, a project put it there |

**Which of those rows apply here is recorded, not guessed:** `spec/PROJECT_INDEX.md`
names the project's agent CLI (`Claude Code` / `Copilot CLI` / `both`). A project on
both holds the seven commands twice — once user-typed under `.claude/commands/`, once
packaged under `.github/skills/` — and both copies update.

## How to use

`/sdlc-update` — update to the latest release. `/sdlc-update v0.4.0` — a specific one.

**When to run it: at a phase/arc boundary, never with an arc in flight.** An update
mid-arc changes the rules governing slices already scoped, and which kit version
governed which slice becomes unreconstructable afterward. If a mid-arc update is truly
unavoidable, record the version change against the affected slices in
`spec/PROJECT_INDEX.md` before continuing.

## Workflow

### 1. Establish both versions

- Read the project's version from `spec/SDLC.md` (*Kit version: X.Y.Z*). Do not guess
  and do not assume the newest: classification runs against the manifest of the version
  the project is *on*, which is what makes "unmodified" provable rather than hopeful.
- Read the project's agent CLI from `spec/PROJECT_INDEX.md` (*Agent CLI:*). It decides
  which directories step 3 enumerates. Absent — projects adopted before 0.14.0 have no
  such line — infer it from what the repo holds (`.claude/settings.json` vs
  `.github/hooks/`), state the inference to the owner, and have them confirm it; the
  update writes the line as part of landing, so the next update reads rather than infers.
- The target is the argument, or the newest release tag.
- No stamp, or a stamp reading `unknown (pre-0.2.0)` → the project predates manifests.
  Clone the kit repo (step 2) and follow the *No version stamp* section of its root
  `README.md` to establish the version once, then continue here — after this update the
  project is stamped and never needs that section again.

### 2. Get both versions of the kit

```bash
git clone https://github.com/ghostpencil/sdlc-kit /tmp/kit      # holds the target
git -C /tmp/kit worktree add /tmp/kit-old vX.Y.Z                # the version you are on
```

### 3. Classify every installed file

Compare everything under `.claude/commands/`, `.claude/skills/`, and `.claude/agents/`
against the **old** version's manifest. Hash committed content (`git cat-file -p :path`), never the working
tree — an unpinned checkout on Windows holds CRLF and would report every file as
drifted, uniformly and plausibly wrong.

```bash
cd <project root>
MAN=/tmp/kit-old/sdlc-kit/MANIFEST.sha256

for f in $(git ls-files .claude/commands .claude/skills .claude/agents \
                        .github/skills .github/agents); do
  have=""
  case "$f" in
    .claude/commands/*)
      base=${f#.claude/commands/}
      # commands/ and reference/REVIEW_LENSES.md install here. So did skills/ on kits
      # <= 0.13.0 — keep that prefix: it is what classifies a project still on one of
      # those versions, and dropping it would report every vendored skill UNKNOWN.
      want=$(awk -v b="$base" \
        '$2 == "commands/" b || $2 == "skills/" b || $2 == "reference/" b {print $1}' "$MAN") ;;
    .claude/skills/*)
      base=${f#.claude/skills/}
      # skills/ installs one directory per skill here from 0.14.0 on; base already
      # carries the directory (tdd/SKILL.md, tdd/tdd-references/tests.md).
      want=$(awk -v b="$base" '$2 == "skills/" b {print $1}' "$MAN") ;;
    .claude/agents/*)
      base=${f#.claude/agents/}
      # agents/ installed into .claude/agents/ on kits 0.6.0–0.9.0; the mapping was
      # retired in 0.10.0, so these classify here for the removal clause in step 5.
      # (Against a pre-0.6.0 manifest they classify UNKNOWN — the denominator check
      # still counts them.)
      want=$(awk -v b="$base" '$2 == "agents/" b {print $1}' "$MAN") ;;
    .github/skills/*/SKILL.md)
      # Copilot packaging: a frontmatter block, one blank line, then the kit command
      # verbatim. Strip that block and the file must hash to commands/<name>.md — which
      # is why setup specifies the shape exactly and inserts nothing else.
      base=${f#.github/skills/}; base=${base%/SKILL.md}
      want=$(awk -v b="commands/$base.md" '$2 == b {print $1}' "$MAN")
      have=$(git cat-file -p ":$f" | awk \
        'NR==1 && $0=="---" {fm=1; next} fm && $0=="---" {fm=0; blank=1; next}
         fm {next} blank && $0=="" {blank=0; next} {blank=0; print}' |
        sha256sum | cut -d' ' -f1)
      base="$base (packaged skill)" ;;
    .github/agents/explore.agent.md)
      base=explore.agent.md
      # copied verbatim from the template — it carries no placeholders to resolve.
      want=$(awk '$2 == "templates/explore.agent.template.md" {print $1}' "$MAN") ;;
    *) base=$f; want="" ;;
  esac
  [ -n "$have" ] || have=$(git cat-file -p ":$f" | sha256sum | cut -d' ' -f1)
  if   [ -z "$want" ];        then echo "UNKNOWN   $base"
  elif [ "$want" = "$have" ]; then echo "UNCHANGED $base"
  else                             echo "DRIFTED   $base"
  fi
done
```

Two checks on the check — required, because both failure modes produce a plausible
result rather than an error:

- **Denominator.** The loop must print exactly as many lines as
  `git ls-files .claude/commands .claude/skills .claude/agents .github/skills
  .github/agents | wc -l` — the same directory list the loop walks, so the two cannot
  drift apart. Fewer means the matching dropped files (`tdd-references/` lives two
  directories down and is the usual casualty). On a Copilot project the count includes
  files under `.github/` that a Claude-only project does not have, and on a "both"
  project the seven commands are counted twice, once per copy; a count that looks too
  high is the recorded CLI telling the truth, not an error.
- **Never probe for a path with `git cat-file … | sha256sum`.** A pipeline reports the
  *last* command's status, so a missing path hashes empty input and silently matches
  the wrong thing. Look paths up in the manifest, as above.
- **The frontmatter strip fails safe, and that is the point.** If it breaks, it yields
  the hash of nothing, which matches no manifest entry, so the file classifies
  `DRIFTED` and reaches the owner. A strip that silently *succeeded* on the wrong bytes
  would report a modified command as untouched — so if every packaged skill classifies
  `DRIFTED` at once, suspect the strip before suspecting seven simultaneous edits.

### 4. Present the plan — the ONE owner halt

Before writing anything, show the owner the full classification plus the changelog
entries marked *[installable]* for every version being skipped. Open with a
plain-English executive summary in bullets — current version, target, what changes
behaviorally — and put every per-file `DRIFTED` call to the owner **numbered and
explicitly marked** (`Decision 1: <file> — keep / overwrite / merge`), each with its
diff as detail below; the classification table follows the summary, never replaces it.

Report **content-changed counts separately from touched counts**: how many files the
update will rewrite with genuinely different committed content, versus how many it
merely touches (line-ending or whitespace churn, byte-identical replacements). "5
changed, 19 touched" keeps the reader looking at the 5; a flat "24 modified" is two
dozen known-meaningless entries hiding the one that matters — which is exactly how a
486-line deletion once went unread inside an update commit. Then:

- `UNCHANGED` → provably untouched since adoption; will be overwritten with the target
  version. No per-file question.
- `DRIFTED` → someone edited it, often deliberately — `spec/SDLC.md` explicitly invites
  fixing a command that disagrees with it. Show the diff against both versions; the
  owner decides per file (keep / overwrite / merge). **Never auto-overwrite a drifted
  file.**
- `UNKNOWN` → not from the kit. Left alone, no question asked.

### 5. Apply

- Copy the target version's files over the `UNCHANGED` set and whatever `DRIFTED` files
  the owner released — plus any files **new in the target's install set**, which
  classification never saw because the project does not hold them yet. Sources and
  destinations: `sdlc-kit/commands/` and `sdlc-kit/reference/REVIEW_LENSES.md` into
  `.claude/commands/`; each `sdlc-kit/skills/<name>/` directory into
  `.claude/skills/<name>/`, copied whole so `tdd/tdd-references/` travels with it. The
  eight `SKILL.md` files share a basename — copy directories, not files. On a Copilot
  project, additionally re-package each command into `.github/skills/<name>/SKILL.md`
  by the rule in `sdlc-setup.md` New mode step 5 — **keeping the existing frontmatter
  block**, since the owner may have edited its `description`, and replacing only the
  body below it — and copy `templates/explore.agent.template.md` over
  `.github/agents/explore.agent.md`. The gate hook is project-owned and is not touched;
  if the target changes the hook recipe, that is a changelog entry for the owner to
  apply by hand, exactly as on the Claude side.
- The symmetric case: files **removed from the target's install set** — listed in the
  old version's manifest under an install mapping but absent from the target's. An
  `UNCHANGED` one is provably the kit's and is deleted; a `DRIFTED` one goes to the
  owner (keep it by moving it to a project-owned path outside the kit-managed
  directories, or delete it) — the owner may have invested in the drift. Step 6's
  re-classification confirms the removal: the file is gone, or it is an owner-kept
  copy living outside the kit-managed directories. First instance:
  `agents/sdlc-surveyor.md` and its whole `agents/` → `.claude/agents/` mapping,
  retired in 0.10.0.
- **The 0.14.0 skills move is the second instance, and it is a removal and a re-add of
  the same content.** A project coming from ≤ 0.13.0 holds the five vendored skills at
  `.claude/commands/<name>.md`; the target installs them at
  `.claude/skills/<name>/SKILL.md`. Both halves run: the old paths leave by the removal
  clause above (`UNCHANGED` → deleted; `DRIFTED` → the owner's call, and a drifted
  vendored skill is worth keeping deliberately — see `reference/SKILLS.md` on
  divergence), and the new paths arrive as files new in the target's install set. Say
  this to the owner as one move rather than as a column of unrelated deletions and
  additions, and check
  afterwards that no skill is left at **both** paths — two copies of `tdd` with
  different content is the one outcome this step must not produce.
- **0.14.0 also adds a skill the process now requires: `diff-review/`.** It arrives by
  the new-files clause like any other addition, but say what it means rather than
  listing it: `/end-slice` step 4 and `/end-phase` step 5 previously named
  `pr-review-toolkit`, a per-machine Claude Code plugin, and now name this skill, which
  travels with the repo and runs on both CLIs. Two consequences for the owner, both
  worth stating at the halt. **A Copilot project gains a per-slice review it never
  had** — the commands used to name a reviewer that did not exist there. **A Claude
  Code project loses nothing**: `pr-review-toolkit` stays installed and stays usable as
  an optional deepening at phase end, it simply stops being required, so no one needs
  to uninstall anything. If the project's onboarding docs tell new developers to
  install that plugin, that instruction is now optional — flag it, but do not edit
  project-owned docs.
- **0.14.0 adds two more kit-written skills, and one of them changes the slice loop:
  `change-simplify/` and `change-verify/`.** Both arrive by the new-files clause, but
  the owner needs the process change stated, not the filenames. `/end-slice` gains a
  **new step 3**, an optional post-green quality pass, which renumbers every step after
  it — review is now step 4, commit step 6, hand-back step 8. `/end-phase` step 2 now
  names `change-verify` for the phase-level verification it previously described only
  as "smoke test, end-to-end run, manual script". Two things to say plainly: the
  quality-pass step is **optional but never silent**, so the hand-back gains a line
  either way; and on Claude Code these do **not** replace the `verify` and `simplify`
  built-ins, which remain available — the kit ships its own so the passes exist on
  Copilot too, and running both over the same range is waste, not rigour.
  A project whose own notes cite `/end-slice` step numbers will be stale after this
  update. Flag that; do not edit project-owned docs to fix it.
- **Touch nothing project-owned** (the table above). The kit cannot regenerate those
  files and must not try.
- If the project kept a `sdlc-kit/` folder from adoption, replace it with the target
  version's bundle — but **enumerate the actual directory contents first** and compare
  them against the old version's manifest. Anything present that the manifest does not
  list is not the kit's to delete: a project put it there (the kit's own field-report
  convention invites exactly that). Report the comparison **with its counts** — N files
  on disk, M in the manifest — so a sweep that enumerated nothing is visibly wrong
  rather than silently clean; then, for every un-manifested file, HALT — a numbered,
  explicitly marked decision per file: the owner
  moves it to a project-owned path (`spec/` is the usual home) or explicitly
  releases it. "It is a verbatim copy of the kit" is the *intended* state of that
  folder, not a fact the procedure may assume; a wholesale replace that never looked
  inside once destroyed a project's only local copy of two commits of authored work.

  Then replace **by copy-over-in-place — never by removing the directory**: delete only
  the *files* the old version's manifest lists (provably the kit's), then copy the
  target bundle over the directory.

  ```bash
  # $K = the target version's sdlc-kit/ folder (inside /tmp/kit)
  cut -d' ' -f3- /tmp/kit-old/sdlc-kit/MANIFEST.sha256 |
    while read -r f; do rm -f "sdlc-kit/$f"; done
  cp -r "$K"/. sdlc-kit/
  ```

  `rm -rf sdlc-kit && cp …` is the wrong shape twice over: on Windows the directory
  removal can fail `Device or resource busy` *after* unlinking every file — a real
  update was left with an empty, still-git-tracked tree exactly this way — and on
  every platform it opens a window in which the project holds no bundle at all if the
  copy then fails. Copy-over-in-place has neither failure mode.

### 6. Verify, re-stamp, land

- Re-run step 3 against the **target** version's manifest: every file just copied must
  now classify `UNCHANGED`, and the only `DRIFTED` entries are the files the owner chose
  to keep. The two runs disagreeing about the copied files (old manifest: changed;
  new: matching) is what proves the classifier discriminates — an all-clear it could
  not fail to produce proves nothing.
- Re-stamp `spec/SDLC.md` (*Kit version: X.Y.Z (updated <date>)*). On a project adopted
  before 0.14.0, also write the *Agent CLI:* line into `spec/PROJECT_INDEX.md` with the
  value the owner confirmed at step 1. **These two lines are the only project-owned
  content an update may write**, and the second only when it is absent — never to
  overwrite an answer already recorded. Do both last, so an aborted update never claims
  a version it does not hold.
- Land as a normal PR (`chore/update-sdlc-kit-X.Y.Z`), the same way the adoption landed.
  Report to the owner what changed *behaviorally* (from the changelog), not just which
  files moved.
- Claim only what was checked. "Nothing project-owned touched" may be said when the
  final diff was read against the ownership table — not asserted from the manifest,
  which structurally cannot see files it never listed. An unverified reassurance is
  worse than silence, because it stops the reader looking.

## Notes

- Changelog entries marked *[adoption-only]* changed templates or the non-installed
  reference docs, read only at `/sdlc-setup` time; they affect new adoptions, not this
  project (`reference/REVIEW_LENSES.md` is installed and its changes are *[installable]*). If one fixes
  something the project cares about, raise it with the owner as a manual follow-up —
  never apply it automatically.
- Skipping several versions is fine: classify against the version the project is on,
  copy from the target, read the changelog for everything in between.
