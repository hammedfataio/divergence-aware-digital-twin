"""Verify live EXP-010 decisions through the Vite-to-FastAPI proxy."""

import json
import sys
import urllib.error
import urllib.request

BASE_URL = "http://127.0.0.1:5173"

EXPECTED = {
    "F0-A": ("allow", False),
    "F1-A": ("restrict", True),
    "F2-A": ("allow", False),
    "F3-A": ("restrict", True),
    "F4-A": ("restrict", True),
}


def main():
    passed = 0

    for scenario_id, (authority, intervene) in EXPECTED.items():
        url = f"{BASE_URL}/api/scenarios/{scenario_id}/run"

        request = urllib.request.Request(
            url,
            data=b"",
            method="POST",
            headers={"Accept": "application/json"},
        )

        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                payload = json.load(response)

            results = [
                result
                for result in payload["assurance_results"]
                if "dara" in result["policy"].lower()
            ]

            assert payload["scenario_id"] == scenario_id
            assert len(results) == 1
            assert results[0]["authority"] == authority
            assert results[0]["intervene"] is intervene

            print(f"PASS | {scenario_id} | {authority}")
            passed += 1

        except (Exception, AssertionError) as error:
            print(f"FAIL | {scenario_id} | {error}")

    print(f"\nLive integration: {passed}/{len(EXPECTED)} passed")

    return 0 if passed == len(EXPECTED) else 1


if __name__ == "__main__":
    sys.exit(main())
