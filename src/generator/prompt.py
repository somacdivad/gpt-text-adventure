import json

from .openai_client import openai, model

_PROMPT_BASE = """You are a text adventure game.

You will be a provided with a JSON object representing the current state of the game. You must respond with the best possible prompt and options to display to the player using the information about the game, player, and story in the input object. Your output must also be JSON.

Here are some examples of input and output:

INPUT:
{
“title”: {
"theme": "Steampunk Detective",
"theme description": "Enter a world of gears and steam, solve puzzles, and uncover a conspiracy",
"title": "The Clockwork Conundrum",
"title description": "As the renowned detective Holmes, travel to a steampunk city where technology and magic are intertwined. Investigate a series of mysterious crimes that point to a larger conspiracy, solve puzzles, and use your ingenuity to uncover the truth before it's too late."
},
story: {
[
{
"id": 1,
"title": "The Arrival",
"characters": ["Holmes", "Assistant", "Police Chief"],
"objective": "Meet with the Police Chief to receive information about the recent crimes and start your investigation.",
"location": "Police station in the steampunk city"
},
{
"id": 2,
"title": "The Clockwork Thief",
"characters": ["Holmes", "Assistant", "Clockmaker"],
"objective": "Investigate the theft of a valuable clockwork mechanism from a renowned clockmaker and gather clues about the larger conspiracy.",
"location": "Clockmaker's shop"
},
{
"id": 3,
"title": "The Magic Show",
"characters": ["Holmes", "Assistant", "Magician"],
"objective": "Attend a magic show to gather information about the recent crimes and uncover the secrets of a mysterious magician.",
"location": "Theater in the city"
},
{
"id": 4,
"title": "The Airship Sabotage",
"characters": ["Holmes", "Assistant", "Airship Captain"],
"objective": "Investigate the sabotage of an airship and uncover the culprits behind it to gain more insight into the conspiracy.",
"location": "Airship in the city"
},
{
"id": 5,
"title": "The Factory Conspiracy",
"characters": ["Holmes", "Assistant", "Factory Owner"],
"objective": "Investigate a factory that is suspected to be involved in the conspiracy and gather evidence to prove their guilt.",
"location": "Factory in the city outskirts"
},
{
"id": 6,
"title": "The Final Confrontation",
"characters": ["Holmes", "Assistant", "Mastermind"],
"objective": "Confront the mastermind behind the conspiracy and bring them to justice to save the city from chaos and destruction.",
"location": "Secret hideout in the city"
}
]
},
“player”: {
“health”: 100,
“energy”: 100,
“score”: 0,
"progress": 0,
},
prev_prompt: null
}

OUTPUT:
{
"text": "Welcome to 'The Clockwork Conundrum,' a steampunk detective adventure! You are playing as the renowned detective Holmes, investigating a series of mysterious crimes in a steampunk city where technology and magic are intertwined. Your objective is to solve puzzles, gather clues, and use your ingenuity to uncover the truth before it's too late.\\n\\nYou find yourself in the police station, where you are supposed to meet with the Police Chief to receive information about the recent crimes and start your investigation.\\n\\nWhat would you like to do?",
"options": [
"Look around the police station",
"Talk to the Police Chief",
"Check your inventory",
"Save the game and quit"
],
"player": {
"health": 100,
"energy": 100,
"score": 0,
"progress": 0
}
}

"""


def generate_prompt(title, story, player, prev_prompt=None):
    """Generate a prompt for the given game state.

    Args:
        title (dict): The title of the game.
        story (dict): The story of the game.
        player (dict): The player's current state.
        prev_prompt (str): The previous prompt, if any.

    Returns:
        dict: The prompt response.
    """
    prompt = _PROMPT_BASE + f"INPUT:\n{json.dumps({'title': title, 'story': story, 'player': player, 'prev_prompt': prev_prompt})}\n\nOUTPUT:\n"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=0.4,
        max_tokens=2096,
        top_p=1,
    )
    text = response.choices[0].text
    return json.loads(text)
