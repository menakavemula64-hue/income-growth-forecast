from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 720, 405
FPS = 8
BG = "#F3F7F4"
INK = "#17251F"
MUTED = "#718078"
GREEN = "#167A56"
PALE_GREEN = "#E5F4EB"
CORAL = "#C46145"
AMBER = "#BB792B"
WHITE = "#FFFFFF"
LINE = "#E4EBE6"
FONT_REGULAR = "C:/Windows/Fonts/arial.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def label(draw, xy, text, size=13, fill=MUTED, bold=False):
    draw.text(xy, text, font=font(size, bold), fill=fill)


def draw_base():
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    rounded(draw, (28, 24, 66, 62), 11, GREEN)
    label(draw, (39, 31), "+", 27, WHITE, True)
    label(draw, (78, 29), "INCOME GROWTH FORECAST", 16, INK, True)
    label(draw, (78, 49), "PERSONAL INCOME ANALYTICS", 9, MUTED, True)
    rounded(draw, (594, 28, 691, 56), 14, PALE_GREEN)
    label(draw, (607, 36), "PRIVATE BY DESIGN", 9, GREEN, True)
    return image, draw


def draw_chart(draw, box, forecast=False):
    x1, y1, x2, y2 = box
    rounded(draw, box, 14, WHITE, LINE)
    label(draw, (x1 + 17, y1 + 14), "INCOME TREND", 10, MUTED, True)
    label(draw, (x1 + 17, y1 + 31), "Monthly earnings", 14, INK, True)
    chart_left, chart_top = x1 + 24, y1 + 67
    chart_right, chart_bottom = x2 - 18, y2 - 22
    for i in range(3):
        y = chart_top + i * ((chart_bottom - chart_top) / 2)
        draw.line((chart_left, y, chart_right, y), fill=LINE, width=1)
    points = [(0.0, 0.77), (.17, .68), (.34, .72), (.51, .48), (.68, .54), (.83, .30), (1.0, .17)]
    coords = [(int(chart_left + px * (chart_right - chart_left)), int(chart_top + py * (chart_bottom - chart_top))) for px, py in points]
    observed = coords[:5]
    draw.line(observed, fill=GREEN, width=4, joint="curve")
    for px, py in observed:
        draw.ellipse((px - 4, py - 4, px + 4, py + 4), fill=GREEN, outline=WHITE, width=1)
    if forecast:
        draw.line(coords[4:], fill=CORAL, width=4, joint="curve")
        for px, py in coords[5:]:
            draw.ellipse((px - 4, py - 4, px + 4, py + 4), fill=CORAL, outline=WHITE, width=1)
    for index, month in enumerate(["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL"]):
        x = chart_left + index * ((chart_right - chart_left) / 6)
        label(draw, (int(x - 10), chart_bottom + 7), month, 8)


def draw_metric(draw, x, y, width, title, value, color=INK):
    rounded(draw, (x, y, x + width, y + 76), 12, WHITE, LINE)
    label(draw, (x + 12, y + 12), title.upper(), 9, MUTED, True)
    label(draw, (x + 12, y + 34), value, 19, color, True)


