import pygame
import random
import math

# Initialize Pygame
pygame.init()

class Button:
    def __init__(self, x, y, width, height, text, font, text_color, bg_color, border_color, on_click):
        """
        Initializes a Button object with specified properties.

        Args:
            x (int): X-coordinate of the button.
            y (int): Y-coordinate of the button.
            width (int): Width of the button.
            height (int): Height of the button.
            text (str): Text displayed on the button.
            font (pygame.font.Font): Font used for the button text.
            text_color (tuple): RGB color of the button text.
            bg_color (tuple): RGB color of the button background.
            border_color (tuple): RGB color of the button border.
            on_click (function): Function to call when the button is clicked.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.on_click = on_click
        self.border_width = 4
        self.radius = height // 2

    def draw(self, window):
        """
        Draws the button on the specified window.

        Args:
            window (pygame.Surface): The window to draw the button on.
        """
        pygame.draw.rect(window, self.bg_color, self.rect, border_radius=self.radius)
        pygame.draw.rect(window, self.border_color, self.rect, self.border_width, border_radius=self.radius)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        """
        Checks if the button has been clicked.

        Args:
            pos (tuple): The position of the mouse click.

        Returns:
            bool: True if the button was clicked, False otherwise.
        """
        return self.rect.collidepoint(pos)

    def click(self):
        """
        Executes the on_click function if the button is clicked.
        """
        if self.on_click:
            print(f"Button '{self.text}' clicked.")
            self.on_click()

def draw(draw_info, buttons, title_text):
    """
    Draws the complete visualization, including the title, buttons, and list.

    Args:
        draw_info (DrawInformation): Contains drawing and display-related information.
        buttons (list): List of Button objects to be drawn.
        title_text (str): The title text to be displayed.
    """
    draw_info.window.fill(draw_info.BLACK)
    title_surface = draw_info.LARGE_FONT.render(title_text, 1, draw_info.WHITE)
    title_rect = title_surface.get_rect(center=(draw_info.width // 2, 45))
    draw_info.window.blit(title_surface, title_rect)
    for button in buttons:
        button.draw(draw_info.window)
    draw_list(draw_info)
    pygame.display.update()

class DrawInformation:
    """
    Stores and manages drawing-related information for the visualization.
    """
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    YELLOW = 255, 255, 0

    GRADIENTS = [
        (34, 139, 34),
        (60, 179, 113),
        (144, 238, 144)
    ]

    FONT = pygame.font.SysFont('segoeuib', 28)
    LARGE_FONT = pygame.font.SysFont('segoeuib', 45)

    WIDTH_PADDING = 100
    HEIGHT_PADDING = 130

    def __init__(self, width, height, lst):
        """
        Initializes DrawInformation with window size and list to visualize.

        Args:
            width (int): Width of the display window.
            height (int): Height of the display window.
            lst (list): List of values to be visualized.
        """
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualiser")
        self.set_list(lst)

    def set_list(self, lst):
        """
        Updates the list and recalculates drawing parameters.

        Args:
            lst (list): New list of values to be visualized.
        """
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.block_width = round((self.width - self.WIDTH_PADDING) / len(lst))
        self.block_height = math.floor((self.height - self.HEIGHT_PADDING) / (self.max_val - self.min_val))
        self.start_x = self.WIDTH_PADDING // 2

    def get_list(self):
        """
        Returns the current list of values.

        Returns:
            list: Current list of values.
        """
        return self.lst

def draw_list(draw_info, color_positions={}, clear_background=False):
    """
    Draws the list of values as bars on the screen.

    Args:
        draw_info (DrawInformation): Contains drawing and display-related information.
        color_positions (dict): Dictionary mapping bar indices to colors.
        clear_background (bool): If True, clears the background before drawing the list.
    """
    lst = draw_info.get_list()

    if clear_background:
        clear_rect = (draw_info.WIDTH_PADDING // 2, draw_info.HEIGHT_PADDING,
                      draw_info.width - draw_info.WIDTH_PADDING, draw_info.height - draw_info.HEIGHT_PADDING)
        pygame.draw.rect(draw_info.window, draw_info.BLACK, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        height = draw_info.height - y

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, height))

    if clear_background:
        pygame.display.update()

def generate_list(n, min_val, max_val):
    """
    Generates a list of random integers.

    Args:
        n (int): Number of integers in the list.
        min_val (int): Minimum value of integers.
        max_val (int): Maximum value of integers.

    Returns:
        list: List of random integers.
    """
    return [random.randint(min_val, max_val) for _ in range(n)]

def bubble_sort(draw_info, ascending=True):
    """
    Bubble Sort algorithm with visualization.

    Args:
        draw_info (DrawInformation): Contains drawing and display-related information.
        ascending (bool): Sort in ascending order if True, otherwise descending.

    Yields:
        bool: Indicates progress in the sorting process.
    """
    lst = draw_info.get_list()
    n = len(lst)

    for i in range(n - 1):
        for j in range(n - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.YELLOW, j + 1: draw_info.RED}, True)
                yield True

    return lst

def insertion_sort(draw_info, ascending=True):
    """
    Insertion Sort algorithm with visualization.

    Args:
        draw_info (DrawInformation): Contains drawing and display-related information.
        ascending (bool): Sort in ascending order if True, otherwise descending.

    Yields:
        bool: Indicates progress in the sorting process.
    """
    lst = draw_info.get_list()

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.YELLOW, i: draw_info.RED}, True)
            yield True

    return lst

def main():
    """
    Main function to run the Sorting Algorithm Visualizer.
    """
    run = True
    sorting = False
    sorting_done = False
    ascending = True
    clock = pygame.time.Clock()
    clock_speed = 120

    lst_size = 50
    lst_min_val = 0
    lst_max_val = 100

    display_height = 800
    display_width = 600

    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None

    lst = generate_list(lst_size, lst_min_val, lst_max_val)
    draw_information = DrawInformation(display_height, display_width, lst)

    def reset():
        """
        Resets the visualization to the initial state.
        """
        nonlocal sorting, sorting_done, lst
        sorting = False
        sorting_done = False
        lst = generate_list(lst_size, lst_min_val, lst_max_val)
        draw_information.set_list(lst)
        update_button_text("Reset", "Start")

    def start_sort():
        """
        Starts the sorting process with the selected algorithm.
        """
        nonlocal sorting, sorting_algorithm_generator
        sorting = True
        sorting_algorithm_generator = sorting_algorithm(draw_information, ascending)

    def toggle_ascending_descending():
        """
        Toggles between ascending and descending sort order.
        """
        nonlocal ascending
        if ascending:
            ascending = False
            update_button_text("Ascending", "Descending")
        else:
            ascending = True
            update_button_text("Descending", "Ascending")

    def toggle_sort_algorithm():
        """
        Toggles between Bubble Sort and Insertion Sort algorithms.
        """
        nonlocal sorting_algorithm, sorting_algorithm_name
        if sorting_algorithm == bubble_sort:
            sorting_algorithm = insertion_sort
            sorting_algorithm_name = "Insertion Sort"
        else:
            sorting_algorithm = bubble_sort
            sorting_algorithm_name = "Bubble Sort"

        for button in buttons:
            if button.text == "Bubble Sort" or button.text == "Insertion Sort":
                button.text = sorting_algorithm_name
                break

    def toggle_reset_start():
        """
        Toggles between starting and resetting the sort.
        """
        nonlocal sorting_done
        if sorting_done:
            reset()
        else:
            start_sort()
            update_button_text("Start", "Reset")

    def update_button_text(current_text, new_text):
        """
        Updates the text of a button.

        Args:
            current_text (str): Current text of the button.
            new_text (str): New text to set on the button.
        """
        for button in buttons:
            if button.text == current_text:
                button.text = new_text
                break

    button_font = draw_information.FONT

    buttons = [
        Button(0, 0, 70, 40, "Start", button_font, draw_information.WHITE, (41, 170, 225), (6, 109, 185), toggle_reset_start),
        Button(0, 0, 150, 40, sorting_algorithm_name, button_font, draw_information.WHITE, (255, 105, 180), (180, 0, 69), toggle_sort_algorithm),
        Button(0, 0, 130, 40, "Ascending", button_font, draw_information.WHITE, (255, 165, 0), (221, 87, 28), toggle_ascending_descending),
    ]

    total_button_width = sum(button.rect.width for button in buttons)
    spacing = 10
    total_width = total_button_width + (len(buttons) - 1) * spacing

    start_x = (draw_information.width - total_width) // 2
    y_position = 80

    for button in buttons:
        button.rect.x = start_x
        button.rect.y = y_position
        start_x += button.rect.width + spacing

    title_text = "Algorithm Visualiser"

    while run:
        clock.tick(clock_speed)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
                sorting_done = True
                update_button_text("Start", "Reset")
        else:
            draw(draw_information, buttons, title_text)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_clicked(pos):
                        button.click()

    pygame.quit()

if __name__ == "__main__":
    main()
