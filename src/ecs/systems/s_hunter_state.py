import pygame
import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_hunter_state(world: esper.World, hunter_info: dict):
    components = world.get_components(CTransform, CVelocity, CAnimation, CHunterState)
    player_components = world.get_components(CTransform, CTagPlayer)

    for _, (c_t, c_v, c_a, c_hst) in components:
        for _, (p_t, _) in player_components:
            if c_hst.state == HunterState.IDLE:
                _do_idle_state(c_t, c_a, c_hst, p_t, hunter_info)
            elif c_hst.state == HunterState.CHASE:
                _do_chase_state(c_t, c_a, c_hst, p_t, c_v, hunter_info)
            elif c_hst.state == HunterState.RETURN:
                _do_return_state(c_t, c_a, c_hst, c_v, hunter_info)

def _do_idle_state(c_t: CTransform, c_a: CAnimation, c_hst: CHunterState, p_t: CTransform, hunter_info: dict):
    _set_animation(c_a, 1)
    init_p = c_hst.init_pos.copy()
    c_t.pos.x = init_p.x
    c_t.pos.y = init_p.y
    distance = c_t.pos.distance_to(p_t.pos)
    if distance <= hunter_info['Hunter']['distance_start_chase']:
        c_hst.state = HunterState.CHASE

def _do_chase_state(c_t: CTransform, c_a: CAnimation, c_hst: CHunterState, p_t: CTransform, c_v: CVelocity, hunter_info: dict):
    _set_animation(c_a, 0)
    distance = c_t.pos.distance_to(c_hst.init_pos)
    pl_p = p_t.pos.copy()
    pos_x = pl_p.x - c_t.pos.x
    pos_y = pl_p.y - c_t.pos.y
    c_v.vel = pygame.Vector2(pos_x, pos_y).normalize() * hunter_info['Hunter']['velocity_chase']

    if distance >= hunter_info['Hunter']['distance_start_return']:
        c_hst.state = HunterState.RETURN

def _do_return_state(c_t: CTransform, c_a: CAnimation, c_hst: CHunterState, c_v: CVelocity, hunter_info: dict):
    _set_animation(c_a, 0)
    distance = c_t.pos.distance_to(c_hst.init_pos)
    init_p = c_hst.init_pos.copy()
    pos_x = init_p.x - c_t.pos.x
    pos_y = init_p.y - c_t.pos.y
    c_v.vel = pygame.Vector2(pos_x, pos_y).normalize() * hunter_info['Hunter']['velocity_return']
    if distance <= 5:
        c_hst.state = HunterState.IDLE

def _set_animation(c_a: CAnimation, num_anim: int):
    if c_a.cur_anim == num_anim:
        return
    c_a.cur_anim = num_anim
    c_a.cur_anim_time = 0
    c_a.curr_frame = c_a.curr_frame = c_a.animations_list[c_a.cur_anim].start