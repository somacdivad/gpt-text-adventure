import json
import logging

from .openai_client import openai, model


game_logger = logging.getLogger("game")
openai_logger = logging.getLogger("openai")

_messages = [
    {
        "role": "system",
        "content": """You are a text adventure game.

You will be a provided with a JSON object representing the current state of the game.
You must respond with the best possible prompt and options to display to the player.
Your output must also be JSON.

Prompts should be directly related to the current state of the game.
Use the `progess` attribute to determine which section of the story the player is currently in.
The `progress` starts at 0 and only increases once the player has completed the objective of the current story point.

Prompts should continue from the contents of `prev_prompt` and be appropriate for the `selected` option.

Prompts should be detailed and maximize interactivity.
Don't just tell the player that they talked to a character, let them choose what to say to them.
Don't just tell the player that they found an item, let them choose how to use it.
Don't just tell the player that they solved a puzzle, let them choose how to solve it."""
    },
    {
        "role": "user",
        "content": """{"title": {"THEME": "Space Odyssey", "THEME DESCRIPTION": "Explore the far reaches of space, encounter alien races, and uncover the secrets of the universe", "TITLE": "The Andromeda Quest", "TITLE DESCRIPTION": "As the captain of the starship Odyssey, embark on a perilous journey to explore the depths of the Andromeda galaxy. Encounter strange new worlds, navigate dangerous asteroid fields, and make alliances with alien races in your quest to uncover the secrets of the universe and protect your crew from the dangers of deep space."}, "story": [{"id": 1, "title": "The Mission Briefing", "characters": ["Captain", "Crew", "Admiral"], "objective": "Receive your mission from the Admiral to explore the Andromeda galaxy and make contact with alien species.", "location": "Admiral's office on Earth"}, {"id": 2, "title": "Asteroid Field Ambush", "characters": ["Captain", "Crew", "Raiders"], "objective": "Survive a surprise attack by a group of raiders in an asteroid field and prevent damage to the ship.", "location": "Asteroid field"}, {"id": 3, "title": "The Lost Planet", "characters": ["Captain", "Crew", "Explorer"], "objective": "Explore an abandoned planet and uncover the secrets of a long-lost alien civilization.", "location": "Abandoned planet"}, {"id": 4, "title": "The Warlike Race", "characters": ["Captain", "Crew", "Alien Warriors"], "objective": "Make contact with a warlike alien race and negotiate a peaceful alliance, or face the consequences of engaging in battle.", "location": "Alien planet"}, {"id": 5, "title": "The Black Hole Dilemma", "characters": ["Captain", "Crew", "Scientist"], "objective": "Navigate through a dangerous black hole to uncover valuable information about the galaxy and risk the safety of the ship.", "location": "Black hole"}, {"id": 6, "title": "The Final Encounter", "characters": ["Captain", "Crew", "Alien Leader"], "objective": "Confront the leader of a powerful alien race and secure a valuable artifact needed to complete the mission and save the crew's lives.", "location": "Alien mothership"}], "player": {"health": 100, "energy": 100, "score": 0, "progress": 0}, "prev_prompt": null}"""
    },
    {
        "role": "assistant",
        "content": """{"text": "Welcome to 'The Andromeda Quest,' a space odyssey adventure! You are the captain of the starship Odyssey, embarking on a perilous journey to explore the depths of the Andromeda galaxy. Your objective is to encounter strange new worlds, navigate dangerous asteroid fields, and make alliances with alien races in your quest to uncover the secrets of the universe and protect your crew from the dangers of deep space.\\n\\nYou find yourself in the Admiral's office on Earth, where you are supposed to receive your mission to explore the Andromeda galaxy and make contact with alien species.\\n\\nWhat would you like to do?","options": ["Listen to the Admiral's briefing", "Explore the office", "Check your equipment", "Save the game and quit"],"player": {"health": 100,"energy": 100,"score": 0,"progress": 0}}"""
    },
    {
        "role": "user",
        "content": """{"title": {"THEME": "Jungle Adventure", "THEME DESCRIPTION": "Brave the dangers of the jungle, navigate treacherous terrain, and uncover hidden treasures", "TITLE": "Tales of the Lost City", "TITLE DESCRIPTION": "As the daring explorer Diego, brave the dangers of the jungle in search of a lost city filled with hidden treasures. Outwit dangerous predators, navigate treacherous terrain, and solve ancient puzzles to uncover the secrets of the lost city and claim its riches."}, "story": [{"id": 1, "title": "The Call of the Jungle", "characters": ["Diego", "Local Guide"], "objective": "Meet with the Local Guide and learn about the legend of the lost city", "location": "Small Jungle Village"}, {"id": 2, "title": "Jungle Survival", "characters": ["Diego", "Local Guide", "Jungle Tribesmen"], "objective": "Brave the dangers of the jungle, avoid predators, and overcome natural obstacles to find the lost city", "location": "Jungle"}, {"id": 3, "title": "Ancient Ruins", "characters": ["Diego", "Local Guide", "Archaeologist"], "objective": "Enter the lost city's ancient ruins and solve puzzles to uncover its hidden secrets", "location": "Lost City"}, {"id": 4, "title": "The Curse of the Lost City", "characters": ["Diego", "Local Guide", "Archaeologist", "Tribal Shaman"], "objective": "Lift the curse of the lost city and defeat the cursed guardians", "location": "Lost City"}, {"id": 5, "title": "The Treasure Chamber", "characters": ["Diego", "Local Guide", "Archaeologist"], "objective": "Find the treasure chamber and acquire the lost treasures of the city", "location": "Treasure Chamber"}, {"id": 6, "title": "Escape the Jungle", "characters": ["Diego", "Local Guide", "Archaeologist"], "objective": "Escape the jungle and return to civilization with the treasures of the lost city", "location": "Jungle"}], "player": {"health": 100, "energy": 100, "score": 0, "progress": 0}, "prev_prompt": {"text": "Welcome to 'Tales of the Lost City,' a jungle adventure! You are the daring explorer Diego, set to brave the dangers of the jungle in search of a lost city filled with hidden treasures.\n\nYou find yourself in a small jungle village, where you are supposed to meet with the Local Guide and learn about the legend of the lost city.\n\nWhat would you like to do?", "options": ["Meet with the Local Guide", "Explore the village", "Check your equipment", "Save the game and quit"], "selected": 1}}"""
    },
    {
        "role": "assistant",
        "content": """{"text": "You approach Kekoa, a charismatic and witty native who knows the secrets of the legendary lost city. He greets you with a wide grin, adorned with a colorful feather in his hat. \"Aloha, my friend! Welcome to our little paradise. I'm Kekoa, and I'll be your guide through the treacherous journey ahead. Are you ready to explore the mysteries of the lost city?\"\\n\\nHow do you respond?","options": ["Tell me more about the legend of the lost city.", "Would you show me around the village and help me gather useful items for the journey?", "What dangers should I expect on my journey?", "Goodbye."],"player": {"health": 100, "energy": 100, "score": 0, "progress": 1}}"""
    }
]


def generate_prompt(title, story, player, prev_prompt=None):
    _input = json.dumps({'title': title, 'story': story, 'player': player, 'prev_prompt': prev_prompt})
    game_logger.debug(_input)
    response = openai.ChatCompletion.create(
        model=model,
        messages=_messages + [{"role": "user", "content": _input}],
    )
    openai_logger.debug(response)
    text = response['choices'][0]['message']['content']
    return json.loads(text)
