# SDLC Retro

Extract lessons from a stretch of real work and route them to the two places they
belong: facts about **this project** into the project's own files, and evidence that
**the process itself** was wrong, unclear, or silent into a field report the owner may
choose to send upstream. Process reference: `spec/SDLC.md`.

Prime directive: **evidence before findings.** Every finding must point at something on
disk — a provenance tag, a Phase History row, a baseline number, a commit. A plausible
lesson with nothing behind it is a guess wearing a finding's clothes. If the run is too
young to have left evidence, say so and stop; that is a real answer, not a failure.

## How to use

`/sdlc-retro` — at a phase boundary (after `/end-phase` merges), before planning the
next one. Optional argument to scope the window: `/sdlc-retro phase 3` or
`/sdlc-retro since v0.2.0`. Default window is the most recent phase.

This command reads and interviews; it writes one new file and proposes edits to the
project's own. It never opens an issue, never pushes, and never sends anything anywhere.

## Workflow

### 1. Orient and set the window

Read `spec/PROJECT_INDEX.md` (Phase History, deferred backlog, Environment gotchas,
Notes) and `spec/SDLC.md` (gate definition, recorded gate baseline, kit version). The
window is the phase named in the argument, or the most recent Phase History row.

**When the kit is co-developed alongside this project** — its home repository is on
this machine, or the project's notes point at kit planning documents — read the kit's
own planning and field-report docs for the window too. Half the friction record of a
co-developed adoption lives on the kit's side; a retro that reads only the project's
spec files once missed a friction item the
kit's plan had already recorded *and labeled as retro material*. For an ordinary
adoption with no kit repo at hand, skip this — it is a co-development clause, not a
new dependency.

**Evidence sufficiency check — do this before anything else.** The command needs
something to reason about. Count what the window actually contains: merged phases,
completed slices, deferred-backlog entries, commits. If the project has been through
less than one full phase *and* the backlog is empty, report that there is not enough
evidence yet, name what would make a retro worthwhile (a merged phase, a populated
backlog with provenance tags), and stop. Do not interview your way around missing
evidence — an interview with no artifacts behind it produces opinions, and opinions are
what this command exists to replace.

### 2. Mine the disk — read-only sweeps

Gather evidence before forming any view. These may run as parallel read-only sweeps;
none of them writes anything.

- **Deferred-backlog provenance tags.** Entries are meant to record where they came from
  (`(slice review, <date>)`, `(whole-arc review, PR #N)`). Cluster the ones that do —
  and treat untagged entries as their own small finding. Ask: which review
  stage produced the most findings, which findings repeat across slices, what has been
  sitting unaddressed longest. Repetition is the signal — the same finding three times
  is a process gap, not three mistakes.
- **Gate-baseline trajectory.** Compare the baseline recorded in `spec/SDLC.md` against
  what the gate reports today. The direction and rate of that burn-down is evidence
  about whether the process is actually moving the number.
- **Phase History.** Slice counts per phase, PR sizes, anything that took more slices
  than it was planned for.
- **Environment gotchas and Notes.** Which were learned the hard way — i.e. appear in
  the log as a fix commit before they appear as a note?
- **`git log` friction signals** over the window: fix commits landing straight after a
  gate run (a red gate that got through), repeated gate runs on one slice, commits after
  a review that undo review changes, reverts, and slices whose commit span is much wider
  than their siblings'.
- **Recorded-but-unactioned friction.** Sweep the *Kit friction log* section of
  `spec/PROJECT_INDEX.md` first (adoptions from kit 0.6.0 on seed it; treat its absence
  as a small finding on an older adoption, since friction with no home goes unrecorded),
  then the project's other notes — and the kit-side docs, when step 1's co-development
  clause applies — for friction someone already wrote
  down and nobody acted on: a warning in a planning doc, a "worth fixing later" that
  never became a backlog entry, a gotcha noted mid-arc and left. Friction that was
  recorded and still not addressed is a stronger finding than friction merely felt — the
  process saw it and had no place to put it. **Read the log for status and age, not only
  for content:** entries a previous retro absorbed carry a marker, so report the ones
  that do not — each with its date and how many phases it has now survived — and carry
  any entry older than one phase into this report automatically, whether or not the
  interview raises it. An entry with no status line is the default state, not a
  conclusion; one adoption's oldest live entry sat unabsorbed across two releases while
  three younger ones beside it were marked absorbed, and nothing in the sweep read the
  difference. The sweep is done when no unabsorbed entry is left unreported — each
  named with its age. This sweep exists because the sweeps above
  are all blind to tooling noise (stderr warnings produce no backlog entry, no commit,
  no gate movement) and the one record of such noise may sit in prose nothing else here
  reads.

Report what the sweeps found as a short evidence summary before interviewing — plain-
English bullets per the hand-back standard (`spec/SDLC.md`, *Owner halt points*). The
owner is about to be asked to interpret it.

