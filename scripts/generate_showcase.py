#!/usr/bin/env python3
"""
Generate logo showcase images using Gemini/Nano Banana or an Image2-compatible
image edit endpoint supplied by environment variables.
"""

import argparse
import base64
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import requests
from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

SKILL_DIR = Path(__file__).resolve().parents[1]
load_dotenv(SKILL_DIR / ".env")
load_dotenv(SKILL_DIR / ".env.local", override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_BASE_URL = os.getenv("GEMINI_API_BASE_URL", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-image-preview")

IMAGE2_API_KEY = os.getenv("IMAGE2_API_KEY")
IMAGE2_IMAGE_EDIT_URL = os.getenv("IMAGE2_IMAGE_EDIT_URL", "").strip()
IMAGE2_MODEL = os.getenv("IMAGE2_MODEL", "gpt-image-2-pro")
IMAGE2_FALLBACK_API_KEY = os.getenv("IMAGE2_FALLBACK_API_KEY")
IMAGE2_FALLBACK_IMAGE_EDIT_URL = os.getenv("IMAGE2_FALLBACK_IMAGE_EDIT_URL", "").strip()
IMAGE2_FALLBACK_MODEL = os.getenv("IMAGE2_FALLBACK_MODEL", IMAGE2_MODEL)
IMAGE2_SIZE = os.getenv("IMAGE2_SIZE", "2048x1152")
IMAGE2_RESPONSE_FORMAT = os.getenv("IMAGE2_RESPONSE_FORMAT", "b64_json")
IMAGE2_TIMEOUT = int(os.getenv("IMAGE2_TIMEOUT", "300"))

BACKGROUND_STYLES = {
    "void": """THE VOID (绝对虚空)
Absolute black (#000000) background with extremely fine silver/white high-contrast micro noise.
Cold, sharp electronic film grain texture. Minimal atmosphere light - only a faint, icy white or blue glow
at the extreme corner, like distant starlight at the edge of the universe.""",

    "frosted": """FROSTED HORIZON (磨砂穹顶)
Deep titanium gray or midnight slate gray base, not pure black. Organic film-like dust noise texture,
resembling unpolished rough metal or stone surface. Large area but extremely low saturation cold-toned
light halo (low-saturation gray-blue), edges completely dissolved like mist.""",

    "fluid": """FLUID ABYSS (流体深渊)
Deep midnight purple or extremely dark Klein blue base. Noise texture with slight color tint,
blending with the base to create deep-sea sediment or nebula texture. Fluid fusion light -
dark orange on right side, dark blue on left side, slowly interweaving in the dark space center.""",

    "spotlight": """STUDIO SPOTLIGHT (物理影棚)
Extremely dark warm carbon gray base. Slightly larger grain simulating low-light camera photography,
like paper print grain in weak light. Single-side softbox or spotlight creating natural vignette,
editorial magazine quality with professional photography feel.""",

    "analog_liquid": """ANALOG LIQUID (物理流体)
Solid color base - choose ONE color only: vibrant orange (#FF6B00), Klein blue (#002FA7), or lime green (#00FF41).
Physical liquid textures with metallic shimmer overlaying the solid base - gold dust flow, metallic mica powder
suspended in liquid, iridescent pigments creating rainbow oil slick effects. Dry mineral textures like crushed
gemstones. Macro photography of natural materials - copper oxidation, rust patterns, gold leaf fragments.
Extreme grainy texture like thermal imaging or pushed film grain. Create maximum contrast between chaotic
organic texture and ultra-clean sharp vector logo.""",

    "led_matrix": """LED MATRIX (数字硬件)
Black background with glowing dot matrix patterns creating waves of light. Simulate old-school CRT displays,
LED billboards, or halftone printing dots. Retro computer display artifacts with modern execution.
Waves of glowing points creating depth, logo as solid entity floating above. Cyberpunk and retro-futurism
aesthetics with hardcore geek appeal.""",

    "editorial": """EDITORIAL PAPER (纸本编辑)
Off-white, alabaster, or pearl white base (not pure white). High-grade watercolor or rough art paper
texture suggesting physical paper tactile quality. Natural light diffuse reflection with slight warm
gray vignette in corners. Humanistic, independent magazine aesthetic.""",

    "iridescent": """IRIDESCENT FROST (幻彩透砂)
Extremely light silver-gray or cold white base, creating calm, rational experimental space.
Extremely fine micro noise, simulating high-density frosted glass or sandblasted aluminum surface.
Restrained holographic/iridescent atmosphere light - faint low-saturation light purple, light blue
or soft pink fluid diffused light in the clean background depth, like through thick frosted glass.""",

    "morning": """MORNING AURA (晨雾光域)
Warm ivory or extremely light cream color base. Soft noise blending into base like morning mist or dust,
creating thin layer of atmospheric haze. Large area blurred low-saturation pastel colors (mint green,
baby blue, dawn orange) dissolving into warm white. Warm, intelligent, pressure-free atmosphere.""",

    "clinical": """CLINICAL STUDIO (无菌影棚)
Pure white or extremely light cold gray base. High-frequency sharp cold-toned digital micro noise with
enhanced sharpness. Pure light/shadow structure - large softbox from top/side creating smooth gray-white
gradient. Sterile space with geometric order, creating 3D depth in 2D presentation.""",

    "ui_container": """UI CONTAINER (容器化界面)
Clean gradient or solid color background with minimal digital noise. Frosted glass container effect
(like app icon base) with rounded corners and subtle transparency. Micro-shadows creating depth illusion.
UI-native presentation suggesting interactivity and digital product context. Logo sits in transparent
container with modern interface design language.""",

    "swiss_flat": """SWISS FLAT (瑞士扁平)
100% pure solid color background - deep vintage green, rich burgundy, or classic navy. Absolutely no
gradients, no noise, no effects. Pure graphic design with zero tricks. Just perfect color and form.
Extreme confidence and timeless authority. Classic Swiss International Style with absolute flatness."""
}


def load_reference_image(image_path: str) -> Optional[str]:
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"Error loading reference image: {e}")
        return None


def build_showcase_prompt(logo_name: str, style: str, product_description: str = "") -> str:
    if style not in BACKGROUND_STYLES:
        raise ValueError(f"Unknown style '{style}'. Available: {list(BACKGROUND_STYLES.keys())}")

    dark_styles = {"void", "frosted", "fluid", "spotlight", "analog_liquid", "led_matrix"}
    logo_color = "pure white (#FFFFFF)" if style in dark_styles else "pure black (#000000)"

    return f"""Extract the core graphic from the reference image as a pure flat single-color vector structure,
removing all decorations. Use high-contrast atmosphere background, delicate film grain noise,
and rigorous micro-typography to create a cutting-edge, restrained, and highly digital order showcase effect.

LOGO PROCESSING:
- Strip background and outer frames
- Extract core graphic only, preserve graphic details
- Extremely flat: 100% solid color flat vector in {logo_color}
- Sharp, clear edges
- The logo MUST be rendered in {logo_color} to ensure maximum contrast with the background

BACKGROUND CONSTRUCTION:
{BACKGROUND_STYLES[style]}

TYPOGRAPHY AND LAYOUT:
Use classic Swiss-style typography logic with extreme proportion contrast.

- Main subject centered: Place the pure flat logo graphic at the absolute visual center with huge breathing space
- Micro-typography: Remove any large, obtrusive titles. Use extremely small font size (6pt to 9pt)
  and clean sans-serif fonts (Inter, Helvetica, Geist) in corners or bottom center
- Text content suggestions (strictly aligned):
  Left corner: {logo_name.upper()}
  Right corner: v. 1.0.0 // 2026
  Bottom center: {product_description.upper() if product_description else 'DIGITAL IDENTITY SYSTEM'}

CRITICAL: The logo graphic MUST be {logo_color}, perfectly centered, extracted from the reference image,
rendered as pure flat vector with sharp edges."""


def extract_image2_payload(response_json: Any) -> Optional[Tuple[str, str]]:
    if isinstance(response_json, dict):
        if isinstance(response_json.get("b64_json"), str):
            return "b64", response_json["b64_json"]
        if isinstance(response_json.get("url"), str):
            return "url", response_json["url"]
        for key in ("data", "result", "output"):
            found = extract_image2_payload(response_json.get(key))
            if found:
                return found
    elif isinstance(response_json, list):
        for item in response_json:
            found = extract_image2_payload(item)
            if found:
                return found
    return None


def build_image2_form_data(prompt: str, model: str) -> Dict[str, str]:
    return {
        "model": model,
        "prompt": prompt,
        "size": IMAGE2_SIZE,
        "n": "1",
        "response_format": IMAGE2_RESPONSE_FORMAT,
    }


def build_image2_configs(
    primary_key: Optional[str] = IMAGE2_API_KEY,
    primary_url: str = IMAGE2_IMAGE_EDIT_URL,
    primary_model: str = IMAGE2_MODEL,
    fallback_key: Optional[str] = IMAGE2_FALLBACK_API_KEY,
    fallback_url: str = IMAGE2_FALLBACK_IMAGE_EDIT_URL,
    fallback_model: str = IMAGE2_FALLBACK_MODEL,
) -> list:
    configs = []
    if primary_key and primary_url:
        configs.append({
            "name": "primary",
            "api_key": primary_key,
            "image_edit_url": primary_url,
            "model": primary_model,
        })
    if fallback_key and fallback_url:
        configs.append({
            "name": "fallback",
            "api_key": fallback_key,
            "image_edit_url": fallback_url,
            "model": fallback_model,
        })
    return configs


def save_image_payload(payload: Tuple[str, str], output_path: str, api_key: Optional[str] = None) -> None:
    kind, value = payload
    if kind == "b64":
        Path(output_path).write_bytes(base64.b64decode(value))
        return
    if kind == "url":
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        response = requests.get(value, headers=headers, timeout=IMAGE2_TIMEOUT)
        response.raise_for_status()
        Path(output_path).write_bytes(response.content)
        return
    raise ValueError(f"Unsupported image payload kind: {kind}")


def generate_showcase_image2(
    logo_name: str,
    reference_image_path: str,
    style: str,
    output_path: str,
    product_description: str = "",
    model: str = IMAGE2_MODEL,
) -> bool:
    configs = build_image2_configs(primary_model=model)
    if not configs:
        print("Error: IMAGE2_API_KEY and IMAGE2_IMAGE_EDIT_URL not set in environment")
        print("Optional fallback: IMAGE2_FALLBACK_API_KEY and IMAGE2_FALLBACK_IMAGE_EDIT_URL")
        return False

    try:
        prompt = build_showcase_prompt(logo_name, style, product_description)
    except ValueError as e:
        print(f"Error: {e}")
        return False

    print(f"Generating showcase image with style: {style}")

    for index, config in enumerate(configs, start=1):
        print(f"Using Image2 {config['name']} provider ({index}/{len(configs)})")
        print(f"Using Image2 model: {config['model']}")
        try:
            with open(reference_image_path, "rb") as image:
                response = requests.post(
                    config["image_edit_url"],
                    headers={"Authorization": f"Bearer {config['api_key']}"},
                    data=build_image2_form_data(prompt, config["model"]),
                    files={"image": (Path(reference_image_path).name, image, "image/png")},
                    timeout=IMAGE2_TIMEOUT,
                )
            if response.status_code >= 400:
                print(f"Error: Image2 {config['name']} request failed ({response.status_code}): {response.text[:500]}")
                continue

            try:
                response_json = response.json()
            except json.JSONDecodeError:
                print(f"Error: Image2 {config['name']} returned non-JSON response: {response.text[:500]}")
                continue

            payload = extract_image2_payload(response_json)
            if not payload:
                print(f"Error: No image found in Image2 {config['name']} response: {str(response_json)[:500]}")
                continue

            save_image_payload(payload, output_path, config["api_key"])
            print(f"✓ Showcase image saved: {output_path}")
            return True
        except Exception as e:
            print(f"Error generating Image2 showcase image with {config['name']} provider: {e}")

    print("Error: all Image2 providers failed")
    return False


def generate_showcase_image_gemini(
    logo_name: str,
    reference_image_path: str,
    style: str,
    output_path: str,
    product_description: str = "",
) -> bool:
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not set in environment")
        return False
    if genai is None or types is None:
        print("Error: google-genai package not installed.")
        print("Install with: pip install google-genai")
        return False

    reference_image_b64 = load_reference_image(reference_image_path)
    if not reference_image_b64:
        return False

    try:
        prompt = build_showcase_prompt(logo_name, style, product_description)
    except ValueError as e:
        print(f"Error: {e}")
        return False

    try:
        client_config = {"api_key": GEMINI_API_KEY}
        if GEMINI_API_BASE_URL:
            client_config["http_options"] = {"api_endpoint": GEMINI_API_BASE_URL}

        client = genai.Client(**client_config)
        contents = [
            types.Part.from_bytes(
                data=base64.b64decode(reference_image_b64),
                mime_type="image/png"
            ),
            types.Part.from_text(text=prompt)
        ]

        print(f"Generating showcase image with style: {style}")
        print(f"Using Gemini model: {GEMINI_MODEL}")
        if GEMINI_API_BASE_URL:
            print("Using custom Gemini API endpoint")

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                    image_size="2K"
                )
            )
        )

        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                image.save(output_path)
                print(f"✓ Showcase image saved: {output_path}")
                return True
            if part.text is not None:
                print(f"Model response: {part.text}")

        print("Error: No image generated in response")
        return False
    except Exception as e:
        print(f"Error generating Gemini showcase image: {e}")
        return False


