import pygame
import sys


# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 400
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("X Drive Sim")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 36)

# Joystick parameters
joystick_radius = 127
joystick_center = (screen_width // 2, 650)
joystick_pos = joystick_center
joystick_dragging = False
joystick_relative = (joystick_center[0] - joystick_pos[0], joystick_center[1] - joystick_pos[1])

# Rotation parameters
rotation_radius = 127
rotation_center = (screen_width // 2, 850)
rotation_pos = rotation_center
rotation_dragging = False
rotation_relative = rotation_center[0] - rotation_pos[0]

v1 = 0
v2 = 0
v3 = 0
v4 = 0


def clamp(n, min, max):
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n

def calc_vel(joy_pos, rotation):
    global v1, v2, v3, v4 #fuckin what
    x = joy_pos[0]
    y = joy_pos[1]
    tv1 = x + y
    tv3 = x + y
    tv2 = y - x
    tv4 = y - x
    rv1 = rotation
    rv2 = -rotation
    rv3 = -rotation
    rv4 = rotation
    v1 = clamp(tv1 + rv1, -127, 127)
    v2 = clamp(tv2 + rv2, -127, 127)
    v3 = clamp(tv3 + rv3, -127, 127)
    v4 = clamp(tv4 + rv4, -127, 127)

def draw_wheel_vec():
    vel = [v1, v2, v3, v4]
    vec = []
    for i in range(len(vel)):
        if i % 2 == 0:
            vec.append(pygame.math.Vector2.from_polar((vel[i]/2, 315)))
        else:
            vec.append(pygame.math.Vector2.from_polar((vel[i]/2, 225)))
        # if vel[i] != 0:
        #     vec.scale_to_length(1)
        # print(f"Wheel {i}: {pygame.math.Vector2.length(vec)}")
        if i == 0:
            if vel[i] > 0:
                pygame.draw.line(screen, "red", (130, 70), (130 + vec[i][0], 70 + vec[i][1]))
            else:
                pygame.draw.line(screen, "red", (70, 130), (70 + vec[i][0], 130 + vec[i][1]))
        elif i == 1:
            if vel[i] > 0:
                pygame.draw.line(screen, "red", (270, 70), (270 + vec[i][0], 70 + vec[i][1]))
            else:
                pygame.draw.line(screen, "red", (330, 130), (330 + vec[i][0], 130 + vec[i][1]))
        elif i == 2:
            if vel[i] > 0:
                pygame.draw.line(screen, "red", (330, 270), (330 + vec[i][0], 270 + vec[i][1]))
            else:
                pygame.draw.line(screen, "red", (270, 330), (270 + vec[i][0], 330 + vec[i][1]))
        elif i == 3:
            if vel[i] > 0:
                pygame.draw.line(screen, "red", (70, 270), (70 + vec[i][0], 270 + vec[i][1]))
            else:
                pygame.draw.line(screen, "red", (130, 330), (130 + vec[i][0], 330 + vec[i][1]))
    return(vec[0] + vec[1] + vec[2] + vec[3])


# Main loop
running = True
while running:
    screen.fill(BLACK)

    # Draw joystick
    pygame.draw.circle(screen, (40, 40, 40), joystick_center, joystick_radius)
    pygame.draw.circle(screen, WHITE, joystick_pos, 15)
    # Robot
    pygame.draw.rect(screen, "green", (100, 100, 200, 200), width=2)
    # wheels
    pygame.draw.line(screen, "blue", (75, 125), (125, 75), width=2)   # 0
    pygame.draw.line(screen, "blue", (275, 75), (325, 125), width=2)  # 1
    pygame.draw.line(screen, "blue", (275, 325), (325, 275), width=2) # 2
    pygame.draw.line(screen, "blue", (75, 275), (125, 325), width=2)  # 3
    final_vec = draw_wheel_vec()
    pygame.draw.line(screen, "purple", (200, 200), (200 + final_vec[0]/2, 200 + final_vec[1]/2))
    # Text bits
    text = font.render("Translation", True, WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, 650-140))
    screen.blit(text, text_rect)
    text = font.render("Rotation", True, WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, 650+150))
    screen.blit(text, text_rect)
    # Draw Rotation Joystick
    pygame.draw.line(screen, (40, 40, 40), (rotation_center[0] - rotation_radius, rotation_center[1]), (rotation_center[0] + rotation_radius, rotation_center[1]), 10)
    pygame.draw.circle(screen, WHITE, rotation_pos, 15)
    

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                joy_distance = ((mouse_pos[0] - joystick_center[0]) ** 2 + (mouse_pos[1] - joystick_center[1]) ** 2) ** 0.5
                rot_distance = ((mouse_pos[0] - rotation_pos[0]) ** 2 + (mouse_pos[1] - rotation_pos[1]) ** 2) ** 0.5
                if joy_distance <= joystick_radius:
                    joystick_dragging = True
                if rot_distance <= 15:
                    rotation_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                joystick_dragging = False
                rotation_dragging = False
                rotation_pos = rotation_center
        elif event.type == pygame.MOUSEMOTION:
            if joystick_dragging:
                mouse_pos = pygame.mouse.get_pos()
                distance = ((mouse_pos[0] - joystick_center[0]) ** 2 + (mouse_pos[1] - joystick_center[1]) ** 2) ** 0.5
                if distance <= joystick_radius:
                    joystick_pos = mouse_pos
                else:
                    angle = pygame.math.Vector2(mouse_pos[0] - joystick_center[0], mouse_pos[1] - joystick_center[1]).normalize() * joystick_radius
                    joystick_pos = (int(joystick_center[0] + angle[0]), int(joystick_center[1] + angle[1]))
            if rotation_dragging:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] < rotation_center[0] - rotation_radius:
                    rotation_pos = (rotation_center[0] - rotation_radius, rotation_center[1])
                elif mouse_pos[0] > rotation_center[0] + rotation_radius:
                    rotation_pos = (rotation_center[0] + rotation_radius, rotation_center[1])
                else:
                    rotation_pos = (mouse_pos[0], rotation_center[1])

    
    rotation_relative = rotation_pos[0] - rotation_center[0]
    joystick_relative = (joystick_pos[0] - joystick_center[0], joystick_center[1] - joystick_pos[1])


    calc_vel(joystick_relative, rotation_relative)
    # print(f"{v1}, {v2}, {v3}, {v4}")

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()