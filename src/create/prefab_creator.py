import random
import pygame
import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
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

def create_enemy_square(world:esper.World, pos:pygame.Vector2, enemy_info:dict):
    size = pygame.Vector2(enemy_info["size"]["x"], 
                          enemy_info["size"]["y"])
    color = pygame.Color(enemy_info["color"]["r"],
                         enemy_info["color"]["g"],
                         enemy_info["color"]["b"])
    vel_max = enemy_info["velocity_max"]
    vel_min = enemy_info["velocity_min"]
    vel_range = random.randrange(vel_min, vel_max)
    velocity = pygame.Vector2(random.choice([-vel_range, vel_range]),
                              random.choice([-vel_range, vel_range]))
    enemy_entity = create_square(world, size, pos, velocity, color)
    world.add_component(enemy_entity, CTagEnemy())

def create_player_square(world: esper.World, player_info: dict, player_lvl_info: dict) -> int:
    size = pygame.Vector2(player_info['size']['x'],
                          player_info['size']['y'])
    color = pygame.Color(player_info['color']['r'],
                         player_info['color']['g'],
                         player_info['color']['b'])
    pos = pygame.Vector2(player_lvl_info['position']['x'] - size.x/2,
                         player_lvl_info['position']['y'] - size.y/2)
    vel = pygame.Vector2(0,0)
    player_entity = create_square(world, size, pos, vel, color)
    world.add_component(player_entity, CTagPlayer())
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
    size = pygame.Vector2(bullet_info['size']['x'],
                          bullet_info['size']['y'])
    color = pygame.Color(bullet_info['color']['r'],
                         bullet_info['color']['g'],
                         bullet_info['color']['b'])
    
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)

    pos_x = pl_t.pos.x + pl_s.surf.get_width()/2 
    pos_y = pl_t.pos.y + pl_s.surf.get_height()/2

    pos = pygame.Vector2(pos_x, pos_y)

    x,y = pos_mouse

    b_pos_x = (x-pos_x) 
    b_pos_y = (y-pos_y) 

    vel = pygame.Vector2(b_pos_x, b_pos_y).normalize() * bullet_info['velocity'] ##Hay que corregirlo

    bullet_entity = create_square(world, size, pos, vel, color)
    world.add_component(bullet_entity, CTagBullet())

def create_input_bullet (world: esper.World):
    input_click = world.create_entity()
    world.add_component(input_click, CInputCommand('PLAYER_CLICK', pygame.BUTTON_LEFT))