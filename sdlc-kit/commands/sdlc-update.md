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
| `.github/hooks/sdlc-close-out.sh` (both CLIs: the close-out evidence checker, from 0.20.0) | kit | same rule; compared against `templates/close-out.template.sh`, which it copies verbatim — it takes no project values, unlike its two `.sh` neighbors |
| `.github/hooks/sdlc-close-out.json` (Copilot: the checker's stop-time backstop wiring, offered from 0.22.0 — present only where accepted) | kit | same rule; compared against `templates/close-out-hook.template.json`, verbatim like its `.sh` sibling. Presence encodes the owner's accept; the update never adds or removes it — the 0.22.0 note below offers it where the choice was never put |
| `CLAUDE.md`, `spec/*.md`, `.claude/settings.json`, `.github/hooks/*.json` other than `sdlc-close-out.json`, `.github/hooks/sdlc-gate.sh`, `.github/hooks/sdlc-tdd-guard.sh`, `.github/hooks/sdlc-tdd-guard.py` | project | never overwritten — they hold the gate baseline, the project's own gate commands, the TDD-guard patterns, owner decisions, backlog, gotchas |
| `.github/copilot-instructions.md`, `AGENTS.md` | project | never written, never overwritten, never removed. Setup does not create either (`reference/COPILOT.md`); if one is present, a project put it there |

**Which of those rows apply here is recorded, not guessed:** `spec/PROJECT_INDEX.md`
names the project's agent CLI (`Claude Code` / `Copilot CLI` / `both`). A project on
both holds the seven commands twice — once user-typed under `.claude/commands/`, once
packaged under `.github/skills/` — and both copies update.

## How to use

`/sdlc-update` — update to the latest release. `/sdlc-update v0.4.0` — a specific one.

Paths written `reference/…` in this command read from step 2's clone of the kit
(`/tmp/kit/sdlc-kit/reference/…`), never from the project — an adopted repo need not
hold the kit folder, and only `REVIEW_LENSES.md` is installed from that directory.

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
  such line — infer it from what the repo holds (`.claude/settings.json` vs the
  Copilot gate pair `.github/hooks/sdlc-gate.*`; the directory alone proves nothing
  from 0.20.0, when the both-CLIs `sdlc-close-out.sh` moves in), state the
  inference to the owner, and have them confirm it; the
  update writes the line as part of landing, so the next update reads rather than infers.
  When the line is present, glance at the same evidence anyway: a recorded CLI the
  repo's own artifacts contradict (a `Copilot CLI` line beside no `.github/`
  install, a `Claude Code` line beside no `.claude/`) is a finding for the owner
  before anything is copied, never a value to proceed on — every later step trusts
  this line.
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
                        .github/skills .github/agents \
                        .github/hooks/sdlc-close-out.sh \
                        .github/hooks/sdlc-close-out.json); do
  have=""
  case "$f" in
    .github/hooks/sdlc-close-out.sh)
      base=sdlc-close-out.sh
      # one of the two kit-owned files in .github/hooks/ — copied verbatim, no
      # project values. Their neighbors are project-owned and deliberately NOT in
      # the pathspec above: this loop must never classify the gate or guard scripts.
      want=$(awk '$2 == "templates/close-out.template.sh" {print $1}' "$MAN") ;;
    .github/hooks/sdlc-close-out.json)
      base=sdlc-close-out.json
      # the other kit-owned file: the stop-time backstop's Copilot wiring, present
      # only where the 0.22.0 offer was accepted (git ls-files skips it otherwise).
      want=$(awk '$2 == "templates/close-out-hook.template.json" {print $1}' "$MAN") ;;
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

Three checks on the check — required, because each failure mode produces a plausible
result rather than an error:

- **Denominator.** The loop must print exactly as many lines as
  `git ls-files .claude/commands .claude/skills .claude/agents .github/skills
  .github/agents .github/hooks/sdlc-close-out.sh .github/hooks/sdlc-close-out.json
  | wc -l` — the same pathspec list
  the loop walks, so the two cannot
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

