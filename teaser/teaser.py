from __future__ import annotations

import csv
from pathlib import Path

from manim import (
    BLACK,
    BOLD,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    GrowFromEdge,
    LaggedStart,
    LEFT,
    Line,
    ORIGIN,
    Rectangle,
    RIGHT,
    RoundedRectangle,
    Scene,
    Text,
    UP,
    ValueTracker,
    VGroup,
    WHITE,
    Write,
    YELLOW,
    config,
    rate_functions,
    DecimalNumber,
    Dot,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HISTORY_CSV = PROJECT_ROOT / "data" / "history.csv"
FFMPEG_FALLBACK_OPTIONS = 983

BG = "#020617"
PANEL = "#0b1020"
PANEL_2 = "#101827"
MUTED = "#94a3b8"
BLUE = "#38bdf8"
CYAN = "#22d3ee"
LIME = "#84cc16"
AMBER = "#facc15"


config.background_color = BLACK
config.frame_rate = 30
config.pixel_width = 1920
config.pixel_height = 1080


def normalize_command(command: str) -> str:
    command = command.strip()
    if command.startswith("./"):
        return command[2:]
    return command


def display_command(command: str) -> str:
    if command.startswith("toybox "):
        return command.split()[-1]
    return command


def latest_values_from_row(row: dict[str, str]) -> list[int]:
    values = []
    for key, value in row.items():
        if key.isdigit() and value:
            values.append(int(float(value)))
    return values


def latest_ffmpeg_count() -> int:
    if not HISTORY_CSV.exists():
        return FFMPEG_FALLBACK_OPTIONS

    with HISTORY_CSV.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if normalize_command(row.get("commande", "")) != "ffmpeg":
                continue

            values = latest_values_from_row(row)
            if values:
                return values[-1]

    return FFMPEG_FALLBACK_OPTIONS


def top_program_counts(limit: int = 8) -> list[tuple[str, int]]:
    fallback = [
        ("ffmpeg", 983),
        ("vdir", 99),
        ("ls", 97),
        ("tar", 73),
        ("stty", 61),
        ("sort", 59),
        ("grep", 43),
        ("date", 31),
    ]
    if not HISTORY_CSV.exists():
        return fallback[:limit]

    rows: list[tuple[str, int]] = []
    with HISTORY_CSV.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            values = latest_values_from_row(row)
            if not values:
                continue

            command = normalize_command(row.get("commande", ""))
            if not command:
                command = row.get("programme", "unknown")
            rows.append((command, values[-1]))

    rows = sorted(rows, key=lambda item: item[1], reverse=True)
    return rows[:limit] if rows else fallback[:limit]


def title_text(content: str, size: int = 62, color=WHITE) -> Text:
    return Text(content, font="Noto Sans", font_size=size, weight=BOLD, color=color)


def body_text(content: str, size: int = 34, color=WHITE) -> Text:
    return Text(content, font="Noto Sans Mono", font_size=size, color=color)


def label_text(content: str, size: int = 26, color=WHITE) -> Text:
    return Text(content, font="Noto Sans", font_size=size, color=color)


class OptionsInTheWildTeaser(Scene):
    def construct(self) -> None:
        self.background = self.make_background()
        self.add(self.background)

        ffmpeg_options = latest_ffmpeg_count()

        self.opening_titles()
        self.command_box_sequence(ffmpeg_options)
        self.ffmpeg_reveal(ffmpeg_options)
        self.compare_programs()
        self.final_title()

    def make_background(self) -> VGroup:
        base = Rectangle(width=16, height=9, fill_color=BG, fill_opacity=1, stroke_width=0)

        grid = VGroup()
        for index in range(17):
            x = -8 + index
            grid.add(Line([x, -4.6, 0], [x, 4.6, 0], stroke_color="#1e293b", stroke_width=1, stroke_opacity=0.23))
        for index in range(10):
            y = -4.5 + index
            grid.add(Line([-8, y, 0], [8, y, 0], stroke_color="#1e293b", stroke_width=1, stroke_opacity=0.18))

        tokens = VGroup()
        token_specs = [
            ("--help", -6.5, 3.4),
            ("--format", -3.1, 2.7),
            ("--codec", 4.8, 3.0),
            ("--map", -5.7, -2.9),
            ("--threads", 3.8, -3.2),
            ("--filter_complex", -1.1, -3.5),
            ("--overwrite", 5.6, 0.9),
            ("--probe", -6.9, 0.6),
            ("--progress", 1.5, 3.6),
        ]
        for token, x, y in token_specs:
            text = body_text(token, 16, color=BLUE)
            text.set_opacity(0.22)
            text.move_to([x, y, 0])
            tokens.add(text)

        top_line = Line([-6.8, 3.85, 0], [6.8, 3.85, 0], stroke_color=CYAN, stroke_width=2, stroke_opacity=0.2)
        bottom_line = Line([-6.8, -3.85, 0], [6.8, -3.85, 0], stroke_color=AMBER, stroke_width=2, stroke_opacity=0.16)

        return VGroup(base, grid, tokens, top_line, bottom_line)

    def opening_titles(self) -> None:
        question_mark = title_text("?", 280, color="#0f172a")
        question_mark.set_opacity(0.92)
        question_mark.shift(0.15 * DOWN)

        question = VGroup(
            title_text("How many command-line options", 62),
            title_text("does a single program have?", 62, color=CYAN),
        ).arrange(DOWN, buff=0.18).move_to(ORIGIN)

        underline = Line([-3.65, -1.05, 0], [3.65, -1.05, 0], stroke_color=AMBER, stroke_width=5)

        counted = VGroup(
            title_text("Nobody had really counted.", 62, color=WHITE),
            label_text("No benchmark. No catalog. No answer.", 30, color=MUTED),
        ).arrange(DOWN, buff=0.25).move_to(ORIGIN)

        did = VGroup(
            title_text("So we did.", 82, color=GREEN),
            label_text("across versions, environments, and years", 30, color=CYAN),
        ).arrange(DOWN, buff=0.25).move_to(ORIGIN)

        self.play(FadeIn(question_mark, scale=0.92), FadeIn(question, shift=0.18 * UP), run_time=0.9)
        self.play(GrowFromEdge(underline, LEFT), run_time=0.45)
        self.wait(0.8)
        self.play(FadeOut(VGroup(question, underline), shift=0.25 * DOWN), FadeOut(question_mark), run_time=0.55)

        self.play(FadeIn(counted, shift=0.22 * UP), run_time=0.75)
        self.wait(0.95)
        self.play(FadeOut(counted, shift=0.22 * DOWN), run_time=0.5)

        self.play(FadeIn(did, scale=0.92), run_time=0.75)
        self.wait(0.8)
        self.play(FadeOut(did, scale=1.04), run_time=0.55)

    def command_box_sequence(self, ffmpeg_options: int) -> None:
        terminal = RoundedRectangle(
            width=9.9,
            height=5.85,
            corner_radius=0.16,
            stroke_color="#dbeafe",
            stroke_width=2,
            fill_color=PANEL,
            fill_opacity=0.98,
        )
        terminal.shift(0.85 * LEFT)

        glow = VGroup()
        for width, opacity in ((8, 0.06), (4, 0.12), (2, 0.2)):
            halo = RoundedRectangle(width=10.0, height=5.95, corner_radius=0.18)
            halo.move_to(terminal)
            halo.set_stroke(CYAN, width=width, opacity=opacity)
            halo.set_fill(opacity=0)
            glow.add(halo)

        header = Rectangle(width=9.9, height=0.62, stroke_width=0, fill_color=PANEL_2, fill_opacity=1)
        header.align_to(terminal, UP)
        header.move_to([terminal.get_center()[0], terminal.get_top()[1] - 0.31, 0])

        dots = VGroup(
            Dot(color="#ff5f57", radius=0.055),
            Dot(color="#febc2e", radius=0.055),
            Dot(color="#28c840", radius=0.055),
        ).arrange(RIGHT, buff=0.16)
        dots.move_to(header.get_left() + 0.55 * RIGHT)

        badge = self.make_badge("counter.py", CYAN, 20)
        badge.move_to(header.get_right() + 0.9 * LEFT)

        command = body_text("$ python src/compteur/compteur.py ./ffmpeg", 24, color="#86efac")
        command.next_to(header, DOWN, buff=0.34).align_to(terminal, LEFT).shift(0.45 * RIGHT)

        box = VGroup(glow, terminal, header, dots, badge)
        self.play(FadeIn(box, scale=0.96), run_time=0.8)
        self.play(Write(command), run_time=0.9)

        option_names = [
            "-h", "-L", "-version", "-formats", "-codecs", "-decoders",
            "-encoders", "-devices", "-protocols", "-filters", "-pix_fmts",
            "-layouts", "-sample_fmts", "-colors", "-loglevel", "-report",
            "-hide_banner", "-cpuflags", "-f", "-i", "-y", "-n", "-stream_loop",
            "-ss", "-sseof", "-t", "-to", "-fs", "-itsoffset", "-itsscale",
            "-timestamp", "-metadata", "-target", "-frames", "-filter",
            "-filter_complex", "-map", "-map_metadata", "-map_chapters",
            "-c:v", "-b:v", "-r", "-s", "-aspect", "-vn", "-c:a", "-b:a",
            "-ar", "-ac", "-an", "-c:s", "-sn", "-vf", "-af", "-preset",
            "-crf", "-profile:v", "-level", "-threads", "-progress",
        ]
        classes = ["global", "format", "video", "audio", "stream", "filter"]

        def build_option_window(start_index: int) -> VGroup:
            window = VGroup()
            for offset in range(10):
                index = (start_index + offset) % len(option_names)
                category = classes[(start_index + offset) % len(classes)]
                window.add(
                    body_text(
                        f"{index + 1:03d}  {option_names[index]:<16} {category:<7} detected",
                        17,
                        color="#d6e4ff",
                    )
                )
            window.arrange(DOWN, aligned_edge=LEFT, buff=0.055)
            window.next_to(command, DOWN, buff=0.35).align_to(command, LEFT)
            return window

        rows = build_option_window(0)
        self.play(
            LaggedStart(*[FadeIn(row, shift=0.1 * UP) for row in rows], lag_ratio=0.04),
            run_time=1.0,
        )
        self.remove(*rows)
        self.add(rows)

        panel = RoundedRectangle(
            width=2.15,
            height=5.05,
            corner_radius=0.16,
            stroke_color="#334155",
            stroke_width=1.5,
            fill_color="#020617",
            fill_opacity=0.92,
        )
        panel.next_to(terminal, RIGHT, buff=0.3)

        progress_label = label_text("OPTIONS", 26, color=WHITE)
        progress_label.move_to(panel.get_top() + 0.55 * DOWN)

        counter = DecimalNumber(0, num_decimal_places=0, font_size=72, color=AMBER)
        counter.next_to(progress_label, DOWN, buff=0.15)

        found = label_text("detected", 22, color=MUTED)
        found.next_to(counter, DOWN, buff=0.06)

        bar_outline = RoundedRectangle(width=0.58, height=2.55, corner_radius=0.12, stroke_color=WHITE, stroke_width=2)
        bar_outline.next_to(found, DOWN, buff=0.32)

        def fill_center(height: float):
            return bar_outline.get_bottom() + (0.07 + height / 2) * UP

        fill = Rectangle(width=0.43, height=0.01, stroke_width=0, fill_color=LIME, fill_opacity=1)
        fill.move_to(fill_center(0.01))

        scan_line = Rectangle(width=8.35, height=0.045, stroke_width=0, fill_color=CYAN, fill_opacity=0.65)

        def place_scan_line() -> None:
            scan_line.move_to([terminal.get_center()[0] - 0.2, rows.get_top()[1] + 0.12, 0])

        place_scan_line()

        self.play(FadeIn(VGroup(panel, progress_label, counter, found, bar_outline, fill)), run_time=0.55)
        self.add(scan_line)

        counter.add_updater(lambda mob: mob.set_value(round(fill.height / 2.4 * ffmpeg_options)))

        for step, start_index in enumerate((10, 20, 30, 40, 50, 0), start=1):
            target_height = 2.4 * step / 6
            next_rows = build_option_window(start_index)
            self.remove(rows, *rows)
            self.add(next_rows)
            rows = next_rows
            place_scan_line()
            scan_line.set_opacity(0.65)
            self.play(
                fill.animate.stretch_to_fit_height(target_height).move_to(fill_center(target_height)),
                scan_line.animate.shift(2.65 * DOWN).set_opacity(0.0),
                rate_func=rate_functions.ease_in_quad,
                run_time=0.52,
            )

        counter.clear_updaters()
        counter.set_value(ffmpeg_options)
        self.wait(0.35)

        scene_group = VGroup(
            box,
            command,
            rows,
            panel,
            progress_label,
            counter,
            found,
            bar_outline,
            fill,
            scan_line,
        )
        self.play(FadeOut(scene_group, shift=0.18 * DOWN), run_time=0.65)
        self.remove(rows, *rows, scan_line)

    def ffmpeg_reveal(self, ffmpeg_options: int) -> None:
        intro = label_text("ffmpeg exposes", 42, color=MUTED)
        number = DecimalNumber(0, num_decimal_places=0, font_size=154, color=AMBER)
        unit = title_text("OPTIONS", 78, color=WHITE)
        group = VGroup(intro, number, unit).arrange(DOWN, buff=0.05).move_to(ORIGIN)

        burst = VGroup()
        burst_specs = [
            ("-codec", -4.8, 1.7), ("-map", 4.5, 1.8), ("-filter", -5.3, -1.1),
            ("-preset", 4.8, -1.2), ("-threads", -2.7, 2.65), ("-progress", 2.85, -2.55),
            ("-vf", -1.8, -2.65), ("-b:v", 2.0, 2.65),
        ]
        for flag, x, y in burst_specs:
            item = body_text(flag, 24, color=CYAN)
            item.move_to([x, y, 0])
            item.set_opacity(0.78)
            burst.add(item)

        tracker = ValueTracker(0)
        number.add_updater(lambda mob: mob.set_value(tracker.get_value()))

        self.play(FadeIn(intro, shift=0.15 * UP), FadeIn(number, scale=0.82), run_time=0.55)
        self.play(
            tracker.animate.set_value(ffmpeg_options),
            FadeIn(unit, shift=0.22 * UP),
            LaggedStart(*[FadeIn(item, scale=0.82) for item in burst], lag_ratio=0.05),
            rate_func=rate_functions.ease_out_quad,
            run_time=1.15,
        )
        number.clear_updaters()
        number.set_value(ffmpeg_options)
        self.wait(0.55)

        second = title_text("but it is not only ffmpeg", 54, color=CYAN)
        second.move_to(ORIGIN)
        self.play(FadeOut(VGroup(group, burst), scale=1.05), run_time=0.55)
        self.play(FadeIn(second, scale=0.92), run_time=0.65)
        self.wait(0.75)
        self.play(FadeOut(second, shift=0.25 * DOWN), run_time=0.5)

    def compare_programs(self) -> None:
        data = top_program_counts(limit=8)
        max_value = max(value for _, value in data)

        headline = title_text("Thousands of flags. Hundreds of choices.", 40, color=WHITE)
        headline.to_edge(UP, buff=0.42)

        chart_width = 11.0
        chart_height = 3.55
        baseline_y = -1.95
        left_x = -5.55
        slot = chart_width / len(data)

        y_axis = Line([left_x, baseline_y, 0], [left_x, baseline_y + chart_height + 0.15, 0], stroke_color="#e2e8f0", stroke_width=2)
        x_axis = Line([left_x, baseline_y, 0], [left_x + chart_width + 0.25, baseline_y, 0], stroke_color="#e2e8f0", stroke_width=2)
        top_label = body_text(f"{max_value}", 20, color=MUTED).next_to(y_axis.get_top(), LEFT, buff=0.18)

        bars = VGroup()
        names = VGroup()
        values = VGroup()
        for index, (name, value) in enumerate(data):
            bar_height = max(0.06, chart_height * value / max_value)
            color = AMBER if index == 0 else (CYAN if index % 2 == 0 else "#60a5fa")
            x = left_x + slot * index + slot * 0.5

            bar = RoundedRectangle(
                width=slot * 0.48,
                height=bar_height,
                corner_radius=0.045,
                stroke_color=color,
                stroke_width=1.5,
                fill_color=color,
                fill_opacity=0.88,
            )
            bar.move_to([x, baseline_y + bar_height / 2, 0])
            bars.add(bar)

            visible_name = display_command(name)
            name_label = label_text(visible_name, 20 if len(visible_name) <= 8 else 16, color="#d1d5db")
            name_label.next_to(bar, DOWN, buff=0.22)
            names.add(name_label)

            value_label = body_text(str(value), 19, color=AMBER if index == 0 else "#bfdbfe")
            value_label.next_to(bar, UP, buff=0.12)
            values.add(value_label)

        caption = title_text("flags that people will NEVER use", 44, color=AMBER)
        caption.to_edge(DOWN, buff=0.38)

        self.play(FadeIn(headline, shift=0.2 * DOWN), run_time=0.65)
        self.play(FadeIn(VGroup(y_axis, x_axis, top_label)), run_time=0.45)
        self.play(LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.08), run_time=1.05)
        self.play(FadeIn(names, shift=0.12 * DOWN), FadeIn(values, shift=0.12 * UP), run_time=0.5)
        self.play(FadeIn(caption, shift=0.22 * UP), run_time=0.6)
        self.wait(1.8)
        self.play(FadeOut(VGroup(headline, y_axis, x_axis, top_label, bars, names, values, caption)), run_time=0.75)

    def final_title(self) -> None:
        title = title_text("Options in the Wild", 92, color=WHITE)
        subtitle = title_text("Measuring options people never counted", 38, color="#cbd5e1")
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.22).move_to(0.35 * UP)

        badges = VGroup(
            self.make_badge("coreutils", "#60a5fa", 22),
            self.make_badge("toybox", "#34d399", 22),
            self.make_badge("ffmpeg", AMBER, 22),
        ).arrange(RIGHT, buff=0.2)
        badges.next_to(title_group, DOWN, buff=0.55)

        self.play(FadeIn(title, scale=0.92), run_time=0.8)
        self.play(FadeIn(subtitle, shift=0.2 * UP), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(badge, shift=0.12 * UP) for badge in badges], lag_ratio=0.12), run_time=0.6)
        self.wait(3.4)
        self.play(FadeOut(VGroup(title_group, badges, self.background)), run_time=1.15)
        self.wait(0.25)

    def make_badge(self, text: str, color: str, font_size: int) -> VGroup:
        label = label_text(text, font_size, color=color)
        box = RoundedRectangle(
            width=label.width + 0.38,
            height=label.height + 0.2,
            corner_radius=0.08,
            stroke_color=color,
            stroke_width=1.4,
            fill_color="#020617",
            fill_opacity=0.72,
        )
        box.move_to(label)
        return VGroup(box, label)
