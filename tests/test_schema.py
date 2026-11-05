import copy
import hashlib
import json
import re
import unicodedata
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
import yaml

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
            "schema_version": "0.5.0",
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

    def artifact_record(self, evidence_type):
        record = copy.deepcopy(RECORD)
        del record['no_identifier_reason']
        record.update(evidence_type=evidence_type, contestable=True,
                      quote='estimate = -0.25', quote_hash='sha256-n2:' + '0' * 64,
                      justification='The located result states the estimate.',
                      retrieved_via=evidence_type)
        artifact = {'path': 'reports/result.txt', 'sha256': 'a' * 64,
                    'locator': 'Treatment row, estimate column'}
        if evidence_type == 'analysis_output':
            record['analysis'] = {'report': artifact, 'script': {'path': 'analysis.py'}}
        else:
            record['source_code'] = artifact
        return record

    def test_reference_default_and_legacy_field(self):
        validator = Draft202012Validator(SCHEMA)
        validator.validate({**RECORD, 'evidence_type': 'reference'})
        for changes in [{'evidence_kind': 'literature'}, {'evidence_type': 'literature'},
                        {'analysis': {}}, {'source_code': {}}, {'derived_from': []}]:
            with self.subTest(changes=changes):
                self.assertFalse(validator.is_valid({**RECORD, **changes}))

    def test_artifact_evidence_requirements(self):
        validator = Draft202012Validator(SCHEMA)
        for kind in ['analysis_output', 'source_code']:
            record = self.artifact_record(kind)
            validator.validate(record)
            field = 'analysis' if kind == 'analysis_output' else 'source_code'
            for missing in [field, 'quote', 'quote_hash', 'justification']:
                with self.subTest(kind=kind, missing=missing):
                    invalid = copy.deepcopy(record)
                    del invalid[missing]
                    self.assertFalse(validator.is_valid(invalid))
            for missing in ['path', 'sha256', 'locator']:
                invalid = copy.deepcopy(record)
                artifact = invalid[field]['report'] if field == 'analysis' else invalid[field]
                del artifact[missing]
                self.assertFalse(validator.is_valid(invalid))
            for value in ['', ' ', 'SHA256:' + 'a' * 64, 'a' * 63, 'A' * 64]:
                invalid = copy.deepcopy(record)
                artifact = invalid[field]['report'] if field == 'analysis' else invalid[field]
                artifact['sha256'] = value
                self.assertFalse(validator.is_valid(invalid))
            self.assertFalse(validator.is_valid({**record, 'locator': {'page': 1}}))
            noncontestable = {**record, 'contestable': False}
            for name in ['quote', 'quote_hash', 'justification']:
                del noncontestable[name]
            validator.validate(noncontestable)
            del noncontestable['contestable_reason']
            self.assertFalse(validator.is_valid(noncontestable))

    def test_analysis_script_and_dependencies(self):
        validator = Draft202012Validator(SCHEMA)
        record = self.artifact_record('analysis_output')
        del record['analysis']['script']
        validator.validate(record)
        validator.validate({**record, 'derived_from': ['R-0002']})
        for dependencies in [['C-0002'], ['R-0002', 'R-0002'], ['']]:
            self.assertFalse(validator.is_valid({**record, 'derived_from': dependencies}))
        for script in [{}, {'path': ' '}, {'path': 'a.py', 'sha256': 'bad'}]:
            invalid = copy.deepcopy(record)
            invalid['analysis']['script'] = script
            self.assertFalse(validator.is_valid(invalid))
        invalid = copy.deepcopy(record)
        invalid['source_code'] = invalid['analysis']['report']
        self.assertFalse(validator.is_valid(invalid))

    def test_contestable_reference(self):
        record = {**RECORD, 'contestable': True, 'quote': 'Illustrative passage',
                  'quote_hash': 'sha256-n2:' + '0' * 64,
                  'justification': 'Illustration', 'locator': {'section': 'Example'}}
        validator = Draft202012Validator(SCHEMA)
        validator.validate(record)
        del record['locator']
        self.assertFalse(validator.is_valid(record))

    def test_remote_artifact_and_script_locations(self):
        validator = Draft202012Validator(SCHEMA)
        for target in ['report', 'script', 'source_code']:
            record = self.artifact_record('source_code' if target == 'source_code' else 'analysis_output')
            artifact = record['source_code'] if target == 'source_code' else record['analysis'][target]
            del artifact['path']
            artifact['url'] = 'https://example.org/archive/v1/file.py'
            with self.subTest(target=target):
                validator.validate(record)
                artifact['path'] = 'local.py'
                self.assertFalse(validator.is_valid(record))
                del artifact['path']
                for url in ['', 'https://', 'http://example.org/file', 'file:///tmp/file',
                            'https://example.org/a b', 'relative/file.py']:
                    artifact['url'] = url
                    self.assertFalse(validator.is_valid(record))
                del artifact['url']
                self.assertFalse(validator.is_valid(record))
                artifact['path'] = 'https://example.org/file.py'
                self.assertFalse(validator.is_valid(record))
                for path in ['src/model.py', '../reports/result.txt', 'C:\\project\\model.py']:
                    artifact['path'] = path
                    validator.validate(record)

    def test_optional_script_locator(self):
        validator = Draft202012Validator(SCHEMA)
        for location in [{'path': 'analysis.py'}, {'url': 'https://example.org/v1/analysis.py'}]:
            record = self.artifact_record('analysis_output')
            script = record['analysis']['script'] = dict(location)
            validator.validate(record)
            for locator in ['estimate_treatment, lines 42–48', 'Notebook cell: treatment-estimate']:
                script['locator'] = locator
                validator.validate(record)
            for locator in ['', '   ', 42, {'line': 42}]:
                script['locator'] = locator
                self.assertFalse(validator.is_valid(record))

    def test_artifact_urls_and_hashes_reject_trailing_newlines(self):
        validator = Draft202012Validator(SCHEMA)
        for target in ['report', 'script', 'source_code']:
            for field, value in [('url', 'https://example.org/file.py'), ('sha256', 'a' * 64)]:
                for ending in ['\n', '\r\n']:
                    with self.subTest(target=target, field=field, ending=repr(ending)):
                        record = self.artifact_record('source_code' if target == 'source_code' else 'analysis_output')
                        artifact = record['source_code'] if target == 'source_code' else record['analysis'][target]
                        if field == 'url':
                            del artifact['path']
                        artifact[field] = value
                        validator.validate(record)
                        artifact[field] += ending
                        self.assertFalse(validator.is_valid(record))

    def test_readme_examples(self):
        readme = (Path(__file__).resolve().parents[1] / 'README.md').read_text(encoding='utf-8')
        examples = re.findall(r'```yaml\n(.*?)```', readme, re.DOTALL)
        self.assertEqual(len(examples), 2)
        for example in examples:
            record = yaml.safe_load(example)[0]
            Draft202012Validator(SCHEMA).validate(record)
            normalized = unicodedata.normalize('NFKC', record['quote']).casefold()
            normalized = unicodedata.normalize('NFKC', normalized)
            normalized = ''.join(ch for ch in normalized if ch.isalnum())
            self.assertEqual(record['quote_hash'],
                             'sha256-n2:' + hashlib.sha256(normalized.encode('utf-8')).hexdigest())
            if record.get('evidence_type') == 'analysis_output':
                self.assertEqual(record['analysis']['report']['sha256'],
                                 hashlib.sha256(b'estimate = -0.25\n').hexdigest())