### 4. Present the plan — the main owner halt

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
  destinations follow the per-CLI table in `sdlc-setup.md` New mode step 5 — **plus
  step 6's kit-owned artifacts, `templates/close-out.template.sh` →
  `.github/hooks/sdlc-close-out.sh` (both CLIs, verbatim) and, where the backstop
  offer was accepted, `templates/close-out-hook.template.json` →
  `.github/hooks/sdlc-close-out.json` (Copilot, verbatim), which live outside the
  step-5 table because they install beside the hooks** — the
  *Agent CLI:* line says which column applies, and "both" gets both columns. Claude
  Code column: `sdlc-kit/commands/` into `.claude/commands/`. Copilot column: each
  command re-packaged into `.github/skills/<name>/SKILL.md` by that step's packaging
  rule — **keeping the existing frontmatter block**, since the owner may have edited
  its `description`, and replacing only the body below it — and
  `templates/explore.agent.template.md` copied over `.github/agents/explore.agent.md`.
  On either CLI: `sdlc-kit/reference/REVIEW_LENSES.md` into `.claude/commands/`, and
  each `sdlc-kit/skills/<name>/` directory into `.claude/skills/<name>/`, copied whole
  so `tdd/tdd-references/` travels with it — the eight `SKILL.md` files share a
  basename, so copy directories, not files. The gate hook is project-owned and is not touched;
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
  Code project loses nothing**: `pr-review-toolkit` stays installed where it is and
  stays usable as
  an optional deepening at phase end, it simply stops being required, so no one needs
  to uninstall anything. If the project's onboarding docs tell new developers to
  install that plugin, that instruction is now optional — flag it, but do not edit
  project-owned docs.
- **0.14.0 adds two more kit-written skills, and one of them changes the slice loop:
  `change-simplify/` and `change-verify/`.** Both arrive by the new-files clause, but
  the owner needs the process change stated, not the filenames. `/end-slice` gains a
  **new step 3**, an optional post-green quality pass, which renumbers every step after
  it — review became step 4 (the 0.14.0 commit/hand-back numbers were 6 and 8; 0.15.0
  renumbers again — next bullet). `/end-phase` step 2 now
  names `change-verify` for the phase-level verification it previously described only
  as "smoke test, end-to-end run, manual script" (0.15.0 adds a slice-close naming
  too — next bullet). Two things to say plainly: the
  quality-pass step is **optional but never silent**, so the hand-back gains a line
  either way; and on Claude Code these do **not** replace the `verify` and `simplify`
  built-ins, which remain available — the kit ships its own so the passes exist on
  Copilot too, and running both over the same range is waste, not rigour.
  A project whose own notes cite `/end-slice` step numbers will be stale after this
  update. Flag that; do not edit project-owned docs to fix it.
- **0.15.0 changes the slice loop again, and prescribes two record formats.**
  `/end-slice` gains a **new step 6** — slice verification via `change-verify`,
  optional but never silent, same contract as the quality pass — renumbering commit to
  7, PROJECT_INDEX to 8, hand-back to 9. The TDD loop's RED becomes evidence-bearing:
  the failing run is observed and recorded as it happens, and the slice commit body
  now carries the `RED:` lines and a `verify:` outcome line. The Kit friction log gets
  one prescribed entry shape (`- <date> — <friction> — open`, flipped by the retro to
  `absorbed by retro <date>`). The catch to state at the halt: those rules live in the
  target's `templates/SDLC.template.md`, `templates/TESTING.template.md`, and
  `templates/PROJECT_INDEX.template.md`, which an update never re-instantiates — so
  the project's `spec/SDLC.md` and `spec/TESTING.md` still describe the old loop, and
  `spec/SDLC.md` **wins over the commands by its own first paragraph**. Until the
  owner folds the template diff into their spec files, the updated commands and the
  project's process file disagree, in the direction that disables the new steps. Hand
  the owner the diff of the three templates between the two versions; do not edit
  project-owned files. Step-number citations in project notes go stale again — flag,
  do not fix.
