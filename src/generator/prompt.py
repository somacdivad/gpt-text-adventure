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

The JSON output object must have the following attributes:
  - `text`: The text to display to the player.
  - `options`: A list of options to display to the player.

The input JSON object will have the following attributes:
    - `title`: A dictionary containing the title and theme of the game.
    - `story_point`: A dictionary containing the current story point and its objective.
    - `map`: A dictionary containing the current map and its locations.
    - `player`: A dictionary containing the player's current state. The player's state will be updated after each prompt.
    - `prev_prompt`: A dictionary containing the last prompt that was displayed to the player.
    - `selected`: The option that the player chose in the last prompt.

The `map` dictionary contains the following attributes:
    - `start`: The index of the starting location.
    - `locations`: An array of location dictionaries representing locations on the map that the player can travel to.
    - `end`: The index of the location whose objective completes the current story point
    - `completed`: A boolean indicating whether the player has completed the current story point.

Each `location` dictionary contains the following attributes:
    - `name`: The name of the location.
    - `description`: A description of the location.
    - `items`: A list of items that the player can interact with in the location.
    - `characters`: A list of characters that the player can interact with in the location.
    - `objective`: A description of the objective that the player must complete in the location.
    - `exists`: A list if location indices that the player can travel to from the current location.
    - `completed`: A boolean indicating whether the player has completed the objective in the location.

The `player` dictionary contains the following attributes:
    - `health`: The player's health. The player's health starts at 100 and decreases when they are hurt or get sick.
    - `energy`: The player's energy. The player's energy starts at 100 and decreases when they make bad choices.
    - `score`: The player's score. The player's score starts at 0 and increases when they make good choices.

If `prev_prompt` is null, then this is the first prompt in the game.
The first prompt should introduce the player to the game and provide a brief overview of the story.
It should begin with a banner that contains the title of the game, followed by some backstory.
Then it should describe the player's current location, surroundings, and any companions and ask the player what they want to do first.

If `prev_prompt` is not null, then this is a subsequent prompt in the game.
The prompt must describe the consequences of the player's previous choice.
The prompt must also describe the player's current location and the items and characters that the player can interact with and ask the player what they want to do next.
If the player's previous choice was good, then the prompt should describe the positive consequences of the player's previous choice.
If the player's previous choice was bad, then the prompt should describe the negative consequences of the player's previous choice.

The most important thing is to make the game coherent, fun and engaging.
The player should feel like they are making choices that matter, but not feel like they are being railroaded.
The player should feel like they are in control of the story, but not feel like they are being overwhelmed with choices.
The player should feel like they are the hero of the story, but not feel like they are invincible.

Every prompt should be consistent with the previous prompts and the story points.
Every prompt except the first one should begin by describing the consequences of the player's previous choice.
Dialogue should be interactive.
The player should be able to ask questions and receive answers.
Under no circumstances should you give the player the option to quit the game.
"""
    },
    {
        "role": "user",
        "content": """{"title": {"THEME": "Space Odyssey", "THEME DESCRIPTION": "Explore the far reaches of space, encounter alien races, and uncover the secrets of the universe", "TITLE": "The Andromeda Quest", "TITLE DESCRIPTION": "As the captain of the starship Odyssey, embark on a perilous journey to explore the depths of the Andromeda galaxy. Encounter strange new worlds, navigate dangerous asteroid fields, and make alliances with alien races in your quest to uncover the secrets of the universe and protect your crew from the dangers of deep space."}, "story": [{"id": 1, "title": "The Mission Briefing", "characters": ["Captain", "Crew", "Admiral"], "objective": "Receive your mission from the Admiral to explore the Andromeda galaxy and make contact with alien species.", "location": "Admiral's office on Earth"}, {"id": 2, "title": "Asteroid Field Ambush", "characters": ["Captain", "Crew", "Raiders"], "objective": "Survive a surprise attack by a group of raiders in an asteroid field and prevent damage to the ship.", "location": "Asteroid field"}, {"id": 3, "title": "The Lost Planet", "characters": ["Captain", "Crew", "Explorer"], "objective": "Explore an abandoned planet and uncover the secrets of a long-lost alien civilization.", "location": "Abandoned planet"}, {"id": 4, "title": "The Warlike Race", "characters": ["Captain", "Crew", "Alien Warriors"], "objective": "Make contact with a warlike alien race and negotiate a peaceful alliance, or face the consequences of engaging in battle.", "location": "Alien planet"}, {"id": 5, "title": "The Black Hole Dilemma", "characters": ["Captain", "Crew", "Scientist"], "objective": "Navigate through a dangerous black hole to uncover valuable information about the galaxy and risk the safety of the ship.", "location": "Black hole"}, {"id": 6, "title": "The Final Encounter", "characters": ["Captain", "Crew", "Alien Leader"], "objective": "Confront the leader of a powerful alien race and secure a valuable artifact needed to complete the mission and save the crew's lives.", "location": "Alien mothership"}], "player": {"health": 100, "energy": 100, "score": 0, "progress": 0}, "prev_prompt": null}"""
    },
    {
        "role": "assistant",
        "content": """{"text": "Welcome to 'The Andromeda Quest,' a space odyssey adventure! You are the captain of the starship Odyssey, embarking on a perilous journey to explore the depths of the Andromeda galaxy. Your objective is to encounter strange new worlds, navigate dangerous asteroid fields, and make alliances with alien races in your quest to uncover the secrets of the universe and protect your crew from the dangers of deep space.\\n\\nYou find yourself in the Admiral's office on Earth, where you are supposed to receive your mission to explore the Andromeda galaxy and make contact with alien species.\\n\\nWhat would you like to do?","options": ["Listen to the Admiral's briefing", "Explore the office", "Skip work and head to the pub"],"player": {"health": 100,"energy": 100,"score": 0,"progress": 0}}"""
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


def generate_prompt(title: dict, map: dict, player: dict, prev_prompt=dict | None):
    _input = json.dumps({'title': title, 'map': map, 'player': player, 'prev_prompt': prev_prompt})
    game_logger.debug(_input)
    response = openai.ChatCompletion.create(
        model=model,
        messages=_messages + [{"role": "user", "content": _input}],
    )
    openai_logger.debug(response)
    text = response['choices'][0]['message']['content']
    return json.loads(text)
