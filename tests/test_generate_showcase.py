import base64
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "generate_showcase.py"
spec = importlib.util.spec_from_file_location("generate_showcase", SCRIPT)
generate_showcase = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_showcase)


class GenerateShowcaseTests(unittest.TestCase):
    def test_build_showcase_prompt_uses_style_and_logo_color(self):
        dark_prompt = generate_showcase.build_showcase_prompt("MUNSUN", "void", "Family office")
        light_prompt = generate_showcase.build_showcase_prompt("MUNSUN", "clinical", "Family office")

        self.assertIn("THE VOID", dark_prompt)
        self.assertIn("pure white (#FFFFFF)", dark_prompt)
        self.assertIn("MUNSUN", dark_prompt)
        self.assertIn("CLINICAL STUDIO", light_prompt)
        self.assertIn("pure black (#000000)", light_prompt)

    def test_extract_image2_payload_accepts_common_response_shapes(self):
        raw = base64.b64encode(b"png-bytes").decode("ascii")

        self.assertEqual(
            generate_showcase.extract_image2_payload({"data": [{"b64_json": raw}]}),
            ("b64", raw),
        )
        self.assertEqual(
            generate_showcase.extract_image2_payload({"result": {"url": "result-image.png"}}),
            ("url", "result-image.png"),
        )

    def test_build_image2_form_data_requests_base64_response(self):
        data = generate_showcase.build_image2_form_data("prompt", "gpt-image-2-pro")

        self.assertEqual(data["model"], "gpt-image-2-pro")
        self.assertEqual(data["prompt"], "prompt")
        self.assertEqual(data["response_format"], "b64_json")

    def test_build_image2_configs_uses_fallback_after_primary(self):
        configs = generate_showcase.build_image2_configs(
            primary_key="primary-key",
            primary_url="primary-url",
            primary_model="primary-model",
            fallback_key="fallback-key",
            fallback_url="fallback-url",
            fallback_model="fallback-model",
        )

        self.assertEqual([config["name"] for config in configs], ["primary", "fallback"])
        self.assertEqual(configs[1]["api_key"], "fallback-key")
        self.assertEqual(configs[1]["image_edit_url"], "fallback-url")
        self.assertEqual(configs[1]["model"], "fallback-model")

    def test_build_image2_configs_allows_fallback_only(self):
        configs = generate_showcase.build_image2_configs(
            primary_key="",
            primary_url="",
            primary_model="primary-model",
            fallback_key="fallback-key",
            fallback_url="fallback-url",
            fallback_model="fallback-model",
        )

        self.assertEqual(len(configs), 1)
        self.assertEqual(configs[0]["name"], "fallback")

    def test_parser_exposes_image2_provider_settings(self):
        parser = generate_showcase.build_parser()
        args = parser.parse_args([
            "MUNSUN",
            "logo.png",
            "--provider",
            "image2",
            "--image2-model",
            "gpt-image-2-pro",
        ])

        self.assertEqual(args.provider, "image2")
        self.assertEqual(args.image2_model, "gpt-image-2-pro")


if __name__ == "__main__":
    unittest.main()