- **0.16.0 changes BOTH edit-time hook recipes, and both are project-owned — so this
  update delivers neither.** Two changes affect every adopted project on either CLI.
  (a) The hooks now carry **two JSON-parser dialects, python and node, and detect which
  is available at run time**; previously they hard-coded `python`, which was an
  undocumented dependency and simply failed on a machine without it. (b) They pipe the
  parser's output through `tr -d '\r'`, because Windows python writes CRLF and a stray
  carriage return falsifies the hook's own string comparisons — invisible under Git Bash,
  which strips it, and fatal under WSL bash, which does not. On the **Claude Code** side
  there is a third: the hook used to `exit 0` silently whenever it could not find the
  edited file's path, so a broken hook was indistinguishable from a clean edit; it now
  reports on stderr and exits 2, matching the Copilot dialect. Hand the owner the diff of
  `templates/settings.template.json` and/or `templates/copilot-hook.template.json` against
  the values their instantiated hook carries, and let them re-apply. Do not rewrite either
  file. **Re-run the hook-environment probe while you are here** (`reference/GATE_RECIPES.md`,
  *The hook environment*) and compare it against what `spec/SDLC.md` recorded at setup: a
  machine that has gained WSL, or lost the JSON parser the hook picks at run time, moves
  that answer, and nothing else in the process ever looks again. Where it has moved, that
  is a finding for the halt — not a line to update silently.
- **0.16.0 fixes a defect in the Copilot gate hook that this update cannot deliver.**
  On Copilot CLI the write tool is `apply_patch`, and its `toolArgs` is raw patch text
  rather than the JSON every other tool sends. The hook body through 0.15.0 JSON-parsed
  it unconditionally, so on the only write tool that actually fires it fell to its
  "could not find the file" branch **on every edit** and never once ran lint or
  typecheck. On a Copilot project, `.github/hooks/sdlc-gate.json` is where to look: the
  symptom is the hook reporting on every edit that it did not run. Read it with the
  owner rather than assuming its state — it is project-owned, this command never
  classified it, and it may have been hand-patched, replaced, or never installed.
  0.16.0's `templates/copilot-hook.template.json` is the fix to compare against —
  though a project crossing 0.18.0 in the same update should skip straight to that
  release's restructured pair (its note below) rather than re-applying 0.16.0's
  single-JSON body only to replace it again.
  The instantiated `.github/hooks/sdlc-gate.json` is **project-owned** — it holds this
  project's own lint and typecheck commands — so an update must not rewrite it. Hand the
  owner the diff between the two template versions and the values their current hook
  carries, and let them re-instantiate. State the consequence plainly at the halt: until
  they do, the hook stays broken, and this is one of the few defects an update cannot
  fix for them. Claude Code projects are unaffected.
