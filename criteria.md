# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

Overall accuracy is at least 0.70 on the held-out set, in all three seeds.

**Why this target:** Three labels means a random guesser gets about 33%, but `supported` and
`unsupported` will probably make up most of my data, so always guessing the
bigger one could reach roughly 45–50%. 0.70 sits clearly above that. I didn't
go higher because the notebook reads only 128 tokens, which cuts off the
reasoning in many long `supported` posts on r/math.

---

## 2.

`supported` and `unsupported` each have an F1 of at least 0.65 in all three seeds; `quip` has an F1 of at least 0.50.

**Why this target:** `quip` will be my smallest label in a heavily moderated sub, with maybe 6–8
posts in the test split, so its F1 will swing between seeds and gets a looser
target. The two main labels have enough data for a tighter one, and the
`supported`/`unsupported` boundary is the one my decision rule exists to make
learnable.

---

## 3.

Every label is at least 20% of the 200 posts (40 or more), and no label is more than 50%.

**Why this target:** r/math moderation removes a lot of low-effort content, so quips may be hard
to find. If I can't reach 40, that's my signal to drop to two labels. Capping
the largest label at 50% keeps "always guess `supported`" from looking like a
good model.

---

## 4.

The model's most confident third of predictions is at least 15 percentage points more accurate than its least confident third.

**Why this target:** My hardest boundary is a matter of degree (how much support counts), so
borderline posts like the AI black-box one should be the ones the model is
unsure about. If confidence doesn't separate right from wrong, the model is
guessing on the boundary rather than learning it.

---

## 5.

When I relabel 30 of my own posts cold, at least 3 days later, I agree with my original labels at least 85% of the time.

**Why this target:** In my stress test I applied the decision rule differently from my own
definition on 3 of 8 posts. This checks that the revised rule actually stuck.
The 15% allowance is for real borderline cases, which should mostly be
`supported` vs. `unsupported`.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
