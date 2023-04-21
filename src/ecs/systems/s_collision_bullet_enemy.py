import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_collision_bullet_enemy(world: esper.World):
    enemy_components = world.get_components(CSurface, CTransform, CTagEnemy)
    bullet_components = world.get_components(CSurface, CTransform, CTagBullet)
    
    for bullet_entity, (b_s, b_t, _) in bullet_components:
        b_rect = CSurface.get_area_relative(b_s.area, b_t.pos)
        for enemy_entity, (c_s, c_t, _) in  enemy_components:
            ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
            if ene_rect.colliderect(b_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)