### 3. Owner interview — rounds of ≤4 questions

AskUserQuestion in rounds, each round informed by the last, until a full round surfaces
nothing new. Lead with what the sweeps found — "the backlog shows X three times, was
that friction or noise?" beats an open-ended prompt. Cover, minimum:

- **What did you fight?** Where did the work feel harder than the thing being built
  justified?
- **What did you override or work around?** A rule that gets bypassed is either wrong or
  unenforceable, and both are findings. This is the highest-yield question — ask it
  concretely, against specific slices.
- **Where was the process silent?** Moments where the kit said nothing and a decision got
  made anyway, on nothing.
- **What would you delete?** Ceremony that cost time and returned nothing.
- **What worked?** Not politeness — a practice that carried its weight is worth
  protecting from a future simplification, and the report has a section for it.

### 4. Sort every lesson into exactly two piles

This is the one structural rule of the command, and nothing may land in both piles or
neither.

- **Project lessons** — facts about *this* codebase, environment, or team. A gotcha, a
  data-compatibility rule, a tooling quirk, a follow-up worth doing. These go into the
  project's own files: `spec/PROJECT_INDEX.md` Notes, Environment gotchas, or the
  deferred backlog (with a `(retro, <date>)` provenance tag, like every other entry).
  They never leave the repo.
- **Kit lessons** — the *process* was wrong, unclear, or silent. A command that asserted
  something false, a rule written but never enforced, a number trusted but never
  measured, a step the process does not cover at all. These go into the report in step 5.

The test for the boundary: would this lesson be true for a different project using the
same process? Yes → kit lesson. No → project lesson. When it is genuinely both (a
project gotcha the process should have prompted for), record the project half as a
project lesson and the *should have prompted* half as a kit finding.

### 5. Write the report

Write `spec/SDLC_RETRO_<YYYY-MM-DD>.md` — project-owned, committed with the project like
any other spec file. Use this shape, which is the one the kit's own field report used
(that file lives in the kit's home repository, not in this project — the skeleton below
is the authoritative statement of the format):

```
# Retro — <window: phase/version range>
  Project, adoption date + mode, what the window covered, headline result numbers
  (tests, gate baseline movement, PRs merged) — measured, not remembered.

## N. <finding title>                 (numbered, ordered by damage caused)
  Severity. What happened, with the evidence quoted. Which kit text it implicates,
  by path and quoted section. What the fix would be.

## What worked well
  Practices that earned their place.

## Suggested priority                 (table: # | change | file(s) | effort)

## Cross-cutting theme                (the one thing, if only one thing is taken)
```

Each finding must name the kit file it implicates (`commands/end-slice.md`,
`templates/SDLC.template.md`, …) and quote the evidence it rests on. A finding that
cannot name a file is not yet a finding — it is a feeling, and it goes back to step 3 as
a question.

The citation is **read off the file at writing time, never from memory of the
process**: quote the implicated text with a section or step number taken from the file
as it is now — or, for a finding about silence, locate the silence between two named
steps that do exist. Then name **every home** of the quoted wording: a rule usually
lives in a command *and* in `spec/SDLC.md`'s canonical statement, and a fix that
misses a home leaves the two disagreeing. A finding whose citation was not read off
the file is not yet verified — two consecutive real reports shipped step numbers for
steps that do not exist and quotes reworded from memory, and every one was caught only
on the maintainer's side. The review verifies its findings against the source; the
retro, which produces findings about kit files, holds itself to the same rule.

If the sweeps and interview produced **no** kit findings, say exactly that and write the
report anyway with its *What worked well* section filled in. Zero findings is a
legitimate outcome and worth recording; a manufactured finding is not.

### 6. Apply the project half, and hand off the rest

- Apply the project lessons to `spec/PROJECT_INDEX.md` (Notes, Environment gotchas,
  backlog entries tagged `(retro, <date>)`).
- Commit the report and the index together as a docs commit.
- Tell the owner what the report contains — per the hand-back standard: a plain-English
  executive summary of the findings in damage order, with the submit-upstream call as
  an explicitly marked decision (`Decision 1: submit as a GitHub issue on the kit's
  repository, or keep it local?`). **Do not open it, and do not draft a
  submission unless asked.** The report is written for a reader who does not have this
  project; if the owner does want to submit, offer to check it reads that way.

## Notes

- Two audiences, two files, no leakage: project facts in the project's files, process
  findings in the report. A retro that dumps everything into one pile is unusable by
  either reader.
- Ordering findings by damage caused, not by how annoying they felt, is what makes the
  priority table worth reading.
- The window matters. A retro spanning three phases smears the signal; one phase per
  retro keeps findings attached to the work that produced them.
- A retro that produces only compliments is as suspect as a phase plan that survives
  adversarial analysis unchanged — look harder at the workarounds question.
