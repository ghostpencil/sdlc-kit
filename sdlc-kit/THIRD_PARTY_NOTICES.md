# Third-Party Notices

**Not everything under `skills/` is third-party.** Three files are **kit-written and
carry no upstream** — `skills/diff-review/SKILL.md`, `skills/change-simplify/SKILL.md`,
and `skills/change-verify/SKILL.md` (all 2026-08-03). They are covered by this kit's own
`LICENSE`, and nothing in this file applies to them. `diff-review` owes a design debt to
`mattpocock/skills` that is recorded in `reference/SKILLS.md`; the text is not copied and
the file is not a derivative, so the debt is real without being a licence obligation.

The **remaining** files under `skills/` are vendored from (or derived from) the following
projects — all *identified* upstreams are MIT-licensed; `python-pro/SKILL.md` has no
identified upstream repo or license text, only its in-file author attribution. Full
provenance detail, including how each local copy was verified against its upstream, is in
`reference/SKILLS.md`.

| File(s) in this repo | Upstream | Copyright |
|---|---|---|
| `skills/tdd/SKILL.md`, `skills/tdd/tdd-references/tests.md`, `skills/tdd/tdd-references/mocking.md` | [mattpocock/skills](https://github.com/mattpocock/skills) (`skills/engineering/tdd/`) | Copyright (c) 2026 Matt Pocock |
| `skills/hypothesis-tests/SKILL.md` (verbatim), `skills/mutation-testing/SKILL.md` (condensed derivative) | [honnibal/claude-skills](https://github.com/honnibal/claude-skills) | Copyright (c) 2026 Matthew Honnibal |
| `skills/tdd-guide/SKILL.md` (truncated, lightly adapted) | [alirezarezvani/claude-code-skill-factory](https://github.com/alirezarezvani/claude-code-skill-factory) (`generated-skills/tdd-guide/`) | Copyright (c) 2025 Reza Rezvani |
| `skills/python-pro/SKILL.md` | attributed in-file to [github.com/Jeffallan](https://github.com/Jeffallan) (attribution header kept intact) | see file header |

Each of the three repositories above is distributed under the MIT License. The
license text below applies to each, with the copyright line as listed in the table:

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

If you redistribute this kit (or install its `skills/` files into another
project), keep this notices file and the attribution in `reference/SKILLS.md`
intact.
