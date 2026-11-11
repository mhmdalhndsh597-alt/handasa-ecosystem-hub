# FOX Studio Gateway Contract

The public community repository receives only a browser-safe Studio surface. It never receives repository secrets, payment credentials, wallet signers, or private backend URLs. Private integrations remain behind this Hub and the locked revenue/on-chain repositories.

## Request contract

The gateway accepts only these routes:

- `GET /v1/studio/status`
- `GET /v1/studio/capabilities`
- `POST /v1/creators/submissions`

Every request must include `x-fox-client-id`, `x-fox-timestamp`, and `x-fox-signature`. The signature is HMAC-SHA256 over:

```text
METHOD\nPATH\nUNIX_TIMESTAMP\nSHA256(BODY)
```

The server rejects unknown routes, unsupported methods, missing headers, invalid signatures, and timestamps older than five minutes. A sliding-window limiter is applied per client ID. Secrets are supplied at runtime through the private deployment environment and are never committed to Git.

## Boundary rules

- Public: Studio UI, contributor guidance, rights metadata, and submission hand-off.
- Private Hub: signature verification, rate limiting, capability/status responses, and routing policy.
- Locked revenue/on-chain systems: payment processing and blockchain calls only; this gateway has no signer or transfer capability.
- Production changes require a reviewed Pull Request and human approval.
