# Teaser video

This folder contains a Manim teaser for the project.

Install the local dependency:

```bash
python -m venv /tmp/options-teaser-venv
. /tmp/options-teaser-venv/bin/activate
pip install -r teaser/requirements.txt
```

Render from the repository root with:

```bash
manim -qm --disable_caching --media_dir teaser/output teaser/teaser.py OptionsInTheWildTeaser
cp teaser/output/videos/teaser/1080p30/OptionsInTheWildTeaser.mp4 teaser/options-in-the-wild-teaser.mp4
```

The generated video is copied to:

```text
teaser/options-in-the-wild-teaser.mp4
```
