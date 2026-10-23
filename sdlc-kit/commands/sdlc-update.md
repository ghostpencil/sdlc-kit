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
| `.github/hooks/sdlc-close-out.sh` (both CLIs: the close-out evidence checker, from 0.20.0) | kit | same rule; compared against `templates/close-out.template.sh`, which it copies verbatim — one of the four kit-owned files in that directory; its other neighbors are project-owned |
| `.github/hooks/sdlc-impact.py` (both CLIs: the architecture-impact adapter, from 0.28.0) | kit | same rule; compared against `templates/sdlc-impact.template.py`, copied verbatim. Installed unconditionally and inert without an Understand Anything graph, so it is never offered or declined |
| `.github/hooks/sdlc-cosmetic.py` (both CLIs: the cosmetic-edit classifier, from 0.34.0) | kit | same rule; compared against `templates/sdlc-cosmetic.template.py`, copied verbatim. Installed unconditionally — it can only grant an exemption, so it is never offered or declined |
| `.github/hooks/sdlc-close-out.json` (Copilot: the checker's stop-time backstop wiring, offered from 0.22.0 — present only where accepted) | kit | same rule; compared against `templates/close-out-hook.template.json`, verbatim like its `.sh` sibling. Presence encodes the owner's accept; the update never adds or removes it — step 5's record-against-artifact bullet offers it where the choice was never put |
| `CLAUDE.md`, `README.md` (where setup instantiated it — from 0.25.0), `spec/*.md`, `.claude/settings.json`, `.github/hooks/*.json` other than `sdlc-close-out.json`, `.github/hooks/sdlc-gate.sh`, `.github/hooks/sdlc-gate-claude.sh`, `.github/hooks/sdlc-tdd-guard.sh`, `.github/hooks/sdlc-tdd-guard.py`, `.github/hooks/sdlc-skill-ledger.sh` | project | never overwritten — they hold the gate baseline, the project's own gate commands, the TDD-guard patterns, owner decisions, backlog, gotchas |
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

Compare every installed file — `.claude/commands/`, `.claude/skills/`, `.claude/agents/`,
`.github/skills/`, `.github/agents/` and the four kit-owned `.github/hooks/` files, as the
script below enumerates them — against the **old** version's manifest. Hash committed content (`git cat-file -p :path`), never the working
tree — an unpinned checkout on Windows holds CRLF and would report every file as
drifted, uniformly and plausibly wrong.

```bash
cd <project root>
MAN=/tmp/kit-old/sdlc-kit/MANIFEST.sha256

for f in $(git ls-files .claude/commands .claude/skills .claude/agents \
                        .github/skills .github/agents \
                        .github/hooks/sdlc-close-out.sh \
                        .github/hooks/sdlc-close-out.json \
                        .github/hooks/sdlc-impact.py \
                        .github/hooks/sdlc-cosmetic.py); do
  have=""
  case "$f" in
    .github/hooks/sdlc-close-out.sh)
      base=sdlc-close-out.sh
      # one of the FOUR kit-owned files in .github/hooks/ — copied verbatim, no
      # project values. Their neighbors are project-owned and deliberately NOT in
      # the pathspec above: this loop must never classify the gate, guard, or
      # ledger scripts.
      want=$(awk '$2 == "templates/close-out.template.sh" {print $1}' "$MAN") ;;
    .github/hooks/sdlc-close-out.json)
      base=sdlc-close-out.json
      # the second kit-owned file: the stop-time backstop's Copilot wiring, present
      # only where the 0.22.0 offer was accepted (git ls-files skips it otherwise).
      want=$(awk '$2 == "templates/close-out-hook.template.json" {print $1}' "$MAN") ;;
    .github/hooks/sdlc-impact.py)
      base=sdlc-impact.py
      # the third kit-owned file: the architecture-impact adapter (0.28.0), copied
      # verbatim on both CLIs. A project updating FROM a pre-0.28.0 kit has no such
      # file, so git ls-files skips it and the add happens at step 5 like any other
      # new install — this branch classifies it on every update after that.
      want=$(awk '$2 == "templates/sdlc-impact.template.py" {print $1}' "$MAN") ;;
    .github/hooks/sdlc-cosmetic.py)
      base=sdlc-cosmetic.py
      # the fourth: the cosmetic-edit classifier (0.34.0), verbatim on both CLIs;
      # absent before 0.34.0, so it is added at step 5 the first time, like the third.
      want=$(awk '$2 == "templates/sdlc-cosmetic.template.py" {print $1}' "$MAN") ;;
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
  .github/hooks/sdlc-impact.py .github/hooks/sdlc-cosmetic.py | wc -l` — the same
  pathspec list
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

**Then the friction this release may close — every live entry, not a filtered few.**
List each entry in `spec/PROJECT_INDEX.md` *Kit friction log* still `open` or absorbed
as `RULING OPEN`, and beside each the changelog entry in the update range that
addresses it, quoted, or `nothing in range`. Visit them all: the log has no field
naming the file an entry implicates, so a filter has nothing to match on, and an
entry's own words are the only evidence. The cost of skipping this is measured: an
adopter's update shipped the exact fix for two such entries, the guard applied it 84
times, and both stayed `RULING OPEN` for seven weeks because nothing asked. A
`RULING OPEN` entry with a match is proposed for closure at step 6, after the verify;
an `open` one is left for the next `/sdlc-retro`, whose carry-forward re-checks it
against the upstream artifact.

**Then the process-file rules an earlier update may have missed — every marker, from
the first.** `spec/SDLC.md` is project-owned, so a rule reaches it only by the owner
folding the template diff, and each update hands over only the diff from the
installed version forward. A rule missed at an earlier hop sits below every later
diff, and the spec, which wins over the commands, goes on stating the old rule. One
adopter's spec missed two releases' rules this way, each found by chance, and a
reading of three adopters' specs found six more. So for **every** row below whose
version is no newer than the target, whatever the installed version, run
`grep -cF -- '<marker>' spec/SDLC.md`, skipping a row the spec's *Records* already
answers (`Fold marker answered:`, below). List
each absent marker at this halt with its rule and the current template's text for
that rule, as a numbered decision (`Decision N: <version> <rule> — fold now / reworded
on purpose`). An absence is a question, not proof: a spec that wraps a line inside
the phrase, or tags it `(kit X.Y.Z)`, hides a rule it holds, so read the section
before you call it missing. A fold the owner takes goes into this update's spec
change. A "reworded on purpose" answer is recorded once in *Records*, after the
hook-script re-derive lines: `Fold marker answered: <version> "<marker>" — reworded
on purpose (<date>)`. Without that record the question would come back at every
update.

The markers are phrases from the current `SDLC.template.md`, one line each, and each
occurs there exactly once. Where a later release rewrote a rule, the marker follows the
rewrite. Several rows are rules the template gained with **no** fold instruction in
their release's note, which is how they were missed. A note dated before 0.32.0 is in
`reference/UPDATE_NOTES.md`, not in step 5. A release that changes a rule in
`SDLC.template.md` adds or moves its row here.

| Version | Rule | Marker |
|---|---|---|
| 0.15.0 | a RED is observed and recorded as it happens | `RED is observed, not assumed` |
| 0.15.0 | the slice verification step | `exercise the changed behavior through the path` |
| 0.15.0 | the friction log's one entry shape | `<friction> — open` |
| 0.17.0 | a finding against a ratified decision takes halt 3 | `is a spec conflict and takes this halt` |
| 0.17.0 | the coverage floor is proven to fire | `prove it fires — once` |
| 0.17.0 | the run's log is part of acceptance | `log output is part of the acceptance` |
| 0.20.0 | the record is verified after the commit | `Verify the record: run the close-out checker` |
| 0.20.0 | the `RED:` zero-form | `behavior batches writing the zero-form` |
| 0.23.0 | the product contract | `is the current-truth statement of owner-ratified` |
| 0.23.0 | the *Records* section | `The per-project record the close-outs run on` |
| 0.23.0 | closed items retire out of the index | `Closed items retire out of the index` |
| 0.26.0 | the index line budget | `budget of 25` |
| 0.27.0 | a friction line closes only with an outcome | `implemented in <commit>` |
| 0.27.0 | a retro's absorption does not close a gotcha | `absorption records that the finding was transmitted` |
| 0.27.0 | a check records its negative verdict | `check records its verdict whether or not` |
| 0.27.0 | a mutation is undone by inverting the edit | `inverting the edit that made it` |
| 0.27.0 | a backlog id is the next integer up | `integer above the file's current maximum` |
| 0.29.0 | a control row records its catch and reach | `flagged state arises in ordinary operation` |
| 0.29.0 | the baseline names its commit | `commit it was measured at` |
| 0.31.0 | `quality:` names its reuse search | `searched, not eyeballed` |
| 0.31.0 | `verify:` names what it did not exercise | `not exercised: <what could not be reached` |
| 0.32.0 | the docs-only slice | `A docs-only slice is declared here` |
| 0.32.0 | the verification's docs form | `the step runs in a narrower form` |
| 0.33.0 | the slice-end graph refresh | `Slice end — incremental` |
| 0.33.0 | a graph built inside the change set reads current | `one built on a sibling branch` |
| 0.34.0 | a cosmetic edit keeps a slice docs-only | `docs-only only on the cosmetic` |
| 0.35.0 | the graph refresh switch line | `Graph refresh: slice-end incremental` |
| 0.35.0 | the scripted mutation runner | `whole-file restore is a scripted runner's, byte-exact` |
| 0.35.0 | the approved libraries record | `### Approved libraries` |
| 0.35.0 | a draft PR for CI is not the phase PR | `PR opened only so CI runs` |
| 0.35.0 | a restored mutation is confirmed by a bare run | `restored and confirmed green by a` |
| 0.36.0 | the architecture graph record | `### Architecture graph` |
| 0.37.0 | the index carries no coverage-floor figure | `the index points here` |
| 0.37.0 | the quality pass's trimmed gate between moves | `run in full, once, after the last move` |
| 0.37.0 | the phase close stamps an unstamped baseline | `An unstamped gate baseline is stamped here` |

### 5. Apply

- Copy the target version's files over the `UNCHANGED` set and whatever `DRIFTED` files
  the owner released — plus any files **new in the target's install set**, which
  classification never saw because the project does not hold them yet. Sources and
  destinations follow the per-CLI table in `sdlc-setup.md` New mode step 5 — **plus
  step 6's kit-owned artifacts, `templates/close-out.template.sh` →
  `.github/hooks/sdlc-close-out.sh` (both CLIs, verbatim) and, where the backstop
  offer was accepted, `templates/close-out-hook.template.json` →
  `.github/hooks/sdlc-close-out.json` (Copilot, verbatim), and
  `templates/sdlc-impact.template.py` → `.github/hooks/sdlc-impact.py` (from 0.28.0)
  and `templates/sdlc-cosmetic.template.py` → `.github/hooks/sdlc-cosmetic.py` (from
  0.34.0), both CLIs, verbatim — all of which live outside the step-5 table because
  they install beside the hooks** — the
  *Agent CLI:* line says which column applies, and "both" gets both columns. Claude
  Code column: `sdlc-kit/commands/` into `.claude/commands/`. Copilot column: each
  command re-packaged into `.github/skills/<name>/SKILL.md` by that step's packaging
  rule — **keeping the existing frontmatter block**, since the owner may have edited
  its `description`, and replacing only the body below it — and
  `templates/explore.agent.template.md` copied over `.github/agents/explore.agent.md`.
  On either CLI: `sdlc-kit/reference/REVIEW_LENSES.md` into `.claude/commands/`, and
  each `sdlc-kit/skills/<name>/` directory into `.claude/skills/<name>/`, copied whole
  so `tdd/tdd-references/` travels with it — the `SKILL.md` files share a
  basename, so copy directories, not files. The gate hook is project-owned and is not
  copied over; a change to its template reaches it through the hook-script
  walk-through below, exactly as on the Claude side.
- The symmetric case: files **removed from the target's install set** — listed in the
  old version's manifest under an install mapping but absent from the target's. An
  `UNCHANGED` one is provably the kit's and is deleted; a `DRIFTED` one goes to the
  owner (keep it by moving it to a project-owned path outside the kit-managed
  directories, or delete it) — the owner may have invested in the drift. Step 6's
  re-classification confirms the removal: the file is gone, or it is an owner-kept
  copy living outside the kit-managed directories. First instance:
  `agents/sdlc-surveyor.md` and its whole `agents/` → `.claude/agents/` mapping,
  retired in 0.10.0. The 0.14.0 skills move was the second (`reference/UPDATE_NOTES.md`);
  0.37.0's removal of `tdd-guide/` is the third (its note below).
- **Crossing a version older than 0.32.0? Read `reference/UPDATE_NOTES.md` first.** The
  notes for 0.14.0 through 0.31.3 live there; they moved at 0.37.0. They are part of
  this step, read for every version the update crosses (from the target clone,
  `/tmp/kit/sdlc-kit/reference/UPDATE_NOTES.md`), and they carry what no classification
  can infer. A project already on 0.32.0 or later skips the file.
- **Every update: each optional hook's record against its artifact.** Three offers are
  recorded in `spec/SDLC.md` whether taken or declined, and every update reads each
  record beside its artifact, for each CLI the *Agent CLI:* line names. The TDD guards:
  `.github/hooks/sdlc-tdd-guard.sh` + `.json` on Copilot, `.github/hooks/sdlc-tdd-guard.py`
  plus its four `.claude/settings.json` blocks on Claude Code. The skill ledger:
  `.github/hooks/sdlc-skill-ledger.json` on Copilot, the `"Skill"` block on Claude Code.
  The close-out backstop: `.github/hooks/sdlc-close-out.json` on Copilot, the `Stop`
  block on Claude Code. Read both directions, because the branch that skips reading the
  record is the branch that can never notice:
  - **A recorded decline, no artifact** → settled. One sentence in the report; never
    re-open it.
  - **No record line at all** → the project never had the choice. Offer it now, as a
    first setup would: logging mode, setup's step 6 proof (non-skippable because this is
    an update), and the outcome recorded, a decline with its date.
  - **Record and artifact disagree** — installed with the artifact gone, or the artifact
    present beside a recorded decline → a contradiction to report. Only the owner knows
    which side is right; never silently fix either.
  - **They agree** → nothing to do. Where the record claims deny mode, say the flag
    file deciding it lives in the git directory, so it holds for this clone only.

  An accepted offer's `.claude/settings.json` blocks arrive by hand; the update never
  edits that file. The pre-0.32.0 notes add version readings: a guard line saying the
  guards are Copilot-only was setup's statement about the kit before 0.21.0, not a
  decline.
