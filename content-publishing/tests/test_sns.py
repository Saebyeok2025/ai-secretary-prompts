import copy
import unittest

from sns import build_plan


class SnsPlanningTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "source_root": "/private/books", "instagram_handle": "@example",
            "threads_handle": "@example", "facebook_profile": "Example profile",
            "publication_route": "instagram_connected_share", "card_count": 8,
            "books": [{"id": "crypto", "title": "Example", "source": "book.pdf",
                       "total_chapters": 46, "chapters_per_post": 2}],
        }

    def test_independent_state_and_no_mutation(self):
        state = {"completed": {"crypto": [1, 2]}}
        before = copy.deepcopy((self.config, state))
        target = build_plan(self.config, state)
        self.assertEqual(target["chapters"], [3, 4])
        self.assertEqual(len(target["cards"]), 8)
        self.assertEqual((self.config, state), before)
        self.assertNotIn("blog_url", target)

    def test_refuses_unapproved_route(self):
        self.config["publication_route"] = "direct_all_platforms"
        with self.assertRaises(ValueError):
            build_plan(self.config, {})

    def test_refuses_invalid_card_count(self):
        for value in (5, 11, True, "8"):
            self.config["card_count"] = value
            with self.assertRaises(ValueError):
                build_plan(self.config, {})

    def test_missing_account(self):
        self.config["threads_handle"] = ""
        with self.assertRaises(ValueError):
            build_plan(self.config, {})

    def test_finished(self):
        self.assertIsNone(build_plan(self.config, {"completed": {"crypto": list(range(1, 47))}}))


if __name__ == "__main__":
    unittest.main()
