## 🛣️ Roadmap

This project is under active development. Below is a living roadmap of what’s been completed ✅ and what’s coming up 🚧.

---

### ✅ Completed
- [x] **Seed Strategy System**
  - JSON-only seed format (no YAML).
  - Node-RED GUI for seed creation/management.
  - File convention: `strategies/seeded/YYYY-MM-DD_HHMM_slug.json`.

- [x] **Evolutionary Engine Core**
  - Stable imports, arguments, and config.
  - Per-generation outputs (`gen_0.json`, `gen_1.json`, …).
  - Final run summary (`summary.json`).
  - Working EF, Profit, Rolls, CQ, Danger metrics.

- [x] **Infrastructure & Sanity**
  - Repo structure cleaned up.
  - Sanity check script added.
  - Legal bets enforced (whole dollars, correct 6/8 handling, no impossible wagers).

---

### 🚧 In Progress
- [ ] **Strategy Seeds Expansion**
  - Add: Hot Bet Slot Machines, Hit-It-and-Quit-It, The Arnold, more hybrids.
  - Expand JSON schema fields (bets, triggers, stop rules).

- [ ] **Reporting & UI**
  - Command-line `--report` summaries.
  - Dashboard hooks: EF, CQ, bankroll curves.
  - “Hall of Shame” tracking for worst strategies.

- [ ] **Evolution Features**
  - Taxonomy-aware crossovers (Light-Side, Dark-Side, Hybrid).
  - Smarter mutation tuning (weights, thresholds).
  - Chaos Quotient penalties/bonuses for edge cases.

---

### 📍 Mid-Term
- [ ] **Strategy Taxonomy System**
  - Domain → Phylum → Class → Species classification pipeline.
  - Breeding bias within categories with occasional crossovers.

- [ ] **EF Refinement**
  - Comp-friendly play incorporated into EF scoring.
  - Balance survivability against profit.

- [ ] **Hall of Shame UI**
  - “Show Me the Idiot” button.
  - Category fail archives.

- [ ] **Dashboard Polish**
  - Roll histories, bankroll graphs, trend lines.
  - Strategy genome viewer (JSON → human-readable).

---

### 🌌 Long-Term
- [ ] **Narrator Mode**
  - Emotional/tonal summaries tagged with Table Temp, Threat Level, Vegas Vibes.
  - Integrate **Cosmic Drink Mixer™** mascot commentary.

- [ ] **Supernova Evolution**
  - Extended evolutions (100+ gens, large pops).
  - Capture best evolved strategy (*Supernova*) with full genealogy.

- [ ] **Packaging & Community**
  - GitHub releases with pre-zipped builds.
  - Documentation for Node-RED seed builder.
  - Dockerized one-command deployment.

---

_This roadmap is flexible and may evolve as the project does._