- **0.32.0 adds the docs-only slice, and its rule lives in `spec/SDLC.md`.** The
  updated `/next-slice` §4 lets a slice whose ratified test approach is `none` and which
  touches no source or test file skip the TDD loop, and `/end-slice` confirms that
  against the diff and runs `change-verify`'s new docs form (each command the diff adds
  is run, each path it adds is opened). The commands and the skill arrive with the
  update; the canonical statement is in `templates/SDLC.template.md` slice-loop steps 4
  and 9, which an update never re-instantiates. Until the owner folds that diff, the
  project's process file says every slice runs the loop and **wins** — the safe
  direction: the shortcut stays off. Hand the owner the template diff; never edit
  `spec/SDLC.md`. **The same release asks three setup-written records for their reach
  note** — the hook-environment line, the close-out checker note, and
  `spec/TESTING.md`'s harness record (*Records*: the catch named, and whether it has
  arisen on its own or only in the proof). Nothing re-proves; the owner adds what the
  proofs already saw when folding. The close-out checker is unchanged, so existing
  records stay valid.
- **0.33.0 refreshes the architecture graph at every slice end**, not only at the phase
  boundary. It matters only to a project carrying an Understand Anything graph; for any
  other project it is currency only. `/end-slice` gains the refresh as its last act, and
  the adapter (`.github/hooks/sdlc-impact.py`, kit-owned, replaced as usual) now reads a
  graph built **inside** the change set — between the base and HEAD — as current, which
  the phase-scope view needs once slices refresh it. The rule lives in
  `SDLC.template.md` *Architecture impact view*: hand the owner that diff to fold into
  `spec/SDLC.md`; until it is folded the project's process file names only the phase
  boundary and wins, so the slice-end refresh stays off. Where the graph directory is
  **tracked**, say so: each refresh then needs its own commit.
