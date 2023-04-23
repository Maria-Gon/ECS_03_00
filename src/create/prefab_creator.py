import random
import pygame
import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_hunter import CTagHunter
from src.ecs.components.tags.c_tag_player import CTagPlayer

def create_square(world:esper.World, size:pygame.Vector2,
                    pos:pygame.Vector2, vel:pygame.Vector2, col:pygame.Color) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                CSurface(size, col))
    world.add_component(cuad_entity,
                CTransform(pos))
    world.add_component(cuad_entity, 
                CVelocity(vel))
    return cuad_entity

def create_sprite(world:esper.World, pos:pygame.Vector2, vel: pygame.Vector2, surf: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity,
                        CTransform(pos))
    world.add_component(sprite_entity, 
                        CVelocity(vel))
    world.add_component(sprite_entity, 
                        CSurface.from_surface(surf))
    return sprite_entity

def create_enemy_square(world:esper.World, pos:pygame.Vector2, enemy_info:dict):
    enemy_surface = pygame.image.load(enemy_info['image']).convert_alpha()
    vel_max = enemy_info["velocity_max"]
    vel_min = enemy_info["velocity_min"]
    vel_range = random.randrange(vel_min, vel_max)
    velocity = pygame.Vector2(random.choice([-vel_range, vel_range]),
                              random.choice([-vel_range, vel_range]))
    
    enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
    world.add_component(enemy_entity, CTagEnemy())

def create_enemy_hunter(world:esper.World, pos:pygame.Vector2, enemy_info:dict):
    enemy_surface = pygame.image.load(enemy_info['image']).convert_alpha()
    vel = pygame.Vector2(0,0)
    enemy_entity = create_sprite(world, pos, vel, enemy_surface)
    world.add_component(enemy_entity, CTagHunter())
    world.add_component(enemy_entity, CAnimation(enemy_info['animations']))
    world.add_component(enemy_entity, CHunterState())

def create_player_square(world: esper.World, player_info: dict, player_lvl_info: dict) -> int:
    player_surface = pygame.image.load(player_info['image']).convert_alpha()
    size = player_surface.get_size()
    size = (size[0]/player_info['animations']['number_frames'], size[1])
    pos = pygame.Vector2(player_lvl_info['position']['x'] - size[0]/2,
                         player_lvl_info['position']['y'] - size[1]/2)
    vel = pygame.Vector2(0,0)

    player_entity = create_sprite(world, pos, vel, player_surface)

    world.add_component(player_entity, CTagPlayer())
    world.add_component(player_entity, CAnimation(player_info['animations']))
    world.add_component(player_entity, CPlayerState())
    
    return player_entity

def create_enemy_spawner(world:esper.World, level_data:dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CEnemySpawner(level_data["enemy_spawn_events"]))
    
def create_input_player (world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()

    world.add_component(input_left, CInputCommand('PLAYER_LEFT', pygame.K_LEFT))
    world.add_component(input_right, CInputCommand('PLAYER_RIGHT', pygame.K_RIGHT))
    world.add_component(input_up, CInputCommand('PLAYER_UP', pygame.K_UP))
    world.add_component(input_down, CInputCommand('PLAYER_DOWN', pygame.K_DOWN))

def create_bullet(world: esper.World, bullet_info: dict, player_entity: int, pos_mouse: pygame.Vector2):
    bullet_surface = pygame.image.load(bullet_info['image']).convert_alpha()
    bullet_size = bullet_surface.get_rect().size

    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)

    pos_x = pl_t.pos.x + (pl_s.area.w/2) - (bullet_size[0]/2)
    pos_y = pl_t.pos.y + (pl_s.area.h/2) - (bullet_size[1]/2)

    pos = pygame.Vector2(pos_x, pos_y)

    x,y = pos_mouse
    b_pos_x = (x-pos_x) 
    b_pos_y = (y-pos_y) 

    vel = pygame.Vector2(b_pos_x, b_pos_y).normalize() * bullet_info['velocity'] ##Hay que corregirlo

    bullet_entity = create_sprite(world, pos, vel, bullet_surface)
    world.add_component(bullet_entity, CTagBullet())

def create_input_bullet (world: esper.World):
    input_click = world.create_entity()
    world.add_component(input_click, CInputCommand('PLAYER_CLICK', pygame.BUTTON_LEFT))