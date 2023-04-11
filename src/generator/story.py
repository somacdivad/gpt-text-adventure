import json
import logging

from .openai_client import openai, model

game_logger = logging.getLogger('game')
openai_logger = logging.getLogger('openai')

MESSAGES = [
    {
        "role": "system",
        "content": """
You are a game text adventure game architect. Your job is to provide the primary story points for a game.

You will be given a JOSN object containing information about a game. Provide a JSON response containing an array of 4 to 6 story points in chronological order that carry out the objective of the game.

The JSON Object for each story point must have the following properties:
- title: the title of the story point. This will be displayed to the player. Be creative!
- scenario: a description of the story point.
- objective: the objective of the story point. This will be displayed to the player so they know what their goal is in order to advance to next part of the story. Be creative!
- characters: a list of characters that the player may interact with during the story point. Be specific and give the caracters names. Be creative!
- items: a list of items that the player may interact with during the story point. Be specific and creative!"""
    },
    {
        "role": "user",
        "content": """{"title": "The Sands of Destiny", "description": "As the time-traveling archaeologist Alexandria, embark on a journey to unravel the mysteries of ancient civilizations. Battle mythological creatures, solve ancient puzzles, and uncover powerful artifacts to rewrite history and prevent a looming catastrophe."}"""
    },
    {
        "role": "assistant",
        "content": """{"storyPoints":[{"title":"The Temple of Ra","scenario":"You arrive at the Temple of Ra, a sacred place shrouded in mystery. You must navigate through the temple and solve its intricate puzzles to find the hidden artifact.","objective":"Find the artifact hidden within the Temple of Ra."},{"title":"The Battle of the Titans","scenario":"As you venture further into your journey, you encounter a powerful Titan that has been awakened from its slumber. You must fight for your life and defeat the Titan to continue on your quest.","objective":"Defeat the Titan and continue on your journey."},{"title":"The Lost City of Atlantis","scenario":"You discover the lost city of Atlantis and must navigate its treacherous ruins. In doing so, you uncover a powerful artifact that could rewrite history.","objective":"Find the artifact hidden within the ruins of Atlantis."},{"title":"The Gates of Time","scenario":"You finally arrive at the Gates of Time, the key to rewriting history. But you must solve the puzzles and battle the guardians to enter the gates and prevent the looming catastrophe.","objective":"Solve the puzzles and battle the guardians to enter the Gates of Time and prevent the catastrophe."}]}```"""
    },
    {
        "role": "user",
        "content": """{"title": "Starfall Symphony: The Cosmic Conquest", "description": "As the legendary space warrior Orion, journey across the cosmos to stop the evil Empress Xarina and her army of mind-controlled starfighters from enslaving the galaxy. Navigate treacherous black holes, uncover ancient artifacts, and engage in intense dogfights in your quest to liberate the stars and restore peace to the universe. The fate of the galaxy rests on your shoulders, Orion. Will you rise to the challenge and lead the Starfall Symphony to victory?"}"""
    },
    {
        "role": "assistant",
        "content": """{"storyPoints":[{"title":"The Ambush","scenario":"As you travel through space, your ship is suddenly ambushed by a swarm of Xarina's mind-controlled starfighters. You must engage in a dogfight to defend your ship and fend off the attackers.","objective":"Survive the ambush and protect your ship."},{"title":"The Lost Planet","scenario":"You receive a transmission from a stranded alien race who possess knowledge of an ancient artifact that could aid in your mission. They are located on a lost planet in a treacherous region of space. You must navigate through the hazardous environment to reach the stranded aliens and gain the artifact.","objective":"Find the stranded aliens on the lost planet and retrieve the ancient artifact."},{"title":"The Black Hole","scenario":"As you continue your journey, you encounter a massive black hole that threatens to pull your ship into its void. You must navigate through the gravitational forces and avoid hazards to escape the black hole's grasp.","objective":"Escape the black hole's gravitational pull and continue on your journey."},{"title":"The Battle for the Galactic Gateway","scenario":"You arrive at the Galactic Gateway, the entrance to Xarina's stronghold. You must battle through her army of starfighters and reach her stronghold to put an end to her reign.","objective":"Defeat Xarina's army and reach her stronghold."},{"title":"The Final Showdown","scenario":"You finally confront Empress Xarina and engage in a fierce battle to stop her from enslaving the galaxy. You must use all your skills and weapons to defeat her and restore peace to the universe.","objective":"Defeat Empress Xarina and restore peace to the universe."}]}"""
    },
]


def generate_story(game_info):
    game_logger.info(f"Generating story for game: {game_info}")
    response = openai.ChatCompletion.create(
        model=model,
        messages=MESSAGES + [{"role": "user", "content": f"{game_info}"}]
    )
    openai_logger.info(f"OpenAI response: {response}")
    story = response['choices'][0]['message']['content']
    return json.loads(story)["storyPoints"]
