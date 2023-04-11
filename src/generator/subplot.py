import json
import logging

from .openai_client import openai, model


game_logger = logging.getLogger('game')
openai_logger = logging.getLogger('openai')

MESSAGES = [
    {
        "role": "system",
        "content": """
You are an award winning plot writer for text adventure games.
You are tasked with writing the plot for a scene in a new game.

You will be given a JSON object with the following properties:
- game: a json object containing the title and description of the game
- scene: a JSON object containing the scene's title, description, and objective

You will provide a JSON array of plot points for the scene.
Each plot point must have the following properties:
- title: the title of the plot point
- description: the description of the plot point. Be creative!
- location: the location of the plot point. Be specific and creative!
- objective: the objective of the plot point. Be specific and use your imagination!
- characters: an array of characters that appear in the plot point that the player can interact with. Give character's names and descriptions.
- items: an array of items that appear in the plot point that the player can interact with. Be specific!

Your plot must:
- Be appropriate to the theme of the game
- Describe the course of events that carry out the scene

Your plot must never involve locations, characters, and events that are not a part of the scene.

Be creative and imaginative. The success of the game depends on your ability to provide the best plot!"""
    },
    {
        "role": "user",
        "content": """{"game": {"title": "The Sands of Destiny", "description": "As the time-traveling archaeologist Alexandria, embark on a journey to unravel the mysteries of ancient civilizations. Battle mythological creatures, solve ancient puzzles, and uncover powerful artifacts to rewrite history and prevent a looming catastrophe."}, "scene": {"title":"The Temple of Ra","scenario":"You arrive at the Temple of Ra, a sacred place shrouded in mystery. You must navigate through the temple and solve its intricate puzzles to find the hidden artifact.","objective":"Find the artifact hidden within the Temple of Ra."}}"""
    },
    {
        "role": "assistant",
        "content": """{"plot_points":[{"title":"Entering the Temple","description":"As you approach the Temple of Ra, you notice the entrance is heavily guarded by ancient stone statues. You must find a way to deactivate the statues and gain entry to the temple.","location":"The entrance of the Temple of Ra","objective":"Deactivate the statues and gain entry to the temple","characters":[{"name":"Guardian Statues","description":"Ancient stone statues of the gods Horus and Anubis, with eyes that glow ominously."}],"items":[]},{"title":"The Corridor of Traps","description":"You enter a long, narrow corridor filled with traps. The floor is covered in pressure plates that trigger arrows and darts to shoot out from the walls. You must navigate through the corridor and avoid the traps to reach the next room.","location":"The Corridor of Traps","objective":"Navigate through the corridor and avoid the traps","characters":[],"items":[]},{"title":"The Puzzle Room","description":"You enter a large room filled with puzzles. There are hieroglyphics etched into the walls and a large pedestal in the center of the room. You must solve the puzzles to reveal the location of the hidden artifact.","location":"The Puzzle Room","objective":"Solve the puzzles to reveal the location of the hidden artifact","characters":[],"items":[]},{"title":"The Guardian of Ra","description":"You reach the inner sanctum of the temple and encounter the Guardian of Ra, a powerful being with the head of a hawk and the body of a man. The guardian challenges you to a battle to the death.","location":"The Inner Sanctum","objective":"Defeat the Guardian of Ra in battle","characters":[{"name":"Guardian of Ra","description":"A powerful being with the head of a hawk and the body of a man, wielding a giant scythe."}],"items":[]},{"title":"The Hidden Artifact","description":"After defeating the Guardian of Ra, you discover the hidden artifact - a golden scepter with a ruby at its tip. You must take the artifact and leave the temple before it collapses.","location":"The Inner Sanctum","objective":"Take the artifact and leave the temple before it collapses","characters":[],"items":[{"name":"Golden Scepter","description":"A golden scepter with a ruby at its tip, pulsing with an otherworldly energy."}]}]}"""
    },
    {
        "role": "user",
        "content": """{"game":{"title": "Starfall Symphony: The Cosmic Conquest", "description": "As the legendary space warrior Orion, journey across the cosmos to stop the evil Empress Xarina and her army of mind-controlled starfighters from enslaving the galaxy. Navigate treacherous black holes, uncover ancient artifacts, and engage in intense dogfights in your quest to liberate the stars and restore peace to the universe. The fate of the galaxy rests on your shoulders, Orion. Will you rise to the challenge and lead the Starfall Symphony to victory?"}, "scene": {"title":"The Ambush","scenario":"As you travel through space, your ship is suddenly ambushed by a swarm of Xarina's mind-controlled starfighters. You must engage in a dogfight to defend your ship and fend off the attackers.","objective":"Survive the ambush and protect your ship."}}"""
    },
    {
        "role": "assistant",
        "content": """{"plot_points":[{"title":"The Ambush Begins","description":"As you are traveling through space, suddenly, an alarm goes off indicating that your ship is being targeted. Looking out of the cockpit, you see a swarm of Xarina's starfighters closing in on your position.","location":"The cockpit of your ship","objective":"Initiate defensive maneuvers to evade the enemy's attacks","characters":[{"name":"Ship's AI","description":"An advanced artificial intelligence system that manages the ship's functions and provides assistance to the crew."}],"items":[{"name":"Ship's controls","description":"The various buttons, levers, and displays that allow the player to control the ship."},{"name":"Defensive weapons","description":"Various weapons equipped on the ship that can be used to defend against enemy attacks."}]},{"title":"Engaging in Battle","description":"The enemy fighters are closing in, firing their lasers at your ship. You must use your piloting skills to evade their attacks and retaliate with your own weapons.","location":"The cockpit of your ship","objective":"Take down a certain number of enemy fighters to weaken their attack","characters":[{"name":"Enemy starfighter pilots","description":"The pilots of the enemy fighters, all of whom are under the control of Empress Xarina's mind-control technology."}],"items":[{"name":"Ship's weapons","description":"Various weapons equipped on the ship that can be used to attack enemy fighters."},{"name":"Countermeasures","description":"Tools and techniques that can be used to evade enemy attacks, such as flares and chaff."}]},{"title":"The Enemy's Secret Weapon","description":"As you're fighting off the swarm of enemy fighters, you notice that some
"""
    },
]

def generate_subplot(title: dict, scene: dict):
    """Generate a subplot for a scene in a game.

    Args:
        title (dict): A dictionary containing the title and description of the game.
        scene (dict): A dictionary containing the scene's title, description, and objective.

    Returns:
        list: A list of plot points for the scene.
    """
    game_logger.debug("Generating subplot for scene: %s", scene["title"])
    _input = {"game": title, "scene": scene}
    response = openai.ChatCompletion.create(
        model=model,
        messages = MESSAGES + [{"role": "user", "content": f"{json.dumps(_input)}"}],
    )
    openai_logger.debug("OpenAI response: %s", response)
    subplot = response["choices"][0]["message"]["content"]
    return json.loads(subplot)["plot_points"]
