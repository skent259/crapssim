# CrapsSim Engine API Bible

This document tracks the narrative history and intent behind the CrapsSim Engine API, including major phases and design decisions.

### Phase 3 — Python Support & Packaging Hardening

Phase 3 is about making the Engine API feel like a first-class, optional Python package rather than a loose collection of HTTP helpers.

The goals are:

- Be explicit about which Python versions the API targets.
- Keep the core CrapsSim engine free from new mandatory dependencies.
- Treat `crapssim_api` as an optional wrapper that can be installed separately or via an extra.
- Align local development, CI, and documentation around the same installation story.

P3·A (this step) is planning-only: we are writing down the support window, dependency groups, and installation model. Future steps will update packaging metadata, INSTALLING docs, and CI so that everything matches the same picture.