- **0.34.0 exempts comment- and layout-only source edits from the TDD guard, and lets
  them keep a slice docs-only.** One new kit-owned file, `.github/hooks/sdlc-cosmetic.py`,
  copied verbatim and installed unconditionally like the impact adapter: it can only
  grant, so every failure it has — no python, no `typescript`/JDK/.NET SDK for that
  language, a parse error, a timeout — is today's rule. Two halves of the change live in
  **project-owned** files, so the update replaces neither: the guard scripts
  (`.github/hooks/sdlc-tdd-guard.py` / `.sh`) consult the classifier only once their
  bodies are re-derived from the 0.34.0 templates with the project's three resolved
  patterns carried over — offer that at the hook-script walk-through below, and
  say a guard left as it is keeps today's rule exactly. The docs-only rule lives in
  `SDLC.template.md` step 4 of the slice loop: hand the owner that diff to fold into
  `spec/SDLC.md`; until it is folded the project's process file says a source comment
  voids a docs-only slice, and wins. Name in one line which of the project's languages
  have their toolchain on your shell's PATH (a claim — the guard log is the
  measurement); install nothing for it. A re-derived guard changes the guard note
  (`spec/SDLC.md` *Records*): it now consults the classifier, and the note says so —
  a guard left as it is says it does not. Where the shell guard is installed, run
  `sh -n .github/hooks/sdlc-tdd-guard.sh` with an `sh` that resolves (Git Bash's on
  Windows): a pattern value with a space is a syntax error that denies every Copilot
  write (the recipe now says so).
