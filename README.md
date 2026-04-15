# Logo Generator

Professional SVG logo generator with high-end showcase presentations. Generate 6+ design variants based on product characteristics, then create stunning showcase images with 12 professional background styles.

## Features

- **SVG Logo Generation**: Create geometric logos with dot matrix, line systems, and mixed compositions
- **Design Variety**: Generate 6+ distinct variants per request with different pattern types
- **Professional Showcase**: 12 curated background styles (void, frosted, fluid, spotlight, analog liquid, LED matrix, editorial, iridescent, morning, clinical, UI container, Swiss flat)
- **Nano Banana Integration**: High-end showcase images using Gemini 3.1 Flash Image Preview
- **Interactive Previews**: Beautiful HTML showcases with hover effects and smooth transitions

## Installation

### Method 1: AI-Assisted Installation (Recommended)

Simply tell your AI assistant:

```
Install the logo-generator skill from /path/to/logo-generator
```

The AI will automatically set up the skill and make it available for use.

### Method 2: Manual Installation

1. Clone or download this repository
2. Copy the `logo-generator` folder to your skills directory
3. Install Python dependencies:

```bash
cd logo-generator
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

## Usage

### Basic Workflow

1. **Start a logo project**:
   ```
   Generate a logo for my AI product called "DataFlow"
   ```

2. **Provide context** (the AI will ask):
   - Industry/Category (e.g., AI, fintech, design tools)
   - Core Concept (e.g., connection, flow, security)
   - Design Preferences (minimal/complex, cold/warm)

3. **Review variants**: The AI generates 6+ SVG logo variants with design rationale

4. **Select and refine**: Choose your favorite, request adjustments

5. **Generate showcase**: Create professional presentation images with multiple background styles

### Example Commands

```
Create a logo for a blockchain security platform

Generate 6 logo variants for "CloudSync" - a file sync tool

Show me the logo in different background styles

Export the logo as PNG at 2048x2048
```

## Workflow Phases

### Phase 1: Information Gathering
Collect product name, industry, core concept, and design preferences

### Phase 2: Pattern Matching & SVG Generation
- Generate 6+ distinct design variants
- Create interactive HTML showcase
- Explain design rationale for each variant

### Phase 3: Iteration & Refinement
- Select favorite variants
- Adjust parameters (size, spacing, rotation)
- Combine elements from different variants

### Phase 4: High-End Showcase Generation
- Export SVG to PNG (1024x1024px)
- Select 4 showcase styles based on product type
- Generate showcase images with Nano Banana
- Create final presentation webpage

### Phase 5: Delivery
- Interactive HTML showcase page
- SVG files (editable vector format)
- PNG exports (various sizes)
- Showcase images (4 professional backgrounds)

## Background Styles

### Dark Styles (6)
- **The Void** - Absolute black with silver micro noise (hardcore tech)
- **Frosted Horizon** - Titanium gray with organic texture (premium products)
- **Fluid Abyss** - Deep purple with fluid fusion (AI-native)
- **Studio Spotlight** - Carbon gray with editorial lighting (magazine quality)
- **Analog Liquid** - Metallic shimmer on solid color base (creative brands)
- **LED Matrix** - Digital retro with glowing dots (cyberpunk)

### Light Styles (6)
- **Editorial Paper** - Off-white with paper texture (humanistic brands)
- **Iridescent Frost** - Silver-gray with holographic hints (tech hardware)
- **Morning Aura** - Warm ivory with pastel colors (approachable AI)
- **Clinical Studio** - Pure white with geometric shadows (algorithm-driven)
- **UI Container** - Frosted glass container effect (SaaS platforms)
- **Swiss Flat** - Pure solid color, zero effects (timeless authority)

## Design Principles

1. **Extreme Simplicity** - 1-2 core elements maximum
2. **Generous Negative Space** - At least 40-50% empty canvas
3. **Precise Proportions** - Line weights 2.5-4px, proper spacing
4. **Visual Tension** - Intentional asymmetry creates interest
5. **Restraint Over Decoration** - Every element must justify its existence
6. **Single Focal Point** - Clear visual hierarchy

## File Structure

```
logo-generator/
├── SKILL.md                    # Skill definition and workflow
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── scripts/
│   ├── svg_to_png.py          # SVG to PNG converter
│   └── generate_showcase.py   # Showcase image generator
├── references/
│   ├── design_patterns.md     # Comprehensive design guide
│   └── background_styles.md   # Background style specifications
└── assets/
    └── showcase_template.html # HTML template for showcases
```

## Requirements

- Python 3.8+
- Dependencies: `google-genai`, `python-dotenv`, `cairosvg`, `Pillow`
- Gemini API key (for showcase generation)

## API Configuration

### Official Google Gemini API

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.1-flash-image-preview
```

### Third-Party API Endpoint

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_API_BASE_URL=https://api.example.com/v1
GEMINI_MODEL=gemini-3.1-flash-image-preview
```

## Examples

See the `examples/` directory for sample outputs:
- SVG logo variants
- Interactive HTML showcases
- Professional showcase images

## License

MIT License - feel free to use for personal or commercial projects

## Credits

- Design patterns inspired by modern brand identity systems
- Showcase styles curated from high-end design presentations
- Powered by Gemini 3.1 Flash Image Preview (Nano Banana)

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

## Support

For questions or issues, please open an issue on GitHub or contact the maintainers.
