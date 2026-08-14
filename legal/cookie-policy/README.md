# Cookie Policy & Consent Banner Spec

Two artifacts:

1. `cookie-policy.md` — versioned cookie disclosure (categories, purposes,
   lifetimes, third parties incl. processors from the vendor register).
2. `banner-spec.md` — **server-side enforcement contract** for the consent
   banner: no non-essential cookies/scripts before consent; reject path as
   prominent as accept; withdrawal as easy as grant; consent state stored
   server-side (`ConsentRecord`), not only client-side.

The spec is a compliance contract: CI/acceptance tests in the product repo
verify banner behavior against it (G4 evidence).
