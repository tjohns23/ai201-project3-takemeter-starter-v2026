# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter reads posts and comments from r/math and sorts them by how much
support they bring. A `supported` post backs its main point with something on
the page a reader can check: a fact, the content of a source, a worked
example, or a chain of reasoning. An `unsupported` post makes a claim, gives an
opinion, or asks a question with nothing behind it, and a `quip` makes its
point through a joke. Tone and hedging don't count either way; only what
backs the point does.


---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `supported`

**Definition:** Backs its point or question with something on the page that
does work: a specific fact, a source, a worked example, or a chain of
reasoning.

**Example 1:**
> I would certainly not agree that no cryptographer ever recommends using RSA
> any more […] For instance, NIST employs good cryptographers, and they have a
> whole standard dealing with integer-factorization-based key establishment.
> Saying that nobody recommends it any more for anything is just at odds with
> reality. […] In the vast majority of imaginable settings, this is less
> attractive than just factoring the public modulus using GNFS, which also the
> paper itself readily admits.

**Example 2:**
> Can 'concrete' statements be undecidable? […] I'll take the Collatz
> conjecture (CC) as an example. Suppose the CC is undecidable in ZFC. Then, if
> we believe ZFC is consistent, we cannot find a counterexample. […] Compare
> this with the continuum hypothesis (CH) […] To me, this seems like a
> different flavour to CC. There, it seems that any counterexample would be
> constructive (it's just a natural number!), and hence, if CC is undecidable,
> such a counterexample cannot exist. […] Am I wrong to assume this?

### `unsupported`

**Definition:** Makes a claim, gives an opinion, or asks a question with
nothing on the page backing it.

**Example 1:**
> I went and skimmed the original paper, and it was really refreshing to have
> them trip over themselves to say "we haven't absolutely set everything on
> fire, but this is kind of a big deal". It's wonderful to see academia not
> sensationalised in a world where it seems like everything else increasingly
> is.

**Example 2:**
> For the non communication between Alice and Bob, does that include using
> their guesses as communication? I.e. can Bob alter his guess based on what
> Alice guesses?

### `quip`

**Definition:** A joke or one-liner whose point is carried by the humour
rather than stated.

**Example 1:**
> We've finally created a real life magic 8 ball.

**Example 2:**
> I hope you like reading Lean!

### The hardest boundary

**Which two labels:** `supported` and `unsupported`

**The decision rule I used every time:**
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->

If a post gives the reader something on the page they can use to verify its
main point (a specific fact, the content of a source, a worked example, or
reasoning they can follow step by step), it's `supported`. Otherwise it's
`unsupported`. Naming or linking a source without using what it says doesn't
count.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Public r/math comments and text posts from May
to October 2026. Reddit now blocks anonymous access to its own JSON, so
`collect.py` reads r/math from the Arctic Shift archive
(arctic-shift.photon-reddit.com) instead. It sampled ten evenly spaced points
across six months, kept at most 12 posts per thread, and dropped deleted,
removed, bot and moderator posts. That gave 440 candidates from 121 threads
(`data/candidates.csv`).

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->
Pre-labelled with AI. Claude labelled all 440 candidates using my definitions
and decision rule, flagged 135 borderline calls with a reason, and marked 35
as not fitting the taxonomy at all (thank-yous, bot commands, off-topic
politics, replies that make no sense without the thread). The pre-labels and
flags are in `data/prelabeled.csv`. I dropped the 35, kept all 35 quips, and
took a seeded random sample (`random_state=42`) of 80 `supported` and 85
`unsupported` to keep every label under 50%. None of the 200 final labels
differ from the pre-labels. See **How I Used AI** below.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `unsupported` | 85 | 42.5% |
| `supported` | 80 | 40.0% |
| `quip` | 35 | 17.5% |
| **Total** | 200 | 100% |

Quips are scarce. Only 35 of 440 candidates (8%) were quips, so I kept all of
them and still fell short of the 40 that criterion 3 asks for.

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "He's a prof at UChicago. Of course he thinks anxiety is
> unnecessary."
>
> *Could have been:* `quip` or `unsupported`
>
> *I chose, because:* `quip`. It does carry a point (comfortable senior
> people underrate early-career anxiety), but the point is never stated. It's
> delivered entirely through sarcasm. When the joke is the vehicle, it's a
> quip, even if a real claim sits underneath.

**2.**
> *The post:* "The Fields Medal is specifically for young people"
>
> *Could have been:* `supported` or `unsupported`
>
> *I chose, because:* `supported`. It's one sentence, but the whole post is a
> single checkable fact (the medal has an under-40 age limit) that settles the
> point it replies to. Under my rule, length doesn't matter; a single
> checkable fact that backs the main point is enough.

**3.**
> *The post:* "I wondered why you were so heavily downvoted then noticed all
> of the links were zenodo or vixra. Just so you know, vixra is notoriously
> infested with cranks (in fact it's 99.99% cranks)…"
>
> *Could have been:* `supported` or `unsupported`
>
> *I chose, because:* `supported`. "99.99% cranks" is exaggeration, not
> evidence, but the main point (don't trust these papers by default) rests on
> something checkable: the links in the thread really are to zenodo and vixra.
> One checkable fact backing the main point outweighs the made-up number.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** <!-- epochs, learning rate, batch size, seed -->
3 epochs, learning rate 2e-5, batch size 16, 128 tokens per post, seed 42.
Trained on CPU (`device: cpu`, torch 2.14.1+cpu).

**Anything I changed from the defaults, and why:** Nothing. I kept 128 tokens
even though about 61 of the 440 candidates run past 100 words, so the
reasoning in some long `supported` posts gets cut off. I'm recording that as a
known limitation rather than doubling the training time.

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->
Stratified 70/15/15: 140 train, 30 validation, 30 test. The test split has 13
`unsupported`, 12 `supported`, and **5 `quip`**. That's under 8, so expect
`quip`'s scores to swing a lot between seeds.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* Eight posts written to sit on my label boundaries, to
  stress-test the definitions.
- *What came back:* Eight short r/math-style posts. Labelling them showed I
  was applying my decision rule as "there's an external source to go to," so
  a post with a checkable counterexample (Cantor set) came out `unsupported`
  and a bare "read the Tao blog post, wild stuff" came out `supported`. My own
  definition said the opposite in both cases.
- *What I changed:* I rewrote the decision rule to match the definition:
  support has to be on the page and back the main point, and naming or
  linking a source without using what it says doesn't count.

**Moment 2**

- *What I asked for:* A way to collect posts programmatically, then
  pre-labels for all of them.
- *What came back:* A `collect.py` that first failed (Reddit now blocks
  anonymous JSON) and was rewritten to use the Arctic Shift archive. Then a
  pre-labelled file with 135 flagged borderline calls, and a note that only 35
  quips existed, below criterion 3's target of 40.
- *What I changed:* I decided to keep three labels and accept the criterion 3
  miss rather than collect more or drop `quip`. I agreed with the four
  recurring calls Claude raised: specific recommendations are `supported`,
  anecdotes are `unsupported`, a single checkable fact is `supported`, and
  point-carrying sarcasm is a `quip`.

**Pre-labelling disclosure:** All 200 labels were pre-labelled by Claude
(Anthropic) from my written definitions and decision rule. None of the 200
were changed afterwards. <!-- TODO (you): say how closely you reviewed them —
"read every one and agreed", or "spot-checked the flagged ones". Only you know
which is true. -->

Claude also wrote `collect.py`, built `labels.csv` from the pre-labels, ran
`baseline.py` and the 8-epoch improvement run (the notebook's code cells,
executed in a scratch copy so `results.json` wasn't overwritten), and drafted
this README from my decisions, notes, and results.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.467 | 0.567 | +0.100 |
| Macro F1 | 0.443 | 0.412 | -0.031 |
| F1 — `quip` | 0.444 | 0.000 | -0.444 |
| F1 — `supported` | 0.286 | 0.621 | +0.335 |
| F1 — `unsupported` | 0.600 | 0.615 | +0.015 |

Baseline: `facebook/bart-large-mnli`, zero-shot, using only
`label_definitions.txt`, on the same 30 posts in `test_split.csv`. Trained:
seed 42, 3 epochs (`results.json`).

**What my definitions were worth.** I also ran the baseline once with no
definitions file, so it saw only the bare label names
(`baseline_bare_results.json`). The table above is the definitions run.

| Measure | Bare names | With definitions | Difference |
|---|---|---|---|
| Overall accuracy | 0.300 | 0.467 | +0.167 |
| Macro F1 | 0.241 | 0.443 | +0.202 |
| F1 — `quip` | 0.286 | 0.444 | +0.158 |
| F1 — `supported` | 0.438 | 0.286 | -0.152 |
| F1 — `unsupported` | 0.000 | 0.600 | +0.600 |

The definitions are worth about 17 points of accuracy. Nearly all of it comes
from `unsupported`. The word on its own means nothing to the model (F1 0.000),
but "makes a claim, gives an opinion, or asks a question with nothing on the
page backing it" does (0.600). `supported` got worse with its definition,
which fits the main finding: the zero-shot model can't apply "something on
the page that backs the main point", and spelling that out pulled it away
from the label rather than toward it.

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->
No prediction was written down before the numbers came in. The trained results
already existed when the baseline was run, so anything written here now would
be hindsight.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->
Fine-tuning helped on one thing: telling `supported` from everything else
(F1 0.286 → 0.621). The zero-shot model reads my definition but can't apply
"something on the page that backs the main point". The trained model picked up
some of that from 140 examples. On everything else, training added nothing or
made it worse. `unsupported` is a wash (+0.015), and on `quip` the zero-shot
model beats the trained one outright (0.444 vs 0.000). On macro F1, which
weighs every label equally, the untrained baseline is slightly ahead. With
only about 24 quips to learn from, fine-tuning taught the model to stop
predicting quips at all, while a general model that just reads "a joke or
one-liner" catches about half of them.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.70 | 0.567 | 0.567 | 0.667 | MISSED |
| 2. Per-label F1 | `supported`, `unsupported` ≥ 0.65; `quip` ≥ 0.50 | 0.621 / 0.615 / 0.000 | 0.667 / 0.571 / 0.000 | 0.769 / 0.690 / 0.000 | MISSED |
| 3. Balance | every label 20–50% | quip 17.5% | quip 17.5% | quip 17.5% | MISSED |
| 4. Confidence gap | top third ≥ 15 pts above bottom third | 0.50 vs 0.50 (+0) | 0.70 vs 0.40 (+30) | 0.80 vs 0.70 (+10) | MISSED |
| 5. Self-agreement | ≥ 85% on 30 relabelled cold | — | — | — | NOT YET MEASURED |

Criterion 2 is shown as `supported` / `unsupported` / `quip`. Criterion 3 is a
property of `labels.csv`, so it's the same for every seed. All three runs are
in `results_three_seeds_before.json`. All three runs were on CPU (torch
2.14.1+cpu), 3 epochs. The file was first written with `RUN_LABEL = "after"`
by mistake and renamed to `_before`, since no improvement had been made yet.

**The spread.** Accuracy was 0.567, 0.567, 0.667: a 10-point swing, right at
the line where the measure stops being stable. Each seed gets a different
30-post test split, so one seed's test set being friendlier is worth 3 posts.
Macro F1 moved less (0.412 → 0.486), held down in every seed by `quip` at
0.000. My dataset is small and lopsided enough that a single seed's accuracy
shouldn't be trusted to within about 10 points. That's mostly down to 200
posts, with only 5 quips in each test split.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

Seed 42:

| true \ predicted | supported | unsupported | quip |
|---|---|---|---|
| **supported** | 9 | 3 | 0 |
| **unsupported** | 5 | 8 | 0 |
| **quip** | 3 | 2 | 0 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->
5 real `unsupported` posts were called `supported`, and only 3 went the other
way. The model leans toward `supported` on my hardest boundary, but only
mildly: in seed 2024 it's 3 against 2. The bigger story is the `quip` column.
It's all zeros in every seed. The model never predicted a quip once, so all 5
real quips were absorbed into the other two labels.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.70 in all three seeds | MISSED | Best seed was 0.667; two seeds were 0.567 |
| 2 | Per-label F1 | `supported`/`unsupported` ≥ 0.65, `quip` ≥ 0.50 | MISSED | `quip` F1 was 0.000 in every seed; `unsupported` was below 0.65 in seeds 42 and 7; `supported` below 0.65 in seed 42 |
| 3 | Balance | every label 20–50% | MISSED | `quip` is 35/200 = 17.5% |
| 4 | Confidence gap | ≥ 15 points in all three seeds | MISSED | Gaps of 0, 30 and 10 points; only seed 7 cleared it |
| 5 | Self-agreement | ≥ 85% | NOT YET MEASURED | <!-- TODO (you): pick 30 random rows of labels.csv, hide the label column, relabel them yourself, and count matches. Because the labels were pre-labelled by Claude, this compares you against Claude's labels, which is worth saying when you report it. --> |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

**Criteria 2 and 3: `quip` has too few examples.** 35 quips total means about
24 in training and 5 in test. The model never predicted `quip` in any seed, and
the miss doesn't move between seeds the way a noisy-but-learnable label would.
It's zero every time. Criterion 3 already flagged this before training. It's
not an inconsistency in how I applied the rule: the quips are the easiest
posts in the set to recognise by eye. There just aren't enough of them.

**Criterion 1: the model barely learned anything.** Mean confidence on its
predictions was about 0.43–0.50 across seeds. For three labels, pure guessing
gives 0.33, so the model is close to undecided on almost every post. With 140
training posts and 3 epochs, that suggests a task this model can't reach from
this much data (or this little training), more than a single bad boundary.

**Criterion 4: confidence doesn't separate right from wrong.** It follows from
the same cause. When every prediction sits near 0.45, the "most confident
third" isn't meaningfully more confident than the rest, and the gap swings
from 0 to 30 points depending on the seed.

**The `supported`/`unsupported` boundary: labelling or model?** The mild lean
toward `supported` (5 vs 3) could be a genuinely hard pair, or me applying the
"single checkable fact" rule inconsistently. The agreement report is what
separates those two.
<!-- TODO (you): once the agreement report is done, use it here. If your
disagreements with staff land mostly in pile (a), the boundary problem is your
labelling; if they don't, it's the pair itself. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- TODO (you): NOT DONE YET. This needs two things that aren't in the repo:
     your own labels for the 30 posts in data/staff_posts.csv (applying
     data/staff_taxonomy.md, not your taxonomy), and data/staff_labels.csv from
     your TF. Then run `python agreement.py --mine my_labels.csv` and fill in
     this section from its output. It has to be your labelling. It's the one
     instrument that tests you, not the model. -->


<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:** Epochs, from 3 to 8. That's the only change: same
`labels.csv`, same seeds, learning rate 2e-5, batch size 16, 128 tokens.

**Which diagnosis pointed at it:** Criteria 1 and 4. In the before-run the
model's mean confidence was about 0.45 on a three-way choice (guessing is
0.33), so it was close to undecided on almost every post. That looked like a
model that hadn't trained long enough, more than one specific bad boundary.

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.70 | 0.600 | 0.633 | 0.600 | MISSED |
| 2. Per-label F1 | `supported`, `unsupported` ≥ 0.65; `quip` ≥ 0.50 | 0.667 / 0.645 / 0.000 | 0.720 / 0.667 / 0.000 | 0.667 / 0.667 / 0.000 | MISSED |
| 3. Balance | every label 20–50% | quip 17.5% | quip 17.5% | quip 17.5% | MISSED |
| 4. Confidence gap | top third ≥ 15 pts above bottom third | 0.80 vs 0.70 (+10) | 0.70 vs 0.50 (+20) | 0.90 vs 0.40 (+50) | MISSED |
| 5. Self-agreement | ≥ 85% on 30 relabelled cold | — | — | — | NOT YET MEASURED |

Criterion 2 is shown as `supported` / `unsupported` / `quip`. All three runs
are in `results_three_seeds_after.json`.

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->
A little, and not enough to change any verdict.

- **Accuracy** averaged 0.611 across seeds, against 0.600 before. That's
  about one more post right out of 30, which is within the seed-to-seed
  spread. Seed 2024 actually went down (0.667 → 0.600).
- **The two main labels did improve consistently.** `supported` F1 is now
  0.667–0.720 in every seed, clearing 0.65 each time. `unsupported` cleared
  0.65 in two seeds and just missed in the third (0.645). Criterion 2 would
  have been met for those two labels if `quip` weren't in it.
- **Confidence now means something.** Mean confidence when right rose from
  about 0.45 to about 0.70, and the confident third is more accurate than the
  unsure third in every seed (+10, +20, +50). The +10 in seed 42 is what keeps
  criterion 4 a miss.
- **`quip` didn't move at all.** It's still F1 0.000 in every seed. Training
  longer made the model more sure of itself on the two labels it has data for.
  It didn't create a label it has about 24 examples of. Quips now go mostly to
  `unsupported` (4 of 5 in every seed), where before they were split.

So the diagnosis was half right. Under-training was real: the confidence
change shows it. But it wasn't what was holding accuracy down. The `quip`
shortage is.



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

- **Criterion 3 (balance) and the `quip` part of criterion 2.** The fix is
  more quips, about 25 more to reach 40 at 20%, and 8% of r/math posts are
  quips, so roughly 300 more candidates to read. `collect.py` appends, so
  that's one command plus labelling time. The other option is to fold `quip`
  into `unsupported` and run two labels, which the baseline suggests the data
  can't support as three anyway. I stopped because the unit allows one
  improvement, and I spent it on the training length.
- **Criterion 1 (accuracy ≥ 0.70).** With `quip` stuck at zero, 5 of every 30
  test posts are wrong before the model tries, which caps accuracy at 0.83.
  The realistic gains are more quips and raising `MAX_LENGTH` to 256, so long
  `supported` posts aren't cut off before their evidence.
- **Criterion 4 (confidence gap).** It's now positive in every seed but
  below 15 points in one. Each third is only 10 posts, so one post moves the
  gap by 10 points. A bigger test set would say more than another setting
  change.
- **Criterion 5 and the agreement report** are not done yet. Those are what
  would show whether the `supported`/`unsupported` errors are my labelling or
  the model.

**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->
I meant `quip` to capture posts that make their point through a joke, but the
model learned that every post is either `supported` or `unsupported`. Every
real quip in every seed lands in one of those two columns, mostly
`unsupported`. On the boundary I worried about most, it did learn something
real: the `supported`↔`unsupported` errors are now 3 and 3 or 4 and 3 in each
seed, balanced rather than leaning one way.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
