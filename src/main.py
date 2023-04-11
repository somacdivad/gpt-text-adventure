import logging
import random
import sys
from pprint import pprint

import pyfiglet

from generator.title import generate_title
from generator.story import generate_story
from generator.subplot import generate_subplot
from generator.prompt import generate_prompt

DEFAULT_THEMES = [
    "epic space battle",
    "old west gunslinger",
    "fantasy",
    "cold war espionage",
]

logging.basicConfig(
    filename='game.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
)

logger = logging.getLogger('game')
logger.info("Starting new game")

if len(sys.argv) > 1:
    theme = sys.argv[1]
else:
    theme = random.choice(DEFAULT_THEMES)

# Generate the title and description of the game
title = generate_title(theme)
logger.debug("Generated title: %s", title)

# Display the game title
pyfiglet.print_figlet(title["title"], font="standard")

# Display the game description
print(f"""
{title["description"]}

=========================================
""")

# Generate the plot of the game
story = generate_story(title)
# Run the game
scene_idx = 0
while scene_idx < len(story):
    # Display the scene
    scene = story[scene_idx]
    # Display the scene title and objective
    pyfiglet.print_figlet(scene["title"], font="smslant")
    print(f"{scene['scenario']}")
    # Generate the scene's subplot
    subplot = generate_subplot(title, scene)
    # Run the scene
    story_point_idx = 0
    while story_point_idx < len(subplot):
        # Get the current story point in the scene
        story_point = subplot[story_point_idx]
        # Generate a prompt for the story point
        previous_prompt = None
        selected_action = None
        story_point_complete = False
        while not story_point_complete:
            prompt = generate_prompt(title, scene, story_point, previous_prompt, selected_action)
            # Display the prompt text
            print()
            print(prompt["text"])
            # If the game is over, exit the game
            if prompt["game_over"] is True:
                print("Game over!")
                sys.exit(0)
            # If the prompt has any choices,
            if len(prompt["choices"]) > 0:
                # Display the prompt's choices
                print()
                print("Your options are:")
                for i, action in enumerate(prompt["choices"]):
                    print(f"{i + 1}. {action}")
                print()
                # Get the player's choice
                choice = int(input("Enter your choice: "))
                selected_action = prompt["choices"][choice - 1]
            prev_prompt = prompt
            prompt = generate_prompt(title, scene, story_point, prev_prompt, selected_action)
        story_point_idx += 1




# import logging

# import pyfiglet
# from generator.title import generate_title
# from generator.figlet import generate_figlet_font
# from generator.story import generate_story
# from generator.backstory import generate_backstory
# from generator.prompt import generate_prompt

# logging.basicConfig(
#     filename='game.log',
#     filemode='a',
#     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#     datefmt='%H:%M:%S',
#     level=logging.DEBUG
# )

# logging.info("Starting new game")

# logger = logging.getLogger('game')

# theme = input("Enter a theme: ")
# logger.debug(theme)
# title = generate_title(theme)
# logger.debug(title)
# story_points = generate_story(title)
# logger.debug(story_points)

# player = {
#     "health": 100,
#     "energy": 100,
#     "score": 0,
#     "progress": 0,
# }

# # Display the game title
# figlet_font = generate_figlet_font(title["TITLE"], title["TITLE DESCRIPTION"])
# try:
#     banner = pyfiglet.figlet_format(title["TITLE"], font=figlet_font)
# except pyfiglet.FontNotFound:
#     banner = pyfiglet.figlet_format(title["TITLE"])
# print()
# print(banner)
# print()
# print()

# # Display the game backstory
# backstory = generate_backstory({"title": title, "location": story_points[0]["location"]})
# print(backstory)
# print()

# # Start the game
# prompt = generate_prompt(title, story_points, player)
# while player["progress"] < len(story_points):
#     logger.debug(prompt)
#     print("=========================================")
#     print()
#     print(prompt["text"])
#     print()
#     print("Your options are:")
#     for i, option in enumerate(prompt["options"]):
#         print(f"{i + 1}. {option}")
#     print()
#     choice = int(input("Enter your choice: "))
#     print()
#     prev_prompt = {"text": prompt["text"], "options": prompt["options"], "selected": prompt["options"][choice - 1]}
#     prompt = generate_prompt(title, story_points, player, prev_prompt)
