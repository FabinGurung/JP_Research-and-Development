# OpenSees validation lane

This lane independently checks the existing thesis structural demo without replacing or silently editing the governed MDM data.

## Current scope

`mdm_two_span_validation.py` reads `data/website_demo_data.json`, rebuilds `SAMPLE_MDM_001` as a 2D linear-elastic OpenSeesPy model, and compares:

- AB and BC member-end moments;
- support reactions at A, B and C;
- global vertical equilibrium.

The source model is interpreted as:

- A: fixed support;
- B: continuous intermediate support, vertical translation restrained and rotation free;
- C: fixed support;
- AB: 6 m, EI = 25,000 kN·m², UDL = 10 kN/m downward;
- BC: 6 m, EI = 25,000 kN·m², unloaded.

The script does **not** mutate `website_demo_data.json`.

## Reproducible run

```bash
python -m pip install -r analysis/opensees/requirements.txt
python analysis/opensees/mdm_two_span_validation.py
```

For a CI failure whenever any stored value differs from OpenSees:

```bash
python analysis/opensees/mdm_two_span_validation.py --strict
```

The default report is written to:

`analysis/opensees/results/mdm_two_span_validation.json`

## Baseline reconciliation finding

A separate direct-stiffness check made before adding this lane found that the stored member-end moments are consistent with the stated beam and support interpretation, while the stored member reactions are not consistent with those moments. The OpenSees run is intentionally designed to verify that independently rather than changing the thesis dataset to match an assumption.

Expected elastic solution for the stated support interpretation:

- member end moments in the source MDM sign convention: AB = (-37.5, +15.0) kN·m; BC = (-15.0, -7.5) kN·m;
- total support reactions: A = 33.75 kN, B = 30.00 kN, C = -3.75 kN;
- total vertical reaction = 60.00 kN = applied UDL resultant.

The present stored aggregate reactions are A = 38.75 kN, B = 22.50 kN, C = -1.25 kN. They also sum to 60 kN, so global equilibrium alone cannot detect the inconsistency; member equilibrium and end-moment compatibility are required.

## Boundary

This is a validation/verification lane. It is not yet a general building-design engine and it does not claim that OpenSees reproduces ETABS design modules. Subsequent lanes can extend the normalized model toward 1–3 storey frame checks, modal analysis, response spectrum, P-Delta, pushover and time-history analysis after the input model and governing-code assumptions are explicitly defined.