- **0.34.1 makes the classifier lint-clean**: 0.34.0's `.github/hooks/sdlc-cosmetic.py`
  failed ruff's default `E741`, which turns a gate red wherever lint covers
  `.github/hooks/`. It is kit-owned, so it is replaced like any other; take 0.34.1
  rather than 0.34.0. Behavior is unchanged.
- **0.35.0 puts the graph refreshes behind two switches** (`spec/SDLC.md`,
  *Architecture impact view*): `Graph refresh: slice-end incremental on · phase-end
  full-when-code-missing on`. Like 0.33.0's note, it matters only to a project carrying
  an Understand Anything graph; for any other project it is currency only. The adapter
  (kit-owned, replaced as usual) gains two modes. `refresh-check` lets `/end-slice` skip
  the refresh when the graph is already at HEAD, where `/understand` would stop to ask.
  `coverage` runs the plugin's own scanner at `/end-phase` and calls for
  `/understand --full` only when code or script files are missing from the graph. The
  commands now read the line, and **where it is absent they refresh nothing** — so,
  until the owner folds the `SDLC.template.md` diff, no refresh runs. Hand the owner
  that diff with the line **already filled from the project's own recorded rulings**,
  not re-asked:
  - a recorded owner ruling against the slice-end refresh → `slice-end incremental off`;
    one against regenerating at the phase end → `phase-end … off`;
  - no recorded ruling on a switch → `on`, the default every new adoption gets;
  - a recorded ruling neither value expresses (an owner-run regeneration, say) → the
    one case to ask. Name the ruling, recommend `on`, and replace that ruling's text in
    the same fold so the line and the prose cannot disagree.

  Quote each ruling you carried over beside the value it set. **A local amendment to
  the adapter's `freshness()` that reads any graph descending from the base as current
  is retired, not re-applied as a hunk.** It skips the second ancestry test, so a graph
  built on a sibling branch reads current where the kit says `may be stale`. Drop the
  hunk; a project test pinning its wording changes its expected string to the kit's
  (`current - graph at <sha>, built inside this change set after the base`), and its
  scenario still passes. A project-owned coverage script is the owner's to keep or
  retire, since the adapter's `coverage` mode now does the same comparison. Say so;
  delete nothing. **Where Copilot CLI is a runtime, offer `plugin-fix` at this halt**
  (`python .github/hooks/sdlc-impact.py plugin-fix`). Copilot refuses the plugin's
  `understand` skill until its list-form `argument-hint` is a string, so no Copilot
  session has been able to refresh the graph. That is a likely reason for a stale graph
  on a Copilot project. The mode also rewrites the plugin's auto-update hooks, which
  never ran on Copilot, so a project with `autoUpdate` on starts getting its orders to
  run the plugin's incremental update unprompted, at the agent's token cost, from the
  next session. Say that before asking. It writes outside the repository, so
  run it only on a yes.
- **0.35.0 also makes the TDD guards count the test, not the command.** A failing run
  is a RED only when the runner's own report is in its output; a command that only
  names the runner (a reader, `git`, an install, a heredoc) never counts, so a
  successful `cat vitest.config.ts` no longer records a GREEN; configs, one-off script
  directories and the graph tool's directory stop being production source; and three
  encoding defects that let a non-ASCII path slip the guard are fixed. The guard
  scripts are **project-owned**, so the update replaces neither: at the hook-script
  walk-through below, offer to re-derive `.github/hooks/sdlc-tdd-guard.py` / `.sh`
  from the 0.35.0 templates with the project's three resolved patterns carried over
  and the two new ones resolved the way setup does — `TEST_REPORT_PATTERN` from
  the recipe's runner table, `GUARD_EXEMPT_PATTERN` proposed from the tree and
  confirmed, never empty. Say a guard left as it is keeps today's rules exactly,
  including the wrapper failure that licenses a write. A re-derived guard needs the
  report-pattern proof setup now runs (one real red counted, one wrapper failure
  refused) before it is trusted, and `sh -n` where the shell dialect is installed; the
  guard note in `spec/SDLC.md` *Records* then names both values and the proof's catch
  — the refused wrapper failure's `NOT counted` line, quoted — with its reach note, as
  setup writes it. **If the project has its own guard tests, run them after the
  re-derive.** A fixture that fakes a failing run must carry the runner's real report
  (the pattern's marker), because one without it is now refused — that is the guard
  working, as one adopter's update found. Fix the fixture; never loosen the pattern to
  fit it. **A local amendment
  that counts a test file written through the shell as a test edit is retired, not
  carried as a hunk** (owner ruling, 0.35.0): once the edit-tools
  rule exists, a shell-written test is out of process, and licensing its red rewards
  the breach. Say so, and delete nothing without the owner's yes.
- **0.35.0 also changes the edit-time gate hook's body** (both dialects): it skips a
  file outside the project, names the check that failed and prints only that check's
  output, runs the lint value as one group so a compound `lint && format check` has both
  commands' output, and passes a typecheck block's non-blocking note (`tn`) back as
  context instead of a failure. The hook script (`.github/hooks/sdlc-gate-claude.sh` /
  `sdlc-gate.sh`) is **project-owned**, so the update replaces neither: offer, at the
  same walk-through, to re-derive it from the 0.35.0 template with the project's source
  glob, lint command and typecheck block carried over, and three recipe changes offered,
  not imposed — the format check folded into the lint value where the project's gate
  runs one (read the gate; never assume a formatter); a TypeScript block that runs a
  project-wide `tsc` or a workspace `typecheck` script offered GATE_RECIPES's
  one-tsconfig block in its place; and a Python block that assigns `m=` corrected to
  `t=`, without which mypy's errors never printed. Python projects are also offered the
  opt-in `--ignore F401,F821,F841` lint variant, with its cost said. A local patch that
  already does one of these (an out-of-repo skip, a per-tsconfig filter) is retired
  where the template now does it and carried where it is project-specific. Prove the
  re-derived hook the way setup does — a deliberate lint error in a scratch source file
  is reported — and record the catch, named, with its reach note where setup records the
  hook's proof; say a hook left as it is keeps today's behavior.
- **0.35.0 adds the edit-tools rule:** code — source and test files, less the guard's
  exempt paths — changes only through the editor tools, overriding any harness
  guidance that permits shell edits, because the edit-time hook and the guards see
  nothing written through the shell. Its exceptions are a tool's own output and
  `/end-slice` step 5's hash-verified mutation runner, whose form the installed
  `/end-slice` now carries. Its home is `CLAUDE.md` *Always-Active Rules*, which is
  project-owned: hand the owner the `CLAUDE.template.md` bullet to fold in, never edit
  it. Where the guards are installed, the guard note in `spec/SDLC.md` *Records* gains
  the same rule, that a shell-written test does not license its red, and that the
  guards see only the editor tools — fold it with the guard re-derive above. The
  slice-loop restore text in `SDLC.template.md` gains the runner carve-out; hand that
  diff over too. Until folded, the project's files win and the rule is not in force.
- **0.35.0 gives approved libraries one home:** an *Approved libraries* record in
  `spec/SDLC.md` *Records* (ratified into at `/plan-phase`, a `/next-slice` halt for an
  unlisted library) and a pointer to it in `CLAUDE.md`'s *No new libraries* bullet. Both
  files are project-owned: hand the owner the two diffs. Search the project for
  approvals already recorded elsewhere — phase-spec *Owner Decisions*, a
  `spec/PROJECT_INDEX.md` line — and offer them as the list's first entries; the owner
  moves them, never this command. The installed commands assume the record from this
  release on, so say that `/next-slice` halts on every new library until it exists.
  Hand over *Shape*'s new sentence with them — a draft PR opened only so CI runs is not
  the phase PR, and `/end-phase` marks it ready.
- **0.35.0 changes the Claude Code close-out Stop launcher's message** (Claude Code
  projects that accepted the backstop): where it said the script *is missing* it now
  says *not found from `<pwd>`* and tells the session to `cd` back to the root, because
  a shell `cd` below the root produced the same message as a real missing script. The
  block lives in `.claude/settings.json`, which is project-owned: hand the owner the
  template's new `Stop` command to paste over the old one, never edit it. Until then
  the old message stands, and a *missing* block may mean a moved cwd.
