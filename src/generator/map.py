import json
import logging

from .openai_client import openai, model

game_logger = logging.getLogger("game")
openai_logger = logging.getLogger("openai")

_messages = [
    {
        "role": "system",
        "content": """
You are a map generator for a text adventure game.

I will provide you with a JSON object representing a story point in the game.
A story point describes the location, characters, and objective of a plot point in the game.
The JSON object will have the following properties:
- title: the title of the game
- description: a description of the game
- plot: an array of story points in the game
- location: the index of the current location in the plot array

You will return a JSON object representing a map of the location whose index is provided.
The map should be for this location only, and none of the other locations in the plot.
The map is a JSON object with three properties:
- locations: an array of locations in the map
- start: the index of the starting location in the locations array
- end: the index of the ending location in the locations array
- completed: a boolean indicating whether the map has been completed. A map is completed when the player has completed the objective of the end location.
- depends_on: an array of indices of other locations that must be completed before this location can be completed

Each location object has the following properties:
- name: the name of the location
- description: a description of the location
- exits: an array indices of other locations in the map that the player can travel to from this location
- items: an array of items that the player can interact with at the location
- characters: an array of characters that the player can interact with at the location
- objective: a string describing the objective of the location, such as:
    - "Find the key to unlock the door"
    - "Defeat the dragon"
    - "Find the treasure"
    - "Gather the ingredients for the potion"
- completed: a boolean indicating whether the objective has been completed

The objective a map point must make sense in the context of the story and the story point."""
    },
    {
        "role": "user",
        "content": """{'title': 'No One to Trust', 'description': 'As the hardboiled detective Jack Daniels, navigate the seedy underbelly of Chicago in the 1940s. Solve crimes, gather evidence, and outsmart corrupt officials and ruthless gangsters to uncover the truth behind a conspiracy that threatens the city itself. In a world where no one can be trusted, it’s up to you to find the justice that is buried deep in the shadows.', 'plot': [{'id': 1, 'title': 'The Mysterious Client', 'characters': ['Jack Daniels', 'Gangster Client'], 'objective': 'Get hired to investigate a gangland murder and collect initial evidence to start your investigation.', 'location': 'Office in Chicago'}, {'id': 2, 'title': 'The Seedy Underbelly', 'characters': ['Jack Daniels', 'Barkeep', 'Prostitutes', 'Henchmen'], 'objective': 'Infiltrate the seedy underworld hangouts of Chicago to gather tips, evidence, and interrogate witnesses.', 'location': 'Various Hangouts'}, {'id': 3, 'title': 'The Illegal Gambling Den', 'characters': ['Jack Daniels', 'Shady Gamblers', 'Thugs'], 'objective': 'Bust an illegal gambling den run by a corrupt official to gather intelligence on the murder case and expose corruption.', 'location': 'Secret Gambling Den'}, {'id': 4, 'title': 'The Mysterious Package', 'characters': ['Jack Daniels', 'Delivery Boy', 'The Law'], 'objective': 'Collect a mysterious package with evidence vital to the case, but evade corrupt officials and crooked cops.', 'location': 'Secret Drop-off Point'}, {'id': 5, 'title': 'The Final Confrontation', 'characters': ['Jack Daniels', 'The Killer', 'Corrupt Official'], 'objective': 'Uncover the truth behind the conspiracy linking corrupt officials and ruthless gangsters, and bring the killer to justice.', 'location': "The Killer's Hideout"}], 'location': 0}"""
    },
    {
        "role": "assistant",
        "content": """{"locations":[{"name":"Reception","description":"A small room with a desk and chairs for visitors.","exits":[2],"items":["telephone"],"characters":[],"objective":"","completed":false,"depends on":[]},{"name":"Conference Room","description":"A larger room with a table, chairs, whiteboards, and a coffee maker.","exits":[0,1],"items":["table","chairs","whiteboards","coffee maker"],"characters":["Gangster Client"],"objective":"Get hired to investigate a gangland murder.","completed":false,"depends on":[]},{"name":"Private Office","description":"A small room with a desk, shelves, and clutter.","exits":[],"items":["desk","lamp","empty whiskey bottles","cigarette butts","case files","shelves"],"characters":["Jack Daniels"],"objective":"Collect initial evidence to start your investigation.","completed":false,"depends on":[1]}],"start":0,"end":2,"completed":false}"""
    }
]


def generate_map(story_point: dict):
    game_logger.info(f"Generating map for story point: {story_point}")
    response = openai.ChatCompletion.create(
        model=model,
        messages=_messages + [{"role": "user", "content": f"{story_point}"}],
    )
    openai_logger.info(f"OpenAI response: {json.dumps(response, indent=2)}")
    map = response['choices'][0]['message']['content']
    return json.loads(map)
