import logging

from generator.title import generate_title
from generator.story import generate_story
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
    prev_prompt = {"text": prompt["text"], "options": prompt["options"], "selected": choice}
    prompt = generate_prompt(title, story_points, player, prev_prompt)
