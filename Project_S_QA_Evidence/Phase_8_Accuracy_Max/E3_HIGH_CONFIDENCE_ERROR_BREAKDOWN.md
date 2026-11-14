# E3 high-confidence error breakdown

**Verified / Tested — dev only; legacy cross-generation comparison.** See
`E1_AGGREGATION_AND_RISK_COVERAGE.md`, section “The 110 high-confidence errors”.
Among 156 path-(i) pooled errors at confidence >=0.64: 110 share the same
wrong label across three legacy components and pooled; 21 have all legacy
components wrong but not the same wrong label; 25 do not have all three legacy
components wrong. This does not establish current-v2 component agreement.

**Tested:** Gold five-way counts: contradictory 2, correct 68, irrelevant 2,
partial 84, non-domain 0. Dataset counts: Beetle 65, SciEntsBank 91. Split
counts: seen 40, unseen 116. Dev results are optimistic.
