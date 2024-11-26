import pygame
import random
import sys
import math  # 导入 math 模块

# 初始窗口大小
PANEL_width = 800
PANEL_height = 600
FONT_PX = 15

# 生成随机颜色
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# 生成动态颜色变化
def dynamic_color(offset):
    t = pygame.time.get_ticks() / 1000  # 获取运行时间（秒）
    r = (255 * (0.5 * (1 + math.sin(t + offset)))) % 255
    g = (255 * (0.5 * (1 + math.sin(t + offset + 2)))) % 255
    b = (255 * (0.5 * (1 + math.sin(t + offset + 4)))) % 255
    return (r, g, b)

# 初始化 Pygame
pygame.init()

# 创建全屏窗口
winSur = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # 设置为全屏
PANEL_width, PANEL_height = winSur.get_size()  # 获取当前窗口大小
bg_surface = pygame.Surface((PANEL_width, PANEL_height), flags=pygame.SRCALPHA)
bg_surface.fill(pygame.Color(0, 0, 0, 28))
winSur.fill((0, 0, 0))

# 在字母列表中加入 '0' 和 '1'
letter = ['0', '1', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z',
          'x', 'c', 'v', 'b', 'n', 'm']

# 根据窗口宽度计算列数
column = int(PANEL_width / FONT_PX)
drops = [0 for _ in range(column)]
colors = [random_color() for _ in range(column)]  # 预先生成颜色
fonts = [pygame.font.SysFont('Arial', random.randint(15, 30)) for _ in range(column)]  # 预创建字体

# "1024" 的列号，假设放在屏幕中央并加大间隔
center_columns = [(column // 2) - 6, (column // 2) - 3, (column // 2), (column // 2) + 3]
center_text = ['1', '0', '2', '4']

# 定义动态调整 "1024" 字体大小
def dynamic_font_size():
    t = pygame.time.get_ticks() / 1000  # 获取运行时间（秒）
    return int(100 + 20 * math.sin(t))  # 字体大小在 100 到 120 之间波动

while True:
    # 从事件队列中获取事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # 退出程序
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_SPACE:
                pygame.quit()
                sys.exit()

    # 暂停给定的毫秒数
    pygame.time.delay(30)

    # 重新编辑图像
    winSur.blit(bg_surface, (0, 0))

    # 动态调整 "1024" 的字体大小并在屏幕中央显示
    for idx, col in enumerate(center_columns):
        center_font_size = dynamic_font_size()  # 获取动态字体大小
        center_font = pygame.font.SysFont('Arial', center_font_size)  # 动态字体
        color = dynamic_color(idx * 2)  # 根据时间变化动态调整颜色
        text = center_font.render(center_text[idx], True, color)
        # 字符之间加大间隔，高度设置为屏幕中央
        winSur.blit(text, (col * FONT_PX, PANEL_height // 2 - center_font_size // 2))

    # 随机字母雨效果
    for i in range(len(drops)):
        # 当前列不属于"1024"的列，正常显示随机字母
        if i not in center_columns:
            random_letter = random.choice(letter)
            text = fonts[i].render(random_letter, True, colors[i])
            winSur.blit(text, (i * FONT_PX, drops[i] * FONT_PX))

            # 字母下落
            drops[i] += 1

            # 如果字母超过屏幕高度或随机数触发重置
            if drops[i] * FONT_PX > PANEL_height or random.random() > 0.95:
                drops[i] = 0
                colors[i] = random_color()  # 重新生成颜色

    pygame.display.flip()
