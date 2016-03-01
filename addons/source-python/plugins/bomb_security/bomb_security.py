# ../bomb_security/bomb_security.py

"""Allows CTs to pick up the bomb."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Entities
from entities.helpers import edict_from_pointer
from entities.hooks import EntityCondition
from entities.hooks import EntityPostHook
from entities.hooks import EntityPreHook
#   Events
from events.hooks import EventAction
from events.hooks import PreEvent
#   Memory
from memory import make_object
#   Players
from players.entity import Player


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_bump_player = None


# =============================================================================
# >> PRE GAME EVENTS
# =============================================================================
@PreEvent('player_team')
def _pre_player_team(game_event):
    """Block player joining team message if switch_team is being called."""
    if _bump_player is not None:
        return EventAction.STOP_BROADCAST


# =============================================================================
# >> ENTITY HOOKS
# =============================================================================
@EntityPreHook(EntityCondition.is_human_player, 'bump_weapon')
@EntityPreHook(EntityCondition.is_bot_player, 'bump_weapon')
def _pre_bump_weapon(args):
    """Switch the player's team if they are a CT picking up the bomb."""
    global _bump_player
    if edict_from_pointer(args[1]).classname != 'weapon_c4':
        return
    _bump_player = make_object(Player, args[0])
    if _bump_player.team == 3:
        _bump_player.switch_team(2)
    else:
        _bump_player = None


@EntityPostHook(EntityCondition.is_human_player, 'bump_weapon')
@EntityPostHook(EntityCondition.is_bot_player, 'bump_weapon')
def _post_bump_weapon(args, return_value):
    """Switch the player's team back to CT if they just picked up the bomb."""
    global _bump_player
    if _bump_player is None:
        return
    _bump_player.switch_team(3)
    _bump_player = None
