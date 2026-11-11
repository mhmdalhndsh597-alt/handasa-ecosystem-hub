import unittest

from gateway_contract import SlidingWindowLimiter, sign_request, verify_request


class GatewayContractTests(unittest.TestCase):
    def test_valid_signature_for_allowed_route(self):
        secret = "test-only-secret"
        body = b'{"title":"demo"}'
        signature = sign_request(secret, "POST", "/v1/creators/submissions", "1000", body)
        self.assertTrue(
            verify_request(
                secret=secret,
                method="POST",
                path="/v1/creators/submissions",
                timestamp="1000",
                signature=signature,
                body=body,
                now=1000,
            )
        )

    def test_rejects_stale_or_unlisted_requests(self):
        secret = "test-only-secret"
        signature = sign_request(secret, "GET", "/v1/studio/status", "1000")
        self.assertFalse(
            verify_request(
                secret=secret,
                method="GET",
                path="/v1/studio/status",
                timestamp="1000",
                signature=signature,
                now=1401,
            )
        )
        self.assertFalse(
            verify_request(
                secret=secret,
                method="DELETE",
                path="/v1/studio/status",
                timestamp="1000",
                signature=signature,
                now=1000,
            )
        )

    def test_limiter_blocks_after_limit(self):
        limiter = SlidingWindowLimiter(limit=2, window_seconds=60)
        self.assertTrue(limiter.allow("community", now=1000))
        self.assertTrue(limiter.allow("community", now=1001))
        self.assertFalse(limiter.allow("community", now=1002))
        self.assertTrue(limiter.allow("community", now=1061))


if __name__ == "__main__":
    unittest.main()
