import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA = json.loads(
    (Path(__file__).resolve().parents[1] / "evidence-ledger.schema.json").read_text(
        encoding="utf-8"
    )
)
RECORD = {
    "id": "R-0001",
    "claim_id": "C-0001",
    "claim": "An illustrative claim.",
    "claim_type": "empirical",
    "contestable": False,
    "contestable_reason": "Example only",
    "anchor": {"exact": "An illustrative claim."},
    "key": "example2026",
    "no_identifier_reason": "Invented source",
    "relation": "background",
    "retrieved_via": "pdf",
    "provenance": {"by_type": "human", "by": "Test", "date": "2026-10-30"},
}


class SchemaTests(unittest.TestCase):
    def test_valid_schema(self):
        Draft202012Validator.check_schema(SCHEMA)

    def test_noncontestable_record(self):
        Draft202012Validator(SCHEMA).validate(RECORD)

    def test_contestable_claim_requires_evidence(self):
        record = copy.deepcopy(RECORD)
        record["contestable"] = True
        self.assertFalse(Draft202012Validator(SCHEMA).is_valid(record))

    def test_focus_requires_quote(self):
        self.assertFalse(Draft202012Validator(SCHEMA).is_valid({**RECORD, "quote_focus": "phrase"}))

    def test_masked_budget_header(self):
        validator = Draft202012Validator({"$ref": "#/$defs/header", "$defs": SCHEMA["$defs"]})
        header = {
            "schema_version": "0.4.0",
            "work": {"title": "Example", "type": "manuscript"},
            "level": "masked",
            "max_words": 5,
        }
        validator.validate(header)
        for changes in [
            {"level": "full"},
            {"level": "locator"},
            {"max_words": 0},
            {"max_words": 26},
        ]:
            with self.subTest(changes=changes):
                self.assertFalse(validator.is_valid({**header, **changes}))
