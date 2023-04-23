import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_explosion import CTagExplosion


def system_explosion_stop(world: esper.World):
    components = world.get_components(CAnimation, CTagExplosion)
    for explosion_entity, (e_a, _) in components:
        if e_a.curr_frame == e_a.animations_list[e_a.cur_anim].end:
            world.delete_entity(explosion_entity)