- **0.35.1 makes three hook scripts start far fewer processes, with no change in what
  they decide.** The Copilot TDD guard (`sdlc-tdd-guard.sh`) and both edit-time gate
  hooks (`sdlc-gate.sh`, `sdlc-gate-claude.sh`) did their string work through dozens
  of `$(printf … | sed)` and `tr` pipelines per call, and Windows `sh` pays tens of
  milliseconds for each process. Measured 2026-10-21 on the kit's Windows development
  machine: a guard call ~2 s before and ~0.85 s after, a gate-hook call ~1.5 s before
  and ~0.65 s after, plus the project's own lint. This host's saving is not measured
  here; say so. All three are project-owned, so this arrives only through the
  walk-through below. Recommend it on a Windows host, where the saving is largest;
  say that a script left as it is decides exactly as before, only slower. The new
  bodies set names of their own, which a project's lint value or typecheck block must
  not assign — in the Copilot gate hook `TK`, `SL`, `_tk`, `_sl`, `RP`, `RR`, `rp`,
  `g1`–`g3`, `h1`–`h3`, `k`, `c`, `cl`; in the Claude gate hook `TK`, `SL`, `_tk`,
  `_sl`, `c1`–`c3`, `l1`–`l3`, `k`, `c`, `cl`. Search the project's values for each:
  a hit is a conflict to show the owner, not one to resolve silently.
- **0.36.0 changes both TDD-guard dialects twice, and both arrive only through the
  walk-through below.** The stop now names code that changed outside the editor tools
  (armed, it blocks once and asks for the owner to be told), and a comment- or
  format-only test edit no longer stales a live red or revokes a refactor licence. Say
  both, and say a guard left as it is keeps today's rules: shell writes stay unseen. The
  shell dialect's report needs `git` on the hook shell's PATH; without it the report is
  silent and the guard otherwise unchanged. Where the project has its own guard tests,
  run them after the re-derive (as for 0.35.0).
- **0.36.0 adds *Records* → *Architecture graph*** (`spec/SDLC.md`, project-owned): hand
  the owner the template's subsection to fold and the line to write, resolved the way
  setup resolves the graph-tool note's placeholder, from what is true now (the plugin
  installed or not, its version, auto-update, the directory tracked or ignored). The
  markers check in step 4 asks for it too.
- **0.36.0 changes the impact adapter's output** (kit-owned, replaced as usual): phase
  views gain `untracked-files`, every view gains `graph-coverage:`, `coverage` gains
  `gone-files`, and `refresh-check`'s needed line names how many files the graph is
  behind. `freshness()`'s wording is unchanged. A project with its own tests on these
  lines is told before the replace.
- **0.36.0 anchors every launcher in `.claude/settings.json` at the repository root**
  (Claude Code projects): each kit launcher gains the prefix
  `cd "$(git rev-parse --show-toplevel)"; `, so a shell `cd` below the root no longer
  leaves test runs unrecorded, the gate skipped in silence, or every edit denied by the
  guard's launcher until the session `cd`s back. The file is project-owned: hand the
  owner the prefix to put at the front of each kit launcher that is installed — the
  guard's four, the gate's, the ledger's, the close-out `Stop` block — never edit the
  file, and never prefix a hook the project added itself. It must be copied exactly:
  `;`, never `|| exit 2`, because Copilot runs these launchers through PowerShell, where
  5.1 cannot parse `||`, and a PreToolUse launcher that fails to parse denies every
  edit. Until it is added, the 0.35.0 message is the only sign of a moved cwd.
