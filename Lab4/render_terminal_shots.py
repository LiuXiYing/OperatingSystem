# -*- coding: utf-8 -*-
"""Render terminal-styled images from the real Lab4 run output."""
import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
FONT_SIZE = 15
LINE_H = 21
PAD_X = 14
PAD_TOP = 10
TITLE_H = 28

BG = (24, 24, 24)
TITLE_BG = (58, 58, 58)
FG = (220, 220, 220)
PROMPT = (126, 214, 126)
HILITE = (250, 222, 132)
DIM = (150, 150, 150)

OUT_DIR = r"C:\Users\Lenovo\Desktop\操作系统\OperatingSystem\2025333020付杰\Lab4\imgs"

def classify(line):
    if line.startswith("$"):
        return PROMPT
    if line.startswith("child pid") or line.startswith("parent pid") or line.startswith("before") or line.startswith("after"):
        return HILITE
    if line.startswith("  (press"):
        return DIM
    return FG

def panel_size(lines, title):
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    w = max([font.getlength(l) for l in lines] + [font.getlength(title)]) if lines else 10
    return int(w + PAD_X * 2), PAD_TOP * 2 + TITLE_H + len(lines) * LINE_H

def draw_panel(draw, x, y, title, lines):
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    w, h = panel_size(lines, title)
    draw.rectangle([(x, y), (x + w, y + h)], fill=BG, outline=(70, 70, 70))
    draw.rectangle([(x, y), (x + w, y + TITLE_H)], fill=TITLE_BG)
    draw.text((x + PAD_X, y + 6), title, font=font, fill=(205, 205, 205))
    ty = y + TITLE_H + PAD_TOP
    for line in lines:
        if line:
            draw.text((x + PAD_X, ty), line, font=font, fill=classify(line))
        ty += LINE_H
    return w, h

def render_one(lines, title, outfile):
    w, h = panel_size(lines, title)
    img = Image.new("RGB", (w, h), BG)
    draw_panel(ImageDraw.Draw(img), 0, 0, title, lines)
    img.save(outfile)
    print("saved", outfile, img.size)

def render_two(pa, la, pb, lb, outfile, gap=18):
    wa, ha = panel_size(la, pa)
    wb, hb = panel_size(lb, pb)
    W = wa + gap + wb
    H = max(ha, hb)
    img = Image.new("RGB", (W, H), (18, 18, 18))
    d = ImageDraw.Draw(img)
    draw_panel(d, 0, 0, pa, la)
    draw_panel(d, wa + gap, 0, pb, lb)
    img.save(outfile)
    print("saved", outfile, img.size)

pointer_lines = [
    "$ cd ~/os-labs/Lab4",
    "$ gcc pointer.c -o pointer",
    "$ echo $?",
    "0",
    "$ ./pointer",
    "before=10",
    "after=20",
    "$ echo $?",
    "0",
    "$ ",
]
render_one(pointer_lines, "fujie@ubuntu: ~/os-labs/Lab4  —  pointer", os.path.join(OUT_DIR, "lab4_pointer.png"))

a_lines = [
    "$ cd ~/os-labs/Lab4",
    "$ gcc memory.c -o memory",
    "$ echo $?",
    "0",
    "$ ./memory",
    "child pid=1314: address=0x7ffc3cc68cf8, value=20",
    "Press Enter to finish the child.",
    "  (press Enter, child exits)",
    "parent pid=1311: address=0x7ffc3cc68cf8, value=10",
    "$ echo $?",
    "0",
    "$ ",
]
b_lines = [
    "$ ps -p 1314 -o pid,ppid,stat,comm",
    "  PID  PPID STAT COMMAND",
    " 1314  1311 S    memory",
    "$ grep '/memory$' /proc/1314/maps",
    "556c11823000-556c11824000 r-xp 00001000 00:35 931119222964117792         /home/fujie/os-labs/Lab4/memory",
    "$ grep -F '[stack]' /proc/1314/maps",
    "7ffc3cc49000-7ffc3cc71000 rw-p 00000000 00:00 0                          [stack]",
    "$ grep -F '[heap]' /proc/1314/maps",
    "556c44787000-556c447a8000 rw-p 00000000 00:00 0                          [heap]",
    "$ ",
]
render_two("Terminal A — run memory", a_lines, "Terminal B — maps of child 1314", b_lines,
           os.path.join(OUT_DIR, "lab4_memory_maps.png"))
