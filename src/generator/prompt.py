import json

from .openai_client import openai, model

_messages = [
    {
        "role": "system",
        "content": """You are a text adventure game.

You will be a provided with a JSON object representing the current state of the game.
You must respond with the best possible prompt and options to display to the player using the information about the game, player, and story in the input object.
Your output must also be JSON.

Prompts should be detailed and maximize interactivity.
Don't just tell the player that they talked to a charcter, let them choose what to say to them.
Don't just tell the player that they found an item, let them choose how to use it.
Don't just tell the player that they solved a puzzle, let them choose how to solve it."""
    },
    {
        "role": "user",
        "content": """{
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
}"""
    },
    {
        "role": "assistant",
        "content": """{
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
}"""
    },
    {
        "role": "user",
        "content": """{
“title”: {
"THEME": "Steampunk Detective",
"THEME DESCRIPTION": "Enter a world of gears and steam, solve puzzles, and uncover a conspiracy",
"TITLE": "The Clockwork Conundrum",
"TITLE DESCRIPTION": "As the renowned detective Holmes, travel to a steampunk city where technology and magic are intertwined. Investigate a series of mysterious crimes that point to a larger conspiracy, solve puzzles, and use your ingenuity to uncover the truth before it's too late."
},
“STORY”: {
"STORY POINTS": [
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
“PLAYER”: {
“Health”: 100,
“Energy”: 100,
“Score”: 0,
"progress": 0,
},
“PREV_PROMPT”: {
"text": "Welcome to "The Clockwork Conundrum," a steampunk detective adventure! You are playing as the renowned detective Holmes, investigating a series of mysterious crimes in a steampunk city where technology and magic are intertwined. Your objective is to solve puzzles, gather clues, and use your ingenuity to uncover the truth before it's too late.\n\nYou find yourself in the police station, where you are supposed to meet with the Police Chief to receive information about the recent crimes and start your investigation.\n\nWhat would you like to do?",
"options": [
"Look around the police station",
"Talk to the Police Chief",
"Check your inventory",
"Save the game and quit"
],
"selected": 1
}
}"""
    },
    {
        "role": "assistant",
        "content": """{
"text": "You approach the Police Chief, who greets you with a stern look. He hands you a folder containing information about the recent crimes and suspects. He also gives you a map of the city, which may come in handy during your investigation. What would you like to do next?",
"options": [
"Ask the Police Chief about the suspects",
"Examine the folder for clues",
"Study the map of the city",
"Save the game and quit"
],
"player": {
"health": 100,
"energy": 100,
"score": 0,
"progress": 1
}
}"""
    }
]


def generate_prompt(title, story, player, prev_prompt=None):
    _input = json.dumps({'title': title, 'story': story, 'player': player, 'prev_prompt': prev_prompt})
    response = openai.ChatCompletion.create(
        model=model,
        messages=_messages + [{"role": "user", "content": _input}],
    )
    text = response['choices'][0]['message']['content']
    return json.loads(text)