- **0.37.0 removes the optional `tdd-guide/` skill**, the third instance of the removal
  clause above. Every known adopter accepted the offer, and no skill ledger ever
  recorded an activation; its model of TDD (test generation, coverage analysis) is not
  the one-failing-test-first order the `tdd` skill and the guards enforce. An
  `UNCHANGED` `.claude/skills/tdd-guide/` is deleted. A `DRIFTED` one goes to the owner,
  who keeps it by moving it to a project-owned path outside `.claude/skills/` or deletes
  it. Say this as one decision, not a column of deletions.
- **0.37.0 makes the index's coverage-floor line a pointer** (`spec/PROJECT_INDEX.md`,
  project-owned). The floor's one home is `spec/SDLC.md` *Records*; `/end-phase` now
  asserts that value against the enforced threshold and no longer reads the index. Hand
  the owner the fold: replace the figure in the phase block with `Coverage floor:
  recorded in spec/SDLC.md.` **Compare first:** a figure in the index that differs from
  *Records* is a finding for the owner, not a value to drop silently. The canonical rule
  moved in `templates/SDLC.template.md` (*Coverage floor*); step 4's marker table
  carries it.
- **0.37.0 adds two rules to `spec/SDLC.md`'s template**, each with a step 4 marker
  row, so this update puts each to the owner as a fold. The quality pass may trim the
  gate between moves but runs it in full once after the last, and the `quality:` line
  says which form ran (slice loop step 6; `/end-slice` §3 arrives with the update).
  The phase close stamps any baseline that carries no `@ <short-sha>`, green or red
  (*Phase end*, the *Records* reconcile), which also covers a green baseline recorded
  before 0.29.0. The guard note's comment now asks for the proof's catch by name and a
  reach note; a project whose guard note lacks them adds them when folding. Setup's
  baseline stamp, the guard note's one list and `python-pro`'s caveat reach only a
  fresh adoption, and the 0.14.0–0.31.3 notes now live in `reference/UPDATE_NOTES.md`.
