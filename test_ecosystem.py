import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from ecosystem_sdk import EcosystemClient
from grants_manager import build_grant, main


class EcosystemTests(unittest.TestCase):
    def test_grant_requires_review_and_multisig(self):
        proposal = build_grant({"full_name": "x/y"}, Decimal("1000"), ["audit"])
        self.assertEqual(proposal["status"], "pending_review")
        self.assertFalse(proposal["payout_enabled"])
        self.assertTrue(proposal["requires_multisig_approval"])

    def test_sdk_is_read_only(self):
        request = EcosystemClient("https://api.example", "runtime-secret").build_metrics_request("demo")
        self.assertEqual(request["method"], "GET")
        self.assertTrue(request["read_only"])
        self.assertNotIn("runtime-secret", str(request))
        self.assertNotIn("<from-secret-store>", request["headers"]["X-Api-Key"] if request["headers"] else "")

    def test_grant_rejects_zero(self):
        with self.assertRaises(ValueError):
            build_grant({}, Decimal("0"), ["audit"])

    def test_missing_grant_amount_skips_without_creating_proposal(self):
        with TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "proposal.json"
            with patch.dict("os.environ", {"GRANT_AMOUNT_USD": "", "GRANT_OUTPUT": str(output)}):
                self.assertEqual(main(), 0)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
