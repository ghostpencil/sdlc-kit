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
| `.claude/commands/*.md` (from the kit's `commands/`, `skills/`, `reference/REVIEW_LENSES.md`) | kit | overwrite when provably unmodified; owner decides when drifted |
| `CLAUDE.md`, `spec/*.md`, `.claude/settings.json` | project | never overwritten — they hold the gate baseline, owner decisions, backlog, gotchas |

## How to use

`/sdlc-update` — update to the latest release. `/sdlc-update v0.4.0` — a specific one.

## Workflow

### 1. Establish both versions

- Read the project's version from `spec/SDLC.md` (*Kit version: X.Y.Z*). Do not guess
  and do not assume the newest: classification runs against the manifest of the version
  the project is *on*, which is what makes "unmodified" provable rather than hopeful.
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

Compare everything under `.claude/commands/` against the **old** version's manifest.
Hash committed content (`git cat-file -p :path`), never the working tree — an unpinned
checkout on Windows holds CRLF and would report every file as drifted, uniformly and
plausibly wrong.

```bash
cd <project root>
MAN=/tmp/kit-old/sdlc-kit/MANIFEST.sha256

for f in $(git ls-files .claude/commands); do
  base=${f#.claude/commands/}
  # commands/, skills/, and reference/REVIEW_LENSES.md all install into
  # .claude/commands/, so try all three prefixes.
  want=$(awk -v b="$base" \
    '$2 == "commands/" b || $2 == "skills/" b || $2 == "reference/" b {print $1}' "$MAN")
  have=$(git cat-file -p ":$f" | sha256sum | cut -d' ' -f1)
  if   [ -z "$want" ];        then echo "UNKNOWN   $base"
  elif [ "$want" = "$have" ]; then echo "UNCHANGED $base"
  else                             echo "DRIFTED   $base"
  fi
done
```

Two checks on the check — required, because both failure modes produce a plausible
result rather than an error:

- **Denominator.** The loop must print exactly as many lines as
  `git ls-files .claude/commands | wc -l`. Fewer means the matching dropped files
  (`tdd-references/` lives in a subdirectory and is the usual casualty).
- **Never probe for a path with `git cat-file … | sha256sum`.** A pipeline reports the
  *last* command's status, so a missing path hashes empty input and silently matches
  the wrong thing. Look paths up in the manifest, as above.

### 4. Present the plan — the ONE owner halt

Before writing anything, show the owner the full classification plus the changelog
entries marked *[installable]* for every version being skipped. Then:

- `UNCHANGED` → provably untouched since adoption; will be overwritten with the target
  version. No per-file question.
- `DRIFTED` → someone edited it, often deliberately — `spec/SDLC.md` explicitly invites
  fixing a command that disagrees with it. Show the diff against both versions; the
  owner decides per file (keep / overwrite / merge). **Never auto-overwrite a drifted
  file.**
- `UNKNOWN` → not from the kit. Left alone, no question asked.

### 5. Apply

- Copy the target version's files over the `UNCHANGED` set and whatever `DRIFTED` files
  the owner released. Sources: `sdlc-kit/commands/`, `sdlc-kit/skills/`, and
  `sdlc-kit/reference/REVIEW_LENSES.md` — all into `.claude/commands/`, preserving the
  `tdd-references/` subfolder.
- **Touch nothing project-owned** (the table above). The kit cannot regenerate those
  files and must not try.
- If the project kept a `sdlc-kit/` folder from adoption, replace it wholesale with the
  target version's bundle — it is a verbatim copy of the kit and holds nothing of the
  project's.

### 6. Verify, re-stamp, land

- Re-run step 3 against the **target** version's manifest: every file just copied must
  now classify `UNCHANGED`, and the only `DRIFTED` entries are the files the owner chose
  to keep. The two runs disagreeing about the copied files (old manifest: changed;
  new: matching) is what proves the classifier discriminates — an all-clear it could
  not fail to produce proves nothing.
- Re-stamp `spec/SDLC.md` (*Kit version: X.Y.Z (updated <date>)*) — the one line an
  update may change in a project-owned file. Do it last, so an aborted update never
  claims a version it does not hold.
- Land as a normal PR (`chore/update-sdlc-kit-X.Y.Z`), the same way the adoption landed.
  Report to the owner what changed *behaviorally* (from the changelog), not just which
  files moved.

## Notes

- Changelog entries marked *[adoption-only]* changed templates or reference docs read
  only at `/sdlc-setup` time; they affect new adoptions, not this project. If one fixes
  something the project cares about, raise it with the owner as a manual follow-up —
  never apply it automatically.
- Skipping several versions is fine: classify against the version the project is on,
  copy from the target, read the changelog for everything in between.