- **Project-owned hook scripts: walk the owner through every template change, and
  offer to apply it — with review.** Five scripts are instantiated from templates and
  then owned by the project: `.github/hooks/sdlc-gate.sh` (from
  `templates/copilot-hook.template.sh`), `sdlc-gate-claude.sh`
  (`claude-gate.template.sh`), `sdlc-tdd-guard.sh` (`tdd-guard.template.sh`),
  `sdlc-tdd-guard.py` (`tdd-guard-claude.template.py`) and `sdlc-skill-ledger.sh`
  (`skill-ledger.template.sh`). A kit fix to one of them reaches the project only
  through this walk-through, so it runs for **every installed script of the five**,
  whether or not a version note above names it — a note says what a change means;
  the helper below says whether there is one. A hand-apply that depends on someone
  reading the changelog is the kind of step this kit exists to remove. The version
  notes' re-derive offers are made here, as this one decision per script — never as
  a second, separate offer.

  For each installed script, in order:

  1. **Read its values, never retype them.** Write a `values.json` under the git
     directory (`$(git rev-parse --git-dir)/sdlc-update/`, so nothing lands in the
     working tree), mapping each placeholder marker in the template — the key spelled
     exactly as the template spells it, braces included — to the exact text the
     committed file holds in its place (`git show HEAD:<path>`; a multi-line
     typecheck block is copied whole). The helper checks you: a value read wrong
     shows up as a local amendment on that line. Where a local patch has replaced a
     placeholder's text outright — a rewritten typecheck tail, say — the original
     value is no longer in the file: take it from the gate record in `spec/SDLC.md`
     or the patch's own comment, say which, and expect the patch to surface as an
     amendment. A value a version note offers to **change** (a format check folded
     into the lint value, a corrected typecheck block) goes in a second file holding
     only the keys that change, confirmed with the owner first: it fills the target
     template alone, so the merge applies it the way it applies a template change.
  2. **Run the helper** (below). It refuses a script with uncommitted changes, since
     a failed proof restores from `HEAD`, and a target that is not a release tag. It
     finds the release the script was derived from — the one, no newer than the
     target, whose template, filled with those values, is closest to the committed
     file — because the version the project is on is not always it: an earlier
     update may have offered a change and been declined. Then it prints either
     `CURRENT` (nothing to offer; say so in one line) or a proposal: the **local
     amendments** (the derived-from template, filled, against the committed file),
     the **proposed file** (a three-way merge of the target template into the
     committed one, so amendments carry), and **`diff -u` from committed to
     proposed**. A placeholder the target template adds stops it with `UNRESOLVED`:
     resolve that value the way `sdlc-setup.md` does and the version note says,
     confirm it with the owner, add it to `values.json`, and run it again. Every
     other stop names its cause (`NO TARGET`, `UNCOMMITTED`, `NOT COMMITTED`,
     `NO BASE`, `MERGE FAILED`, and `NO SUCH AMENDMENT` for a `--drop`
     number it did not print); none of them is a proposal.
  3. **Walk the owner through it — a numbered, explicitly marked decision per
     script** (`Decision N: <script> — apply the proposal / keep as it is`). In
     plain words: what changes behaviorally, from the changelog entries in range
     that touch its template, and from any version note above; each local amendment,
     by the number the helper printed, and whether it is carried. An amendment is
     carried by default. It is retired only where a version note retires it, or where
     the target template now does what it did (subsumed). Name the reason, and get the
     owner's yes. A retirement must then **run**: re-run the helper with `--drop N[,N…]`
     and present that proposal, never a hand-built file, which no check of the
     helper's would cover. For each drop it prints whether the target template changes
     that region too (read the proposal to confirm it does what the amendment did), or
     `BEHAVIOR CHANGE`, which means the template's old text comes back; say that one to
     the owner in plain words. A merge carries every amendment by construction, so
     without `--drop` a retired amendment ships silently. Then every merge conflict,
     shown with both sides and a recommended resolution; and what keeping the script
     costs, as concretely as the notes allow ("a guard left as it is keeps today's
     rules exactly"). Then the
     full diff from committed to proposed, so the owner reviews the file that will be
     written, not a description of it. Offer to apply it for them; never apply it on
     a summary alone.
  4. **On yes:** write the proposed file — with every conflict resolved the way the
     owner chose, and no `<<<<<<<` marker left in it — then check its syntax (`sh -n`
     with an `sh` that resolves, Git Bash's on Windows; `python -m py_compile` for the
     `.py`), then run the proof `sdlc-setup.md` runs when it installs that file.
     Record the proof's catch, named, and its reach note, where setup records them.
     A proof that fails puts the committed script back — from a POSIX shell, since
     PowerShell's `>` re-encodes the bytes: `git show HEAD:<path> > <path>` — and
     goes to the owner with its output. Never report a re-derived script as working
     on its syntax check alone. Where the script carries a decline line (step 5),
     append `— superseded by re-derive at kit <target> (<date>)` to it; never delete
     it.
  5. **On no:** say in one line what the project keeps, and record the decline in
     `spec/SDLC.md` *Records*, after the edit-time hook's record, where the template
     says it goes — `Hook re-derive declined: <script> at kit <target offered>
     (<date>)` — so a later update does not re-ask it. Before offering a script, read
     those lines: for the newest one naming it, unsuperseded,
     `git -C /tmp/kit diff --quiet <that version> "$T" -- sdlc-kit/templates/<template>`
     succeeding means the template has not changed since the decline — say so in one
     line and move on; failing means offer it again and name the earlier decline. A
     second decline is a second line: the newest governs.

  ```bash
  # Run once per installed script. T is the target tag; the kit clone is an argument,
  # not a constant, because Git Bash translates a /tmp path only on a command line -
  # native Windows git cannot open one written inside the script.
  T=v$(cat /tmp/kit/sdlc-kit/VERSION)   # the target tag, read from the clone, never typed
  GD=$(git rev-parse --git-dir); mkdir -p "$GD/sdlc-update"
  cat > /tmp/kit-rederive.py <<'PY'
  import difflib, json, os, re, subprocess, sys
  # <script> <template> <values.json> <target tag> <kit clone> [<target-only values>]
  #   [--drop N[,N...]]   local amendments to retire, numbered as an earlier run printed
  args, drop = sys.argv[1:], set()
  if "--drop" in args:
      i = args.index("--drop")
      drop = {int(n) for n in (args[i + 1:i + 2] or [""])[0].split(",") if n.strip()}
      del args[i:i + 2]
  path, tpl, vals_file, target, kit = args[:5]
  tgt_file = args[5] if len(args) > 5 else None
  OLD_NAMES = {"skill-ledger.template.sh": ["skill-ledger-claude.template.sh"]}
  run = lambda *a: subprocess.run(a, capture_output=True)
  def show(tag):                                # a renamed template, by every name
      for name in [tpl] + OLD_NAMES.get(tpl, []):
          p = run("git", "-C", kit, "show", "%s:sdlc-kit/templates/%s" % (tag, name))
          if p.returncode == 0 and p.stdout:
              return p.stdout.decode("utf-8")
      return ""
  tags = [t for t in run("git", "-C", kit, "tag", "--sort=-v:refname")
          .stdout.decode().split() if re.fullmatch(r"v\d+\.\d+\.\d+", t)]
  if target not in tags:
      sys.exit("NO TARGET: %r is not a release tag in %s - set T" % (target, kit))
  target_body = show(target)
  if not target_body:
      sys.exit("NO TARGET: %s holds no %s - check the template name" % (target, tpl))
  if run("git", "status", "--porcelain", "--", path).stdout.strip():
      sys.exit("UNCOMMITTED: %s has uncommitted changes - commit or stash them; a "
               "failed proof restores the script from HEAD" % path)
  head = run("git", "show", "HEAD:" + path)
  if head.returncode != 0:
      sys.exit("NOT COMMITTED: %s is not in HEAD - commit it first" % path)
  installed = head.stdout.decode("utf-8")
  vals = json.load(open(vals_file, encoding="utf-8"))
  tvals = dict(vals, **json.load(open(tgt_file, encoding="utf-8"))) if tgt_file else vals
  def fill(body, v):
      for k, x in v.items():
          body = body.replace(k, x)
      return body, sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", body)))
  def diff(a, b, la, lb):
      return list(difflib.unified_diff(a.splitlines(), b.splitlines(), la, lb,
                                       lineterm=""))
  best = None                       # no newer than the target; the newest wins a tie
  for tag in tags[tags.index(target):]:
      body = show(tag)
      filled, left = fill(body, vals) if body else (None, ["(absent)"])
      if left:
          continue
      n = len(diff(filled, installed, "", ""))
      if best is None or n < best[1]:
          best = (tag, n, filled)
  if best is None:
      sys.exit("NO BASE: no release's %s, filled with these values, resembles %s - "
               "re-read the values from the committed file" % (tpl, path))
  base_tag, _, base = best
  new, left = fill(target_body, tvals)
  if left:
      sys.exit("UNRESOLVED in %s's template: %s - resolve each as setup does, add it "
               "to %s, run again" % (target, ", ".join(left), vals_file))
  b_lines, i_lines = base.splitlines(True), installed.splitlines(True)
  ops = difflib.SequenceMatcher(None, b_lines, i_lines, autojunk=False).get_opcodes()
  amends = [o for o in ops if o[0] != "equal"]
  if drop - set(range(1, len(amends) + 1)):
      sys.exit("NO SUCH AMENDMENT: %s - %s has %d; run without --drop to list them"
               % (sorted(drop - set(range(1, len(amends) + 1))), path, len(amends)))
  if base == new and not drop:
      print("CURRENT: %s already matches the %s template - nothing to offer"
            % (path, target))
      sys.exit(0)
  print("%s: derived from %s" % (path, base_tag))
  # A retired amendment is merged as if it had never been made: its lines go back to
  # the derived-from template's before the merge, so the target's text wins there.
  dropped = [o for n, o in enumerate(amends, 1) if n in drop]
  committed = "".join("".join(b_lines[o[1]:o[2]] if o in dropped else i_lines[o[3]:o[4]])
                      for o in ops)
  t_ops = [o for o in difflib.SequenceMatcher(None, b_lines, new.splitlines(True),
                                              autojunk=False).get_opcodes()
           if o[0] != "equal"]
  out = os.path.join(run("git", "rev-parse", "--git-dir").stdout.decode().strip(),
                     "sdlc-update")
  os.makedirs(out, exist_ok=True)
  name = os.path.basename(path)
  files = {}
  for label, text in (("installed", committed), ("base", base), ("target", new)):
      files[label] = os.path.join(out, "%s.%s" % (name, label))
      open(files[label], "w", encoding="utf-8", newline="").write(text)
  m = run("git", "merge-file", "-p", "--diff3", "-L", "committed",
          "-L", "derived-from " + base_tag, "-L", "target " + target,
          files["installed"], files["base"], files["target"])
  if not 0 <= m.returncode <= 127:              # a conflict count, or git failed
      sys.exit("MERGE FAILED: %s" % m.stderr.decode("utf-8", "replace"))
  proposed = os.path.join(out, name + ".proposed")
  open(proposed, "wb").write(m.stdout)
  print("LOCAL AMENDMENTS (%s, against the %s template, filled):"
        % (len(amends) or "none", base_tag))
  for n, (_, i1, i2, j1, j2) in enumerate(amends, 1):
      print("AMENDMENT %d%s - template lines %d-%d, committed lines %d-%d:"
            % (n, " (DROPPED)" if n in drop else "", i1 + 1, i2, j1 + 1, j2))
      hunk = ("".join("-" + l for l in b_lines[i1:i2]) +
              "".join("+" + l for l in i_lines[j1:j2]))
      print(hunk if hunk.endswith("\n") else hunk + "\n", end="")
  for n, (_, i1, i2, _, _) in [(n, o) for n, o in enumerate(amends, 1) if n in drop]:
      if any(t1 <= i2 and i1 <= t2 for _, t1, t2, _, _ in t_ops):
          print("DROP %d: the %s template changes this region too - check in the "
                "proposal that it does what the amendment did" % (n, target))
      else:
          print("DROP %d: BEHAVIOR CHANGE - the %s template leaves this region as the "
                "amendment found it, so dropping it reverts to the template's text"
                % (n, target))
  print("MERGE CONFLICTS: %d" % m.returncode)
  print("PROPOSED FILE: %s\n" % proposed)
  print("\n".join(diff(installed, m.stdout.decode("utf-8"), path, path + " (proposed)")))
  PY
  python /tmp/kit-rederive.py .github/hooks/sdlc-gate.sh copilot-hook.template.sh \
    "$GD/sdlc-update/values-gate.json" "$T" /tmp/kit
  ```

- **Touch nothing project-owned** (the table above). The kit cannot regenerate those
  files and must not try — the walk-through above writes one only on the owner's word,
  after they have read its diff.
- **Three further owner decisions can arise inside this step**, and all are real halts
  even though step 4 carries the main one: an un-manifested file in a kept `sdlc-kit/`
  folder (below), an optional-hook offer (the record-against-artifact bullet above),
  and the hook-script walk-through above (which carries the version notes' re-derive
  offers). None is decided on the owner's
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
  **with three stated exceptions**: the artifacts an accepted re-offer installs (the
  TDD-guard pair; the ledger's Copilot JSON, or its `"Skill"` block merged into the
  existing `.claude/settings.json` the way setup's Existing mode merges hooks; a hook
  script the step-5 walk-through re-derived, with its proof's record), each
  written only on the owner's word at that halt, following setup's own step; and the
  empty `spec/PRODUCT_CONTRACT.md` the 0.23.0 note (`reference/UPDATE_NOTES.md`) creates
  — a verbatim template copy, only when absent, never content.
  **A third exception is the friction closure step 4 proposed:** once the verify above
  passes, for each `RULING OPEN` entry the owner confirms the release fixed — checked
  against the installed file, not the changelog's word — flip its disposition in place
  to `implemented in kit vX.Y.Z` — the release tag names the commit, and this update's
  own commit does not exist yet — the shape `/sdlc-retro` step 6 writes and closes on.
  An entry the owner does not confirm keeps `RULING OPEN`; nothing is flipped without
  that word.
  Do them last, so an aborted update never claims a version it does not hold.
  **More lines join them only when this update actually put an offer to the owner** —
  the TDD-guard, skill-ledger and backstop offers (step 5's record-against-artifact
  bullet), and each declined hook-script re-derive (`Hook re-derive declined:`, step
  5's walk-through) — then their answer is recorded in `spec/SDLC.md` the way setup records it — a declined
  re-derive in the form the walk-through gives, since setup writes none — decline
  included. Each is written only when its offer was made and answered in this session,
  never inferred and never rewritten: an update that did not ask does not get to record
  an answer. Without it a decline leaves no trace and every later update re-asks a
  settled question, which is the whole reason the lines exist.
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
  copied verbatim to `.github/hooks/sdlc-close-out.json`; from 0.28.0
  `templates/sdlc-impact.template.py` → `.github/hooks/sdlc-impact.py`, and from 0.34.0
  `templates/sdlc-cosmetic.template.py` → `.github/hooks/sdlc-cosmetic.py`, both CLIs,
  verbatim). If one fixes
  something the project cares about, raise it with the owner as a manual follow-up —
  never apply it automatically.
- Skipping several versions is fine: classify against the version the project is on,
  copy from the target, read the changelog for everything in between.
