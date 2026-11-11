import tempfile
import unittest
from pathlib import Path
from agent import plan, verify


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.config = {"source_root": "books", "blog_url": "https://blog.naver.com/example",
                       "category": "작가 > 책리뷰", "books": [
                           {"id": "a", "title": "A", "source": "a.pdf", "total_chapters": 5, "chapters_per_post": 2},
                           {"id": "b", "title": "B", "source": "b.pdf", "total_chapters": 2, "chapters_per_post": 1}]}

    def test_next_batch_and_final_odd_chapter(self):
        self.assertEqual(plan(self.config, {"completed": {"a": [1, 2]}})["chapters"], [3, 4])
        self.assertEqual(plan(self.config, {"completed": {"a": [1, 2, 3, 4]}})["chapters"], [5])

    def test_finished_book_moves_to_next_and_all_done_stops(self):
        completed = {"a": [1, 2, 3, 4, 5]}
        self.assertEqual(plan(self.config, {"completed": completed})["book_id"], "b")
        completed["b"] = [1, 2]
        self.assertIsNone(plan(self.config, {"completed": completed}))

    def test_partial_batch_refuses_to_guess(self):
        with self.assertRaises(ValueError):
            plan(self.config, {"completed": {"a": [1]}})

    def test_verification_rejects_wrong_blog_missing_evidence_and_unchecked(self):
        with tempfile.TemporaryDirectory() as folder:
            errors = verify(self.config, {"published_url": "https://blog.naver.com/other/123"}, Path(folder))
            self.assertTrue(any("URL" in e for e in errors))
            self.assertTrue(any("Missing evidence" in e for e in errors))
            self.assertTrue(any("Unverified" in e for e in errors))

    def test_complete_local_evidence_passes_and_escape_fails(self):
        import json
        manifest = json.loads(Path("manifest.example.json").read_text(encoding="utf-8"))
        manifest["published_url"] = "https://blog.naver.com/example/123"
        manifest["checks"] = dict.fromkeys(manifest["checks"], True)
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            for name in manifest["images"] + [manifest["screenshot"]]:
                (base / name).write_bytes(b"local evidence fixture")
            self.assertEqual(verify(self.config, manifest, base), [])
            manifest["screenshot"] = "../outside.png"
            self.assertTrue(verify(self.config, manifest, base))


if __name__ == "__main__":
    unittest.main()