- **0.16.0 adds the optional TDD-ordering guards, Copilot CLI only — and every update
  from here on checks whether this project was ever offered them.** Two hook files
  (`.github/hooks/sdlc-tdd-guard.sh` and `.json`) that deny a production write outside
  TDD's two licenses (an observed fresh red since the last test edit, or a declared
  behavior-preserving refactor edit behind a counted green) and refuse a stop from a
  coding session while no counted green has been observed or the latest observed run
  is red. They are
  **not** part of the automatic new-files clause: they are project-owned, optional, and
  carry this project's own test patterns, so nothing is installed without the owner's
  word. Decide from two pieces of evidence, in this order:
  1. **Does this project run Copilot CLI?** The *Agent CLI:* line in
     `spec/PROJECT_INDEX.md` says so (`Copilot CLI` or `both`) — the same line step 1
     already reads. A Claude-Code-only project gets
     no offer and no mention — the guards do not exist for it, and saying otherwise
     describes a backstop it cannot have.
  2. **Is `.github/hooks/sdlc-tdd-guard.sh` present?** If yes, nothing to do: it is
     project-owned and this update leaves it alone. If no, read the TDD-guard line in
     `spec/SDLC.md` — the one `/sdlc-setup` writes whether the guards were taken *or*
     declined:
     - **It records a decline** → the owner already decided. One sentence in the report,
       then move on; do not re-open a settled question at every update.
     - **There is no such line at all** → this project predates the offer, or setup
       never made it. **Offer the guards now, as a first setup would.** This is the case
       the re-offer exists for, and it is invisible unless you look: the guards being
       absent looks identical either way from the filesystem, which is why the decision
       is recorded in prose rather than inferred from the tree.
     - **The line says "installed" but the files are gone** → do not re-offer as though
       nothing happened. Report the contradiction: the record and the repository
       disagree, and only the owner knows which is right (a removal on purpose, or a
       file lost in a merge). This is the reconcile step — you are holding the record
       and its artifact at the same instant, and comparing them is the whole point of
       having both.
  **Reconcile the other direction too, in the "nothing to do" case above**: when the
  guard files *are* present, still read the line. Present-but-recorded-as-declined is
  the same contradiction pointing the other way, and the branch that skips reading the
  record is exactly the branch that can never notice. Where the line claims **deny mode**,
  say plainly that the flag file deciding it (`.git/sdlc-tdd/deny-enabled`) is inside
  `.git` and therefore per-clone — the line describes the machine that wrote it, not
  this checkout.
  Taking them up means following `sdlc-setup.md` step 6 in full — test patterns derived
  and confirmed, the logging-mode ramp, and the proof step — none of it skippable
  because this is an update rather than a first setup. A guard armed before the log
  shows it recognising the project's own test runs blocks every production write in the
  repo. Record the outcome, **including a decline**, in `spec/SDLC.md` the way setup
  does, so the next update can still tell the two apart. Say which CLI they cover, too:
  a project running both CLIs gets the backstop on the Copilot side only.
- **0.17.0 adds six process rules whose canonical statements live in the templates —
  so this update delivers the commands that point at them, not the rules themselves.**
  Halt 4's acceptance surface now includes the run's log, read against the recorded
  logging conventions; a review finding that contradicts a **ratified spec decision**
  is CRITICAL, named a spec conflict, and takes halt 3 instead of the backlog; a
  coverage floor is **proven to fire** when first established or inherited; the
  whole-arc review gains *the unconsumed artifact* lens (that file updates by
  classification, so the lens itself arrives); the retro cites catches only with
  their disposition attached and sweeps every artifact the spec files name against
  the tree. The catch to state at the halt, same shape as 0.15.0's: the updated
  commands point at sections of `spec/SDLC.md` — halt 3's spec-conflict sentence,
  *Coverage floor*'s prove-it-fires rule, halt 4's log sentence — **that the
  project's un-re-instantiated copy does not yet carry**, and `spec/SDLC.md` wins
  over the commands by its own first paragraph. Hand the owner the template diff of
  `SDLC.template.md` (and `PROJECT_INDEX.template.md`'s phase-block comment) between
  the two versions; do not edit project-owned files. 0.17.0 also widens the
  slice-review lens triggers and requires a backlog entry's cause to be reproduced
  **in the environment it was observed in** — those arrive with the commands and need
  no spec change.
- **0.18.0 adds the optional skill-activation ledger, both CLIs — and every update from
  here on checks whether this project was ever offered it.** A logging-only hook
  appending one line per tool-dispatched skill activation to
  `.git/sdlc-skill-ledger.jsonl`, read by
  `/sdlc-retro`'s step-evidence sweep (*The skill-activation ledger* in
  `reference/GATE_RECIPES.md` is the recipe). It is **not** part of the automatic
  new-files clause: hooks are project-owned and nothing is installed without the
  owner's word. Same two-state check as the TDD guards, but with no CLI gate — the
  ledger exists for both: is the ledger artifact present (`.github/hooks/
  sdlc-skill-ledger.json` on Copilot, the `"Skill"`-matcher block in
  `.claude/settings.json` on Claude Code — check the artifact for the CLI the *Agent
  CLI:* line records)? If yes, leave the artifact alone — **but still read the
  skill-ledger line in `spec/SDLC.md`**: present-but-recorded-as-declined is a
  contradiction only that read can notice, and the branch that skips reading the
  record is exactly the branch that can never notice. If no, read the same line: a recorded decline is a settled decision that gets one sentence; no
  line at all is a project that never had the choice — offer it now, as a first setup
  would, with the proof step (invoke a skill, read the last ledger line back)
  non-skippable because this is an update. Record the outcome, including a decline
  with its date, the way setup does. Present-but-recorded-as-declined, or a line
  claiming installed with the artifact gone, is a contradiction to report, not to
  silently fix.
  **0.18.0 also fixes the TDD-guard hook config for machines where the CLI's hook
  shell is the WSL launcher** — the old config's prelude was silently corrupted on
  that route and the guards never ran there. Both guard files are project-owned, so
  a project that has them gets this only by hand: `.github/hooks/sdlc-tdd-guard.json`
  is a verbatim template copy — replacing it with the 0.18.0 template inherits the
  offline proof — and `sdlc-tdd-guard.sh` carries the project's patterns, so its
  change (the root-defaulting block at the top, per the changelog) is applied as a
  template diff, the way the G1 fix was in 0.16.1. State the consequence at the halt:
  until both land, the guards may be silently inert in some launch environments even
  though the log looked healthy from others.
  **And 0.18.0 restructures the Copilot gate hook the same way, for the same
  boundary** — `.github/hooks/sdlc-gate.json` becomes a bare launcher (verbatim
  template copy, no values, only `timeoutSec` ever edited) and the logic moves to a
  new project-owned `.github/hooks/sdlc-gate.sh`, instantiated from
  `templates/copilot-hook.template.sh` with the project's existing hook values — the
  source glob, the lint command, and the typecheck block, read out of the current
  `sdlc-gate.json` before replacing it, per the changelog. On the affected machines the old single-JSON hook reported a **false**
  "no JSON parser" on every edit; a project that has been seeing that message gets
  its explanation and its fix in the same motion. Hand-apply both files, then re-run
  the proof step (a deliberate lint error must produce hook feedback), in a session
  launched the way this project's operator actually launches the CLI — the hook shell
  is per-launcher, and the proof certifies only the route it ran on. Re-run the
  hook-environment probe here too: the 0.16.0 note's probe instruction is standing at
  every hook-touching crossing, not a one-release step, and this restructure exists
  because the probe's answer is per-launcher.
