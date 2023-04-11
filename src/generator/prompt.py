import json
import logging

from .openai_client import openai, model


game_logger = logging.getLogger("game")
openai_logger = logging.getLogger("openai")

_messages = [
    {
        "role": "system",
        "content": """ou are an award-winning text adventure game prompt generator.
Your prompts are known for their wit, creativity, and challenging and engaging gameplay.

You will be provided with a JSON object with information about the game, the current scene, the previous story point, the current story point, the previous prompt, and the player's selected action.
Your task is to provide a JSON response representing the next prompt to display to the player.

If there is no previous prompt or previous story point, this is the first prompt in the game.
You do not need to tell the player the game's title and character's name, but you must introduce the scene in a descriptive and immersive manner.

If there is a previous prompt, you must use the previous prompt's text and the player's selected action to generate the next prompt.
If the action the player took complete's the story point's objective, set the `story_point_complete` propoerty of your output to true.
If the action the player took failed their objective or killed them, set the `game_over` property of your output to true.

Your JSON response must have the following properties:
- text: 3 to 6 sentences that describe the consequences of the player's selected action and the new scenario presented to the player. Be specific, descriptive, and creative. Immerse the player in the story. If there is no selected action, introduce the scene and story point.
- choices: an array of strings representing the player's available actions. The player can only interact with the characters and items in the story point.
- story_point_complete: a boolean indicating whether or not the current story point is complete. The story point is complete if the player's actions complete the objective.
- scene_complete: a boolean indicating whether or not the scene is complete
- game_over: a boolean indicating whether or not the player lost the game

If the scene or the story point is complete, do not return any choices.

Provide 3 to 5 specific, descriptive, and atomic actions for the player to choose from.
At least one actions much lead the player closer to or complete their objective.
At least one action must have negative consequences, but it shouldn't be obvious.
The player must feel like their choices matter and have real stakes.
The player must feel challenged to make the correct choice.
If the player dies or fails an objective, the the game is over and `game_over` should be true in your response.

The most import thing is that the player have fun.
The success of our game depends on you!
"""
    },
    {
        "role": "user",
        "content": """{"game":{"title":"The Sands of Destiny","description":"As the time-traveling archaeologist Alexandria, embark on a journey to unravel the mysteries of ancient civilizations. Battle mythological creatures, solve ancient puzzles, and uncover powerful artifacts to rewrite history and prevent a looming catastrophe."},"scene":{"title":"The Temple of Ra","scenario":"You arrive at the Temple of Ra, a sacred place shrouded in mystery. You must navigate through the temple and solve its intricate puzzles to find the hidden artifact.","objective":"Find the artifact hidden within the Temple of Ra."},"previous_story_point":null,"current_story_point":{"title":"Entering the Temple","description":"As you approach the Temple of Ra, you notice the entrance is heavily guarded by ancient stone statues. You must find a way to deactivate the statues and gain entry to the temple.","location":"The entrance of the Temple of Ra","objective":"Deactivate the statues and gain entry to the temple","characters":[{"name":"Guardian Statues","description":"Ancient stone statues of the gods Horus and Anubis, with eyes that glow ominously."}],"items":[]},"previous_prompt":null,"selected_action":null}"""
    },
    {
        "role": "assistant",
        "content": """{"text":"You stand before the entrance to the Temple of Ra, guarded by the stone statues of Horus and Anubis. The statues stare down at you with glowing eyes, unblinking. You study the statues carefully and notice that they each have a large ruby embedded in their foreheads. Suddenly, you hear a faint clicking noise, and the ground beneath you starts to shake. You jump back as a pit opens up before you, revealing a hidden passage beneath the temple. You see a glimmer of light emanating from within. What will you do?","choices":["Inspect the ruby on the Horus statue","Inspect the ruby on the Anubis statue","Attempt to jump over the pit","Investigate the hidden passage","Yell for help"],"story_point_complete":false,"scene_complete":false,"game_over":false}"""
    },
    {
        "role": "user",
        "content": """{"game":{"title":"Starfall Symphony: The Cosmic Conquest","description":"As the legendary space warrior Orion, journey across the cosmos to stop the evil Empress Xarina and her army of mind-controlled starfighters from enslaving the galaxy. Navigate treacherous black holes, uncover ancient artifacts, and engage in intense dogfights in your quest to liberate the stars and restore peace to the universe. The fate of the galaxy rests on your shoulders, Orion. Will you rise to the challenge and lead the Starfall Symphony to victory?"},"scene":{"title":"The Ambush","scenario":"As you travel through space, your ship is suddenly ambushed by a swarm of Xarina's mind-controlled starfighters. You must engage in a dogfight to defend your ship and fend off the attackers.","objective":"Survive the ambush and protect your ship."},"previous_story_point":null,"current_story_point":{"title":"The Ambush Begins","description":"As you are traveling through space, suddenly, an alarm goes off indicating that your ship is being targeted. Looking out of the cockpit, you see a swarm of Xarina's starfighters closing in on your position.","location":"The cockpit of your ship","objective":"Initiate defensive maneuvers to evade the enemy's attacks","characters":[{"name":"Ship's AI","description":"An advanced artificial intelligence system that manages the ship's functions and provides assistance to the crew."}],"items":[{"name":"Ship's controls","description":"The various buttons, levers, and displays that allow the player to control the ship."},{"name":"Defensive weapons","description":"Various weapons equipped on the ship that can be used to defend against enemy attacks."}]}, "previous_prompt":null,"selected_action":null}"""
    },
    {
        "role": "assistant",
        "content": """{"text":"You quickly take control of the ship's controls and maneuver it to evade the enemy's attacks. You feel the ship jolt as the enemy fire hits its shields. You hear the Ship's AI warning you that the shields won't last long under this barrage. You must find a way to retaliate and defend the ship.","choices":["Use defensive weapons to fire back at the enemy","Activate the ship's cloaking device to hide from the enemy","Perform evasive maneuvers to avoid the enemy fire","Contact nearby allies for backup","Attempt to hack into the enemy's communication system to gather intelligence"],"story_point_complete":false,"scene_complete":false,"game_over":false}"""
    }
]


def generate_prompt(title, scene, story_point, prev_prompt=None, selected_action=None):
    _input = json.dumps({'game': title, 'scene': scene, 'story_point': story_point, 'prev_prompt': prev_prompt, 'selected_action': selected_action})
    game_logger.debug("Generating prompt for input: %s", _input)
    response = openai.ChatCompletion.create(
        model=model,
        messages=_messages + [{"role": "user", "content": _input}],
    )
    openai_logger.debug("OpenAI response: %s", response)
    text = response['choices'][0]['message']['content']
    return json.loads(text)