def draw_scene(scene):
    image, draw = draw_base()
    if scene == 0:
        rounded(draw, (30, 91, 690, 360), 22, "#173C30")
        label(draw, (61, 123), "A CLEARER VIEW OF YOUR EARNINGS", 11, "#A8D9BC", True)
        label(draw, (60, 160), "Make your income", 34, WHITE, True)
        label(draw, (60, 202), "history useful.", 34, WHITE, True)
        label(draw, (62, 263), "See your pattern. Explore what's next.", 15, "#D6E8DC")
        rounded(draw, (62, 305, 249, 339), 10, "#E5F4EB")
        label(draw, (79, 315), "INCOME FORECAST", 11, GREEN, True)
        draw_chart(draw, (388, 119, 658, 330), True)
    elif scene == 1:
        label(draw, (42, 94), "01  /  ADD YOUR EARNINGS", 11, GREEN, True)
        label(draw, (42, 116), "Upload the spreadsheet you already use.", 23, INK, True)
        rounded(draw, (42, 161, 678, 342), 16, WHITE, LINE)
        rounded(draw, (61, 184, 659, 252), 12, BG, "#B7C8BD", 2)
        label(draw, (80, 198), "Date", 11, MUTED, True)
        label(draw, (264, 198), "Source / Category", 11, MUTED, True)
        label(draw, (533, 198), "Amount", 11, MUTED, True)
        for index, values in enumerate([
            ("Jan 15, 2025", "Salary", "$4,200.00"),
            ("Feb 15, 2025", "Salary", "$4,350.00"),
            ("Mar 15, 2025", "Freelance", "$680.00"),
        ]):
            y = 270 + index * 21
            label(draw, (62, y), values[0], 11, INK)
            label(draw, (264, y), values[1], 11, MUTED)
            label(draw, (536, y), values[2], 11, INK, True)
        label(draw, (44, 356), "Excel template: Date  ·  Source/Category  ·  Amount", 11, MUTED)
    elif scene == 2:
        label(draw, (42, 94), "02  /  SPOT THE PATTERN", 11, GREEN, True)
        label(draw, (42, 116), "Turn rows into a useful overview.", 23, INK, True)
        draw_metric(draw, 42, 161, 198, "Income to date", "$13,580")
        draw_metric(draw, 261, 161, 198, "Average per day", "$226")
        draw_metric(draw, 480, 161, 198, "Month growth", "+15.6%", GREEN)
        draw_chart(draw, (42, 253, 678, 371), False)
    elif scene == 3:
        label(draw, (42, 94), "03  /  EXPLORE A FUTURE PERIOD", 11, GREEN, True)
        label(draw, (42, 116), "Model a possible next step.", 23, INK, True)
        draw_chart(draw, (42, 161, 427, 353), True)
        rounded(draw, (447, 161, 678, 353), 16, WHITE, LINE)
        label(draw, (466, 181), "FORECAST HORIZON", 9, MUTED, True)
        rounded(draw, (466, 201, 659, 239), 9, BG, LINE)
        label(draw, (479, 213), "90 days", 13, INK, True)
        label(draw, (466, 259), "ESTIMATED INCOME", 9, MUTED, True)
        label(draw, (466, 278), "$15,150", 24, GREEN, True)
        rounded(draw, (466, 317, 556, 341), 12, PALE_GREEN)
        label(draw, (477, 323), "R²   88%", 10, GREEN, True)
        label(draw, (564, 323), "Trend fit", 9, MUTED)
    else:
        rounded(draw, (30, 91, 690, 360), 22, WHITE, LINE)
        label(draw, (62, 121), "A LITTLE MORE CLARITY, EVERY DAY", 11, GREEN, True)
        label(draw, (61, 157), "Spot growth. Compare months.", 28, INK, True)
        label(draw, (61, 194), "Plan ahead with context.", 28, INK, True)
        draw_metric(draw, 62, 252, 174, "Your history", "Organized")
        draw_metric(draw, 253, 252, 174, "Your trend", "Visible")
        draw_metric(draw, 444, 252, 174, "Your forecast", "Estimated", CORAL)
        label(draw, (62, 342), "Your spreadsheet stays in your browser. Forecasts are estimates, not promises.", 10, MUTED)

    draw.rounded_rectangle((28, 386, 692, 390), radius=2, fill=LINE)
    progress_x = 28 + int(664 * (scene + 1) / 5)
    draw.rounded_rectangle((28, 386, progress_x, 390), radius=2, fill=GREEN)
    return image


def main():
    output_dir = Path(__file__).parent / "assets"
    output_dir.mkdir(exist_ok=True)
    scenes = [draw_scene(index) for index in range(5)]
    frames = []
    for index, scene in enumerate(scenes):
        frames.extend([scene.copy() for _ in range(8)])
        if index < len(scenes) - 1:
            next_scene = scenes[index + 1]
            for step in range(1, 4):
                frames.append(Image.blend(scene, next_scene, step / 4))
    scenes[0].save(output_dir / "income-growth-forecast-promo.gif", save_all=True, append_images=frames[1:], duration=125, loop=0, optimize=True, disposal=2)
    scenes[0].save(output_dir / "income-growth-forecast-poster.png", optimize=True)
    draw_scene(1).save(output_dir / "income-upload-preview.png", optimize=True)
    draw_scene(2).save(output_dir / "income-dashboard-preview.png", optimize=True)
    draw_scene(3).save(output_dir / "income-forecast-preview.png", optimize=True)
    print(f"Created {len(frames)} frames in {output_dir}")
    print(f"GIF size: {(output_dir / 'income-growth-forecast-promo.gif').stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
