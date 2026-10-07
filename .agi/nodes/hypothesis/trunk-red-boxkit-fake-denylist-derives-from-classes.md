---
id: hypothesis:trunk-red-boxkit-fake-denylist-derives-from-classes
mint_id: 6cee7c4346c54301b4ca0a262b470545
type: hypothesis
parents:
  - goal:g1.31.5.1.2
next_edges: []
edited_by: director-general-2
scaffold_hash: 5dbbe18551fc58ef
season: 2
testable_claim: test_one_planted_kit_copy_goes_red_and_the_kits_own_bytes_stay_clean is green with a fake denylist built from anonymize.CLASSES and no bin/ or kit byte changed
title: "trunk red: test_boxkit_templates' fake denylist misses the email/secret classes -- derive it from anonymize.CLASSES"
town: core
---
# hypothesis:trunk-red-boxkit-fake-denylist-derives-from-classes

## Measured
SM board 13:5xZ 09-30: trunk HEAD 34cb1ce460 red on test_boxkit_templates.py::test_one_planted_kit_copy_goes_red_and_the_kits_own_bytes_stay_clean -- "the fake denylist did not reach every class". anonymize.CLASSES (anonymize.py:12) is now ("hostname", "ip", "mac", "board", "secret", "home", "email"): 'email' (+ 'secret') arrived in 30175ea7e9 (goal:g1.31.5.1.2, 08:35Z) and the test's fake denylist was never widened.

## CLAIM
The test's fake denylist is DERIVED from anonymize.CLASSES (one entry per class, so a future class needs no test edit), the row is green, and the kit's own bytes stay clean (0 hits of the real denylist over the kit): no assert removed or loosened.

## Dispatch line
kid (Sonnet 5.5, isolated worktree): FIRST run the file on the base and show the red + which classes the fake misses; then fix ONLY the test fixture. Fake values must be obviously synthetic (never a real host, address, email, key or path). config-max: none. template-max: the fixture reads CLASSES, never a typed class list.

## FALSIFIERS
1. The row red on the fix, or green on the base.
2. A diff to any bin/ file or to the kit's bytes.
3. The fake still lists classes by hand (a new CLASSES entry would red the row again).
4. Any fake value that is a real-looking secret, address or email.

## TESTS
test_boxkit_templates.py whole (one run, --basetemp under /tmp, -p no:cacheprovider); test_anonymize*.py unchanged and green.

## FILE SCOPE
extensions/agi/tests/test_boxkit_templates.py only.

## CEILING
0 production lines · tests +20.
