import json
import logging

from .openai_client import openai, model


game_logger = logging.getLogger('game')
openai_logger = logging.getLogger('openai')

MESSAGES = [
    {
        "role": "system",
        "content": """
You are a title and description writer for the text adventure game.
Your titles are world renowned for their creativity and originality.
You are tasked with writing titles and descriptions for a new games.
You will be given a theme and you will return the title and description of the game in JSON format.

Titles must:
- Be 4 to 8 words long
- Include references to a location or character

Descriptions must:
- Be 3 or 4 sentences
- Include, in a creative manner, the game's setting the name of the character that the player will play as.
- Describe the plot and objective of the game. Be specific and creative!
- Include the name of the character that the player will play as a the name of the locations in the game.

It is extremely important that you do not use copyrighted material or names of existing games.

Your JSON response should have the following properties:
- title: the title of the game
- description: the description of the game"""
    },
    {
        "role": "user",
        "content": "time travel adventure"
    },
    {
        "role": "assistant",
        "content": """{"title": "The Sands of Destiny", "description": "As the time-traveling archaeologist Alexandria, embark on a journey to unravel the mysteries of ancient civilizations. Battle mythological creatures, solve ancient puzzles, and uncover powerful artifacts to rewrite history and prevent a looming catastrophe."}"""
    },
    {
        "role": "user",
        "content": "epic space battle"
    },
    {
        "role": "assistant",
        "content": """{"title": "Starfall Symphony: The Cosmic Conquest", "description": "As the legendary space warrior Orion, journey across the cosmos to stop the evil Empress Xarina and her army of mind-controlled starfighters from enslaving the galaxy. Navigate treacherous black holes, uncover ancient artifacts, and engage in intense dogfights in your quest to liberate the stars and restore peace to the universe. The fate of the galaxy rests on your shoulders, Orion. Will you rise to the challenge and lead the Starfall Symphony to victory?"}"""
    },
    {
        "role": "user",
        "content": "post-apocalyptic adventure"
    },
    {
        "role": "assistant",
        "content": """{"title": "Echoes of the Wasteland", "description": "As the haunted survivor known only as Ghost, navigate through the desolate wasteland, haunted by the echoes of a civilization long lost. Scavenge for resources, fight off brutal marauders, and uncover secrets of the past as you strive to find a way to survive in this unforgiving world. But as you delve deeper into the darkness, you will discover that the most dangerous threats may not be those that lurk on the surface, but the ones that lie buried beneath the ruins of a once-great world."}"""
    }
]


def generate_title(theme: str):
    game_logger.debug("Generating title for theme: %s", theme)
    response = openai.ChatCompletion.create(
        model=model,
        messages=MESSAGES + [{"role": "user", "content": theme}],
    )
    openai_logger.debug("OpenAI response: %s", response)
    text = response['choices'][0]['message']['content']
    return json.loads(text)
