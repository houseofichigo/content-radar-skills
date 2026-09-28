"""Layout and packaging tests for the Content Radar suite."""

import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_dist  # noqa: E402
import skill_rules as sr  # noqa: E402


class ContentRadarSuiteTest(unittest.TestCase):
    def test_exact_skill_set(self):
        found = sorted(path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(found, sorted(build_dist.SKILL_NAMES))

    def test_every_skill_passes_cross_host_validation(self):
        for root in build_dist.skill_roots():
            _, findings = sr.validate_skill_dir(root, "all")
            blockers = [item for item in findings if item[0] == "blocker"]
            self.assertEqual(blockers, [], f"{root.name}: {sr.format_findings(blockers)}")

    def test_individual_zips_match_skills(self):
        for root in build_dist.skill_roots():
            diffs = sr.compare_zip(root, ROOT / "dist" / f"{root.name}.zip", root.name)
            self.assertEqual(diffs, [], f"{root.name}: {diffs}")

    def test_bundle_contains_all_skills_and_resources(self):
        with zipfile.ZipFile(ROOT / "dist" / f"{build_dist.SUITE_NAME}.zip") as archive:
            names = set(archive.namelist())
        for name in build_dist.SKILL_NAMES:
            self.assertIn(f"{build_dist.SUITE_NAME}/skills/{name}/SKILL.md", names)
        self.assertIn(f"{build_dist.SUITE_NAME}/resources/profile.template.md", names)

    def test_distributions_are_current(self):
        self.assertEqual(build_dist.check_all(), [])


if __name__ == "__main__":
    unittest.main()
