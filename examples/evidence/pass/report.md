# ProofRunner Test Report

**PASS** — Acceptance journey

Target: http://127.0.0.1:33475/
Started: 2026-09-16T02:36:13.445184+00:00
Duration: 1.08s
Planner: controlled

## Steps

### 01 · PASS · fill Email

Expected: fill
Observed: Field filled (value omitted)

![Step 1](screenshots/step-01.png)

### 02 · PASS · fill_secret Password

Expected: fill_secret
Observed: Field filled (value omitted)

![Step 2](screenshots/step-02.png)

### 03 · PASS · click Sign In

Expected: click
Observed: Click completed; see subsequent assertions for acceptance

![Step 3](screenshots/step-03.png)

### 04 · PASS · assert_visible Dashboard

Expected: assert_visible
Observed: Element visible

![Step 4](screenshots/step-04.png)

### 05 · PASS · click Add to cart

Expected: click
Observed: Click completed; see subsequent assertions for acceptance

![Step 5](screenshots/step-05.png)

### 06 · PASS · assert_text cart-count

Expected: 1
Observed: 1

![Step 6](screenshots/step-06.png)

### 07 · PASS · assert_text cart-total

Expected: R$ 100,00
Observed: R$ 100,00

![Step 7](screenshots/step-07.png)

## Reproduction

Replay the frozen plan (fresh browser; same test data required):

```sh
proofrunner replay <run-directory> --allow-interactions
```

Screenshots show observed state; root causes are not inferred from a failed assertion.