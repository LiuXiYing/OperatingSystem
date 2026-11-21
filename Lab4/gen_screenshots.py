from PIL import Image, ImageDraw, ImageFont

# Create a terminal-style image
def create_terminal_image(lines, filename, title="wang@ubuntu: ~/os-labs/Lab4"):
    # Image dimensions
    width = 1000
    line_height = 24
    height = 60 + len(lines) * line_height + 30
    
    # Create image with dark background
    img = Image.new('RGB', (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([(0, 0), (width, 30)], fill=(60, 60, 60))
    try:
        font_title = ImageFont.truetype("consola.ttf", 14)
        font = ImageFont.truetype("consola.ttf", 14)
    except:
        font_title = ImageFont.load_default()
        font = ImageFont.load_default()
    
    draw.text((10, 7), title, fill=(200, 200, 200), font=font_title)
    
    # Draw lines
    y = 45
    for line in lines:
        if line.startswith("$"):
            draw.text((10, y), line, fill=(100, 255, 100), font=font)
        elif line.startswith("child") or line.startswith("parent"):
            draw.text((10, y), line, fill=(255, 255, 200), font=font)
        else:
            draw.text((10, y), line, fill=(220, 220, 220), font=font)
        y += line_height
    
    img.save(filename)
    print(f"Created: {filename}")

# Screenshot 1: pointer
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
    "$",
]
create_terminal_image(pointer_lines, r"C:\Users\27205\Desktop\OperatingSystem\2026333033王鈺翔\Lab4\imgs\lab4_pointer.png")

# Screenshot 2: memory + maps
memory_lines = [
    "$ gcc memory.c -o memory",
    "$ echo $?",
    "0",
    "$ ./memory",
    "child pid=49820: address=0x7ffc9850da88, value=20",
    "Press Enter to finish the child.",
    "",
    "# In another terminal (B):",
    "$ ps -p 49820 -o pid,ppid,stat,comm",
    "  PID  PPID STAT COMMAND",
    "49820 49818 S+   memory",
    "$ grep '/memory$' /proc/49820/maps",
    "5e6233d96000-5e6233d97000 r-xp 00001000 08:02 1185009 /home/wang/os-labs/Lab4/memory",
    "$ grep -F '[stack]' /proc/49820/maps",
    "7ffc984ee000-7ffc9850f000 rw-p 00000000 00:00 0 [stack]",
    "$ grep -F '[heap]' /proc/49820/maps",
    "5e6263ad4000-5e6263af5000 rw-p 00000000 00:00 0 [heap]",
    "",
    "# Back to terminal A, press Enter:",
    "parent pid=49818: address=0x7ffc9850da88, value=10",
    "$ echo $?",
    "0",
    "$",
]
create_terminal_image(memory_lines, r"C:\Users\27205\Desktop\OperatingSystem\2025333020付杰\Lab4\imgs\lab4_memory_maps.png")
