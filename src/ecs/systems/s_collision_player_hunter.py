import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_hunter import CTagHunter


def system_collision_player_hunter(world: esper.World, player_entity: int, lever_cfg: dict):
    components = world.get_components(CSurface, CTransform, CTagHunter)
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)

    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)

    for enemy_entity, (c_s, c_t, _) in components:
        ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if ene_rect.colliderect(pl_rect):
            world.delete_entity(enemy_entity)
            pl_t.pos.x = lever_cfg['player_spawn']['position']['x'] - pl_s.area.w/2
            pl_t.pos.y = lever_cfg['player_spawn']['position']['y'] - pl_s.area.h/2