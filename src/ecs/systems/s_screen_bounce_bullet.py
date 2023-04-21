

import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet

def system_screen_bounce_bullet(world:esper.World, screen:pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagBullet)

    c_t:CTransform
    c_s:CSurface
    c_b:CTagBullet
    for bullet_entity, (c_t, c_s, c_b) in components:
        bullet = c_s.surf.get_rect(topleft=c_t.pos)
        if bullet.left < 0 or bullet.right > screen_rect.width or bullet.top < 0 or bullet.bottom > screen_rect.height:
            world.delete_entity(bullet_entity)