- **0.19.0 and 0.19.1 change hook-script behavior, and every change arrives by hand —
  the files are project-owned.** 0.19.0 carries four TDD-guard fixes in
  `sdlc-tdd-guard.sh`, each named in the CHANGELOG with its reason: the declared
  refactor license (G1's second license — without it, armed close-out passes force
  synthetic test-edit/red cycles), the spoken refusal (an uncounted run says so
  in-context instead of only logging), the single-`&` separator fix (a single-`&`
  compound could record a false observation), and G2's session scoping (a session
  with no production write and no test edit stops clean). 0.19.1 adds three more,
  one per hook: `sdlc-tdd-guard.sh` speaks counted RED/GREEN observations as state
  facts; `sdlc-gate.sh` marks truncated output so clipped lint feedback cannot read
  as complete; and — Claude Code — `.claude/settings.json`'s gate hook frames its
  lint failure (hook named, file named, expectation stated) instead of emitting raw
  linter output. Apply each as a template diff against the project's instantiated
  copy, the way the G1 fix was in 0.16.1; the `.json` launchers are unchanged
  throughout. State at the halt which of these are still pending — a guard note
  describing 0.19.x semantics over a script still running 0.18.0 behavior
  misdescribes the project in the direction that hides fixes.
- **0.20.0 adds the close-out evidence checker, and the file arrives automatically
  but its wiring does not.** `.github/hooks/sdlc-close-out.sh` is kit-owned and
  verbatim (the classification table above), so the new-files clause delivers it —
  but three things live in project-owned files and arrive only by hand. (a)
  `spec/SDLC.md` needs the close-out checker note beside the gate: the proven
  invocation per installed CLI, each form actually run against a real commit before
  being recorded. On Claude Code that is `sh .github/hooks/sdlc-close-out.sh check`;
  on Copilot CLI the shell tool on Windows resolves no `sh` (measured 2026-08-10 —
  and its PATH's `bash` is WSL's, the corrupting route), so there the working form
  derives sh from
  the git on its PATH (`bin\sh.exe` beside `git.exe`'s `cmd` directory) and the note
  carries that literal proven path; a non-Windows Copilot project measures its own
  answer. Prove it the way setup does: run it against a
  pre-record commit and watch it fail INCOMPLETE naming all four keys. (b) The
  slice loop in `spec/SDLC.md` gains the verify-the-record step after the commit
  step and the `RED:` zero-form (`RED: none — no behavior batches this slice`) in
  the commit step's record contract — hand the owner the template diff, do not edit
  the spec. (c) `/end-slice` renumbers again: PROJECT_INDEX 8→9, hand-back 9→10.
  Project notes citing those numbers go stale — flag, do not fix. Until (a) and (b)
  land, the updated command names a checker invocation and a record form the
  project's process file does not know — the same disagreement direction as the
  0.15.0 note, and the same resolution: the spec wins until the owner folds the
  diff.
- **0.21.0 adds the Claude Code TDD-guard dialect, and it retires the 0.16.0 CLI
  gate: the guard offer is now per-CLI, per dialect.** The new artifacts — a
  project-owned `.github/hooks/sdlc-tdd-guard.py` (instantiated from
  `templates/tdd-guard-claude.template.py` with the same three patterns as the sh
  dialect) plus four hook blocks in `.claude/settings.json` (PreToolUse
  `Edit|Write`; PostToolUse and PostToolUseFailure `Bash|PowerShell`; Stop) — are
  **not** part of the automatic new-files clause, for the same reason as ever:
  project-owned, optional, patterned. Run the 0.16.0 two-state check per CLI the
  project runs, with one 0.21.0-specific reading: a `spec/SDLC.md` guard line that
  says the guards are *Copilot-CLI-only and this project does not run that CLI* was
  setup's pre-0.21.0 statement about the kit, **not an owner decline** — that
  project never had the choice, so offer the Claude dialect now, as a first setup
  would (instantiate, keep or add the settings blocks, logging mode, fail-first
  proof in a Claude Code session). On acceptance the four settings blocks arrive by
  hand — `.claude/settings.json` is project-owned and the update never edits it.
  0.21.0 also rewords the guard deny message and the guard note (the refactor
  license names the case, not "close-out") — hand-applied as template diffs per the
  CHANGELOG, alongside its other hand-apply notes (the skill-ledger scope sentence,
  the coverage-floor procedure text).
- **0.22.0 adds the close-out checker's stop-time backstop, as an offer.** The
  checker script itself updates automatically (kit-owned; its new `stop-check`
  mode arrives with the file), but the *wiring* is optional and per-CLI:
  `.github/hooks/sdlc-close-out.json` on Copilot (kit-owned verbatim, present only
  where accepted), a `Stop` block in `.claude/settings.json` on Claude Code
  (project-owned, arrives by hand, and its `"shell": "bash"` key is load-bearing —
  measured 2026-08-13). Read the backstop half of the close-out checker note
  line in `spec/SDLC.md` with the 0.16.0 two-state rule: a recorded decline is
  settled; a line that predates 0.22.0 says nothing about the backstop, so put the
  choice now as setup would (logging mode, never create
  `.git/sdlc-close-out/deny-enabled`, fire-first proof per `sdlc-setup.md` step 6,
  outcome recorded in that same note line). Its bare-commit class is log-only by
  design on every install — say so when offering. Reconcile both directions, as the
  guard check does: a note saying installed beside no artifact, or the artifact
  present beside a recorded decline, is a contradiction to report — and on Copilot
  the artifact whose presence encodes the accept is
  `.github/hooks/sdlc-close-out.json`.
- **0.23.0 adds the product contract, and the artifact arrives only by hand — it is
  project-owned.** A new spec file, `spec/PRODUCT_CONTRACT.md` (from
  `templates/PRODUCT_CONTRACT.template.md`, placeholder-free, seeds empty), holds
  the current-truth statement of owner-ratified externally observable behavior —
  the file `/plan-phase`'s new preserved-contract sweep and `/end-phase`'s new
  per-item acceptance verdicts, preserved-contract check, and contract reconcile
  all read or write. Those commands arrive by classification, but they point at
  this file and at `spec/SDLC.md` sections (*Product contract*; the phase-start,
  halt-4, arc-review, and bookkeeping additions; the slice-loop trigger line) that
  the project's un-re-instantiated spec does not yet carry — the 0.15.0
  disagreement direction, same resolution: the spec wins until the owner folds the
  template diff. Create the file by copying the template as-is, hand the owner the
  `SDLC.template.md` diff, and say plainly: **the contract starts empty on
  purpose** — the one-time backfill over prior phases' ratified decisions is
  offered at the next `/end-phase`, owner-confirmed there, never inferred at
  update time.
- **Touch nothing project-owned** (the table above). The kit cannot regenerate those
  files and must not try.
- **Two further owner decisions can arise inside this step**, and both are real halts
  even though step 4 carries the main one: an un-manifested file in a kept `sdlc-kit/`
  folder (below), and the TDD-guard re-offer above. Neither is decided on the owner's
  behalf.
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
  value the owner confirmed at step 1. On a project whose `spec/SDLC.md` has no *Kit
  home repository:* line (adopted before the placeholder existed), write it with the
  URL this update cloned the target kit from at step 2 — the same fact, observed in
  this session. When the line **is** present, compare it against step 2's clone URL:
  this is the one moment the record and its artifact are held at the same instant, and
  a mismatch goes to the owner as a finding — never a silent rewrite — because the
  recorded URL is where `/sdlc-retro` will submit.
  **These lines are the only project-owned content an update may write** —
  and the latter two only when absent, never to overwrite an answer already recorded —
  **with one stated exception**: the artifacts an accepted re-offer installs (the
  TDD-guard pair; the ledger's Copilot JSON, or its `"Skill"` block merged into the
  existing `.claude/settings.json` the way setup's Existing mode merges hooks), each
  written only on the owner's word at that halt, following setup's own step.
  Do them last, so an aborted update never claims a version it does not hold.
  **Two more lines join them only when this update actually put an offer to the
  owner** — the TDD-guard offer and the skill-ledger offer (step 5's re-offer clauses)
  — then their answer is recorded in
  `spec/SDLC.md` the way setup records it, decline included. Each is written only when
  its offer was made and answered in this session, never inferred and never rewritten:
  an update that did not ask does not get to record an answer. Without it a decline
  leaves no trace and every later update re-asks a settled question, which is the whole
  reason the lines exist.
- Land as a normal PR (`chore/update-sdlc-kit-X.Y.Z`).
  Report to the owner what changed *behaviorally* (from the changelog), not just which
  files moved.
- Claim only what was checked. "Nothing project-owned touched" may be said when the
  final diff was read against the ownership table — not asserted from the manifest,
  which structurally cannot see files it never listed. An unverified reassurance is
  worse than silence, because it stops the reader looking.

## Notes

- Changelog entries marked *[adoption-only]* changed templates or the non-installed
  reference docs, read only at `/sdlc-setup` time; they affect new adoptions, not this
  project (`reference/REVIEW_LENSES.md` is installed and its changes are
  *[installable]*; on a Copilot project so is `templates/explore.agent.template.md`,
  copied verbatim to `.github/agents/`; from 0.20.0 so is
  `templates/close-out.template.sh`, copied verbatim to
  `.github/hooks/sdlc-close-out.sh` on both CLIs; and from 0.22.0, on a Copilot
  project that accepted the backstop, so is `templates/close-out-hook.template.json`,
  copied verbatim to `.github/hooks/sdlc-close-out.json`). If one fixes
  something the project cares about, raise it with the owner as a manual follow-up —
  never apply it automatically.
- Skipping several versions is fine: classify against the version the project is on,
  copy from the target, read the changelog for everything in between.
