import logging

import pyfiglet
from generator.title import generate_title
from generator.figlet import generate_figlet_font
from generator.story import generate_story
from generator.backstory import generate_backstory
from generator.prompt import generate_prompt

logging.basicConfig(
    filename='game.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
)

logging.info("Starting new game")

logger = logging.getLogger('game')

theme = input("Enter a theme: ")
logger.debug(theme)
title = generate_title(theme)
logger.debug(title)
story_points = generate_story(title)
logger.debug(story_points)

player = {
    "health": 100,
    "energy": 100,
    "score": 0,
    "progress": 0,
}

# Display the game title
figlet_font = generate_figlet_font(title["TITLE"], title["TITLE DESCRIPTION"])
try:
    banner = pyfiglet.figlet_format(title["TITLE"], font=figlet_font)
except pyfiglet.FontNotFound:
    banner = pyfiglet.figlet_format(title["TITLE"])
print()
print(banner)
print()
print()

# Display the game backstory
backstory = generate_backstory({"title": title, "location": story_points[0]["location"]})
print(backstory)
print()

# Start the game
prompt = generate_prompt(title, story_points, player)
while player["progress"] < len(story_points):
    logger.debug(prompt)
    print("=========================================")
    print()
    print(prompt["text"])
    print()
    print("Your options are:")
    for i, option in enumerate(prompt["options"]):
        print(f"{i + 1}. {option}")
    print()
    choice = int(input("Enter your choice: "))
    print()
    prev_prompt = {"text": prompt["text"], "options": prompt["options"], "selected": prompt["options"][choice - 1]}
    prompt = generate_prompt(title, story_points, player, prev_prompt)
