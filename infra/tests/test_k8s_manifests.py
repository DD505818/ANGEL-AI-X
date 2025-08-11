"""Simple tests ensuring Kubernetes manifests are well-formed."""
from pathlib import Path
import unittest
import yaml


class TestK8sManifests(unittest.TestCase):
    """Verify that Kubernetes YAML files parse correctly."""

    def test_manifests_parse(self) -> None:
        base = Path(__file__).resolve().parents[1] / "k8s"
        for name in ("network-policy.yaml", "resource-quota.yaml"):
            with self.subTest(file=name):
                path = base / name
                manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
                self.assertIn("apiVersion", manifest)
                self.assertIn("kind", manifest)


if __name__ == "__main__":
    unittest.main()