def generate_showcase_image(
    logo_name: str,
    reference_image_path: str,
    style: str,
    output_path: str,
    product_description: str = "",
    provider: str = "gemini",
    image2_model: str = IMAGE2_MODEL,
) -> bool:
    if provider == "image2":
        return generate_showcase_image2(
            logo_name,
            reference_image_path,
            style,
            output_path,
            product_description,
            image2_model,
        )
    return generate_showcase_image_gemini(
        logo_name,
        reference_image_path,
        style,
        output_path,
        product_description,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate logo showcase images using Gemini/Nano Banana or Image2"
    )
    parser.add_argument("logo_name", help="Name of the logo/product")
    parser.add_argument("reference_image", help="Path to reference logo image (PNG)")
    parser.add_argument("--style",
                        choices=list(BACKGROUND_STYLES.keys()),
                        default="iridescent",
                        help="Background style")
    parser.add_argument("--output", "-o",
                        help="Output path (default: output/{logo_name}_{style}.png)")
    parser.add_argument("--description", "-d",
                        default="",
                        help="Product description for context")
    parser.add_argument("--all-styles",
                        action="store_true",
                        help="Generate all 12 styles")
    parser.add_argument("--provider",
                        choices=["gemini", "image2"],
                        default=os.getenv("SHOWCASE_PROVIDER", "gemini"),
                        help="Image generation provider")
    parser.add_argument("--image2-model",
                        default=IMAGE2_MODEL,
                        help="Image2 model, e.g. gpt-image-2 or gpt-image-2-pro")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    if args.all_styles:
        success_count = 0
        for style in BACKGROUND_STYLES.keys():
            output_path = output_dir / f"{args.logo_name}_{style}.png"
            if generate_showcase_image(
                args.logo_name,
                args.reference_image,
                style,
                str(output_path),
                args.description,
                args.provider,
                args.image2_model,
            ):
                success_count += 1

        print(f"\n✓ Generated {success_count}/{len(BACKGROUND_STYLES)} showcase images")
        return

    output_path = args.output or output_dir / f"{args.logo_name}_{args.style}.png"
    success = generate_showcase_image(
        args.logo_name,
        args.reference_image,
        args.style,
        str(output_path),
        args.description,
        args.provider,
        args.image2_model,
    )
    raise SystemExit(0 if success else 1)


if __name__ == "__main__":
    main()
