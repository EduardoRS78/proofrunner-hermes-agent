# Demo for a judge

1. Run `proofrunner demo`. It starts a disposable loopback store, signs in,
   adds a notebook and checks count 1 / total R$ 100,00.
2. Open the printed `report.html`; inspect all seven screenshots and the
   frozen acceptance criteria in `execution.json`.
3. Run `proofrunner demo --broken`. The same test should fail at the count
   assertion. The deliberately broken store leaves the counter at 0.
4. Show that the original expected value remains 1 and step 7 is skipped.
5. Run `proofrunner replay <the-pass-run> --allow-interactions` to demonstrate
   repeatability without additional model calls.
6. For the complete agent demonstration, run `proofrunner demo --planner
   hermes`, then a free-form journey against your authorized staging site.
   This requires configured inference and must be demonstrated before claiming
   the natural-language MVP is complete.

The first two demos use a deliberately small controlled-English parser.
They verify browser/report plumbing; they are not evidence that the Hermes
planner has been validated. A demo video should make this distinction clear.

Expected demo grammar (one instruction per line):

```text
Fill "Email" with "test@example.com"
Fill secret "Password" with "PR_TEST_PASSWORD"
Click "Sign In"
Verify visible "Dashboard"
Click "Add to cart"
Verify "cart-count" equals "1"
Verify "cart-total" equals "R$ 100,00"
```

Additional supported phrases: `Wait for "X"`, `Read "X"`,
`Select "X" with "Option label"`, `Verify enabled "X"`,
`Verify checked "X"`, `Open "https://..."`, `Verify URL "https://..."`.
Other natural language requires the Hermes planner. Unsupported controlled
instructions are rejected rather than silently ignored.
