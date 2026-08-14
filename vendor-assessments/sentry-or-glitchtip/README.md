# Sentry or GlitchTip (processor — error tracking)

- Role: error telemetry; vendor choice itself is a compliance decision
  (SaaS with egress vs. self-hosted GlitchTip)
- Required artifacts: DPA (SaaS option) or hosting documentation (self-hosted),
  scrubbing rules evidence
- Controls: error payloads scrubbed of personal data before egress
  (`policies/11-logging-monitoring.md` req. 5)
- Status: decision pending — self-host preferred if scrubbing cannot be evidenced
- Next review: 2027-08-15
