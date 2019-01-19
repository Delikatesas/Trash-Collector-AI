import contextlib
with contextlib.redirect_stdout(None):
    import pygame

# Customizable settings below
# ----------------------------------------------------------------------------------------------------------------
colors = {"white": (255, 255, 255), "grey": (212, 212, 212), "purple": (128, 0, 128), "green": (0, 255, 0),
          "red": (255, 0, 0), "blue": (0, 0, 255), "orange": (255, 153, 51), "custom_color": (0, 0, 0)}

colors["custom_color"] = (50, 128, 50)
background_colors = [colors["white"], colors["grey"]]
# ------------------------------------------------------------------------------------------------------------------


def trigger_questions():
    new_size = 15
    new_res = (1020, 600)
    saiz = input("Game cell size: ")
    if saiz != "":
        new_size = int(saiz)
    scr_res1 = input("Screen resolution WIDTH: ")
    scr_res2 = input("Screen resolution HEIGHT: ")
    if scr_res1 != "":
        new_res = (int(scr_res1), int(scr_res2))
    return new_size, new_res


def questions2():
    new_fps = 50
    tail = False
    speed = input("Game speed in Frames Per Second (in range of 1-200): ")
    if speed != "":
        new_fps = int(speed)
    tail_q = input("Show Garbage Man's trail (True/False): ")
    if tail_q != "":
        tail = tail_q
    return new_fps, tail


def color_choice(rinkinys):
    print("Choose a color from ")
    print(rinkinys)
    trash_color = "purple"
    robot_color = "custom_color"
    trash_q = input("Trash color: ")
    if trash_q != "":
        trash_color = trash_q
    robot_q = input("Garbage man color: ")
    if robot_q != "":
        robot_color = robot_q
    return trash_color, robot_color


print("Welcome, Mr. X! Please insert the settings for the Garbage Man:\n\n *just click enter for default values*\n")

cell_size, screen_res = trigger_questions()
while screen_res[0] % cell_size != 0 or screen_res[1] % cell_size != 0:
    print("Unacceptable screen resolution. Please make sure resolution is divisible by Cell Size")
    cell_size, screen_res = trigger_questions()

FPS, trail = questions2()

selection = []
for key in colors:
    selection.append(key)

a, b = color_choice(selection)
spawn_color = colors[a]
AI_color = colors[b]

center = [int(i / 2) // cell_size * cell_size for i in screen_res]
screen = pygame.display.set_mode(screen_res)
pygame.display.set_caption("Trash Collector -- PRE-ORDER NOW!!!")
fps_clock = pygame.time.Clock()

# FAIL SAFE assert creates a check for errors i.e. shitty cell size
assert screen_res[0] % cell_size == 0, "Unacceptable screen resolution"
assert screen_res[1] % cell_size == 0, "Unacceptable screen resolution"


class Dot:
    def __init__(self, color, pos=center):
        self.color = color
        self.pos = pos

    def draw(self, pos):
        self.pos = pos
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(pos[0], pos[1], cell_size, cell_size))


AI = Dot(AI_color)
spawn = Dot(spawn_color)
temp = Dot(background_colors[0])


def create_background(resolution):
    background = pygame.Surface(resolution)
    y = 0
    while y < resolution[1]:
        x = 0
        while x < resolution[0]:
            row = y // cell_size
            col = x // cell_size
            pygame.draw.rect(
                background,
                # mind-blowing color selection based on remainder of 0 or 1
                background_colors[(row + col) % 2],
                pygame.Rect(x, y, cell_size, cell_size))
            x += cell_size
        y += cell_size
    return background


def trash_collector():
    pygame.init()
    screen.blit(create_background(screen_res), (0, 0))  # blit draws the item on the surface at coordinates
    spawnlist = []
    closest_at = center
    x_or_y = "y"

    running = True

    while running:

        # everything here is run for each Frame

        closest_so_far = 99999
        for x, y in spawnlist:  # get the closest coordinates
            comparable_sum = abs(AI.pos[0] - x) + abs(AI.pos[1] - y)
            if comparable_sum < closest_so_far:
                closest_at = [x, y]
                closest_so_far = comparable_sum

        if not trail:
            temp.color = background_colors[(AI.pos[0] // cell_size + AI.pos[1] // cell_size) % 2]
            temp.draw(AI.pos)

        if AI.pos == closest_at:
            if spawnlist:
                spawnlist.remove(closest_at)
            else:
                pass
        else:
            if x_or_y == "y":
                if AI.pos[1] == closest_at[1]:  # cuts right back to while loop with xory = x
                    x_or_y = "x"
                    continue
                elif AI.pos[1] > closest_at[1]:
                    AI.pos[1] -= cell_size
                elif AI.pos[1] < closest_at[1]:
                    AI.pos[1] += cell_size
                x_or_y = "x"

            else:
                if AI.pos[0] == closest_at[0]:
                    x_or_y = "y"
                    continue
                elif AI.pos[0] > closest_at[0]:
                    AI.pos[0] -= cell_size
                elif AI.pos[0] < closest_at[0]:
                    AI.pos[0] += cell_size
                x_or_y = "y"

        AI.draw(AI.pos)

        # event driven operations below

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                spawn.pos = [i // cell_size * cell_size for i in pygame.mouse.get_pos()]
                spawn.draw(spawn.pos)
                spawnlist.append(spawn.pos)

            if event.type == pygame.QUIT:
                running = False  # change the value to False, to exit the main loop

        pygame.display.flip()  # update the screen and tick the time
        fps_clock.tick(FPS)


trash_collector()
