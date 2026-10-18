# Milestone 1 — Community and candidate distinctions

## Community

**r/math** (public subreddit). I'm treating comments as "posts" as well as
top-level posts, since many top-level posts are images or links and most of
the variation in quality is in the comment threads.

Threads read so far: an AI-generated Navier–Stokes proof checked in Lean, an
RSA signature-forgery paper (Shea et al.), a question about whether "concrete"
statements can be undecidable, and a shared derivation of the Lagrangian.

## Candidate distinctions

### 1. How much support the post brings (main axis)

Some posts back their point with something on the page: a specific fact, a
source, a worked example, or a chain of reasoning. Others give an opinion or
ask a question with nothing behind it. Some are just quips.

- Quip: "We've finally created a real life magic 8 ball."
- Bare opinion: praising the AI paper's authors for not sensationalising, with
  no claim about what the paper says.
- Supported: the RSA comment citing NIST's integer-factorization standard and
  comparing SNFS vs. GNFS cost to argue the paper isn't worrying.
- Supported with reasoning and no facts at all: the undecidability post, which
  builds its question from Collatz vs. continuum-hypothesis examples.

The fact has to do work in the argument. Mentioning a paper isn't enough.

### 2. Question vs. claim

Some posts ask, some assert, some do both ("…AI maths becomes a complete
blackbox. Am I offbase?"). This is independent of #1: the undecidability post
is a question and one of the most substantial things I read.

### 3. Sharing/announcing vs. discussing

Some posts exist to point at something elsewhere (a paper, a blog post, their
own article) and the substance is behind a link. The Lagrangian post explains
its motivation but the actual derivation is off-page.

### 4. About the math vs. about the community, tools or culture

Most of the AI-proof thread was about how mathematicians work and what AI
means for the field, not about any mathematics. The undecidability and
Lagrangian posts are about the math itself.

## Observations to carry forward

- **Hedging is independent of support.** The RSA comment says "in my opinion"
  and is the best-supported thing I read. Tone shouldn't decide the label.
- **Label what's on the page, not what's behind a link or above in the
  thread.** "I hope you like reading Lean!" only makes sense as a reply; the
  model will never see the thread or follow a URL.
- **Long posts get truncated.** The notebook reads 128 tokens (~90–100 words).
  The undecidability post's substance starts well after that. Consider raising
  `MAX_LENGTH` to 256, or record it as a limitation.
- **URLs may become a shortcut.** If sharing posts nearly always contain links,
  the model can learn "has URL" instead of anything about content.
- **Sample is skewed so far** toward one AI-proof thread. Read more
  doing-the-math threads and simple Q&A before fixing labels.
