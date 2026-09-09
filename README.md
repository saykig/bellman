# Bellman

Bellman is a research programme for making consequential decisions easier to understand,
inspect and correct. It asks what we can reasonably conclude when information is incomplete,
the future is uncertain, and other people can respond to what we do.

We make the assumptions explicit, work out what follows from them, and keep the evidence
needed to revisit the answer. The guiding aim is:

> Make consequential decision-making mathematically inspectable, cumulative, and correctable.

Suppose someone makes a promise and puts money at stake. They can share or withhold evidence,
and later they may benefit from breaking the agreement. Under a specified model, Bellman can
check whether keeping the promise remains worthwhile at each decision point. Whether that
model describes real people is a further question we need evidence to answer.

A question runs through the whole programme: **what information do we need to preserve for
the decisions that come next?** Two histories can suggest the same action today while carrying
different implications for tomorrow. We want to know when simplifying them is safe—and when
it changes the conclusion.

## What we're working on

The repository brings together mathematical proofs, reproducible checks and early empirical
research. Current work includes:

- **Decisions under uncertainty:** what remains justified across several possible explanations,
  including when some causal outcomes are unknown.
- **Evidence and credible promises:** how disclosure, remembered information, monitoring and
  incentives affect a proposed arrangement.
- **Learning from observations:** reproducing human experiments, comparing explanations and
  testing which parts of history help us understand behavior.

These are specific, limited results. A calculation can be correct for a model while the model
is wrong for the situation. Testing and improving that connection is part of the research.
We build on established mathematics and keep failures and revisions alongside successes.

## Bellman, Decision Lab and Writ

Bellman develops the mathematics and its limits.
[Decision Lab](https://github.com/saykig/writ-decision-lab) is a small computational test bench
for putting selected results to work. Writ is the companion engineering effort for keeping
sources, modelling choices, decisions and revisions connected over time. The
[architecture guide](docs/programme/ARCHITECTURE.md) explains what is implemented and what
still needs to be earned.

## Explore the work

- [Purpose and ambition](foundations/BELLMAN_NORTH_STAR.md)
- [Current progress and open questions](docs/programme/ROADMAP.md)
- [Human trust experiment and findings](research/empirical_trust_2016/README.md)
- [Run the current checks](verification/measurement_acceptance/README.md)
- [v0.0.7: Decisions, evidence, and credible promises](https://github.com/saykig/bellman/releases/tag/v0.0.7)
- [Research history](docs/history/README.md), including earlier results, corrections and stopped experiments
