try:
    import pygame
except ModuleNotFoundError:
    print("ERROR: Pygame is not installed.")
    print("Install it with: py -m pip install pygame")
    input("Presiona ENTER para cerrar...")
    raise SystemExit

import math
import random
import sys
import os
import json
from array import array
from pathlib import Path

                                                              
           
                                 
                                             
                                                                
 
         
                                                     
                                                             
                                                              

pygame.init()

AUDIO_OK = False
AUDIO_DRIVER = "sin iniciar"
AUDIO_ERROR = ""

def init_audio():
    global AUDIO_OK, AUDIO_DRIVER, AUDIO_ERROR
    attempts = [None]
    if sys.platform.startswith("win"):
        attempts += ["wasapi", "directsound", "winmm"]

    errors = []
    for driver in attempts:
        try:
            pygame.mixer.quit()
            if driver:
                os.environ["SDL_AUDIODRIVER"] = driver
            else:
                os.environ.pop("SDL_AUDIODRIVER", None)
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
            pygame.mixer.set_num_channels(32)
            AUDIO_OK = True
            AUDIO_DRIVER = driver or "default"
            AUDIO_ERROR = ""
            print(f"AUDIO OK - driver: {AUDIO_DRIVER}")
            return True
        except Exception as e:
            errors.append(f"{driver or 'default'}: {e}")

    AUDIO_OK = False
    AUDIO_DRIVER = "none"
    AUDIO_ERROR = " | ".join(errors)
    print("AUDIO ERROR:", AUDIO_ERROR)
    return False

init_audio()

                                                        
WIDTH, HEIGHT = 1100, 700
FPS = 60
TITLE = "CUBED PORTABLE"
PORTABLE_TOUCH = True
PORTABLE_TOUCH_ALPHA = 118
PORTABLE_DATA_DIR = None
PORTABLE_FAST_MODE = True
PORTABLE_LOGICAL_SIZE = (960, 540)

                                                     
                                               
GAME_MUSIC_FILE = "BY_MODE"
MENU_MUSIC_FILE = "menu.ogg"
MODE_MUSIC_FILES = {
    "main": "IllusionaryNight",
    "mardcore": "nhelv",
    "sandbox": "sandbox"
}

MODE_MUSIC_START = {
    "main": 0.0,
    "mardcore": 197.90,
    "sandbox": 0.0
}
MUSIC_VOLUME = 0.75
MENU_MUSIC_VOLUME = 0.75
SOUND_VOLUME = 0.70
SCREEN_SHAKE_ENABLED = True
IMPACT_FLASH_ENABLED = True

             
GRAVITY = 1900.0
MOVE_ACCEL = 3000.0
MAX_X_SPEED = 640.0
AIR_FRICTION = 0.985
GROUND_FRICTION = 0.82

                                                 
JUMP_SPEED = 690.0
COYOTE_TIME = 0.11
JUMP_BUFFER = 0.11

DASH_SPEED = 2150.0
DASH_COOLDOWN = 0.16
PARRY_COOLDOWN = 0.30
MARDCORE_PARRY_COOLDOWN = 0.24
PARRY_TIME = 0.14
PARRY_RADIUS = 92

                            
PLATFORM_GAP_MIN = 92
PLATFORM_GAP_MAX = 132
PLATFORM_WIDTH_MIN = 105
PLATFORM_WIDTH_MAX = 185

BOB_APPEAR_TIME = 20.0
HARDCORE_5D_APPEAR_TIME = 14.0

                                                           
POWERUP_SPAWN_CHANCE = 0.13
POWERUP_DURATION = {
    "INFINITE JUMPS": 9.0,
    "SHIELD": 14.0,
    "ANGEL": 8.0,
    "FLIGHT": 7.0,
}

                                                         
BG = (8, 10, 16)
BG2 = (12, 15, 24)
WHITE = (245, 247, 252)
LIGHT = (190, 205, 228)
BLUE = (70, 145, 255)
CYAN = (70, 230, 255)
GREEN = (85, 230, 145)
YELLOW = (255, 222, 75)
ORANGE = (255, 145, 65)
RED = (255, 75, 92)
PINK = (255, 95, 205)
PURPLE = (170, 95, 255)
DARK = (18, 22, 33)
DARK2 = (20, 30, 48)
DARKER = (12, 15, 24)
BLACK = (0, 0, 0)

PLAYER_NAME = "YURI"

ENTITY_NAMES = {
    "drone": "BRIX",
    "wraith": "VEIL",
    "hunter": "PEEK",
    "orbiter": "SWAY",
    "dasher": "JOLT",
    "monster": "TESSERACT",
    "m_drone": "REND",
    "m_wraith": "MOAN",
    "m_hunter": "PURSUER",
    "m_orbiter": "DEADMASS",
    "m_dasher": "BURNOUT",
    "monster5d": "PENTARACT"
}

HARDCORE_ENTITY_BASE = {
    "m_drone": "drone",
    "m_wraith": "wraith",
    "m_hunter": "hunter",
    "m_orbiter": "orbiter",
    "m_dasher": "dasher"
}

HARDCORE_ENTITY_KINDS = ("m_drone","m_wraith","m_hunter","m_orbiter","m_dasher")


MARDCORE_WEAPONS = {
    "AK-47": {"cooldown":0.09,"damage":1,"speed":1500.0,"spread":0.040,"pellets":1,"knockback":150.0,"color":ORANGE},
    "M1 GARAND": {"cooldown":0.42,"damage":3,"speed":1700.0,"spread":0.014,"pellets":1,"knockback":380.0,"color":LIGHT},
    "SHOTGUN": {"cooldown":0.62,"damage":1,"speed":1280.0,"spread":0.24,"pellets":6,"knockback":115.0,"color":YELLOW}
}
MARDCORE_WEAPON_ORDER = ["AK-47","M1 GARAND","SHOTGUN"]
MARDCORE_WEAPON_DURATION = 60.00

RANK_COLORS = {
    "FUCK": RED,
    "Efficient": ORANGE,
    "Dull": LIGHT,
    "Cool": CYAN,
    "Bold": GREEN,
    "Agreeable": YELLOW,
    "Sensational": PINK,
    "SUPER Sensational": PURPLE,
    "HYPER Sensational": BLUE,
    "HELL YEAH!": WHITE,
    "CUBE": WHITE,
}

                                                                
WINDOWED_SIZE = [1100, 700]
FULLSCREEN = True
DISPLAY_SWITCH_UNTIL = 0
def portable_data_dir():
    global PORTABLE_DATA_DIR
    if PORTABLE_DATA_DIR is not None:
        return PORTABLE_DATA_DIR
    candidates=[]
    for key in ("ANDROID_PRIVATE","ANDROID_ARGUMENT","HOME"):
        value=os.environ.get(key)
        if value:
            candidates.append(Path(value))
    try:
        candidates.append(Path(__file__).resolve().parent)
    except Exception:
        pass
    candidates.append(Path.cwd())
    for base in candidates:
        try:
            folder=base if base.name.lower()=="cubed" else base/"CUBED"
            folder.mkdir(parents=True,exist_ok=True)
            probe=folder/".cubed_write_test"
            probe.write_text("ok",encoding="utf-8")
            probe.unlink(missing_ok=True)
            PORTABLE_DATA_DIR=folder
            return folder
        except Exception:
            pass
    PORTABLE_DATA_DIR=Path.cwd()
    return PORTABLE_DATA_DIR

SETTINGS_FILE = portable_data_dir()/"cubed_settings.json"
GRAPHICS_LEVELS = ["HIGHEST", "High", "Meduim", "low key", "super low key", "potato"]
GRAPHICS_QUALITY = 0

def graphics_value():
    return GRAPHICS_LEVELS[GRAPHICS_QUALITY]

def graphics_particle_step():
    return [1,1,2,3,5,8][GRAPHICS_QUALITY]

def graphics_bg_factor():
    return [1.0,.82,.64,.48,.30,.16][GRAPHICS_QUALITY]

def load_settings():
    global GAME_MUSIC_FILE, MENU_MUSIC_FILE, MUSIC_VOLUME, MENU_MUSIC_VOLUME, SOUND_VOLUME, SCREEN_SHAKE_ENABLED, IMPACT_FLASH_ENABLED, FULLSCREEN, WINDOWED_SIZE, GRAPHICS_QUALITY
    try:
        if SETTINGS_FILE.exists():
            data=json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
            if isinstance(data,dict):
                GAME_MUSIC_FILE="BY_MODE"
                MENU_MUSIC_FILE=data.get("menu_music",MENU_MUSIC_FILE)
                MUSIC_VOLUME=max(0.0,min(1.0,float(data.get("music_volume",MUSIC_VOLUME))))
                MENU_MUSIC_VOLUME=MUSIC_VOLUME
                SOUND_VOLUME=max(0.0,min(1.0,float(data.get("sound_volume",SOUND_VOLUME))))
                SCREEN_SHAKE_ENABLED=bool(data.get("screen_shake",SCREEN_SHAKE_ENABLED))
                IMPACT_FLASH_ENABLED=bool(data.get("impact_flash",IMPACT_FLASH_ENABLED))
                saved_graphics=data.get("graphics",graphics_value())
                if saved_graphics in GRAPHICS_LEVELS:
                    GRAPHICS_QUALITY=GRAPHICS_LEVELS.index(saved_graphics)
                FULLSCREEN=True
                size=data.get("windowed_size",WINDOWED_SIZE)
                if isinstance(size,list) and len(size)==2:
                    WINDOWED_SIZE=[max(800,int(size[0])),max(600,int(size[1]))]
    except:
        pass

def save_settings():
    try:
        data={
            "fullscreen":True,
            "windowed_size":[int(WINDOWED_SIZE[0]),int(WINDOWED_SIZE[1])],
            "menu_music":MENU_MUSIC_FILE,
            "game_music":"BY_MODE",
            "music_volume":round(float(MUSIC_VOLUME),2),
            "sound_volume":round(float(SOUND_VOLUME),2),
            "screen_shake":bool(SCREEN_SHAKE_ENABLED),
            "impact_flash":bool(IMPACT_FLASH_ENABLED),
            "graphics":graphics_value()
        }
        SETTINGS_FILE.write_text(json.dumps(data,indent=2),encoding="utf-8")
    except:
        pass

load_settings()
if PORTABLE_FAST_MODE:
    GRAPHICS_QUALITY=max(GRAPHICS_QUALITY,3)
    IMPACT_FLASH_ENABLED=False

def apply_display(fullscreen):
    global screen, WIDTH, HEIGHT, FULLSCREEN, DISPLAY_SWITCH_UNTIL, WINDOWED_SIZE
    old_w, old_h = WIDTH, HEIGHT
    target_fullscreen = bool(fullscreen)

    if not FULLSCREEN and screen is not None:
        current_w, current_h = screen.get_size()
        if current_w >= 800 and current_h >= 600:
            WINDOWED_SIZE[0] = current_w
            WINDOWED_SIZE[1] = current_h

    FULLSCREEN = target_fullscreen

    if FULLSCREEN:
        try:
            desktop_w, desktop_h = pygame.display.get_desktop_sizes()[0]
        except Exception:
            info = pygame.display.Info()
            desktop_w, desktop_h = info.current_w, info.current_h
        if PORTABLE_FAST_MODE and hasattr(pygame,"SCALED"):
            try:
                screen=pygame.display.set_mode(PORTABLE_LOGICAL_SIZE,pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.SCALED)
            except Exception:
                screen=pygame.display.set_mode((desktop_w,desktop_h),pygame.FULLSCREEN|pygame.DOUBLEBUF)
        else:
            screen=pygame.display.set_mode((desktop_w,desktop_h),pygame.FULLSCREEN|pygame.DOUBLEBUF)
    else:
        screen = pygame.display.set_mode((WINDOWED_SIZE[0], WINDOWED_SIZE[1]), pygame.RESIZABLE | pygame.DOUBLEBUF)

    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption(TITLE)
    DISPLAY_SWITCH_UNTIL = pygame.time.get_ticks() + 350

    resize_events = [pygame.VIDEORESIZE]
    if hasattr(pygame, "WINDOWSIZECHANGED"):
        resize_events.append(pygame.WINDOWSIZECHANGED)
    try:
        pygame.event.clear(resize_events)
    except Exception:
        pass

    save_settings()
    return old_w, old_h, WIDTH, HEIGHT

screen = None
apply_display(True)
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Comic Sans MS", 17, bold=True)
font_ui = pygame.font.SysFont("Comic Sans MS", 23, bold=True)
font_mid = pygame.font.SysFont("Comic Sans MS", 30, bold=True)
font_big = pygame.font.SysFont("Comic Sans MS", 48, bold=True)
font_title = pygame.font.SysFont("Comic Sans MS", 70, bold=True)
font_rank = pygame.font.SysFont("Comic Sans MS", 72, bold=True)
font_rank_mid = pygame.font.SysFont("Comic Sans MS", 48, bold=True)
font_rank_small = pygame.font.SysFont("Comic Sans MS", 34, bold=True)

                                                         
def clamp(v, a, b):
    return max(a, min(b, v))

def lerp(a, b, t):
    return a + (b - a) * t

def sine_tween(current, target, speed, dt):
    k = clamp(dt * speed, 0.0, 1.0)
    k = math.sin(k * math.pi * 0.5)
    return current + (target - current) * k

def sine_ease01(v):
    v = clamp(v, 0.0, 1.0)
    return math.sin(v * math.pi * 0.5)

def sign(v):
    return -1 if v < 0 else 1

class PortableKeys:
    def __init__(self, physical, touch):
        self.physical=physical
        self.touch=touch

    def __getitem__(self,key):
        value=False
        try:
            value=bool(self.physical[key])
        except Exception:
            value=False
        if key in (pygame.K_LEFT,pygame.K_a):
            return value or self.touch.held.get("left",False)
        if key in (pygame.K_RIGHT,pygame.K_d):
            return value or self.touch.held.get("right",False)
        if key==pygame.K_SPACE:
            return value or self.touch.held.get("jump",False)
        return value

class TouchController:
    def __init__(self):
        self.held={"left":False,"right":False,"jump":False}
        self.fingers={}
        self.last_finger_ms=-10000
        self.last_pointer=(0,0)
        self.joystick_finger=None
        self.joystick_dx=0.0
        self.joystick_dy=0.0

    def keys(self,physical):
        return PortableKeys(physical,self)

    def reset(self):
        self.held={"left":False,"right":False,"jump":False}
        self.fingers.clear()
        self.joystick_finger=None
        self.joystick_dx=0.0
        self.joystick_dy=0.0

    def size(self):
        return int(clamp(min(WIDTH,HEIGHT)*.088,46,70))

    def gameplay_rects(self,game=None):
        s=self.size()
        pad=max(9,int(s*.17))
        small=int(s*.74)
        jump=pygame.Rect(WIDTH-pad-s,HEIGHT-pad-s,s,s)
        dash=pygame.Rect(WIDTH-pad-s-int(s*.90),HEIGHT-pad-small,small,small)
        parry=pygame.Rect(WIDTH-pad-small,HEIGHT-pad-s-int(s*.88),small,small)
        fire=pygame.Rect(WIDTH-pad-small-int(s*.90),HEIGHT-pad-s-int(s*.88),small,small)
        pause=pygame.Rect(WIDTH-pad-46,pad,46,36)
        spawner=pygame.Rect(pad,pad,104,36)
        retry=pygame.Rect(int(WIDTH*.5-90),int(HEIGHT*.69),180,48)
        return {
            "jump":jump,
            "dash":dash,
            "parry":parry,
            "fire":fire,
            "pause":pause,
            "spawner":spawner,
            "retry":retry
        }

    def spawner_rects(self):
        s=int(clamp(min(WIDTH,HEIGHT)*.058,40,54))
        gap=max(6,int(s*.13))
        bottom=HEIGHT-gap-s
        return {
            "close":pygame.Rect(WIDTH-96-gap,gap,96,38),
            "section_prev":pygame.Rect(WIDTH-gap-s*4-gap*3,bottom,s,s),
            "section_next":pygame.Rect(WIDTH-gap-s*3-gap*2,bottom,s,s),
            "item_prev":pygame.Rect(WIDTH-gap-s*2-gap,bottom,s,s),
            "item_next":pygame.Rect(WIDTH-gap-s,bottom,s,s),
            "clear":pygame.Rect(WIDTH-96-gap,gap+46,96,36),
            "x_minus":pygame.Rect(WIDTH-gap-s*4-gap*3,bottom-s-gap,s,s),
            "x_plus":pygame.Rect(WIDTH-gap-s*3-gap*2,bottom-s-gap,s,s),
            "y_minus":pygame.Rect(WIDTH-gap-s*2-gap,bottom-s-gap,s,s),
            "y_plus":pygame.Rect(WIDTH-gap-s,bottom-s-gap,s,s)
        }

    def joystick_geometry(self):
        s=self.size()
        radius=int(clamp(s*.74,40,56))
        pad=max(12,int(s*.24))
        center=(pad+radius,HEIGHT-pad-radius)
        return center,radius

    def joystick_contains(self,pos):
        center,radius=self.joystick_geometry()
        return math.hypot(pos[0]-center[0],pos[1]-center[1])<=radius*1.32

    def update_joystick(self,pos):
        center,radius=self.joystick_geometry()
        dx=float(pos[0]-center[0])
        dy=float(pos[1]-center[1])
        dist=math.hypot(dx,dy)
        if dist>radius and dist>0:
            scale=radius/dist
            dx*=scale
            dy*=scale
        self.joystick_dx=dx
        self.joystick_dy=dy
        dead=radius*.20
        self.held["left"]=dx<-dead
        self.held["right"]=dx>dead

    def release_joystick(self):
        self.joystick_finger=None
        self.joystick_dx=0.0
        self.joystick_dy=0.0
        self.held["left"]=False
        self.held["right"]=False

    def draw_joystick(self,t):
        center,radius=self.joystick_geometry()
        pulse=.5+.5*math.sin(t*5.8)
        ring=int(radius+4+math.sin(t*4.6)*3)
        pad=10
        size=(radius+pad)*2
        local=pygame.Surface((size,size),pygame.SRCALPHA)
        lc=(size//2,size//2)
        pygame.draw.circle(local,(*DARK,int(72+26*pulse)),lc,radius)
        pygame.draw.circle(local,(*CYAN,int(135+55*pulse)),lc,ring,2)
        pygame.draw.circle(local,(*LIGHT,72),lc,int(radius*.58),1)
        knob_r=int(radius*.34+math.sin(t*7.2)*1.2)
        kx=lc[0]+int(self.joystick_dx)
        ky=lc[1]+int(self.joystick_dy)
        active=self.joystick_finger is not None
        knob_color=WHITE if active else CYAN
        pygame.draw.circle(local,(*DARK,190),(kx,ky),knob_r)
        pygame.draw.circle(local,(*knob_color,235),(kx,ky),knob_r,3)
        pygame.draw.circle(local,(*knob_color,int(35+55*pulse)),(kx,ky),knob_r+5,2)
        screen.blit(local,(center[0]-size//2,center[1]-size//2))
        draw_cursive_text("MOVE",font_small,LIGHT,center[0],center[1]+radius+13+math.sin(t*4.0)*1.5,True,.48)

    def hit_game_action(self,pos,game):
        rects=self.gameplay_rects(game)
        if game.dead and rects["retry"].collidepoint(pos):
            return "retry"
        if rects["pause"].collidepoint(pos):
            return "pause"
        if game.sandbox_mode and rects["spawner"].collidepoint(pos):
            return "spawner"
        for action in ("jump","dash","parry"):
            if rects[action].collidepoint(pos):
                return action
        armed=game.hardcore_mode or (game.sandbox_mode and game.weapon_active_timer>0)
        if armed and rects["fire"].collidepoint(pos):
            return "fire"
        return None

    def begin_finger(self,finger_id,pos,game):
        self.last_finger_ms=pygame.time.get_ticks()
        self.last_pointer=pos
        if not game.dead and self.joystick_finger is None and self.joystick_contains(pos):
            self.joystick_finger=finger_id
            self.fingers[finger_id]="joystick"
            self.update_joystick(pos)
            return "joystick"
        action=self.hit_game_action(pos,game)
        if action in self.held:
            self.fingers[finger_id]=action
            self.held[action]=True
        else:
            self.fingers[finger_id]=action
        return action

    def move_finger(self,finger_id,pos,game):
        self.last_finger_ms=pygame.time.get_ticks()
        self.last_pointer=pos
        previous=self.fingers.get(finger_id)
        if finger_id==self.joystick_finger or previous=="joystick":
            self.update_joystick(pos)
            self.fingers[finger_id]="joystick"
            return "joystick"
        if previous in self.held:
            self.held[previous]=False
        action=self.hit_game_action(pos,game)
        if action in self.held:
            self.held[action]=True
            self.fingers[finger_id]=action
        elif previous in self.held:
            self.fingers[finger_id]=None
        return action

    def end_finger(self,finger_id):
        self.last_finger_ms=pygame.time.get_ticks()
        action=self.fingers.pop(finger_id,None)
        if action=="joystick" or finger_id==self.joystick_finger:
            self.release_joystick()
            return "joystick"
        if action in self.held:
            self.held[action]=False
        return action

    def draw_button(self,rect,label,color,active,t,round_button=True):
        pulse=.5+.5*math.sin(t*7.0+rect.x*.007+rect.y*.009)
        alpha=int(PORTABLE_TOUCH_ALPHA+(34 if active else 0)+pulse*20)
        pad=12
        local=pygame.Surface((rect.w+pad*2,rect.h+pad*2),pygame.SRCALPHA)
        center=(rect.w//2+pad,rect.h//2+pad)
        if round_button:
            radius=int(min(rect.w,rect.h)*.47)
            pygame.draw.circle(local,(*DARK,alpha),center,radius)
            pygame.draw.circle(local,(*color,min(255,alpha+70)),center,radius,4 if active else 2)
            ring=radius+int(3+4*pulse)
            pygame.draw.circle(local,(*color,int(35+45*pulse)),center,ring,2)
        else:
            rr=pygame.Rect(pad,pad,rect.w,rect.h)
            pygame.draw.rect(local,(*DARK,alpha),rr,border_radius=11)
            pygame.draw.rect(local,(*color,min(255,alpha+70)),rr,3 if active else 2,border_radius=11)
        screen.blit(local,(rect.x-pad,rect.y-pad))
        scale=.68 if len(label)<=5 else .52 if len(label)<=8 else .44
        draw_cursive_text(label,font_ui,WHITE,rect.centerx,rect.centery,True,scale)

    def draw_game_controls(self,game):
        if not PORTABLE_TOUCH:
            return
        t=game.elapsed
        rects=self.gameplay_rects(game)
        if game.dead:
            self.draw_button(rects["retry"],"RETRY",RED,False,t,False)
            return
        self.draw_joystick(t)
        self.draw_button(rects["jump"],"JUMP",WHITE,self.held["jump"],t)
        self.draw_button(rects["dash"],"DASH",CYAN,game.player.dash_move_timer>0,t)
        self.draw_button(rects["parry"],"PARRY",GREEN,game.player.parry_timer>0,t)
        armed=game.hardcore_mode or (game.sandbox_mode and game.weapon_active_timer>0)
        if armed:
            self.draw_button(rects["fire"],"FIRE",ORANGE,game.weapon_flash>0,t)
        self.draw_button(rects["pause"],"II",LIGHT,False,t,False)
        if game.sandbox_mode:
            self.draw_button(rects["spawner"],"SPAWNER",YELLOW,False,t,False)

    def draw_spawner_controls(self,menu):
        if not PORTABLE_TOUCH:
            return
        t=menu.t
        rects=self.spawner_rects()
        self.draw_button(rects["close"],"CLOSE",LIGHT,False,t,False)
        self.draw_button(rects["clear"],"CLEAR",RED,False,t,False)
        self.draw_button(rects["section_prev"],"SEC ←",CYAN,False,t,False)
        self.draw_button(rects["section_next"],"SEC →",CYAN,False,t,False)
        self.draw_button(rects["item_prev"],"ITEM ↑",WHITE,False,t,False)
        self.draw_button(rects["item_next"],"ITEM ↓",WHITE,False,t,False)
        if menu.current_spawner_section()=="PLATFORMS":
            self.draw_button(rects["x_minus"],"X -",YELLOW,False,t,False)
            self.draw_button(rects["x_plus"],"X +",YELLOW,False,t,False)
            self.draw_button(rects["y_minus"],"Y -",GREEN,False,t,False)
            self.draw_button(rects["y_plus"],"Y +",GREEN,False,t,False)

CURSIVE_PATHS = {
    "a":[[(0.00,.76),(.10,.69),(.18,.48),(.34,.36),(.53,.39),(.59,.55),(.50,.70),(.34,.76),(.19,.68),(.18,.52),(.31,.39),(.52,.41),(.58,.58),(.62,.76),(.76,.72)]],
    "b":[[(0.00,.76),(.10,.70),(.17,.34),(.20,.05),(.29,-.05),(.38,.08),(.34,.32),(.25,.56),(.23,.72),(.31,.53),(.45,.39),(.61,.43),(.67,.58),(.61,.71),(.47,.77),(.32,.70),(.40,.61),(.64,.60),(.78,.72)]],
    "c":[[(0.00,.76),(.10,.69),(.18,.49),(.34,.38),(.53,.39),(.61,.48),(.54,.51),(.42,.45),(.27,.48),(.20,.61),(.27,.72),(.45,.76),(.66,.71),(.78,.72)]],
    "d":[[(0.00,.76),(.10,.69),(.18,.49),(.34,.37),(.52,.40),(.58,.57),(.51,.71),(.34,.76),(.20,.69),(.20,.54),(.34,.42),(.56,.43),(.62,.57),(.62,.30),(.66,.04),(.73,-.05),(.81,.08),(.77,.34),(.70,.61),(.73,.76),(.87,.72)]],
    "e":[[(0.00,.76),(.10,.70),(.18,.59),(.34,.54),(.50,.55),(.57,.48),(.49,.40),(.34,.42),(.22,.50),(.20,.63),(.30,.73),(.48,.76),(.67,.71),(.78,.72)]],
    "f":[[(0.00,.76),(.10,.70),(.20,.50),(.27,.18),(.35,-.04),(.47,-.10),(.56,.00),(.49,.17),(.36,.31),(.28,.48),(.24,.74),(.23,1.02),(.17,1.18),(.10,1.12),(.15,.93),(.31,.72),(.50,.70),(.67,.72)],[(.10,.39),(.55,.35)]],
    "g":[[(0.00,.76),(.10,.69),(.18,.49),(.34,.37),(.52,.40),(.58,.56),(.51,.70),(.34,.76),(.20,.69),(.20,.53),(.34,.41),(.56,.43),(.62,.59),(.59,.78),(.57,1.01),(.50,1.18),(.38,1.26),(.25,1.18),(.34,1.10),(.52,1.07),(.69,.86),(.78,.72)]],
    "h":[[(0.00,.76),(.10,.70),(.17,.34),(.20,.05),(.29,-.05),(.38,.08),(.34,.31),(.25,.53),(.23,.74),(.31,.57),(.42,.43),(.55,.42),(.62,.52),(.63,.72),(.72,.76),(.82,.72)]],
    "i":[[(0.00,.76),(.11,.70),(.18,.54),(.19,.72),(.28,.76),(.39,.72)],[(.18,.27),(.19,.24)]],
    "j":[[(0.00,.76),(.10,.70),(.18,.54),(.18,.77),(.16,1.01),(.10,1.17),(.03,1.15),(.07,1.03),(.20,.87),(.34,.73)],[(.18,.27),(.19,.24)]],
    "k":[[(0.00,.76),(.10,.70),(.17,.34),(.20,.05),(.29,-.05),(.37,.08),(.33,.31),(.25,.52),(.23,.75),(.31,.61),(.42,.48),(.55,.40),(.46,.55),(.36,.61),(.46,.62),(.58,.73),(.72,.72)]],
    "l":[[(0.00,.76),(.10,.70),(.18,.40),(.23,.10),(.31,-.06),(.41,.02),(.39,.18),(.28,.38),(.23,.60),(.26,.73),(.38,.76),(.52,.72)]],
    "m":[[(0.00,.76),(.10,.70),(.18,.51),(.19,.73),(.27,.57),(.38,.43),(.49,.44),(.56,.54),(.56,.73),(.64,.57),(.75,.43),(.87,.44),(.94,.55),(.94,.72),(1.04,.76),(1.15,.72)]],
    "n":[[(0.00,.76),(.10,.70),(.18,.51),(.19,.73),(.28,.57),(.40,.43),(.53,.44),(.60,.55),(.60,.72),(.70,.76),(.82,.72)]],
    "o":[[(0.00,.76),(.10,.69),(.18,.49),(.34,.37),(.52,.40),(.59,.55),(.54,.69),(.39,.76),(.23,.72),(.18,.58),(.24,.45),(.41,.39),(.56,.47),(.61,.64),(.71,.74),(.82,.72)]],
    "p":[[(0.00,.76),(.10,.70),(.18,.52),(.17,.76),(.15,1.03),(.10,1.18),(.17,1.09),(.24,.83),(.28,.57),(.37,.43),(.51,.40),(.61,.49),(.61,.62),(.52,.71),(.39,.72),(.29,.63),(.38,.58),(.61,.62),(.75,.72)]],
    "q":[[(0.00,.76),(.10,.69),(.18,.49),(.34,.37),(.52,.40),(.59,.55),(.52,.70),(.35,.76),(.20,.69),(.19,.53),(.34,.41),(.56,.43),(.61,.58),(.61,.78),(.62,1.04),(.70,1.18),(.78,1.06),(.72,.88),(.70,.72),(.84,.72)]],
    "r":[[(0.00,.76),(.10,.70),(.18,.53),(.19,.73),(.27,.58),(.37,.44),(.48,.43),(.55,.50),(.48,.55),(.39,.52),(.47,.58),(.55,.72),(.68,.72)]],
    "s":[[(0.00,.76),(.10,.69),(.20,.51),(.34,.39),(.49,.42),(.52,.50),(.42,.55),(.28,.58),(.22,.66),(.30,.74),(.46,.75),(.62,.70),(.74,.72)]],
    "t":[[(0.00,.76),(.10,.70),(.18,.49),(.23,.20),(.28,.07),(.31,.30),(.27,.58),(.28,.72),(.39,.76),(.54,.72)],[(.08,.42),(.47,.38)]],
    "u":[[(0.00,.76),(.10,.70),(.18,.51),(.18,.68),(.25,.76),(.37,.75),(.49,.61),(.54,.47),(.55,.72),(.65,.76),(.78,.72)]],
    "v":[[(0.00,.76),(.10,.70),(.18,.50),(.27,.73),(.39,.77),(.52,.62),(.61,.43),(.67,.58),(.70,.72),(.82,.72)]],
    "w":[[(0.00,.76),(.10,.70),(.18,.50),(.26,.73),(.37,.77),(.48,.61),(.54,.48),(.60,.71),(.71,.77),(.82,.61),(.90,.44),(.96,.59),(1.00,.72),(1.12,.72)]],
    "x":[[(0.00,.76),(.10,.70),(.18,.52),(.30,.43),(.42,.57),(.53,.73),(.66,.72)],[(.17,.72),(.29,.59),(.42,.45),(.54,.39)]],
    "y":[[(0.00,.76),(.10,.70),(.18,.50),(.27,.73),(.39,.77),(.51,.62),(.58,.45),(.60,.67),(.58,.88),(.53,1.07),(.43,1.20),(.31,1.18),(.37,1.10),(.55,1.02),(.68,.84),(.80,.72)]],
    "z":[[(0.00,.76),(.10,.70),(.20,.50),(.35,.42),(.50,.44),(.39,.57),(.27,.69),(.43,.74),(.60,.70),(.69,.73),(.62,.87),(.53,.99),(.60,1.06),(.72,.96),(.79,.73)]]
}

CURSIVE_DIGITS = {
    "0":[[(.05,.72),(.12,.44),(.28,.26),(.48,.25),(.61,.43),(.60,.67),(.47,.80),(.26,.79),(.10,.63),(.05,.44),(.12,.30),(.31,.25),(.52,.34),(.62,.55),(.56,.72)]],
    "1":[[(.06,.48),(.20,.35),(.31,.24),(.31,.74),(.48,.74)]],
    "2":[[(.05,.46),(.15,.30),(.34,.24),(.51,.31),(.53,.43),(.43,.55),(.22,.69),(.09,.77),(.33,.75),(.56,.73)]],
    "3":[[(.05,.35),(.19,.25),(.39,.25),(.51,.35),(.43,.48),(.28,.53),(.43,.55),(.54,.66),(.49,.76),(.31,.80),(.13,.73)]],
    "4":[[(.48,.76),(.48,.24),(.12,.61),(.61,.60)]],
    "5":[[(.54,.27),(.19,.27),(.14,.50),(.34,.47),(.51,.53),(.55,.68),(.45,.77),(.25,.78),(.09,.69)]],
    "6":[[(.52,.29),(.37,.24),(.20,.32),(.11,.49),(.12,.68),(.26,.78),(.43,.76),(.53,.63),(.48,.51),(.33,.46),(.18,.52)]],
    "7":[[(.08,.27),(.57,.27),(.43,.43),(.31,.59),(.22,.76)]],
    "8":[[(.31,.51),(.16,.42),(.16,.30),(.30,.23),(.45,.29),(.47,.40),(.31,.51),(.16,.60),(.15,.72),(.30,.80),(.47,.73),(.48,.61),(.31,.51)]],
    "9":[[(.50,.54),(.38,.60),(.22,.56),(.13,.44),(.17,.31),(.31,.24),(.47,.31),(.55,.46),(.53,.65),(.43,.78),(.26,.81)]]
}

CURSIVE_SYMBOLS = {
    "!":[[(.20,.22),(.20,.60)],[(.20,.76),(.21,.76)]],
    "?":[[(.04,.36),(.13,.25),(.30,.22),(.43,.29),(.45,.40),(.36,.49),(.25,.54),(.23,.62)],[(.23,.76),(.24,.76)]],
    ".":[[(.12,.76),(.13,.76)]],
    ",":[[(.13,.75),(.10,.86)]],
    ":":[[(.13,.42),(.14,.42)],[(.13,.75),(.14,.75)]],
    ";":[[(.13,.42),(.14,.42)],[(.13,.74),(.10,.86)]],
    "-":[[(.03,.56),(.42,.54)]],
    "_":[[(.02,.80),(.48,.80)]],
    "+":[[(.23,.36),(.23,.72)],[(.05,.54),(.42,.54)]],
    "=":[[(.04,.47),(.44,.47)],[(.04,.64),(.44,.64)]],
    "/":[[(.04,.78),(.44,.24)]],
    "\\":[[(.04,.24),(.44,.78)]],
    "'":[[(.13,.22),(.10,.37)]],
    "\"":[[(.10,.22),(.08,.37)],[(.26,.22),(.24,.37)]],
    "(":[[(.30,.18),(.18,.34),(.12,.53),(.17,.72),(.29,.86)]],
    ")":[[(.10,.18),(.22,.34),(.28,.53),(.23,.72),(.11,.86)]],
    "[":[[(.30,.20),(.14,.20),(.14,.82),(.30,.82)]],
    "]":[[(.10,.20),(.26,.20),(.26,.82),(.10,.82)]],
    "%":[[(.06,.76),(.46,.24)],[(.10,.34),(.15,.28),(.22,.31),(.21,.39),(.14,.42),(.10,.34)],[(.32,.67),(.37,.61),(.44,.64),(.43,.72),(.36,.75),(.32,.67)]],
    "<":[[(.42,.32),(.08,.54),(.42,.76)]],
    ">":[[(.08,.32),(.42,.54),(.08,.76)]],
    "↑":[[(.22,.78),(.22,.28)],[(.08,.42),(.22,.28),(.36,.42)]],
    "↓":[[(.22,.28),(.22,.78)],[(.08,.64),(.22,.78),(.36,.64)]],
    "←":[[(.42,.54),(.08,.54)],[(.22,.40),(.08,.54),(.22,.68)]],
    "→":[[(.08,.54),(.42,.54)],[(.28,.40),(.42,.54),(.28,.68)]],
    "•":[[(.18,.55),(.19,.55)]],
    "|":[[(.18,.22),(.18,.80)]],
    "*":[[(.20,.34),(.20,.72)],[(.06,.45),(.34,.62)],[(.34,.45),(.06,.62)]]
}

CURSIVE_WIDTHS = {
    "i":.30,"j":.34,"l":.34,"t":.42,"f":.46,"r":.48,"s":.50,"c":.52,"e":.52,
    "a":.55,"o":.56,"u":.57,"v":.57,"x":.57,"y":.58,"z":.58,"b":.60,"d":.61,
    "g":.61,"h":.61,"k":.61,"n":.62,"p":.62,"q":.62,"m":.86,"w":.84
}

CURSIVE_GLYPH_CACHE = {}

def cursive_font_height(font):
    try:
        return max(10.0,float(font.get_height())*.88)
    except Exception:
        return 20.0

def cursive_char_width(ch,height):
    if ch == " ":
        return height*.34
    low=ch.lower()
    if low in CURSIVE_WIDTHS:
        w=CURSIVE_WIDTHS[low]*height
        if ch.isupper():
            w*=1.08
        return w
    if ch.isdigit():
        return height*.47
    return height*.42

def cursive_text_width(text,font,scale=1.0):
    height=cursive_font_height(font)*scale
    total=0.0
    text=str(text)
    for i,ch in enumerate(text):
        total+=cursive_char_width(ch,height)
        if i<len(text)-1 and ch!=" ":
            total-=height*.055
    return max(0.0,total)

def cursive_paths_for(ch):
    low=ch.lower()
    if low in CURSIVE_PATHS:
        return CURSIVE_PATHS[low]
    if ch in CURSIVE_DIGITS:
        return CURSIVE_DIGITS[ch]
    if ch in CURSIVE_SYMBOLS:
        return CURSIVE_SYMBOLS[ch]
    return CURSIVE_SYMBOLS["?"]

def cursive_catmull(points,steps=3):
    if len(points)<2:
        return points[:]
    padded=[points[0]]+points+[points[-1]]
    out=[]
    for i in range(1,len(padded)-2):
        p0,p1,p2,p3=padded[i-1],padded[i],padded[i+1],padded[i+2]
        for s in range(steps):
            u=s/steps
            u2=u*u
            u3=u2*u
            x=.5*((2*p1[0])+(-p0[0]+p2[0])*u+(2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*u2+(-p0[0]+3*p1[0]-3*p2[0]+p3[0])*u3)
            y=.5*((2*p1[1])+(-p0[1]+p2[1])*u+(2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*u2+(-p0[1]+3*p1[0]-3*p2[0]+p3[0])*0+(-p0[1]+3*p1[1]-3*p2[1]+p3[1])*u3)
            out.append((x,y))
    out.append(points[-1])
    return out

def cursive_glyph_surface(ch,height,color):
    h=max(8,int(round(height)))
    key=(ch,h,color)
    cached=CURSIVE_GLYPH_CACHE.get(key)
    if cached is not None:
        return cached

    w=max(4,int(round(cursive_char_width(ch,h))))
    pad=max(4,int(h*.24))
    surf=pygame.Surface((w+pad*2,int(h*1.48)+pad*2),pygame.SRCALPHA)
    thickness=max(1,int(h*.055))
    paths=cursive_paths_for(ch)
    upper=ch.isalpha() and ch.isupper()
    local_h=h*(1.06 if upper else 1.0)
    top=pad-(local_h-h)*.18

    for stroke in paths:
        smooth=cursive_catmull(stroke,3)
        pts=[]
        for px,py in smooth:
            slant=(.76-py)*local_h*.13
            sx=pad+px*w+slant
            sy=top+py*local_h
            if upper:
                sy-=local_h*.045
            pts.append((sx,sy))
        if len(pts)>=2:
            pygame.draw.lines(surf,color,False,pts,thickness)
        elif pts:
            pygame.draw.circle(surf,color,(int(pts[0][0]),int(pts[0][1])),max(1,int(thickness*.65)))

    if ch.lower() in ("i","j"):
        dot_x=pad+w*.48
        dot_y=top+h*.22
        pygame.draw.circle(surf,color,(int(dot_x),int(dot_y)),max(1,int(thickness*.72)))

    CURSIVE_GLYPH_CACHE[key]=(surf,w,pad)
    return surf,w,pad

def draw_cursive_connector(x1,y1,x2,y2,color,h,t,phase,thickness):
    mid=(x1+x2)*.5
    lift=math.sin(t*2.8+phase)*h*.018
    pts=[(x1,y1),(mid,(y1+y2)*.5-h*.045+lift),(x2,y2)]
    pygame.draw.lines(screen,color,False,pts,max(1,int(thickness)))

def draw_cursive_text(text,font,color,x,y,center=False,scale=1.0):
    text=str(text)
    h=max(8.0,cursive_font_height(font)*scale)
    total_h=h*1.30
    total_w=cursive_text_width(text,font,scale)
    t=pygame.time.get_ticks()*.001
    motion_phase=t*2.15+x*.0017+y*.0023
    whole_x=math.sin(motion_phase)*h*.022
    whole_y=math.sin(t*2.75+x*.0011+y*.0019)*h*.040
    start_x=float(x-total_w*.5 if center else x)+whole_x
    top=float(y-total_h*.5 if center else y)+whole_y
    cursor=start_x
    thickness=max(1.0,h*.055)
    previous_exit=None
    previous_was_word=False

    for i,ch in enumerate(text):
        if ch==" ":
            cursor+=cursive_char_width(ch,h)
            previous_exit=None
            previous_was_word=False
            continue

        surf,w,pad=cursive_glyph_surface(ch,h,color)
        phase=i*.73+x*.002+y*.003
        wave_y=math.sin(t*4.15+phase)*h*.045
        wave_x=math.sin(t*3.25+phase*.71)*h*.016
        micro_bob=math.sin(t*6.0+i*.47+phase)*h*.008
        blit_x=cursor-pad+wave_x
        blit_y=top-pad+wave_y+micro_bob

        entry=(cursor,top+.76*h+wave_y+micro_bob)
        if previous_exit is not None and previous_was_word and (ch.isalnum() or ch in "'"):
            draw_cursive_connector(previous_exit[0],previous_exit[1],entry[0],entry[1],color,h,t,phase,thickness)

        screen.blit(surf,(int(blit_x),int(blit_y)))

        previous_exit=(cursor+w*.98,top+.72*h+wave_y+micro_bob)
        previous_was_word=ch.isalnum() or ch in "'"
        cursor+=w-h*.055+math.sin(t*3.0+i*.51)*h*.003

    return pygame.Rect(int(start_x),int(top-h*.12),max(1,int(total_w)),max(1,int(total_h+h*.18)))

def draw_text(text,font,color,x,y,center=False):
    return draw_cursive_text(text,font,color,x,y,center,1.0)

def draw_sine_font(text,color,x,y,max_width=None,height=42,center_y=True):
    class _ProceduralSize:
        def __init__(self,h):
            self.h=h
        def get_height(self):
            return self.h
    temp_font=_ProceduralSize(height/0.88)
    width=cursive_text_width(text,temp_font)
    scale=1.0
    if max_width is not None and width>max_width:
        scale=max_width/max(1.0,width)
    return draw_cursive_text(text,temp_font,color,x,y,center_y,scale)

def rank_scores_for_mode(mode="main"):
    if mode == "mardcore":
        return RANK_SCORE_MARDCORE
    if mode == "sandbox":
        return RANK_SCORE_SANDBOX
    return RANK_SCORE_MAIN

def rank_for_score(score, mode="main"):
    scores=rank_scores_for_mode(mode)
    for rank in reversed(RANK_ORDER):
        if score >= scores[rank]:
            return rank
    return RANK_ORDER[0]

def rank_font_for_name(rank):
    if len(rank) >= 17:
        return font_rank_small
    if len(rank) >= 10:
        return font_rank_mid
    return font_rank

def draw_rank_cube(cx, cy, t, color, scale=1.0):
    size = (34 + math.sin(t * 4.2) * 3) * scale
    angle = t * 2.6 + math.sin(t * 1.9) * 0.22
    tilt = math.sin(t * 3.3) * 0.55
    points3d = [
        (-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),
        (-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)
    ]
    pts=[]
    ca,sa=math.cos(angle),math.sin(angle)
    cb,sb=math.cos(tilt),math.sin(tilt)
    for x,y,z in points3d:
        x,z=x*ca-z*sa,x*sa+z*ca
        y,z=y*cb-z*sb,y*sb+z*cb
        depth=3.4+z
        px=cx+(x/depth)*size*2.5
        py=cy+(y/depth)*size*2.5+math.sin(t*5.2+x*2+y)*2.2
        pts.append((px,py))
    edges=((0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7))
    for a,b in edges:
        pygame.draw.line(screen,color,pts[a],pts[b],3)
    core=8+math.sin(t*6.4)*2
    pygame.draw.rect(screen,DARK,(cx-core,cy-core,core*2,core*2),border_radius=4)
    pygame.draw.rect(screen,color,(cx-core,cy-core,core*2,core*2),2,border_radius=4)

def world_to_screen_y(world_y, camera_y):
    return world_y - camera_y

def rect_overlap_circle(rect, cx, cy, radius):
    nx = clamp(cx, rect.left, rect.right)
    ny = clamp(cy, rect.top, rect.bottom)
    dx = cx - nx
    dy = cy - ny
    return dx*dx + dy*dy <= radius*radius

def audio_search_dirs():
    dirs = []
    if getattr(sys, "frozen", False):
        try:
            exe_dir=Path(sys.executable).resolve().parent
            if exe_dir not in dirs:
                dirs.append(exe_dir)
        except Exception:
            pass
        if hasattr(sys, "_MEIPASS"):
            bundle_dir=Path(sys._MEIPASS).resolve()
            if bundle_dir not in dirs:
                dirs.append(bundle_dir)
    try:
        script_dir=Path(__file__).resolve().parent
        if script_dir not in dirs:
            dirs.append(script_dir)
    except Exception:
        pass
    cwd=Path.cwd().resolve()
    if cwd not in dirs:
        dirs.append(cwd)
    return dirs

def available_song_names():
    names = []
    seen = set()
    for folder in audio_search_dirs():
        try:
            for f in folder.iterdir():
                if f.is_file() and f.suffix.lower() in (".ogg", ".wav", ".mp3"):
                    low = f.name.lower()
                    if low not in seen:
                        seen.add(low)
                        names.append(f.name)
        except OSError:
            pass
    names.sort(key=lambda n: n.lower())
    return names

def cycle_song(current, delta):
    songs = ["AUTO", "OFF"] + available_song_names()
    current_label = "AUTO" if current is None else current
    if current_label not in songs:
        songs.append(current_label)
    idx = songs.index(current_label)
    return songs[(idx + delta) % len(songs)]

def find_audio_file(wanted=None, exclude_names=()):
    search_dirs = audio_search_dirs()
    excluded = {name.lower() for name in exclude_names if name}
    wanted_lower = wanted.lower() if wanted else None

    if wanted_lower:
        for folder in search_dirs:
            try:
                for f in folder.iterdir():
                    if f.is_file() and f.name.lower() == wanted_lower:
                        return f
            except OSError:
                pass

    candidates = []
    for folder in search_dirs:
        try:
            for f in folder.iterdir():
                if f.is_file() and f.suffix.lower() in (".ogg", ".wav", ".mp3") and f.name.lower() not in excluded:
                    candidates.append(f)
        except OSError:
            pass

    if not candidates:
        return None

    return sorted(candidates, key=lambda x: ({".ogg": 0, ".wav": 1, ".mp3": 2}.get(x.suffix.lower(), 9), x.name.lower()))[0]

def audio_name_key(value):
    return "".join(ch for ch in str(value).lower() if ch.isalnum())

def find_named_audio(stem):
    wanted=audio_name_key(stem)
    for folder in audio_search_dirs():
        try:
            for f in folder.iterdir():
                if f.is_file() and f.suffix.lower() in (".ogg",".wav",".mp3") and audio_name_key(f.stem)==wanted:
                    return f
        except OSError:
            pass
    return None

def play_music_file(wanted=None, volume=MUSIC_VOLUME, exclude_names=(), start_pos=0.0):
    global AUDIO_OK, AUDIO_ERROR

    if not AUDIO_OK:
        return None, "Mixer unavailable"

    chosen = find_audio_file(wanted, exclude_names)

    if chosen is None:
        return None, "No compatible music file found"

    try:
        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.unload()
        except Exception:
            pass
        pygame.mixer.music.load(str(chosen))
        pygame.mixer.music.set_volume(volume)
        start_pos=max(0.0,float(start_pos))
        try:
            pygame.mixer.music.play(-1,start=start_pos)
        except Exception:
            pygame.mixer.music.play(-1)
            if start_pos>0:
                try:
                    pygame.mixer.music.set_pos(start_pos)
                except Exception:
                    pass
        print(f"MUSIC OK: {chosen} @ {start_pos:.2f}s")
        return chosen.name, f"PLAYING: {chosen.name} @ {start_pos:.2f}s"
    except Exception as e:
        AUDIO_ERROR = str(e)
        msg = f"Could not play {chosen.name}: {e}"
        print("MUSIC ERROR:", msg)
        return None, msg

def music_setup(game_mode="main"):
    stop_death_tone()
    stop_death_music_pitch()
    target=MODE_MUSIC_FILES.get(game_mode,MODE_MUSIC_FILES["main"])
    start_pos=MODE_MUSIC_START.get(game_mode,0.0)
    chosen=find_named_audio(target)
    if chosen is None:
        if AUDIO_OK:
            pygame.mixer.music.stop()
        searched=", ".join(str(p) for p in audio_search_dirs())
        print(f"MUSIC MISSING FOR {game_mode.upper()}: {target} | SEARCHED: {searched}")
        return None,f"MISSING {game_mode.upper()} MUSIC: {target}"
    name,status=play_music_file(chosen.name,MUSIC_VOLUME,start_pos=start_pos)
    if name:
        if start_pos>0:
            mins=int(start_pos//60)
            secs=start_pos-mins*60
            return name,f"{game_mode.upper()}: {name} FROM {mins}:{secs:05.2f}"
        return name,f"{game_mode.upper()}: {name}"
    return name,status

def menu_music_setup():
    stop_death_tone()
    stop_death_music_pitch()
    if MENU_MUSIC_FILE == "OFF":
        if AUDIO_OK:
            pygame.mixer.music.stop()
        return None, "MENU MUSIC: OFF"
    chosen=find_named_audio("menu")
    if chosen is None:
        if AUDIO_OK:
            pygame.mixer.music.stop()
        searched=", ".join(str(p) for p in audio_search_dirs())
        print(f"MENU MUSIC MISSING | SEARCHED: {searched}")
        return None,"MISSING MENU MUSIC"
    return play_music_file(chosen.name,MUSIC_VOLUME)

SFX_BANK = {}

def synth_cubed_sfx(kind):
    if not AUDIO_OK:
        return None
    rate=44100
    durations={
        "jump":.145,
        "double_jump":.22,
        "dash":.19,
        "parry":.19,
        "parry_hit":.27,
        "step":.045,
        "land":.18,
        "powerup":.34,
        "weapon_pickup":.36,
        "hit":.20,
        "shield":.34,
        "gun_ak":.095,
        "gun_m1":.235,
        "gun_shotgun":.31,
        "orb_yellow":.27,
        "orb_cyan":.32,
        "tesseract":.72,
        "pentaract":.92,
        "death":.10,
        "enemy_hit":.075,
        "enemy_down":.19
    }
    duration=durations.get(kind,.15)
    count=max(1,int(rate*duration))
    samples=array("h")

    def tone(tt,f,phase=0.0):
        return math.sin(math.tau*f*tt+phase)

    def chirp(tt,f0,f1,span,phase=0.0):
        span=max(.001,span)
        x=min(max(tt,0.0),span)
        sweep=(f1-f0)/span
        return math.sin(math.tau*(f0*x+.5*sweep*x*x)+phase)

    def sine_noise(tt,seed=0.0):
        return (
            math.sin(math.tau*2411*tt+seed)
            +math.sin(math.tau*3767*tt+seed*1.37+.8)
            +math.sin(math.tau*5521*tt+seed*.73+1.9)
            +math.sin(math.tau*8167*tt+seed*1.11+2.7)
            +math.sin(math.tau*12011*tt+seed*.51+4.1)
            +math.sin(math.tau*15727*tt+seed*1.83+5.0)
        )/6.0

    def harmonic(tt,f,phase=0.0):
        a=math.tau*f*tt+phase
        return (
            math.sin(a)
            +math.sin(a*2+.31)*.34
            +math.sin(a*3+.77)*.19
            +math.sin(a*5+1.18)*.09
        )

    def bell(tt,f,decay,phase=0.0):
        e=max(0.0,1.0-tt/max(.001,decay))
        return (
            tone(tt,f,phase)*.64
            +tone(tt,f*1.503,phase+.7)*.23
            +tone(tt,f*2.014,phase+1.4)*.13
        )*(e**1.55)

    def pulse_env(x,attack=.02,release=.20):
        a=math.sin(min(1.0,max(0.0,x/attack))*math.pi*.5)
        r=math.sin(min(1.0,max(0.0,(duration-x)/release))*math.pi*.5)
        return a*r

    for i in range(count):
        t=i/rate
        p=t/duration
        attack=math.sin(min(1.0,t/.0035)*math.pi*.5)
        release=math.sin(min(1.0,max(0.0,(duration-t)/max(.015,duration*.25)))*math.pi*.5)
        env=attack*release
        v=0.0

        if kind=="jump":
            snap=max(0.0,1-p*12)
            v=chirp(t,245,760,duration)*.54
            v+=chirp(t,520,1320,duration,.55)*.19
            v+=harmonic(t,305+380*p,.3)*.10*(1-p)
            v+=sine_noise(t,.4)*snap*.22
            v+=tone(t,92)*math.sin(p*math.pi)*.10
        elif kind=="double_jump":
            snap=max(0.0,1-p*10)
            v=chirp(t,360,1080,duration)*.40
            v+=chirp(t,710,1810,duration,.9)*.20
            if t>.047:
                tt=t-.047
                e=max(0.0,1-tt/(duration-.047))
                v+=chirp(tt,540,1470,duration-.047,1.1)*.33*e
            v+=bell(t,1560,duration,.6)*.11
            v+=sine_noise(t,1.3)*snap*.16
        elif kind=="dash":
            body=math.sin(p*math.pi)
            snap=max(0.0,1-p*9)
            v=chirp(t,310,48,duration)*.43
            v+=chirp(t,1280,120,duration,.8)*.24
            v+=tone(t,54+math.sin(t*21)*4)*body*.24
            v+=sine_noise(t,2.1)*(1-p)**1.2*.42
            v+=harmonic(t,88,.2)*snap*.13
        elif kind=="parry":
            snap=max(0.0,1-p*13)
            v=bell(t,1180,duration,.2)*.52
            v+=bell(t,1760,duration,.9)*.32
            v+=chirp(t,3400,1280,duration,1.3)*.16
            v+=tone(t,240)*math.sin(p*math.pi)*(1-p)*.10
            v+=sine_noise(t,3.6)*snap*.14
        elif kind=="parry_hit":
            snap=max(0.0,1-p*10)
            ring=(1-p)**1.25
            v=chirp(t,210,46,duration)*.48
            v+=bell(t,760,duration,.4)*.30
            v+=bell(t,1215,duration,.9)*.23
            v+=bell(t,1870,duration,1.5)*.15
            v+=sine_noise(t,4.2)*(1-p)**1.5*.40
            v+=harmonic(t,116,.7)*snap*.17
            v*=.86+.14*math.sin(t*96)*ring
        elif kind=="step":
            snap=max(0.0,1-p*7)
            v=chirp(t,125,64,duration)*.30
            v+=sine_noise(t,5.1)*snap*.24
        elif kind=="land":
            snap=max(0.0,1-p*8)
            v=chirp(t,138,38,duration)*.60
            v+=harmonic(t,62,.5)*(1-p)**1.7*.17
            v+=sine_noise(t,5.7)*(1-p)**1.45*.39
            v+=tone(t,34)*math.sin(p*math.pi)*.17
            v+=tone(t,310)*snap*.06
        elif kind=="powerup":
            notes=(440.0,659.25,987.77)
            seg=min(2,int(p*3))
            local=p*3-seg
            gate=math.sin(min(1.0,local*5)*math.pi*.5)*math.sin(min(1.0,max(0.0,(1-local)*4))*math.pi*.5)
            f=notes[seg]
            v=tone(t,f)*gate*.29
            v+=tone(t,f*2,.6)*gate*.10
            v+=chirp(t,300,1280,duration,1.0)*.19
            v+=bell(t,1720,duration,1.3)*.12
        elif kind=="weapon_pickup":
            snap=max(0.0,1-p*10)
            v=chirp(t,180,670,duration)*.28
            v+=chirp(t,510,1560,duration,.7)*.23
            v+=harmonic(t,93,.4)*(1-p)*.20
            v+=bell(t,820,duration,1.0)*.16
            v+=sine_noise(t,6.8)*snap*.18
        elif kind=="hit":
            snap=max(0.0,1-p*9)
            v=chirp(t,205,41,duration)*.55
            v+=harmonic(t,84,.6)*(1-p)**1.5*.19
            v+=sine_noise(t,7.4)*(1-p)**1.25*.43
            v+=chirp(t,920,180,duration,.7)*snap*.10
        elif kind=="shield":
            shimmer=(1-p)**1.15
            v=bell(t,510,duration,.2)*.31
            v+=bell(t,1018,duration,.8)*.24
            v+=bell(t,1525,duration,1.4)*.19
            v+=chirp(t,1900,520,duration,1.0)*.13
            v+=tone(t,78)*math.sin(p*math.pi)*.12
            v*=.92+.08*math.sin(t*44)*shimmer
        elif kind=="gun_ak":
            snap=max(0.0,1-p*14)
            v=chirp(t,320,66,duration)*.42
            v+=chirp(t,1880,280,duration,.7)*.23
            v+=harmonic(t,118,.3)*(1-p)**1.6*.18
            v+=sine_noise(t,8.1)*(1-p)**1.65*.48
            v+=tone(t,2600)*snap*.08
        elif kind=="gun_m1":
            snap=max(0.0,1-p*11)
            v=chirp(t,235,38,duration)*.54
            v+=chirp(t,3100,460,duration,.9)*.30
            v+=bell(t,910,duration,.4)*.17
            v+=harmonic(t,76,.8)*(1-p)**1.35*.18
            v+=sine_noise(t,8.8)*(1-p)**1.55*.39
            v+=tone(t,3700)*snap*.07
        elif kind=="gun_shotgun":
            snap=max(0.0,1-p*8)
            v=chirp(t,170,28,duration)*.65
            v+=chirp(t,980,74,duration,.5)*.23
            v+=harmonic(t,54,.2)*(1-p)**1.2*.22
            v+=sine_noise(t,9.5)*(1-p)**.95*.59
            v+=tone(t,1900)*snap*.07
        elif kind=="orb_yellow":
            v=chirp(t,520,1340,duration)*.35
            v+=bell(t,900,duration,.5)*.22
            v+=bell(t,1348,duration,1.1)*.16
            v+=tone(t,1880+math.sin(t*22)*70)*(1-p)*.08
            v+=tone(t,110)*math.sin(p*math.pi)*.07
        elif kind=="orb_cyan":
            v=chirp(t,390,1760,duration)*.37
            v+=chirp(t,760,2460,duration,.9)*.17
            v+=bell(t,1120,duration,.4)*.18
            v+=bell(t,1680,duration,1.2)*.14
            v+=tone(t,88)*math.sin(p*math.pi)*.11
        elif kind=="tesseract":
            swell=math.sin(p*math.pi)
            v=tone(t,69+math.sin(t*4.1)*7)*.24*swell
            v+=tone(t,103+math.sin(t*5.3+1.0)*10,.8)*.18*swell
            v+=tone(t,154+math.sin(t*6.2+2.0)*13,1.4)*.11*swell
            v+=chirp(t,1380,92,duration,.7)*.21*(1-p)
            v+=bell(t,431,duration,1.2)*.12
            v+=sine_noise(t,10.4)*swell*.18
        elif kind=="pentaract":
            swell=math.sin(p*math.pi)
            v=tone(t,43+math.sin(t*3.1)*5)*.29*swell
            v+=tone(t,64+math.sin(t*4.7+.8)*8,.8)*.22*swell
            v+=tone(t,97+math.sin(t*5.9+1.7)*11,1.5)*.17*swell
            v+=tone(t,145+math.sin(t*7.3+2.5)*14,2.1)*.09*swell
            v+=chirp(t,2200,41,duration,.5)*.24*(1-p)
            v+=bell(t,286,duration,1.0)*.10
            v+=sine_noise(t,11.2)*swell*.25
        elif kind=="death":
            v=math.sin(math.tau*660.0*t)*.72
        elif kind=="enemy_hit":
            snap=max(0.0,1-p*12)
            v=chirp(t,620,105,duration)*.27
            v+=sine_noise(t,12.8)*(1-p)**1.8*.39
            v+=tone(t,1030)*snap*.08
        elif kind=="enemy_down":
            snap=max(0.0,1-p*8)
            v=chirp(t,390,52,duration)*.42
            v+=harmonic(t,82,.5)*(1-p)**1.35*.18
            v+=sine_noise(t,13.5)*(1-p)**1.3*.34
            v+=bell(t,280,duration,1.0)*.10
            v+=tone(t,1700)*snap*.06

        motion=.972+.028*math.sin(t*17.0+i*.0007)
        if kind=="death":
            value=clamp(v,-1.0,1.0)
            width=0.0
        else:
            value=clamp(v*env*motion,-1.0,1.0)
            width=.018*math.sin(t*29.0+len(kind))
        left=int(clamp(value*(1.0-width),-1.0,1.0)*24400)
        right=int(clamp(value*(1.0+width),-1.0,1.0)*24400)
        samples.append(left)
        samples.append(right)

    try:
        return pygame.mixer.Sound(buffer=samples.tobytes())
    except Exception:
        return None

def build_sfx():
    global SFX_BANK
    names=(
        "jump","double_jump","dash","parry","parry_hit","step","land",
        "powerup","weapon_pickup","hit","shield","gun_ak","gun_m1",
        "gun_shotgun","orb_yellow","orb_cyan","tesseract",
        "pentaract","death","enemy_hit","enemy_down"
    )
    SFX_BANK={name:synth_cubed_sfx(name) for name in names}

def play_sfx(name,gain=1.0):
    if not AUDIO_OK or SOUND_VOLUME<=0:
        return
    snd=SFX_BANK.get(name)
    if snd is None:
        build_sfx()
        snd=SFX_BANK.get(name)
    if snd is not None:
        try:
            snd.set_volume(clamp(SOUND_VOLUME*gain,0.0,1.0))
            snd.play()
        except Exception:
            build_sfx()
            snd=SFX_BANK.get(name)
            if snd is not None:
                snd.set_volume(clamp(SOUND_VOLUME*gain,0.0,1.0))
                snd.play()

DEATH_TONE_CHANNEL=None

def start_death_tone():
    global DEATH_TONE_CHANNEL
    if not AUDIO_OK or SOUND_VOLUME<=0:
        return
    if DEATH_TONE_CHANNEL is not None and DEATH_TONE_CHANNEL.get_busy():
        return
    snd=SFX_BANK.get("death")
    if snd is None:
        build_sfx()
        snd=SFX_BANK.get("death")
    if snd is not None:
        snd.set_volume(clamp(SOUND_VOLUME*.78,0.0,1.0))
        DEATH_TONE_CHANNEL=snd.play(loops=-1)

def stop_death_tone():
    global DEATH_TONE_CHANNEL
    if DEATH_TONE_CHANNEL is not None:
        try:
            DEATH_TONE_CHANNEL.stop()
        except Exception:
            pass
    DEATH_TONE_CHANNEL=None

DEATH_PITCH_CHANNEL=None
DEATH_PITCH_TRANSITION=None
DEATH_PITCH_TAIL=None
DEATH_PITCH_RECOVERY=None
DEATH_PITCH_TIMER=0.0
DEATH_PITCH_STAGE=0
DEATH_PITCH_ACTIVE=False
DEATH_PITCH_SOURCE_SAMPLES=None
DEATH_PITCH_SOURCE_CHANNELS=2
DEATH_PITCH_SOURCE_RATE=44100
DEATH_PITCH_SOURCE_POS=0.0
DEATH_PITCH_RECOVERY_MODE="main"
DEATH_PITCH_DOWN_SECONDS=2.20
DEATH_PITCH_SLOW_FACTOR=.12
DEATH_PITCH_UP_SECONDS=.85

def make_death_pitch_sound(source_samples,channels,rate,start_frame,out_seconds,start_factor,end_factor):
    total_frames=max(1,len(source_samples)//channels)
    out_frames=max(1,int(rate*out_seconds))
    out=array("h")
    pos=float(start_frame%total_frames)
    for i in range(out_frames):
        q=i/max(1,out_frames-1)
        eased=.5+.5*math.sin((q-.5)*math.pi)
        factor=start_factor+(end_factor-start_factor)*eased
        base=int(pos)
        frac=pos-base
        a=base%total_frames
        b=(a+1)%total_frames
        for c in range(channels):
            s0=source_samples[a*channels+c]
            s1=source_samples[b*channels+c]
            sample=int(s0+(s1-s0)*frac)
            out.append(max(-32768,min(32767,sample)))
        pos+=factor
    return pygame.mixer.Sound(buffer=out.tobytes()),pos

def start_death_music_pitch(game_mode):
    global DEATH_PITCH_CHANNEL, DEATH_PITCH_TRANSITION, DEATH_PITCH_TAIL
    global DEATH_PITCH_TIMER, DEATH_PITCH_STAGE, DEATH_PITCH_ACTIVE
    global DEATH_PITCH_SOURCE_SAMPLES, DEATH_PITCH_SOURCE_CHANNELS
    global DEATH_PITCH_SOURCE_RATE, DEATH_PITCH_SOURCE_POS, DEATH_PITCH_RECOVERY_MODE
    if DEATH_PITCH_ACTIVE or not AUDIO_OK or MUSIC_VOLUME<=0:
        return
    try:
        target=MODE_MUSIC_FILES.get(game_mode,MODE_MUSIC_FILES["main"])
        chosen=find_named_audio(target)
        if chosen is None:
            return
        elapsed=max(0.0,pygame.mixer.music.get_pos()/1000.0)
        base_start=MODE_MUSIC_START.get(game_mode,0.0)
        source=pygame.mixer.Sound(str(chosen))
        raw=source.get_raw()
        samples=array("h")
        samples.frombytes(raw)
        mixer_info=pygame.mixer.get_init()
        rate=int(mixer_info[0]) if mixer_info else 44100
        channels=int(mixer_info[2]) if mixer_info else 2
        if channels<1 or len(samples)<channels*4:
            return
        total_frames=len(samples)//channels
        total_seconds=total_frames/max(1,rate)
        start_seconds=(base_start+elapsed)%max(.001,total_seconds)
        start_frame=int(start_seconds*rate)
        transition,end_pos=make_death_pitch_sound(samples,channels,rate,start_frame,DEATH_PITCH_DOWN_SECONDS,1.0,DEATH_PITCH_SLOW_FACTOR)
        tail,_=make_death_pitch_sound(samples,channels,rate,int(end_pos),5.0,DEATH_PITCH_SLOW_FACTOR,DEATH_PITCH_SLOW_FACTOR)
        pygame.mixer.music.stop()
        DEATH_PITCH_CHANNEL=pygame.mixer.Channel(30)
        DEATH_PITCH_CHANNEL.set_volume(clamp(MUSIC_VOLUME*.92,0.0,1.0))
        DEATH_PITCH_TRANSITION=transition
        DEATH_PITCH_TAIL=tail
        DEATH_PITCH_SOURCE_SAMPLES=samples
        DEATH_PITCH_SOURCE_CHANNELS=channels
        DEATH_PITCH_SOURCE_RATE=rate
        DEATH_PITCH_SOURCE_POS=float(start_frame)
        DEATH_PITCH_RECOVERY_MODE=game_mode
        DEATH_PITCH_CHANNEL.play(DEATH_PITCH_TRANSITION)
        DEATH_PITCH_TIMER=0.0
        DEATH_PITCH_STAGE=1
        DEATH_PITCH_ACTIVE=True
    except Exception as e:
        DEATH_PITCH_ACTIVE=False
        print("DEATH PITCH ERROR:",e)

def update_death_music_pitch(dt):
    global DEATH_PITCH_TIMER, DEATH_PITCH_STAGE, DEATH_PITCH_SOURCE_POS
    global DEATH_PITCH_ACTIVE, DEATH_PITCH_CHANNEL, DEATH_PITCH_RECOVERY
    if not DEATH_PITCH_ACTIVE or DEATH_PITCH_CHANNEL is None:
        return
    DEATH_PITCH_TIMER+=dt
    if DEATH_PITCH_STAGE==1:
        q=clamp(DEATH_PITCH_TIMER/max(.001,DEATH_PITCH_DOWN_SECONDS),0.0,1.0)
        eased=.5+.5*math.sin((q-.5)*math.pi)
        factor=1.0+(DEATH_PITCH_SLOW_FACTOR-1.0)*eased
        DEATH_PITCH_SOURCE_POS+=DEATH_PITCH_SOURCE_RATE*factor*dt
        if DEATH_PITCH_TRANSITION is not None and DEATH_PITCH_TIMER>=max(.1,DEATH_PITCH_TRANSITION.get_length()-.035):
            if DEATH_PITCH_TAIL is not None:
                DEATH_PITCH_CHANNEL.play(DEATH_PITCH_TAIL,loops=-1)
            DEATH_PITCH_TIMER=0.0
            DEATH_PITCH_STAGE=2
    elif DEATH_PITCH_STAGE==2:
        DEATH_PITCH_SOURCE_POS+=DEATH_PITCH_SOURCE_RATE*DEATH_PITCH_SLOW_FACTOR*dt
    elif DEATH_PITCH_STAGE==3:
        if DEATH_PITCH_RECOVERY is not None and DEATH_PITCH_TIMER>=max(.05,DEATH_PITCH_RECOVERY.get_length()-.025):
            mode_name=DEATH_PITCH_RECOVERY_MODE
            source_seconds=DEATH_PITCH_SOURCE_POS/max(1,DEATH_PITCH_SOURCE_RATE)
            target=MODE_MUSIC_FILES.get(mode_name,MODE_MUSIC_FILES["main"])
            chosen=find_named_audio(target)
            if DEATH_PITCH_CHANNEL is not None:
                DEATH_PITCH_CHANNEL.stop()
            DEATH_PITCH_CHANNEL=None
            DEATH_PITCH_RECOVERY=None
            DEATH_PITCH_STAGE=0
            DEATH_PITCH_ACTIVE=False
            if chosen is not None:
                play_music_file(chosen.name,MUSIC_VOLUME,start_pos=source_seconds)

def death_music_recovering():
    return DEATH_PITCH_ACTIVE and DEATH_PITCH_STAGE==3

def start_retry_music_recovery(game_mode):
    global DEATH_PITCH_RECOVERY, DEATH_PITCH_TIMER, DEATH_PITCH_STAGE
    global DEATH_PITCH_SOURCE_POS, DEATH_PITCH_RECOVERY_MODE
    if not DEATH_PITCH_ACTIVE or DEATH_PITCH_SOURCE_SAMPLES is None or DEATH_PITCH_CHANNEL is None:
        return False
    if DEATH_PITCH_STAGE==1:
        q=clamp(DEATH_PITCH_TIMER/max(.001,DEATH_PITCH_DOWN_SECONDS),0.0,1.0)
        eased=.5+.5*math.sin((q-.5)*math.pi)
        start_factor=1.0+(DEATH_PITCH_SLOW_FACTOR-1.0)*eased
    else:
        start_factor=DEATH_PITCH_SLOW_FACTOR
    try:
        DEATH_PITCH_CHANNEL.stop()
        recovery,end_pos=make_death_pitch_sound(
            DEATH_PITCH_SOURCE_SAMPLES,
            DEATH_PITCH_SOURCE_CHANNELS,
            DEATH_PITCH_SOURCE_RATE,
            int(DEATH_PITCH_SOURCE_POS),
            DEATH_PITCH_UP_SECONDS,
            start_factor,
            1.0
        )
        DEATH_PITCH_RECOVERY=recovery
        DEATH_PITCH_SOURCE_POS=end_pos
        DEATH_PITCH_RECOVERY_MODE=game_mode
        DEATH_PITCH_TIMER=0.0
        DEATH_PITCH_STAGE=3
        DEATH_PITCH_CHANNEL.set_volume(clamp(MUSIC_VOLUME*.92,0.0,1.0))
        DEATH_PITCH_CHANNEL.play(DEATH_PITCH_RECOVERY)
        return True
    except Exception as e:
        print("DEATH PITCH RECOVERY ERROR:",e)
        return False

def stop_death_music_pitch():
    global DEATH_PITCH_CHANNEL, DEATH_PITCH_TRANSITION, DEATH_PITCH_TAIL, DEATH_PITCH_RECOVERY
    global DEATH_PITCH_TIMER, DEATH_PITCH_STAGE, DEATH_PITCH_ACTIVE
    global DEATH_PITCH_SOURCE_SAMPLES, DEATH_PITCH_SOURCE_POS
    if DEATH_PITCH_CHANNEL is not None:
        try:
            DEATH_PITCH_CHANNEL.stop()
        except Exception:
            pass
    DEATH_PITCH_CHANNEL=None
    DEATH_PITCH_TRANSITION=None
    DEATH_PITCH_TAIL=None
    DEATH_PITCH_RECOVERY=None
    DEATH_PITCH_SOURCE_SAMPLES=None
    DEATH_PITCH_SOURCE_POS=0.0
    DEATH_PITCH_TIMER=0.0
    DEATH_PITCH_STAGE=0
    DEATH_PITCH_ACTIVE=False

build_sfx()


def capture_windows_desktop():
    if not sys.platform.startswith("win"):
        return None, [], None
    try:
        import ctypes
        from ctypes import wintypes
        import time
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        game_hwnd = pygame.display.get_wm_info().get("window")
        was_visible = False
        if game_hwnd:
            was_visible = bool(user32.IsWindowVisible(game_hwnd))
            user32.ShowWindow(game_hwnd, 0)
            time.sleep(.14)

        width = user32.GetSystemMetrics(0)
        height = user32.GetSystemMetrics(1)
        hdc = user32.GetDC(0)
        memdc = gdi32.CreateCompatibleDC(hdc)
        bitmap = gdi32.CreateCompatibleBitmap(hdc, width, height)
        old_obj = gdi32.SelectObject(memdc, bitmap)
        gdi32.BitBlt(memdc, 0, 0, width, height, hdc, 0, 0, 0x00CC0020)

        class BITMAPINFOHEADER(ctypes.Structure):
            _fields_ = [
                ("biSize", wintypes.DWORD),
                ("biWidth", wintypes.LONG),
                ("biHeight", wintypes.LONG),
                ("biPlanes", wintypes.WORD),
                ("biBitCount", wintypes.WORD),
                ("biCompression", wintypes.DWORD),
                ("biSizeImage", wintypes.DWORD),
                ("biXPelsPerMeter", wintypes.LONG),
                ("biYPelsPerMeter", wintypes.LONG),
                ("biClrUsed", wintypes.DWORD),
                ("biClrImportant", wintypes.DWORD)
            ]

        class BITMAPINFO(ctypes.Structure):
            _fields_ = [
                ("bmiHeader", BITMAPINFOHEADER),
                ("bmiColors", wintypes.DWORD * 3)
            ]

        bmi = BITMAPINFO()
        bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bmi.bmiHeader.biWidth = width
        bmi.bmiHeader.biHeight = -height
        bmi.bmiHeader.biPlanes = 1
        bmi.bmiHeader.biBitCount = 32
        bmi.bmiHeader.biCompression = 0

        buffer = ctypes.create_string_buffer(width * height * 4)
        gdi32.GetDIBits(memdc, bitmap, 0, height, buffer, ctypes.byref(bmi), 0)

        gdi32.SelectObject(memdc, old_obj)
        gdi32.DeleteObject(bitmap)
        gdi32.DeleteDC(memdc)
        user32.ReleaseDC(0, hdc)

        snapshot = pygame.image.frombuffer(buffer.raw, (width, height), "BGRA").convert().copy()
        windows = []
        EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

        def collect(hwnd, lparam):
            try:
                if hwnd == game_hwnd:
                    return True
                if not user32.IsWindowVisible(hwnd) or user32.IsIconic(hwnd):
                    return True
                length = user32.GetWindowTextLengthW(hwnd)
                if length <= 0:
                    return True
                title_buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, title_buf, length + 1)
                title = title_buf.value.strip()
                if not title:
                    return True
                rect = wintypes.RECT()
                if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                    return True
                left = max(0, rect.left)
                top = max(0, rect.top)
                right = min(width, rect.right)
                bottom = min(height, rect.bottom)
                w = right - left
                h = bottom - top
                if w < 120 or h < 70:
                    return True
                if right <= 0 or bottom <= 0 or left >= width or top >= height:
                    return True
                windows.append((left, top, right, bottom, title))
            except Exception:
                pass
            return True

        user32.EnumWindows(EnumWindowsProc(collect), 0)

        if game_hwnd and was_visible:
            user32.ShowWindow(game_hwnd, 5)
            try:
                user32.SetForegroundWindow(game_hwnd)
            except Exception:
                pass

        return snapshot, windows, (0, 0, width, height)
    except Exception:
        try:
            import ctypes
            hwnd = pygame.display.get_wm_info().get("window")
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 5)
        except Exception:
            pass
        return None, [], None

class DesktopEntityManager:
    def __init__(self):
        self.root = None
        self.windows = []
        self.enabled = sys.platform.startswith("win")
        self.last_left = False

    def init(self):
        if not self.enabled or self.root is not None:
            return self.root is not None
        try:
            import tkinter as tk
            self.tk = tk
            self.root = tk.Tk()
            self.root.withdraw()
            return True
        except Exception:
            self.enabled = False
            self.root = None
            return False

    def window_rect(self):
        if not self.enabled:
            return None
        try:
            import ctypes
            from ctypes import wintypes
            hwnd = pygame.display.get_wm_info().get("window")
            if not hwnd:
                return None
            rect = wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            return (rect.left, rect.top, rect.right, rect.bottom)
        except Exception:
            return None

    def global_mouse(self):
        if not self.enabled:
            return None
        try:
            import ctypes
            from ctypes import wintypes
            pt = wintypes.POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
            down = bool(ctypes.windll.user32.GetAsyncKeyState(0x01) & 0x8000)
            return pt.x, pt.y, down
        except Exception:
            return None

    def spawn(self, kind, x, y):
        if not self.init():
            return
        try:
            tk = self.tk
            size = 118 if kind == "monster" else 88
            win = tk.Toplevel(self.root)
            win.overrideredirect(True)
            win.attributes("-topmost", True)
            key = "#010101"
            win.configure(bg=key)
            try:
                win.wm_attributes("-transparentcolor", key)
            except Exception:
                pass
            win.geometry(f"{size}x{size}+{int(x-size/2)}+{int(y-size/2)}")
            canvas = tk.Canvas(win, width=size, height=size, bg=key, highlightthickness=0)
            canvas.pack()
            c = {
                "drone":"#46e6ff",
                "wraith":"#aa5fff",
                "hunter":"#ff9141",
                "orbiter":"#55e691",
                "dasher":"#ffde4b",
                "monster":"#ff4b5c"
            }[kind]
            cx = cy = size / 2
            r = size * (.38 if kind == "monster" else .30)
            if kind == "monster":
                for off in (0, 13):
                    canvas.create_rectangle(cx-r+off, cy-r+off, cx+r-off, cy+r-off, outline=c, width=3)
                canvas.create_line(cx-r,cy-r,cx-r+13,cy-r+13,fill=c,width=3)
                canvas.create_line(cx+r,cy-r,cx+r-13,cy-r+13,fill=c,width=3)
                canvas.create_line(cx-r,cy+r,cx-r+13,cy+r-13,fill=c,width=3)
                canvas.create_line(cx+r,cy+r,cx+r-13,cy+r-13,fill=c,width=3)
            elif kind == "drone":
                pts=[]
                for i in range(8):
                    a=i*math.tau/8
                    rr=r if i%2==0 else r*.42
                    pts.extend((cx+math.cos(a)*rr,cy+math.sin(a)*rr))
                canvas.create_polygon(pts,outline=c,fill="",width=3)
            elif kind == "wraith":
                pts=[]
                for i in range(12):
                    a=i*math.tau/12
                    rr=r*(1.0+.18*math.sin(i*1.8))
                    pts.extend((cx+math.cos(a)*rr,cy+math.sin(a)*rr))
                canvas.create_polygon(pts,outline=c,fill="",width=3)
            elif kind == "hunter":
                canvas.create_polygon(cx+r,cy,cx-r*.8,cy-r*.8,cx-r*.45,cy,cx-r*.8,cy+r*.8,outline=c,fill="",width=3)
            elif kind == "orbiter":
                canvas.create_oval(cx-r*.45,cy-r*.45,cx+r*.45,cy+r*.45,outline=c,width=3)
                for i in range(3):
                    a=i*math.tau/3
                    ox=cx+math.cos(a)*r
                    oy=cy+math.sin(a)*r*.65
                    canvas.create_oval(ox-5,oy-5,ox+5,oy+5,outline=c,width=2)
            elif kind == "dasher":
                canvas.create_polygon(cx+r,cy,cx-r*.55,cy-r*.62,cx-r*.25,cy,cx-r*.55,cy+r*.62,outline=c,fill="",width=3)
            canvas.create_text(cx, size-10, text=ENTITY_NAMES[kind], fill=c, font=("Comic Sans MS", 9, "bold"))
            self.windows.append(win)
        except Exception:
            pass

    def update(self):
        if self.root is None:
            return
        try:
            self.root.update_idletasks()
            self.root.update()
        except Exception:
            self.root = None
            self.windows = []

    def clear(self):
        for win in self.windows[:]:
            try:
                win.destroy()
            except Exception:
                pass
        self.windows = []

desktop_entities = DesktopEntityManager()

class Particle:
    def __init__(self, x, y, color, speed=250, life=0.45, size=4):
        a = random.uniform(0, math.tau)
        s = random.uniform(speed * 0.35, speed)
        self.x = x
        self.y = y
        self.vx = math.cos(a) * s
        self.vy = math.sin(a) * s
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size
        self.phase = random.uniform(0, math.tau)

    def update(self, dt, t):
        self.life -= dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 420 * dt
        self.x += math.sin(t * 11 + self.phase) * 14 * dt

    def draw(self, camera_y, t):
        if self.life <= 0:
            return
        sy = self.y - camera_y
        fade = clamp(self.life / self.max_life, 0.0, 1.0)
        pulse = 0.7 + 0.3 * math.sin(t * 14 + self.phase)
        radius = max(1, int(self.size * fade * (1 + pulse * 0.35)))
        tx = self.x - self.vx * .018
        ty = sy - self.vy * .018
        pygame.draw.line(screen, self.color, (int(tx), int(ty)), (int(self.x), int(sy)), max(1, radius))
        pygame.draw.circle(screen, self.color, (int(self.x), int(sy)), radius)

class Shockwave:
    def __init__(self, x, y, color, radius=18, growth=420, life=.38, width=4, flatten=.35):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.growth = growth
        self.life = life
        self.max_life = life
        self.width = width
        self.flatten = flatten
        self.phase = random.uniform(0, math.tau)

    def update(self, dt):
        self.life -= dt
        self.radius += self.growth * dt
        self.growth *= max(0.0, 1.0 - dt * 2.2)

    def draw(self, camera_y, t):
        if self.life <= 0:
            return
        fade = clamp(self.life / self.max_life, 0.0, 1.0)
        wobble = 1.0 + math.sin(t * 11 + self.phase) * .035
        rx = max(2, int(self.radius * wobble))
        ry = max(2, int(self.radius * self.flatten))
        surf = pygame.Surface((rx * 2 + 12, ry * 2 + 12), pygame.SRCALPHA)
        alpha = int(210 * fade)
        pygame.draw.ellipse(surf, (*self.color, alpha), surf.get_rect().inflate(-8, -8), max(1, int(self.width * fade)))
        screen.blit(surf, (int(self.x - rx - 6), int(self.y - camera_y - ry - 6)))

                                                                   
class BloodParticle:
    def __init__(self,x,y,heavy=False):
        a=random.uniform(-math.pi*0.95,-math.pi*0.05)
        speed=random.uniform(150,430 if heavy else 330)
        self.x=x;self.y=y
        self.vx=math.cos(a)*speed+random.uniform(-90,90)
        self.vy=math.sin(a)*speed-random.uniform(30,150)
        self.life=random.uniform(.55,1.05);self.max_life=self.life
        self.size=random.randint(2,6 if heavy else 5)
        self.phase=random.uniform(0,math.tau)
        self.dark=random.random()<.35

    def update(self,dt,t):
        self.life-=dt
        self.vy+=1050*dt
        self.vx*=.992
        self.x+=self.vx*dt+math.sin(t*13+self.phase)*3*dt
        self.y+=self.vy*dt

    def draw(self,camera_y,t):
        if self.life<=0:return
        sy=self.y-camera_y
        fade=clamp(self.life/self.max_life,0,1)
        color=(115,10,24) if self.dark else (220,24,45)
        r=max(1,int(self.size*(.55+fade*.65)))
        tail_x=self.x-self.vx*.018;tail_y=sy-self.vy*.018
        pygame.draw.line(screen,color,(int(tail_x),int(tail_y)),(int(self.x),int(sy)),max(1,r//2))
        pygame.draw.circle(screen,color,(int(self.x),int(sy)),r)

                                                             
class Platform:
    def __init__(self, x, y, w, h=18):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.phase = random.uniform(0, math.tau)
        self.desktop_app = False
        self.desktop_title = ""
        self.invisible = False

    def top(self):
        return self.y - self.h / 2

    def rect(self):
        return pygame.Rect(self.x - self.w/2, self.y - self.h/2, self.w, self.h)

    def draw(self, camera_y, t, mardcore=False):
        if self.invisible:
            return
        sy = self.y - camera_y
        if sy < -80 or sy > HEIGHT + 80:
            return
        edge_color = (255,92,104) if mardcore else LIGHT
        wave_color = (255,35,55) if mardcore else CYAN
        if self.desktop_app:
            left = self.x - self.w/2
            right = self.x + self.w/2
            glow = 1 + int((math.sin(t*6+self.phase)+1)*.5)
            pygame.draw.line(screen, wave_color, (left, sy-self.h/2), (right, sy-self.h/2), 2+glow)
            return

        wave = math.sin(t * 5.2 + self.phase) * 4.5
        bend = math.sin(t * 3.1 + self.phase * 1.7) * 7
        x = self.x + bend
        left = x - self.w/2
        right = x + self.w/2
        top = sy - self.h/2
        bot = sy + self.h/2
        pts = [
            (left + 12, top + wave),
            (right, top - wave),
            (right - 12, bot + wave),
            (left, bot - wave)
        ]
        if mardcore:
            glow_pulse = .5 + .5*math.sin(t*6.4+self.phase)
            pygame.draw.line(screen,(90+int(40*glow_pulse),5,12),(left+6,sy),(right-6,sy),7)
        pygame.draw.polygon(screen, edge_color, pts, 3)
        prev = None
        for i in range(18):
            f = i / 17
            px = left + f * self.w
            py = sy + math.sin(t * 8 + self.phase + f * math.tau * 2) * 3
            if prev:
                pygame.draw.line(screen, wave_color, prev, (px, py), 2)
            prev = (px, py)


class PowerUp:
    NAMES = ("INFINITE JUMPS", "SHIELD", "ANGEL", "FLIGHT")
    WEAPON_NAMES = ("AK-47","M1 GARAND","SHOTGUN")

    def __init__(self, kind, x, y):
        self.kind = kind
        self.x = x
        self.y = y
        self.phase = random.uniform(0, math.tau)
        self.radius = 20 if kind in self.WEAPON_NAMES else 18
        self.taken = False

    def color(self):
        return {
            "INFINITE JUMPS": CYAN,
            "SHIELD": BLUE,
            "ANGEL": YELLOW,
            "FLIGHT": PINK,
            "AK-47": ORANGE,
            "M1 GARAND": LIGHT,
            "SHOTGUN": YELLOW,
        }[self.kind]

    def draw(self, camera_y, t):
        sy = self.y - camera_y + math.sin(t * 4.5 + self.phase) * 9
        if sy < -90 or sy > HEIGHT + 90:
            return
        x = self.x + math.sin(t * 3.1 + self.phase) * 4
        c = self.color()
        pulse = 1.0 + math.sin(t * 8 + self.phase) * .14
        r = self.radius * pulse

                                            
        pts = []
        for i in range(4):
            a = math.pi/4 + i*math.pi/2 + math.sin(t*3+self.phase)*.08
            rr = r + math.sin(t*7+i+self.phase)*3
            pts.append((x + math.cos(a)*rr, sy + math.sin(a)*rr))
        pygame.draw.polygon(screen, c, pts, 3)
        pygame.draw.circle(screen, c, (int(x), int(sy)), max(3, int(5+math.sin(t*9+self.phase)*2)), 2)

                            
        for j in range(2):
            a = t*(2.2+j*.6) + self.phase + j*math.pi
            ox = x + math.cos(a)*28
            oy = sy + math.sin(a*1.3)*11
            pygame.draw.circle(screen, c, (int(ox), int(oy)), 3)

                                
        short = {
            "INFINITE JUMPS":"∞ JUMPS",
            "SHIELD":"SHIELD",
            "ANGEL":"ANGEL",
            "FLIGHT":"FLIGHT",
            "AK-47":"AK-47 60.00s",
            "M1 GARAND":"M1 60.00s",
            "SHOTGUN":"SHOTGUN 60.00s"
        }[self.kind]
        draw_text(short, font_small, c, x, sy-38, center=True)

                                                           
class Orb:
    KINDS = ("YELLOW", "CYAN")

    def __init__(self, kind, x, y):
        self.kind = kind
        self.x = x
        self.y = y
        self.phase = random.uniform(0, math.tau)
        self.radius = 22
        self.cooldown = 0.0

    def color(self):
        return {"YELLOW":YELLOW,"CYAN":CYAN}[self.kind]

    def update(self, dt):
        self.cooldown = max(0.0, self.cooldown-dt)

    def draw(self, camera_y, t):
        sy = self.y-camera_y
        if sy < -90 or sy > HEIGHT + 90:
            return
        c = self.color()
        pulse = 1.0 + math.sin(t*7+self.phase)*.10
        r = self.radius*pulse
        alpha = 85 if self.cooldown > 0 else 190
        glow = pygame.Surface((80,80),pygame.SRCALPHA)
        pygame.draw.circle(glow,(*c,28 if self.cooldown <= 0 else 10),(40,40),int(r+12))
        pygame.draw.circle(glow,(*c,alpha),(40,40),int(r),3)
        pygame.draw.circle(glow,(255,255,255,150 if self.cooldown <= 0 else 55),(40,40),7,2)
        for i in range(4):
            a=t*(2.4+i*.12)+self.phase+i*math.pi/2
            px=40+math.cos(a)*(r+7)
            py=40+math.sin(a)*(r+7)
            pygame.draw.circle(glow,(*c,150 if self.cooldown <= 0 else 45),(int(px),int(py)),3)
        screen.blit(glow,(int(self.x-40),int(sy-40)))

HYPERCUBE5D_EDGES = [(i, i ^ bit) for i in range(32) for bit in (1,2,4,8,16) if i < (i ^ bit)]
TESSERACT_EDGES = [(i, i ^ bit) for i in range(16) for bit in (1,2,4,8) if i < (i ^ bit)]

def project_5d_cube(cx, cy, radius, t, phase):
    a=t*1.9+math.sin(t*1.15+phase)*.31
    b=t*1.37+math.sin(t*1.72+phase*.7)*.27
    c=t*.93+math.sin(t*2.05+phase*.4)*.23
    ca,sa=math.cos(a),math.sin(a)
    cb,sb=math.cos(b),math.sin(b)
    cc,sc=math.cos(c),math.sin(c)
    verts=[]
    for i in range(32):
        x=1 if i&1 else -1
        y=1 if i&2 else -1
        z=1 if i&4 else -1
        w=1 if i&8 else -1
        v=1 if i&16 else -1
        x1=x*ca-z*sa
        z1=x*sa+z*ca
        y1=y*cb-w*sb
        w1=y*sb+w*cb
        z2=z1*cc-v*sc
        v1=z1*sc+v*cc
        p5=1.0/(3.25-v1*.38)
        p4=1.0/(2.95-w1*.34)
        p3=1.0/(2.55-z2*.27)
        stretch=radius*10.4*p5*p4*p3
        px=cx+x1*stretch
        py=cy+y1*stretch+math.sin(t*4.8+i*.41+phase)*1.4
        verts.append((px,py))
    return verts



class Bullet:
    def __init__(self,x,y,vx,vy,damage,knockback,color,weapon):
        self.x=float(x)
        self.y=float(y)
        self.prev_x=float(x)
        self.prev_y=float(y)
        self.vx=float(vx)
        self.vy=float(vy)
        self.damage=int(damage)
        self.knockback=float(knockback)
        self.color=color
        self.weapon=weapon
        self.life=1.15
        self.dead=False
        self.radius=4 if weapon!="SHOTGUN" else 3
        self.phase=(x*.013+y*.017+vx*.0011+vy*.0013)%math.tau
        self.age=0.0

    def update(self,dt):
        self.prev_x=self.x
        self.prev_y=self.y
        self.age+=dt
        speed=max(1.0,math.hypot(self.vx,self.vy))
        nx=-self.vy/speed
        ny=self.vx/speed
        wave=math.sin(self.age*26+self.phase)
        amp=8.0 if self.weapon=="AK-47" else 5.0 if self.weapon=="M1 GARAND" else 11.0
        self.x+=self.vx*dt+nx*wave*amp*dt
        self.y+=self.vy*dt+ny*wave*amp*dt
        self.life-=dt
        if self.life<=0:
            self.dead=True

    def draw(self,camera_y):
        sy=self.y-camera_y
        if sy < -80 or sy > HEIGHT+80:
            return
        speed=max(1.0,math.hypot(self.vx,self.vy))
        nx=-self.vy/speed
        ny=self.vx/speed
        wave=math.sin(self.age*32+self.phase)
        tail=0.018 if self.weapon=="AK-47" else 0.026
        tx=self.x-self.vx*tail+nx*wave*4
        ty=sy-self.vy*tail+ny*wave*4
        pulse=.5+.5*math.sin(self.age*38+self.phase)
        thickness=2+int(pulse*(1 if self.weapon=="SHOTGUN" else 2))
        pygame.draw.line(screen,self.color,(tx,ty),(self.x,sy),thickness)
        rr=self.radius+int(pulse)
        pygame.draw.circle(screen,WHITE,(int(self.x),int(sy)),rr)

class Entity:
    def __init__(self, kind, x, y):
        self.kind = kind
        self.base_kind = HARDCORE_ENTITY_BASE.get(kind,kind)
        self.hardcore_variant = kind in HARDCORE_ENTITY_KINDS or kind == "monster5d"
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.phase = random.uniform(0, math.tau)
        self.dead = False
        self.timer = 0.0
        self.parry_hits = 0
        self.weapon_hp = {
            "m_drone":3,
            "m_wraith":3,
            "m_hunter":5,
            "m_orbiter":5,
            "m_dasher":4,
            "monster5d":999999
        }.get(kind,1)

        self.radius = {
            "drone": 20,
            "wraith": 22,
            "hunter": 22,
            "orbiter": 19,
            "dasher": 20,
            "monster": 68,
            "monster5d": 76,
        }[self.base_kind]
        if kind in HARDCORE_ENTITY_KINDS:
            self.radius += 3

    def update(self, dt, player, t, difficulty=1.0):
        self.timer += dt
        difficulty = clamp(difficulty, 0.98, 4.60)
        if self.hardcore_variant:
            difficulty = max(difficulty,3.25)
        dx = player.x - self.x
        dy = player.y - self.y
        dist = max(1.0, math.hypot(dx, dy))
        nx, ny = dx / dist, dy / dist

        if self.base_kind == "drone":
            self.vx += nx * 360 * difficulty * dt
            self.vy += ny * 360 * difficulty * dt
            if (self.timer % 1.45) < dt:
                self.vx += nx * 230 * difficulty
                self.vy += ny * 230 * difficulty

        elif self.base_kind == "wraith":
            self.vx += nx * 275 * difficulty * dt
            self.vy += ny * 275 * difficulty * dt
            self.vx += math.sin(t * 7.5 + self.phase) * 98 * dt
            self.vy += math.cos(t * 6.2 + self.phase) * 88 * dt
            if (self.timer % 1.45) < dt:
                self.vx = nx * 475 * difficulty + math.sin(self.phase) * 102
                self.vy = ny * 475 * difficulty + math.cos(self.phase) * 102

        elif self.base_kind == "hunter":
            self.vx += nx * 138 * difficulty * dt
            self.vy += ny * 138 * difficulty * dt
            if (self.timer % 0.88) < dt:
                lead_x = player.x + player.vx * .19 - self.x
                lead_y = player.y + player.vy * .11 - self.y
                lead_d = max(1.0, math.hypot(lead_x, lead_y))
                self.vx = lead_x / lead_d * 730 * difficulty
                self.vy = lead_y / lead_d * 730 * difficulty

        elif self.base_kind == "orbiter":
            tangent_x, tangent_y = -ny, nx
            orbit = math.sin(t * 8.5 + self.phase)
            self.vx += (nx * 270 + tangent_x * orbit * 215) * difficulty * dt
            self.vy += (ny * 270 + tangent_y * orbit * 215) * difficulty * dt
            if dist < 160:
                self.vx += nx * 190 * difficulty * dt
                self.vy += ny * 190 * difficulty * dt

        elif self.base_kind == "dasher":
            self.vx += nx * 148 * difficulty * dt
            self.vy += ny * 148 * difficulty * dt
            if (self.timer % 0.66) < dt:
                self.vx = nx * 920 * difficulty
                self.vy = ny * 920 * difficulty

        elif self.base_kind == "monster":
            target_speed = (620 + min(520, self.timer * 7.5)) * (0.90 + difficulty * 0.22)
            wobble_x = math.sin(t * 5.8 + self.phase) * 95
            wobble_y = math.cos(t * 5.0 + self.phase) * 95
            self.vx = lerp(self.vx, nx * target_speed + wobble_x, clamp(dt * 5.4, 0, 1))
            self.vy = lerp(self.vy, ny * target_speed + wobble_y, clamp(dt * 5.4, 0, 1))

        elif self.base_kind == "monster5d":
            target_speed = (760 + min(680, self.timer * 11.0)) * (0.92 + difficulty * 0.24)
            wobble_x = math.sin(t * 7.4 + self.phase) * 145
            wobble_y = math.sin(t * 6.3 + self.phase + 1.7) * 145
            self.vx = lerp(self.vx, nx * target_speed + wobble_x, clamp(dt * 7.2, 0, 1))
            self.vy = lerp(self.vy, ny * target_speed + wobble_y, clamp(dt * 7.2, 0, 1))

        self.vx *= 0.987
        self.vy *= 0.987

        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, camera_y, t):
        sy = self.y - camera_y
        if sy < -190 or sy > HEIGHT + 190:
            return

        colors = {
            "drone": CYAN,
            "wraith": PURPLE,
            "hunter": ORANGE,
            "orbiter": GREEN,
            "dasher": YELLOW,
            "monster": RED,
            "m_drone": RED,
            "m_wraith": PINK,
            "m_hunter": WHITE,
            "m_orbiter": PURPLE,
            "m_dasher": ORANGE,
            "monster5d": BLACK
        }
        color = colors[self.kind]
        pulse = 1.0 + math.sin(t * 8 + self.phase) * 0.12
        r = self.radius * pulse

        if self.base_kind == "monster5d":
            verts=project_5d_cube(self.x,sy,r,t,self.phase)
            if GRAPHICS_QUALITY <= 2:
                for a,b in HYPERCUBE5D_EDGES:
                    pygame.draw.line(screen,LIGHT,verts[a],verts[b],5)
                for a,b in HYPERCUBE5D_EDGES:
                    pygame.draw.line(screen,BLACK,verts[a],verts[b],3)
            else:
                for a,b in HYPERCUBE5D_EDGES:
                    pygame.draw.line(screen,LIGHT,verts[a],verts[b],3)
            core=10+math.sin(t*10+self.phase)*2
            pygame.draw.circle(screen,LIGHT,(int(self.x),int(sy)),int(core+4))
            pygame.draw.circle(screen,BLACK,(int(self.x),int(sy)),int(core))
            for i in range(5):
                a=t*(2.1+i*.17)+i*math.tau/5
                rr=r+18+math.sin(t*6+i)*7
                ox=self.x+math.cos(a)*rr
                oy=sy+math.sin(a*1.27)*rr*.48
                pygame.draw.circle(screen,LIGHT,(int(ox),int(oy)),5)
                pygame.draw.circle(screen,BLACK,(int(ox),int(oy)),3)
        elif self.base_kind == "monster":
            angle_a = t * 1.7 + math.sin(t * 1.2) * .35
            angle_b = t * 1.15 + math.sin(t * 2.1 + 1.4) * .28
            scale = r * .52
            verts = []
            ca,sa=math.cos(angle_a),math.sin(angle_a)
            cb,sb=math.cos(angle_b),math.sin(angle_b)
            for w in (-1, 1):
                for z in (-1, 1):
                    for y in (-1, 1):
                        for x in (-1, 1):
                            x1 = x * ca - z * sa
                            z1 = x * sa + z * ca
                            y1 = y * cb - w * sb
                            w1 = y * sb + w * cb
                            perspective4 = 1.0 / (2.8 - w1 * .45)
                            perspective3 = 1.0 / (2.4 - z1 * .32)
                            px = self.x + x1 * scale * perspective4 * perspective3 * 4.2
                            py = sy + y1 * scale * perspective4 * perspective3 * 4.2
                            verts.append((px, py))
            for a, b in TESSERACT_EDGES:
                pygame.draw.line(screen, color, verts[a], verts[b], 2)
            core = 7 + math.sin(t * 9 + self.phase) * 2
            pygame.draw.circle(screen, color, (int(self.x), int(sy)), int(core), 2)
            for i in range(4):
                a = t * (1.8 + i * .22) + i * math.pi / 2
                rr = r + 16 + math.sin(t * 5 + i) * 6
                pygame.draw.circle(screen, color, (int(self.x + math.cos(a) * rr), int(sy + math.sin(a * 1.3) * rr * .45)), 3)
        elif self.base_kind == "drone":
            pts = []
            for i in range(8):
                a = i * math.tau / 8 + t * 2.8
                rr = r if i % 2 == 0 else r * .42
                pts.append((self.x + math.cos(a) * rr, sy + math.sin(a) * rr))
            pygame.draw.polygon(screen, color, pts, 3)
            pygame.draw.circle(screen, color, (int(self.x), int(sy)), 5, 2)
        elif self.base_kind == "wraith":
            pts = []
            for i in range(12):
                a = i * math.tau / 12
                rr = r * (1.0 + math.sin(t * 7 + self.phase + i * 1.4) * .28)
                pts.append((self.x + math.cos(a) * rr, sy + math.sin(a) * rr))
            pygame.draw.lines(screen, color, True, pts, 3)
            for i in range(3):
                off = math.sin(t * 6 + i * 2) * 5
                pygame.draw.line(screen, color, (self.x-r*.6, sy+off+i*6-6), (self.x+r*.6, sy-off+i*6-6), 2)
        elif self.base_kind == "hunter":
            ang = math.atan2(self.vy, self.vx)
            tip = (self.x + math.cos(ang) * r * 1.45, sy + math.sin(ang) * r * 1.45)
            left = (self.x + math.cos(ang + 2.45) * r, sy + math.sin(ang + 2.45) * r)
            right = (self.x + math.cos(ang - 2.45) * r, sy + math.sin(ang - 2.45) * r)
            pygame.draw.polygon(screen, color, [tip, left, right], 3)
            pygame.draw.line(screen, color, (self.x, sy), tip, 2)
        elif self.base_kind == "orbiter":
            pygame.draw.circle(screen, color, (int(self.x), int(sy)), int(r * .55), 3)
            for i in range(3):
                a = t * (3.5 + i * .4) + self.phase + i * math.tau / 3
                ox = self.x + math.cos(a) * r * 1.15
                oy = sy + math.sin(a) * r * .7
                pygame.draw.circle(screen, color, (int(ox), int(oy)), 5, 2)
                pygame.draw.line(screen, color, (self.x, sy), (ox, oy), 1)
        elif self.base_kind == "dasher":
            ang = math.atan2(self.vy, self.vx)
            pts = []
            for offset, dist_mul in ((0,1.55),(2.5,.85),(math.pi,.55),(-2.5,.85)):
                a = ang + offset
                pts.append((self.x + math.cos(a) * r * dist_mul, sy + math.sin(a) * r * dist_mul))
            pygame.draw.polygon(screen, color, pts, 3)
            tail = 28 + abs(math.sin(t * 10 + self.phase)) * 18
            pygame.draw.line(screen, color, (self.x-math.cos(ang)*r*.5, sy-math.sin(ang)*r*.5), (self.x-math.cos(ang)*tail, sy-math.sin(ang)*tail), 3)

        if self.kind in HARDCORE_ENTITY_KINDS:
            rr=int(r+9+math.sin(t*8+self.phase)*3)
            halo_red=118+int(38*(.5+.5*math.sin(t*5.7+self.phase)))
            pygame.draw.circle(screen,(halo_red,22,30),(int(self.x),int(sy)),rr,2)
        label_color=WHITE if self.kind=="monster5d" else color
        draw_text(ENTITY_NAMES[self.kind], font_small, label_color, self.x, sy-r-22, center=True)

                                                         
class Player:
    def __init__(self):
        self.x = WIDTH * 0.5
        self.y = HEIGHT - 170
        self.prev_y = self.y
        self.w = 38
        self.h = 38
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.max_health = 10
        self.health = self.max_health
        self.hit_invuln = 0.0
        self.coyote = 0.0
        self.jump_buffer = 0.0
        self.dash_cd = 0.0
        self.parry_cd = 0.0
        self.parry_timer = 0.0
        self.parry_safe_timer = 0.0
        self.permanent_powers = set()
        self.last_action = "READY"
        self.facing = 1
        self.jumps_used = 0
        self.max_jumps = 2
        self.anim_flash = 0.0
        self.anim_spin = 0.0
        self.dash_anim = 0.0
        self.jump_held = False
        self.walk_phase = 0.0
        self.walk_amount = 0.0
        self.land_tween = 0.0
        self.jump_tween = 0.0
        self.lean_tween = 0.0
        self.speed_tween = 0.0
        self.dash_move_timer = 0.0
        self.dash_direction = 1
        self.wall_dash_lock = 0
                            
        self.infinite_jumps = 0.0
        self.shield = 0.0
        self.shield_hits = 0
        self.angel = 0.0
        self.flight = 0.0

    def request_jump(self):
        self.jump_buffer = JUMP_BUFFER

    def dash(self, keys=None):
        if self.dash_cd <= 0 and self.dash_move_timer <= 0:
            direction = self.facing
            if keys is not None:
                right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
                left = keys[pygame.K_LEFT] or keys[pygame.K_a]
                if right and not left:
                    direction = 1
                elif left and not right:
                    direction = -1
            if self.wall_dash_lock == direction:
                return False
            if direction < 0 and self.x <= 32:
                self.wall_dash_lock = -1
                return False
            if direction > 0 and self.x >= WIDTH - 32:
                self.wall_dash_lock = 1
                return False
            self.facing = direction
            self.dash_direction = direction
            self.dash_move_timer = .17
            self.vx = direction * DASH_SPEED
            if self.on_ground:
                self.vy = min(self.vy, -24.0)
                self.coyote = COYOTE_TIME
            else:
                self.vy *= .18
            self.dash_cd = DASH_COOLDOWN
            self.dash_anim = .30
            self.anim_flash = .22
            self.anim_spin += direction * .48
            self.last_action = "DASH"
            return True
        return False

    def parry(self, mardcore=False):
        if self.parry_cd <= 0:
            self.parry_timer = PARRY_TIME
            self.parry_cd = MARDCORE_PARRY_COOLDOWN if mardcore else PARRY_COOLDOWN
            self.anim_flash = .16
            self.last_action = "PARRY"
            return True
        return False

    def give_powerup(self, kind):
        duration = POWERUP_DURATION[kind]
        if kind == "INFINITE JUMPS":
            self.infinite_jumps = max(self.infinite_jumps, duration)
        elif kind == "SHIELD":
            self.shield = max(self.shield, duration)
            self.shield_hits = 1
        elif kind == "ANGEL":
            self.angel = max(self.angel, duration)
        elif kind == "FLIGHT":
            self.flight = max(self.flight, duration)
        self.anim_flash = .28

    def update(self, dt, keys, mouse_left=False):
        self.prev_y = self.y
        self.jump_held = bool(keys[pygame.K_SPACE] or mouse_left)

        target_walk = 1.0 if self.on_ground and abs(self.vx) > 45 else 0.0
        self.walk_amount = sine_tween(self.walk_amount, target_walk, 10.0, dt)
        self.speed_tween = sine_tween(self.speed_tween, clamp(abs(self.vx) / max(1.0, MAX_X_SPEED), 0.0, 1.0), 9.0, dt)
        self.lean_tween = sine_tween(self.lean_tween, clamp(self.vx / max(1.0, MAX_X_SPEED), -1.0, 1.0), 10.0, dt)
        self.walk_phase += dt * (8.0 + self.speed_tween * 13.0) * (1 if self.facing >= 0 else -1)
        self.jump_tween = sine_tween(self.jump_tween, 0.0 if self.on_ground else 1.0, 9.0, dt)
        self.land_tween = sine_tween(self.land_tween, 0.0, 8.0, dt)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx -= MOVE_ACCEL * dt
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx += MOVE_ACCEL * dt
            self.facing = 1

                            
        speed_cap = MAX_X_SPEED * (1.16 if self.angel > 0 else 1.0)
        if self.dash_move_timer > 0:
            self.vx = self.dash_direction * DASH_SPEED
            if self.on_ground:
                self.coyote = COYOTE_TIME
            else:
                self.coyote = max(0.0, self.coyote - dt)
        else:
            self.vx = clamp(self.vx, -speed_cap, speed_cap)
            if self.on_ground:
                self.coyote = COYOTE_TIME
                self.vx *= GROUND_FRICTION
            else:
                self.coyote = max(0.0, self.coyote - dt)
                self.vx *= AIR_FRICTION

        self.jump_buffer = max(0.0, self.jump_buffer - dt)

                                                               
        if self.flight > 0 and self.jump_held:
            self.vy -= 2350 * dt
            self.vy = max(self.vy, -590)

        if self.jump_buffer > 0:
            can_ground_jump = self.coyote > 0 and self.jumps_used == 0
            unlimited = self.infinite_jumps > 0 or self.flight > 0
            can_air_jump = (not self.on_ground) and (unlimited or self.jumps_used < self.max_jumps)

            if can_ground_jump or can_air_jump:
                self.vy = -JUMP_SPEED * (1.05 if self.angel > 0 else 1.0)
                self.on_ground = False
                self.coyote = 0
                self.jump_buffer = 0
                self.jumps_used += 1
                self.anim_spin += math.pi/2 if self.jumps_used > 1 else .35
                self.anim_flash = .09
                if unlimited and self.jumps_used > 2:
                    self.last_action = "INFINITE JUMP"
                else:
                    self.last_action = "DOUBLE JUMP" if self.jumps_used == 2 else "JUMP"

        gravity = GRAVITY
        if self.angel > 0:
            gravity *= .78
        if self.flight > 0:
            gravity *= .52
        if self.dash_move_timer > 0:
            gravity *= .18
        self.vy += gravity * dt

        next_x = self.x + self.vx * dt
        self.y += self.vy * dt
        hit_left = next_x < 24
        hit_right = next_x > WIDTH - 24
        self.x = clamp(next_x, 24, WIDTH - 24)
        if self.dash_move_timer > 0 and ((hit_left and self.dash_direction < 0) or (hit_right and self.dash_direction > 0)):
            self.wall_dash_lock = self.dash_direction
            self.dash_move_timer = 0.0
            self.dash_cd = max(self.dash_cd, .42)
            self.vx = 0.0
        if self.wall_dash_lock < 0 and self.x > 76:
            self.wall_dash_lock = 0
        elif self.wall_dash_lock > 0 and self.x < WIDTH - 76:
            self.wall_dash_lock = 0

        self.dash_cd = max(0.0, self.dash_cd - dt)
        self.dash_move_timer = max(0.0, self.dash_move_timer - dt)
        self.hit_invuln = max(0.0, self.hit_invuln - dt)
        self.parry_safe_timer = max(0.0, self.parry_safe_timer - dt)
        self.parry_cd = max(0.0, self.parry_cd - dt)
        self.parry_timer = max(0.0, self.parry_timer - dt)
        self.anim_flash = max(0.0, self.anim_flash - dt)
        self.dash_anim = max(0.0, self.dash_anim - dt)
        self.anim_spin *= max(0.0, 1.0-dt*4.0)

        if "INFINITE JUMPS" in self.permanent_powers:
            self.infinite_jumps = max(self.infinite_jumps, 1.0)
        else:
            self.infinite_jumps = max(0.0, self.infinite_jumps - dt)
        if "SHIELD" in self.permanent_powers:
            self.shield = max(self.shield, 1.0)
            self.shield_hits = 1
        else:
            self.shield = max(0.0, self.shield - dt)
        if "ANGEL" in self.permanent_powers:
            self.angel = max(self.angel, 1.0)
        else:
            self.angel = max(0.0, self.angel - dt)
        if "FLIGHT" in self.permanent_powers:
            self.flight = max(self.flight, 1.0)
        else:
            self.flight = max(0.0, self.flight - dt)
        if self.shield <= 0:
            self.shield_hits = 0

    def draw(self, camera_y, t):
        sy = self.y - camera_y

                                                  
        walk_sin = math.sin(self.walk_phase)
        walk_abs = abs(math.sin(self.walk_phase))
        walk_bob = walk_abs * 5.0 * self.walk_amount
        walk_sway = math.sin(self.walk_phase * 0.5) * 3.5 * self.walk_amount
        wave_x = math.sin(t * 9.0) * 2.2 + walk_sway
        wave_y = math.sin(t * 11.0 + 1.2) * 1.7 - walk_bob

                                                  
        stretch = clamp(abs(self.vy)/900, 0, .22)
        if self.vy < -80:
            scale_x, scale_y = 1-stretch*.45, 1+stretch
        elif self.vy > 100:
            scale_x, scale_y = 1+stretch*.55, 1-stretch*.45
        else:
            idle = math.sin(t*8)*.045
            scale_x, scale_y = 1+idle, 1-idle

        if self.dash_anim > 0:
            scale_x *= 1.35
            scale_y *= .72

        walk_compress = math.sin(self.walk_phase * 2.0) * .07 * self.walk_amount
        scale_x *= 1.0 + walk_compress
        scale_y *= 1.0 - walk_compress * .8
        scale_x *= 1.0 + self.land_tween * .20
        scale_y *= 1.0 - self.land_tween * .26

        hw = self.w * .5 * scale_x
        hh = self.h * .5 * scale_y
        cx = self.x + wave_x
        cy = sy + wave_y
        ang = self.anim_spin + math.sin(t*3.2)*.035
        ang += self.lean_tween * .10
        ang += math.sin(self.walk_phase) * .07 * self.walk_amount
        ca, sa = math.cos(ang), math.sin(ang)

        base = [(-hw,-hh),(hw,-hh),(hw,hh),(-hw,hh)]
        pts=[]
        for i,(px,py) in enumerate(base):
                                          
            px += math.sin(t*7.4+i*1.7)*2
            py += math.sin(t*8.1+i*1.2)*2
            rx = px*ca - py*sa
            ry = px*sa + py*ca
            pts.append((cx+rx,cy+ry))

        cube_color = WHITE
        if self.angel > 0: cube_color = YELLOW
        elif self.flight > 0: cube_color = PINK
        elif self.infinite_jumps > 0: cube_color = CYAN
        elif self.shield > 0: cube_color = BLUE
        if self.anim_flash > 0 and math.sin(t*45)>0:
            cube_color = WHITE

        pygame.draw.polygon(screen, cube_color, pts, 3)

                          
        inner = 7 + math.sin(t*10)*2
        pygame.draw.circle(screen, cube_color, (int(cx),int(cy)), max(2,int(inner)), 2)

                            
        trail_count = 7 if self.dash_anim > 0 or self.flight > 0 else 4
        for i in range(trail_count):
            k=i+1
            tx = cx - self.vx*.011*k + math.sin(t*8-k)*3
            ty = cy - self.vy*.004*k + math.sin(t*10-k*.7)*3
            rr=max(2,8-i)
            pygame.draw.rect(screen, cube_color, pygame.Rect(int(tx-rr/2),int(ty-rr/2),rr,rr),1)

                                          
        if self.shield > 0 and self.shield_hits > 0:
            rr = 34 + math.sin(t*9)*4
            pygame.draw.circle(screen, BLUE, (int(cx),int(cy)), int(rr), 3)
            pygame.draw.circle(screen, CYAN, (int(cx),int(cy)), int(rr+7+math.sin(t*13)*3), 1)

                                                           
        if self.angel > 0:
            halo_y = cy-34+math.sin(t*5)*3
            pygame.draw.ellipse(screen, YELLOW, pygame.Rect(int(cx-18),int(halo_y-5),36,10),2)
            for side in (-1,1):
                wing=[]
                for j in range(7):
                    f=j/6
                    wx=cx+side*(18+f*28)
                    wy=cy+math.sin(t*7+f*math.pi*2)*7-f*7
                    wing.append((wx,wy))
                pygame.draw.lines(screen,YELLOW,False,wing,3)

                                                   
        if self.flight > 0:
            for i in range(3):
                x0=cx+(i-1)*8
                pts2=[]
                for j in range(6):
                    yy=cy+20+j*6
                    xx=x0+math.sin(t*13+j*.9+i)*5
                    pts2.append((xx,yy))
                pygame.draw.lines(screen,PINK,False,pts2,2)

                                                     
        if self.infinite_jumps > 0:
            pts3=[]
            for j in range(32):
                a=j/31*math.tau
                ox=math.sin(a)*19
                oy=math.sin(a*2)*8
                pts3.append((cx+ox,cy-34+oy))
            pygame.draw.lines(screen,CYAN,False,pts3,2)

        if self.parry_timer > 0:
            rr=PARRY_RADIUS+math.sin(t*18)*8
            pygame.draw.circle(screen,CYAN,(int(cx),int(cy)),int(rr),4)
            pygame.draw.circle(screen,WHITE,(int(cx),int(cy)),int(rr*.72),2)


                                                      
class Game:
    def __init__(self):
                                                  
                                                 
        self.music_name = None
        self.audio_status = "MUSIC READY - PRESS PLAY"
        self.audio_notice_time = 0.0
        self.cheat_noclip = False
        self.cheat_god = False
        self.progress_locked = False
        self.game_mode = "main"
        self.sandbox_mode = False
        self.hardcore_mode = False
        self.progress_data = self.load_progress()
        self.best_style = int(self.progress_data.get("best_style",0))
        self.total_runs = int(self.progress_data.get("total_runs",0))
        self.desktop_snapshot = None
        self.desktop_snapshot_scaled = None
        self.desktop_snapshot_size = None
        self.desktop_source_size = None
        self.desktop_app_count = 0
        self._ui_layer = None
        self._fx_layer = None
        self._vignette_cache = {}
        self._panel_cache = {}
        self.reset()

    def reusable_layer(self, which):
        attr = "_ui_layer" if which == "ui" else "_fx_layer"
        layer = getattr(self,attr,None)
        if layer is None or layer.get_size() != (WIDTH,HEIGHT):
            layer = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA).convert_alpha()
            setattr(self,attr,layer)
        layer.fill((0,0,0,0))
        return layer

    def cached_panel(self, key, size, builder):
        cache_key=(key,size)
        surf=self._panel_cache.get(cache_key)
        if surf is None:
            surf=pygame.Surface(size,pygame.SRCALPHA).convert_alpha()
            builder(surf)
            self._panel_cache[cache_key]=surf
        return surf

    def vignette_layer(self):
        key=(WIDTH,HEIGHT,bool(self.hardcore_mode))
        cached=self._vignette_cache.get(key)
        if cached is not None:
            return cached
        cached=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA).convert_alpha()
        for ring in range(5):
            alpha=(14 if self.hardcore_mode else 10)+ring*7
            inset=ring*18
            pygame.draw.rect(cached,(0,0,0,alpha),pygame.Rect(inset,inset,WIDTH-inset*2,HEIGHT-inset*2),10,border_radius=28)
        self._vignette_cache={key:cached}
        return cached

    def capture_desktop_sandbox(self):
        if not self.sandbox_mode:
            return
        self.desktop_snapshot = None
        self.desktop_snapshot_scaled = None
        self.desktop_snapshot_size = None
        self.desktop_source_size = None
        self.desktop_app_count = 0
        self.platforms = []
        floor_y = HEIGHT - 34
        self.player.x = WIDTH*.5
        self.player.y = floor_y - self.player.h*.5 - 18
        self.player.prev_y = self.player.y
        self.camera_y = 0.0
        self.add_action("SANDBOX RESET",0)

    def start_music(self):
        if not AUDIO_OK:
            init_audio()
        self.music_name, self.audio_status = music_setup(self.game_mode)
        self.audio_notice_time = 5.0

    def start_menu_music(self):
        if not AUDIO_OK:
            init_audio()
        self.music_name, self.audio_status = menu_music_setup()
        self.audio_notice_time = 3.0

    def stop_music(self):
        if AUDIO_OK:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
        self.music_name = None
        self.audio_status = "MUSIC READY - PRESS PLAY"

    def clear_cheat_state(self):
        self.cheat_noclip = False
        self.cheat_god = False
        if hasattr(self, "player"):
            self.player.permanent_powers.clear()
            self.player.infinite_jumps = 0.0
            self.player.shield = 0.0
            self.player.shield_hits = 0
            self.player.angel = 0.0
            self.player.flight = 0.0
            self.player.hit_invuln = 0.0
            self.player.parry_safe_timer = 0.0

    def reset(self):
        stop_death_tone()
        if not death_music_recovering():
            stop_death_music_pitch()
        self.player = Player()
        if getattr(self,"hardcore_mode",False):
            self.player.max_health = 1
            self.player.health = 1
        self.platforms = []
        self.entities = []
        self.bullets = []
        self.weapon_index = 0
        self.weapon_cooldown = 0.0
        self.weapon_flash = 0.0
        self.weapon_active_timer = 0.0
        self.powerups = []
        self.orbs = []
        self.particles = []
        self.shockwaves = []
        self.blood = []
        self.vfx_flash = 0.0
        self.ui_shake_timer = 0.0
        self.ui_shake_strength = 0.0
        self.camera_y = 0.0
        self.start_y = HEIGHT - 170
        self.top_generated = HEIGHT - 120
        self.score = 0                      
        self.death_message = random.choice(['MEHH', 'NUB', 'OMFG', 'GG', '...'])
        self.style_score = 0
        self.style_decay_delay = 0.0
        self.last_rank = rank_for_score(self.style_score,self.game_mode)
        self.rank_pop_timer = 0.0
        self.rank_pop_duration = 0.72
        self.best = int(self.load_best())
        self.best_style = int(getattr(self,"progress_data",{}).get("best_style",getattr(self,"best_style",0)))
        self.total_runs = int(getattr(self,"progress_data",{}).get("total_runs",getattr(self,"total_runs",0)))
        self.attempt = self.total_runs + 1 if not self.sandbox_mode else 0
        self.elapsed = 0.0
        self.entity_timer = 0.0
        self.dead = False
        self.monster_spawned = False
        self.shake = 0.0
        self.impact_timer = 0.0
        self.impact_entity = None
        self.impact_duration = 0.055
        self.action_feed = []                               
        self.last_scored_action = ""
        self.action_repeat = 0
        self.walk_sfx_timer = 0.0
        self.sandbox_active_platform = None
        self.sandbox_clear_button_pressed = False
        self.sandbox_clear_button_flash = 0.0
        self.sandbox_mode = getattr(self, "sandbox_mode", False)

        if self.sandbox_mode:
            floor_y = HEIGHT - 34
            self.player.x = WIDTH * .5
            self.player.y = floor_y - self.player.h * .5 - 12
            self.player.prev_y = self.player.y
            self.start_y = self.player.y
            self.top_generated = floor_y
            self.orbs = [
                Orb("YELLOW", WIDTH*.24, HEIGHT*.69),
                Orb("CYAN", WIDTH*.50, HEIGHT*.49),
                Orb("YELLOW", WIDTH*.36, HEIGHT*.30),
                Orb("CYAN", WIDTH*.68, HEIGHT*.24)
            ]
            self.add_action("SANDBOX READY", 0)
        else:
            self.platforms.append(Platform(WIDTH/2, HEIGHT - 110, 220))
            self.generate_until(-2800)
            self.add_action("RUN START", 0)

    def progress_path(self):
        return portable_data_dir()/"cubed_progress.json"

    def load_progress(self):
        try:
            p=self.progress_path()
            if p.exists():
                data=json.loads(p.read_text(encoding="utf-8"))
                if isinstance(data,dict):
                    return data
        except:
            pass
        legacy_best=0
        try:
            p=portable_data_dir()/"cubed_best.txt"
            legacy=Path(__file__).resolve().parent/'pacedcube_best.txt'
            if p.exists():
                legacy_best=int(p.read_text().strip() or 0)
            elif legacy.exists():
                legacy_best=int(legacy.read_text().strip() or 0)
        except:
            pass
        return {
            "best_height":legacy_best,
            "best_style":0,
            "highest_rank":"FUCK",
            "total_runs":0
        }

    def load_best(self):
        data=getattr(self,"progress_data",None)
        if not isinstance(data,dict):
            data=self.load_progress()
            self.progress_data=data
        return int(data.get("best_height",0))

    def save_best(self, count_run=False):
        if self.progress_locked:
            return
        try:
            self.best=max(int(getattr(self,"best",0)),int(getattr(self,"score",0)))
            self.best_style=max(int(getattr(self,"best_style",0)),int(getattr(self,"style_score",0)))
            if count_run:
                self.total_runs=int(getattr(self,"total_runs",0))+1
            highest_rank=rank_for_score(self.best_style,self.game_mode)
            data={
                "best_height":int(self.best),
                "best_style":int(self.best_style),
                "highest_rank":highest_rank,
                "total_runs":int(getattr(self,"total_runs",0))
            }
            self.progress_data=data
            self.progress_path().write_text(json.dumps(data,indent=2),encoding="utf-8")
            (portable_data_dir()/"cubed_best.txt").write_text(str(int(self.best)))
        except:
            pass

    def add_action(self, name, points=0):
                                                                  
        if name == self.last_scored_action:
            self.action_repeat += 1
        else:
            self.last_scored_action = name
            self.action_repeat = 0
        freshness = max(.35, 1.0 - self.action_repeat*.12)
        gained = int(points*freshness)
        self.style_score += gained
        if gained > 0:
            self.style_decay_delay = 2.4
        self.action_feed.insert(0,[name,gained,3.0])
        self.action_feed = self.action_feed[:7]
        self.player.last_action = name

    def entity_damage_style_penalty(self, entity):
        if self.style_score<=0:
            return 0
        if entity.kind=="monster5d":
            ratio=.26
            floor_loss=520
        elif entity.kind=="monster":
            ratio=.22
            floor_loss=380
        elif entity.kind in HARDCORE_ENTITY_KINDS:
            ratio=.18
            floor_loss=300
        else:
            ratio=.12
            floor_loss=170
        penalty=min(int(self.style_score),max(floor_loss,int(self.style_score*ratio)))
        old_rank=rank_for_score(self.style_score,self.game_mode)
        self.style_score=max(0,self.style_score-penalty)
        new_rank=rank_for_score(self.style_score,self.game_mode)
        self.style_decay_delay=1.2
        self.action_feed.insert(0,["STYLE DAMAGE: "+ENTITY_NAMES[entity.kind],-penalty,3.4])
        self.action_feed=self.action_feed[:7]
        self.last_scored_action=""
        self.action_repeat=0
        self.last_rank=new_rank
        if RANK_ORDER.index(new_rank)<RANK_ORDER.index(old_rank):
            self.ui_shake_timer=max(self.ui_shake_timer,.34)
            self.ui_shake_strength=max(self.ui_shake_strength,1.0)
        return penalty

    def update_style_decay(self, dt):
        if self.dead:
            return
        if self.style_decay_delay > 0.0:
            self.style_decay_delay = max(0.0, self.style_decay_delay - dt)
            return
        if self.style_score <= 0:
            return
        rank = rank_for_score(self.style_score,self.game_mode)
        rates = {
            "FUCK": 0,
            "Efficient": 7,
            "Dull": 10,
            "Cool": 14,
            "Bold": 19,
            "Agreeable": 25,
            "Sensational": 32,
            "SUPER Sensational": 40,
            "HYPER Sensational": 50,
            "HELL YEAH!": 62,
            "CUBE": 76
        }
        self.style_score = max(0, self.style_score - rates.get(rank, 10) * dt)
        if self.style_score < 1:
            self.style_score = 0

    def generate_until(self,target_y):
        if self.sandbox_mode:
            return
        while self.top_generated>target_y:
            gap=random.randint(PLATFORM_GAP_MIN,PLATFORM_GAP_MAX)
            self.top_generated-=gap
            route_wave=math.sin(abs(self.top_generated)*.006)*WIDTH*.24
            center=WIDTH/2+route_wave
            x=clamp(center+random.randint(-210,210),100,WIDTH-100)
            w=random.randint(PLATFORM_WIDTH_MIN,PLATFORM_WIDTH_MAX)
            plat=Platform(x,self.top_generated,w)
            self.platforms.append(plat)

                                                           
            power_chance=.22 if self.hardcore_mode else POWERUP_SPAWN_CHANCE
            if self.top_generated < HEIGHT-250 and random.random()<power_chance:
                if self.hardcore_mode and random.random()<.58:
                    kind=random.choice(PowerUp.WEAPON_NAMES)
                else:
                    kind=random.choice(PowerUp.NAMES)
                self.powerups.append(PowerUp(kind,x,self.top_generated-42))
            if self.top_generated < HEIGHT-220 and random.random()<.18:
                self.orbs.append(Orb(random.choice(Orb.KINDS),x+random.randint(-55,55),self.top_generated-random.randint(55,95)))

    def burst(self,x,y,color,amount=12,speed=280):
        for _ in range(min(amount,32)):
            self.particles.append(Particle(x,y,color,speed=speed,life=random.uniform(.28,.58),size=random.randint(3,6)))

    def blood_burst(self,x,y,amount=18,heavy=False):
        for _ in range(min(amount,48)):
            self.blood.append(BloodParticle(x,y,heavy))

    def shockwave(self, x, y, color, radius=18, growth=420, life=.38, width=4, flatten=.35):
        self.shockwaves.append(Shockwave(x, y, color, radius, growth, life, width, flatten))

    def landing_vfx(self, x, y, impact_speed):
        strength = clamp((impact_speed - 180.0) / 950.0, 0.0, 1.0)
        play_sfx("land", .65 + strength * .35)
        amount = int(10 + strength * 22)
        for _ in range(amount):
            direction = random.choice((-1, 1))
            p = Particle(x + random.uniform(-18, 18), y - 4, WHITE, speed=random.uniform(110, 320 + strength * 260), life=random.uniform(.18, .48), size=random.randint(2, 5))
            p.vx = direction * random.uniform(90, 320 + strength * 420)
            p.vy = random.uniform(-240 - strength * 260, -70)
            p.color = random.choice((WHITE, LIGHT, CYAN))
            self.particles.append(p)
        self.shockwave(x, y, CYAN, 18, 460 + strength * 520, .34 + strength * .18, 5, .24)
        self.shockwave(x, y, WHITE, 10, 300 + strength * 340, .22 + strength * .12, 3, .18)
        if SCREEN_SHAKE_ENABLED:
            self.shake = max(self.shake, 3.0 + strength * 10.0)
        if IMPACT_FLASH_ENABLED:
            self.vfx_flash = max(self.vfx_flash, .06 + strength * .08)

    def action_vfx(self, action):
        p = self.player
        if action == "JUMP":
            play_sfx("jump")
            self.burst(p.x, p.y + p.h * .45, CYAN, 8, 180)
            self.shockwave(p.x, p.y + p.h * .45, CYAN, 10, 220, .2, 2, .3)
        elif action in ("DOUBLE JUMP", "INFINITE JUMP"):
            play_sfx("double_jump")
            self.burst(p.x, p.y, PURPLE if action == "DOUBLE JUMP" else YELLOW, 16, 320)
            self.shockwave(p.x, p.y, PURPLE if action == "DOUBLE JUMP" else YELLOW, 12, 390, .28, 3, 1.0)
        elif action == "DASH":
            play_sfx("dash")
            self.burst(p.x - p.facing * 24, p.y, CYAN, 28, 560)
            self.burst(p.x - p.facing * 34, p.y, WHITE, 12, 430)
            self.shockwave(p.x, p.y, CYAN, 18, 520, .28, 4, .72)
            self.shockwave(p.x, p.y, WHITE, 10, 360, .18, 2, .45)
            if SCREEN_SHAKE_ENABLED:
                self.shake = max(self.shake, 9.5)
            self.vfx_flash = max(self.vfx_flash, .09)
        elif action == "PARRY":
            play_sfx("parry",.78)
            self.shockwave(p.x, p.y, WHITE, 18, 520, .25, 4, 1.0)

    def current_weapon(self):
        return MARDCORE_WEAPON_ORDER[self.weapon_index % len(MARDCORE_WEAPON_ORDER)]

    def select_weapon(self,index):
        return

    def cycle_weapon(self,delta):
        return

    def fire_weapon(self):
        if not (self.hardcore_mode or self.sandbox_mode) or self.dead or self.weapon_cooldown>0 or self.weapon_active_timer<=0:
            return False
        weapon=self.current_weapon()
        data=MARDCORE_WEAPONS[weapon]
        mx,my=pygame.mouse.get_pos()
        world_my=my+self.camera_y
        dx=mx-self.player.x
        dy=world_my-self.player.y
        dist=max(1.0,math.hypot(dx,dy))
        base_angle=math.atan2(dy,dx)
        self.player.facing=1 if dx>=0 else -1
        fire_wave=math.sin(self.elapsed*19.0+self.weapon_index*1.7)
        muzzle_dist=28+fire_wave*2.5
        muzzle_x=self.player.x+math.cos(base_angle)*muzzle_dist
        muzzle_y=self.player.y+math.sin(base_angle)*muzzle_dist
        for i in range(data["pellets"]):
            if data["pellets"]==1:
                spread=math.sin(self.elapsed*31.0+i*2.1+self.weapon_index)*data["spread"]
            else:
                center=(i-(data["pellets"]-1)*.5)/max(1.0,data["pellets"]-1)
                spread=center*data["spread"]+math.sin(self.elapsed*27.0+i*1.93)*.018
            a=base_angle+spread
            speed_wave=.98+.04*(.5+.5*math.sin(self.elapsed*23.0+i*2.7))
            speed=data["speed"]*speed_wave
            self.bullets.append(Bullet(muzzle_x,muzzle_y,math.cos(a)*speed,math.sin(a)*speed,data["damage"],data["knockback"],data["color"],weapon))
        self.weapon_cooldown=data["cooldown"]
        self.weapon_flash=.075
        recoil_base=80 if weapon=="AK-47" else 160 if weapon=="M1 GARAND" else 240
        recoil=recoil_base*(.94+.12*(.5+.5*math.sin(self.elapsed*24.0+self.weapon_index)))
        self.player.vx-=math.cos(base_angle)*recoil
        self.player.vy-=math.sin(base_angle)*recoil*.18
        self.burst(muzzle_x,muzzle_y,data["color"],4 if weapon=="AK-47" else 7,180)
        if SCREEN_SHAKE_ENABLED:
            shake_base=1.5 if weapon=="AK-47" else 3.0 if weapon=="M1 GARAND" else 4.5
            self.shake=max(self.shake,shake_base*(.9+.2*(.5+.5*math.sin(self.elapsed*30.0))))
        play_sfx("gun_ak" if weapon=="AK-47" else "gun_m1" if weapon=="M1 GARAND" else "gun_shotgun",.82 if weapon=="AK-47" else 1.0)
        return True

    def update_bullets(self,dt):
        if not (self.hardcore_mode or self.sandbox_mode):
            self.bullets.clear()
            return
        for b in self.bullets:
            b.update(dt)
            if b.dead:
                continue
            for e in self.entities:
                if e.dead:
                    continue
                if math.hypot(e.x-b.x,e.y-b.y)>e.radius+b.radius:
                    continue
                b.dead=True
                dx=e.x-self.player.x
                dy=e.y-self.player.y
                dist=max(1.0,math.hypot(dx,dy))
                nx,ny=dx/dist,dy/dist
                play_sfx("enemy_hit",.30 if b.weapon=="AK-47" else .42)
                if e.kind in ("monster","monster5d"):
                    mult=.55 if e.kind=="monster5d" else .72
                    e.vx+=nx*b.knockback*mult
                    e.vy+=ny*b.knockback*mult*.5
                    self.burst(b.x,b.y,WHITE if e.kind=="monster5d" else RED,3,120)
                elif e.kind in HARDCORE_ENTITY_KINDS:
                    e.weapon_hp-=b.damage
                    e.vx+=nx*b.knockback
                    e.vy+=ny*b.knockback*.38
                    self.burst(b.x,b.y,b.color,4,150)
                    if e.weapon_hp<=0:
                        e.dead=True
                        play_sfx("enemy_down",.72)
                        self.add_action("GUN DOWN: "+ENTITY_NAMES[e.kind],95 if b.weapon=="AK-47" else 125)
                        self.blood_burst(e.x,e.y,12,False)
                        self.shockwave(e.x,e.y,b.color,10,260,.20,3,.8)
                else:
                    e.dead=True
                    play_sfx("enemy_down",.65)
                    self.add_action("GUN DOWN: "+ENTITY_NAMES[e.kind],70)
                    self.burst(e.x,e.y,b.color,6,170)
                    self.blood_burst(e.x,e.y,10,False)
                break
        self.bullets=[b for b in self.bullets if not b.dead and -600<=(b.y-self.camera_y)<=HEIGHT+600]

    def draw_player_weapon(self,cam):
        if not (self.hardcore_mode or self.sandbox_mode) or self.dead or self.weapon_active_timer<=0:
            return
        weapon=self.current_weapon()
        mx,my=pygame.mouse.get_pos()
        base_px=self.player.x
        base_py=self.player.y-cam
        aim=math.atan2(my-base_py,mx-base_px)
        breathe=math.sin(self.elapsed*5.2+self.weapon_index*.8)
        sway=math.sin(self.elapsed*8.4+self.player.walk_phase*.22)*2.4
        recoil_phase=clamp(self.weapon_flash/.075,0.0,1.0)
        recoil_wave=math.sin(recoil_phase*math.pi)
        ang=aim+math.sin(self.elapsed*4.7+self.weapon_index)*.012+recoil_wave*.018*self.player.facing
        ca,sa=math.cos(ang),math.sin(ang)
        nx,ny=-sa,ca
        px=base_px+nx*(breathe*1.8+sway)-ca*recoil_wave*8
        py=base_py+ny*(breathe*1.8+sway)-sa*recoil_wave*8
        def pt(forward,side=0,wave_amp=0.0,wave_freq=.18):
            wobble=math.sin(self.elapsed*7.0+forward*wave_freq+self.weapon_index)*wave_amp
            return (px+ca*forward+nx*(side+wobble),py+sa*forward+ny*(side+wobble))
        body=MARDCORE_WEAPONS[weapon]["color"]
        if weapon=="AK-47":
            pygame.draw.line(screen,body,pt(8,0,1.2),pt(44,0,1.2),6)
            pygame.draw.line(screen,LIGHT,pt(38,0,.8),pt(58,0,.8),3)
            pygame.draw.line(screen,body,pt(17,3,.9),pt(5,10,.9),5)
            pygame.draw.line(screen,body,pt(25,4,.9),pt(31,13,.9),5)
        elif weapon=="M1 GARAND":
            pygame.draw.line(screen,body,pt(5,0,.7),pt(58,0,.7),5)
            pygame.draw.line(screen,(122,78,48),pt(10,4,.6),pt(43,4,.6),7)
            pygame.draw.line(screen,LIGHT,pt(48,0,.5),pt(65,0,.5),2)
        else:
            barrel_wave=1.4+math.sin(self.elapsed*6.2)*.5
            pygame.draw.line(screen,body,pt(7,-3,barrel_wave),pt(53,-3,barrel_wave),4)
            pygame.draw.line(screen,body,pt(7,3,barrel_wave),pt(53,3,barrel_wave),4)
            pygame.draw.line(screen,(125,82,52),pt(12,7,.8),pt(36,7,.8),7)
        if self.weapon_flash>0:
            tip=pt(64,0,2.0)
            flash=7+int(5*(.5+.5*math.sin(self.elapsed*28)))
            rays=4
            pygame.draw.circle(screen,YELLOW,(int(tip[0]),int(tip[1])),flash,2)
            for i in range(rays):
                a=ang+i*math.tau/rays+math.sin(self.elapsed*34+i)*.18
                rr=flash+5+math.sin(self.elapsed*31+i*1.7)*3
                pygame.draw.line(screen,YELLOW,tip,(tip[0]+math.cos(a)*rr,tip[1]+math.sin(a)*rr),2)

    def draw_weapon_hud(self):
        if not (self.hardcore_mode or self.sandbox_mode):
            return
        pulse=.5+.5*math.sin(self.elapsed*6.8+self.weapon_index)
        x=WIDTH*.5+math.sin(self.elapsed*3.1)*3
        y=HEIGHT-78+math.sin(self.elapsed*4.2+self.weapon_index)*2
        if self.weapon_active_timer<=0:
            draw_text("FIND A WEAPON POWER-UP",font_small,LIGHT,x,y+12,center=True)
            return
        weapon=self.current_weapon()
        data=MARDCORE_WEAPONS[weapon]
        ready=self.weapon_cooldown<=0
        c=data["color"] if ready else LIGHT
        draw_text(f"{weapon}  {self.weapon_active_timer:05.2f}s",font_mid,c,x,y,center=True)
        line_w=180+int(28*pulse)
        pygame.draw.line(screen,c,(x-line_w*.5,y+22),(x+line_w*.5,y+22),1+int(pulse))
        draw_text("M1 = FIRE   WEAPON POWER-UP = 60.00s",font_small,LIGHT,x,y+34,center=True)

    def spawn_sandbox_entity(self, kind, screen_x, screen_y):
        if not self.sandbox_mode:
            return
        world_y=screen_y+self.camera_y
        e=Entity(kind,float(screen_x),float(world_y))
        if kind in ("monster","monster5d"):
            self.monster_spawned=True
        self.entities.append(e)
        special=kind in ("monster","monster5d") or kind in HARDCORE_ENTITY_KINDS
        spawn_color=WHITE if kind=="monster5d" else RED if kind=="monster" or kind in HARDCORE_ENTITY_KINDS else CYAN
        self.burst(screen_x,world_y,spawn_color,18 if special else 10,320 if kind in HARDCORE_ENTITY_KINDS else 260)
        self.add_action("SPAWN: "+ENTITY_NAMES[kind],0)

    def spawn_sandbox_orb(self, kind, screen_x, screen_y):
        if not self.sandbox_mode or kind not in Orb.KINDS:
            return
        world_y=screen_y+self.camera_y
        orb=Orb(kind,float(screen_x),float(world_y))
        self.orbs.append(orb)
        color=orb.color()
        self.burst(screen_x,world_y,color,12,260)
        self.shockwave(screen_x,world_y,color,10,280,.24,3,.8)
        self.add_action("SPAWN: "+kind+" ORB",0)

    def spawn_sandbox_powerup(self, kind, screen_x, screen_y):
        if not self.sandbox_mode or kind not in PowerUp.NAMES:
            return
        world_y=screen_y+self.camera_y
        pu=PowerUp(kind,float(screen_x),float(world_y))
        self.powerups.append(pu)
        color=pu.color()
        self.burst(screen_x,world_y,color,14,280)
        self.shockwave(screen_x,world_y,color,10,300,.24,3,.8)
        self.add_action("SPAWN: "+kind,0)

    def spawn_sandbox_weapon(self, kind, screen_x, screen_y):
        if not self.sandbox_mode or kind not in PowerUp.WEAPON_NAMES:
            return
        world_y=screen_y+self.camera_y
        pu=PowerUp(kind,float(screen_x),float(world_y))
        self.powerups.append(pu)
        color=pu.color()
        self.burst(screen_x,world_y,color,14,280)
        self.shockwave(screen_x,world_y,color,10,300,.24,3,.8)
        self.add_action("SPAWN: "+kind+" POWER-UP",0)

    def spawn_sandbox_platform(self, screen_x, screen_y, width=180, height=18):
        if not self.sandbox_mode:
            return
        world_y=screen_y+self.camera_y
        width=clamp(float(width),40.0,680.0)
        height=clamp(float(height),8.0,220.0)
        plat=Platform(float(screen_x),float(world_y),width,height)
        self.platforms.append(plat)
        self.sandbox_active_platform=plat
        self.burst(screen_x,world_y,CYAN,12,220)
        self.shockwave(screen_x,world_y,CYAN,10,260,.22,3,.35)
        self.add_action("SPAWN: CUSTOM PLATFORM",0)

    def resize_sandbox_active_platform(self, width, height):
        if not self.sandbox_mode:
            return
        plat=self.sandbox_active_platform
        if plat is None or plat not in self.platforms:
            return
        plat.w=clamp(float(width),40.0,680.0)
        plat.h=clamp(float(height),8.0,220.0)

    def spawn_entity(self):
        if self.hardcore_mode:
            kinds=['m_drone','m_wraith','m_hunter','m_orbiter','m_dasher','m_dasher','m_hunter']
        else:
            kinds=['drone','wraith','hunter']
            if self.score>500:
                kinds.append('orbiter')
            if self.score>950:
                kinds.append('dasher')
        kind=random.choice(kinds)
        side=random.choice([-1,1])
        self.entities.append(Entity(kind,80 if side<0 else WIDTH-80,self.player.y-random.randint(180,500)))

    def spawn_bob(self):
        if self.hardcore_mode:
            e=Entity('monster5d',WIDTH*.5,self.player.y-430)
            e.phase+=math.sin(self.elapsed*2.0)*.18
            self.entities.append(e)
            self.monster_spawned=True
            self.add_action('PENTARACT ARRIVED',900)
            play_sfx("pentaract",1.0)
            self.burst(WIDTH*.5,self.player.y-430,WHITE,26,460)
        else:
            side=random.choice([-1,1])
            self.entities.append(Entity('monster',70 if side<0 else WIDTH-70,self.player.y-320))
            self.monster_spawned=True
            self.add_action('TESSERACT ARRIVED',300)
            play_sfx("tesseract",.92)

    def handle_platform_collision(self):
        p=self.player
        p.on_ground=False
        if p.vy<0:return
        prev_bottom=p.prev_y+p.h/2
        new_bottom=p.y+p.h/2
        for plat in self.platforms:
            top=plat.top();left=plat.x-plat.w/2;right=plat.x+plat.w/2
            if prev_bottom<=top+5 and new_bottom>=top and p.x+p.w/2>left and p.x-p.w/2<right:
                impact_speed = p.vy
                p.y=top-p.h/2
                if not p.on_ground and impact_speed > 180:
                    p.land_tween = min(1.0, impact_speed / 900.0)
                    self.landing_vfx(p.x, top, impact_speed)
                p.vy=0
                p.on_ground=True
                p.coyote=COYOTE_TIME
                p.jumps_used=0
                return

    def handle_orbs(self):
        p=self.player
        for orb in self.orbs:
            orb.update(1.0/FPS)
            if orb.cooldown > 0:
                continue
            if math.hypot(orb.x-p.x,orb.y-p.y) < orb.radius+27:
                if orb.kind == "YELLOW":
                    p.vy = -980
                    p.on_ground = False
                    p.jumps_used = min(p.jumps_used,1)
                elif orb.kind == "CYAN":
                    p.vy = -1320
                    p.on_ground = False
                    p.jumps_used = 0
                orb.cooldown = .72
                c=orb.color()
                self.burst(orb.x,orb.y,c,20,390)
                self.shockwave(orb.x,orb.y,c,14,430,.30,4,.8)
                if SCREEN_SHAKE_ENABLED:
                    self.shake=max(self.shake,5.0)
                play_sfx("orb_yellow" if orb.kind=="YELLOW" else "orb_cyan",.88)
                self.add_action(orb.kind+" ORB",45)

    def handle_powerups(self):
        p=self.player
        for pu in self.powerups:
            if pu.taken:continue
            if math.hypot(pu.x-p.x,pu.y-p.y)<pu.radius+26:
                pu.taken=True
                if pu.kind in PowerUp.WEAPON_NAMES and (self.hardcore_mode or self.sandbox_mode):
                    self.weapon_index=MARDCORE_WEAPON_ORDER.index(pu.kind)
                    self.weapon_active_timer=MARDCORE_WEAPON_DURATION
                    self.weapon_cooldown=0.0
                    self.add_action('WEAPON POWER-UP: '+pu.kind+' 60.00s',300)
                    play_sfx("weapon_pickup")
                else:
                    p.give_powerup(pu.kind)
                    self.add_action('POWER-UP: '+pu.kind,250)
                    play_sfx("powerup")
                self.burst(pu.x,pu.y,pu.color(),22,340)
        self.powerups=[x for x in self.powerups if not x.taken and x.y<self.player.y+1000]

    def sandbox_clear_button_rect(self):
        t=self.elapsed
        pulse=.5+.5*math.sin(t*7.2)
        w=190+int(math.sin(t*5.8)*8)
        h=30+int(pulse*4)
        x=WIDTH-w-34+math.sin(t*3.4)*4
        y=10+math.sin(t*5.1)*4
        return pygame.Rect(int(x),int(y),int(w),int(h))

    def clear_sandbox_world(self):
        if not self.sandbox_mode:
            return
        self.entities.clear()
        self.orbs.clear()
        self.powerups.clear()
        self.platforms.clear()
        self.sandbox_active_platform=None
        self.bullets.clear()
        self.particles.clear()
        self.blood.clear()
        self.shockwaves.clear()
        self.weapon_active_timer=0.0
        self.weapon_cooldown=0.0
        self.weapon_flash=0.0
        self.monster_spawned=False
        self.impact_timer=0.0
        self.impact_entity=None
        try:
            desktop_entities.clear()
        except Exception:
            pass
        self.sandbox_clear_button_flash=.62
        self.action_feed.clear()
        self.add_action("SANDBOX ERASED",0)
        play_sfx("parry_hit",.72)

    def handle_sandbox_clear_button(self):
        if not self.sandbox_mode:
            return
        p=self.player
        button=self.sandbox_clear_button_rect()
        player_rect=pygame.Rect(
            int(p.x-p.w*.5),
            int(p.y-p.h*.5),
            int(p.w),
            int(p.h)
        )
        touching=player_rect.colliderect(button)
        if touching and not self.sandbox_clear_button_pressed:
            self.clear_sandbox_world()
            p.vy=520
            p.on_ground=False
            self.shake=max(self.shake,10.0)
            self.shockwave(button.centerx,button.bottom,RED,16,620,.34,5,.55)
        self.sandbox_clear_button_pressed=touching

    def draw_sandbox_clear_button(self):
        if not self.sandbox_mode:
            return
        t=self.elapsed
        r=self.sandbox_clear_button_rect()
        pulse=.5+.5*math.sin(t*8.5)
        flash=clamp(self.sandbox_clear_button_flash/.62,0.0,1.0)
        press=5 if self.sandbox_clear_button_pressed else 0
        body_y=r.y+press
        body_h=max(10,r.h-press)
        body=pygame.Rect(r.x,body_y,r.w,body_h)
        ceiling_wave=[]
        for i in range(31):
            f=i/30
            xx=r.left-12+f*(r.w+24)
            yy=4+math.sin(t*7.0+f*math.tau*3.0)*2.5
            ceiling_wave.append((xx,yy))
        pygame.draw.lines(screen,WHITE,False,ceiling_wave,2)
        for side in (-1,1):
            sx=r.centerx+side*r.w*.34
            sway=math.sin(t*6.3+side)*3
            pygame.draw.line(screen,LIGHT,(sx+sway,5),(sx-sway,r.top+press),3)
        shell=[]
        for i in range(25):
            f=i/24
            xx=body.left+f*body.w
            yy=body.top+math.sin(t*10.0+f*math.tau*2.0)*2.0
            shell.append((xx,yy))
        for i in range(24,-1,-1):
            f=i/24
            xx=body.left+f*body.w
            yy=body.bottom+math.sin(t*10.0+f*math.tau*2.0+math.pi)*2.0
            shell.append((xx,yy))
        glow=self.reusable_layer("fx")
        glow_alpha=int(38+82*pulse+115*flash)
        glow_r=10+int(8*pulse)
        pygame.draw.rect(glow,(255,35,55,glow_alpha),(r.x-glow_r,r.y-glow_r,r.w+glow_r*2,r.h+glow_r*2),3,border_radius=12)
        screen.blit(glow,(0,0))
        fill_r=int(42+28*pulse)
        pygame.draw.polygon(screen,(fill_r,7,12),shell)
        border_mix=.5+.5*math.sin(t*6.8)
        border_color=(255,int(75+180*border_mix),int(88+167*border_mix))
        pygame.draw.lines(screen,border_color,True,shell,3)
        inner_y=body.centery+math.sin(t*11.5)*1.8
        pygame.draw.line(screen,RED,(body.left+14,inner_y),(body.right-14,inner_y),3)
        cap_h=9+int(3*pulse)
        cap=pygame.Rect(body.x+10,body.bottom-cap_h,body.w-20,cap_h)
        pygame.draw.rect(screen,(255,48,66),cap,border_radius=4)
        label_y=body.bottom+12+math.sin(t*5.4)*2
        label_color=WHITE if math.sin(t*6.8)>0 else RED
        draw_text("TOUCH TO ERASE ALL",font_small,label_color,r.centerx,label_y,center=True)

    def handle_entity_collisions(self):
        p=self.player
        for e in self.entities:
            if e.dead:continue
            dx=e.x-p.x;dy=e.y-p.y;dist=math.hypot(dx,dy)
            pretty=ENTITY_NAMES[e.kind]

            if p.parry_timer>0 and dist<=PARRY_RADIUS+e.radius:
                self.trigger_impact(e)
                play_sfx("parry_hit",1.0)
                dash_parry = p.dash_move_timer > 0
                if e.kind in ('monster','monster5d'):
                    e.parry_hits += 1
                    push = sign(e.x-p.x) or 1
                    special_mult = 1.25 if e.kind == 'monster5d' else 1.0
                    special_color = BLACK if e.kind == 'monster5d' else RED
                    if dash_parry:
                        self.add_action('GET THAT YOU PIECE OF SHIT!',1100 if e.kind == 'monster5d' else 900)
                        e.vx += push * 3920 * special_mult
                        e.vy -= 600 * special_mult
                        p.vx -= push * 880
                        p.vy=-2850 if e.kind == 'monster5d' else -2700
                        p.parry_safe_timer = .46 if e.kind == 'monster5d' else .42
                        self.burst(e.x,e.y,special_color,32,620)
                        self.blood_burst(e.x,e.y,44,True)
                        self.shockwave(e.x,e.y,WHITE,24,760,.30,6,1.0)
                        self.shake=20 if e.kind == 'monster5d' else 18
                    else:
                        pts = 520 + min(480, e.parry_hits * 30) if e.kind == 'monster5d' else 420 + min(380, e.parry_hits * 25)
                        self.add_action(f'PARRY: {pretty} x{e.parry_hits}', pts)
                        e.vx += push * 980 * special_mult
                        e.vy -= 150 * special_mult
                        p.vx -= push * 560 if e.kind == 'monster5d' else push * 520
                        p.vy=-2050 if e.kind == 'monster5d' else -1900
                        p.parry_safe_timer = .32 if e.kind == 'monster5d' else .28
                        self.burst(e.x,e.y,special_color,28 if e.kind == 'monster5d' else 26,460 if e.kind == 'monster5d' else 430)
                        self.blood_burst(e.x,e.y,38 if e.kind == 'monster5d' else 34,True)
                        self.shake=14 if e.kind == 'monster5d' else 12
                else:
                    e.dead=True
                    if dash_parry:
                        self.add_action('GET THAT YOU PIECE OF SHIT!',520)
                        p.vy=-2550
                        p.vx=-p.dash_direction*260
                        self.burst(e.x,e.y,WHITE,24,520)
                        self.blood_burst(e.x,e.y,24,False)
                        self.shockwave(e.x,e.y,CYAN,18,620,.26,5,.9)
                        self.shake=11
                    else:
                        self.add_action('PARRY: '+pretty,180)
                        self.burst(e.x,e.y,CYAN,14,320)
                        self.blood_burst(e.x,e.y,18,False)
                        p.vy=-1900
                        self.shake=7
                p.parry_timer = 0
                p.dash_move_timer = 0
                continue

            hit_dist=e.radius+max(p.w,p.h)*.42
            if dist<hit_dist:
                if p.dash_move_timer > 0:
                    continue
                if e.kind in ('monster','monster5d'):
                    if p.parry_safe_timer > 0:
                        push = sign(e.x-p.x) or 1
                        e.vx += push * 760
                        p.vx -= push * 360
                        continue
                    if not self.cheat_god:
                        self.entity_damage_style_penalty(e)
                        p.health=0
                        self.dead=True
                        start_death_tone()
                        start_death_music_pitch(self.game_mode)
                        self.add_action(pretty+' INSTAKILL',0)
                        self.burst(p.x,p.y,RED,30,460)
                        self.blood_burst(p.x,p.y,42,True)
                        self.shake=18
                        self.vfx_flash=max(self.vfx_flash,.14)
                        play_sfx("hit")
                    else:
                        self.add_action('GOD BLOCK: '+pretty,0)
                        self.burst(p.x,p.y,WHITE,14,260)
                    continue
                if p.angel>0:
                    e.dead=True
                    self.add_action('ANGEL SMITE: '+pretty,220)
                    self.burst(e.x,e.y,YELLOW,18,360)
                    self.blood_burst(e.x,e.y,18,False)
                    self.shake=5
                    continue
                if p.shield>0 and p.shield_hits>0:
                    p.shield_hits=0;p.shield=0
                    e.dead=True
                    self.add_action('SHIELD BLOCK: '+pretty,160)
                    self.burst(p.x,p.y,BLUE,22,340);self.blood_burst(e.x,e.y,14,False);self.shake=8
                    play_sfx("shield")
                    continue
                if not self.cheat_god:
                    if p.hit_invuln<=0:
                        self.entity_damage_style_penalty(e)
                        p.health=max(0,p.health-1)
                        p.hit_invuln=.82
                        push=-1 if e.x>p.x else 1
                        p.vx=push*720
                        p.vy=-520
                        self.add_action('HIT BY '+pretty,0)
                        self.burst(p.x,p.y,RED,22,360)
                        self.blood_burst(p.x,p.y,22 if p.health>0 else 34,p.health<=0)
                        self.shake=11 if p.health>0 else 15
                        play_sfx("hit")
                        if p.health<=0:
                            self.dead=True
                            start_death_tone()
                            start_death_music_pitch(self.game_mode)
                    continue
                else:
                    self.add_action('GOD BLOCK: '+pretty,0)
                    self.burst(p.x,p.y,WHITE,10,220)
        for e in self.entities:
            if e.kind in ('monster','monster5d'):
                e.dead = False
        self.entities=[e for e in self.entities if not e.dead]

    def trigger_impact(self, entity):
        self.impact_timer = self.impact_duration
        self.impact_entity = entity

    def update(self,dt):
        if self.dead:return
        if self.impact_timer > 0:
            self.impact_timer = max(0.0, self.impact_timer - dt)
            return
        self.elapsed+=dt
        if not self.sandbox_mode:
            self.update_style_decay(dt)
        current_rank = rank_for_score(self.style_score,self.game_mode)
        if current_rank != self.last_rank:
            old_index = RANK_ORDER.index(self.last_rank)
            new_index = RANK_ORDER.index(current_rank)
            if new_index > old_index:
                self.rank_pop_timer = self.rank_pop_duration
            self.last_rank = current_rank
        self.rank_pop_timer = max(0.0, self.rank_pop_timer - dt)
        self.audio_notice_time=max(0,self.audio_notice_time-dt)
        self.ui_shake_timer=max(0.0,self.ui_shake_timer-dt)
        self.ui_shake_strength=sine_tween(self.ui_shake_strength,1.0 if self.ui_shake_timer>0 else 0.0,14.0,dt)
        mouse_left=pygame.mouse.get_pressed(3)[0]
        keys=touch_controller.keys(pygame.key.get_pressed())
        self.weapon_cooldown=max(0.0,self.weapon_cooldown-dt)
        self.weapon_flash=max(0.0,self.weapon_flash-dt)
        if self.hardcore_mode or self.sandbox_mode:
            previous_weapon_time=self.weapon_active_timer
            self.weapon_active_timer=max(0.0,self.weapon_active_timer-dt)
            if previous_weapon_time>0 and self.weapon_active_timer<=0:
                self.bullets.clear()
                self.add_action("WEAPON POWER-UP EXPIRED",0)
        before=self.player.last_action
        if self.cheat_noclip:
            p=self.player
            p.prev_y=p.y
            speed=980.0
            dx=(1 if keys[pygame.K_RIGHT] or keys[pygame.K_d] else 0)-(1 if keys[pygame.K_LEFT] or keys[pygame.K_a] else 0)
            dy=(1 if keys[pygame.K_DOWN] or keys[pygame.K_s] else 0)-(1 if keys[pygame.K_UP] or keys[pygame.K_w] else 0)
            if p.dash_move_timer > 0:
                p.vx=p.dash_direction*DASH_SPEED
                p.vy*=.72
            else:
                p.vx=dx*speed
                p.vy=dy*speed
            p.x=clamp(p.x+p.vx*dt,24,WIDTH-24)
            p.y+=p.vy*dt
            p.on_ground=False
            p.coyote=0
            p.walk_amount=sine_tween(p.walk_amount,0.0,10.0,dt)
            p.lean_tween=sine_tween(p.lean_tween,dx,10.0,dt)
            p.dash_cd=max(0.0,p.dash_cd-dt)
            p.dash_move_timer=max(0.0,p.dash_move_timer-dt)
            p.parry_cd=max(0.0,p.parry_cd-dt)
            p.parry_timer=max(0.0,p.parry_timer-dt)
            p.anim_flash=max(0.0,p.anim_flash-dt)
            p.dash_anim=max(0.0,p.dash_anim-dt)
            p.anim_spin*=max(0.0,1.0-dt*4.0)
        else:
            armed_mouse=self.hardcore_mode or (self.sandbox_mode and self.weapon_active_timer>0)
            self.player.update(dt,keys,mouse_left and not armed_mouse)
        if (self.hardcore_mode or self.sandbox_mode) and self.weapon_active_timer>0 and mouse_left:
            self.fire_weapon()
        self.update_bullets(dt)
        after=self.player.last_action
        if after!=before:
            pts={'JUMP':12,'DOUBLE JUMP':28,'INFINITE JUMP':18}.get(after)
            if pts is not None:self.add_action(after,pts)
            self.action_vfx(after)

        if not self.cheat_noclip:
            self.handle_platform_collision()
        self.walk_sfx_timer = max(0.0, self.walk_sfx_timer - dt)
        if self.player.on_ground and abs(self.player.vx) > 95 and self.walk_sfx_timer <= 0.0:
            speed_factor = clamp(abs(self.player.vx) / MAX_X_SPEED, 0.0, 1.0)
            play_sfx("step", .38 + speed_factor * .32)
            self.walk_sfx_timer = .23 - speed_factor * .08
        self.handle_orbs()
        self.handle_powerups()
        self.handle_sandbox_clear_button()
        self.sandbox_clear_button_flash=max(0.0,self.sandbox_clear_button_flash-dt)
        if self.sandbox_mode:
            self.camera_y = 0.0
            self.score = 0
            half_w = self.player.w * .5
            half_h = self.player.h * .5
            if self.player.x - half_w < 10:
                self.player.x = 10 + half_w
                if self.player.dash_move_timer > 0 and self.player.dash_direction < 0:
                    self.player.wall_dash_lock = -1
                    self.player.dash_move_timer = 0.0
                    self.player.dash_cd = max(self.player.dash_cd,.42)
                    self.player.vx = 0.0
                else:
                    self.player.vx = max(0.0, self.player.vx) * .35
            elif self.player.x + half_w > WIDTH - 10:
                self.player.x = WIDTH - 10 - half_w
                if self.player.dash_move_timer > 0 and self.player.dash_direction > 0:
                    self.player.wall_dash_lock = 1
                    self.player.dash_move_timer = 0.0
                    self.player.dash_cd = max(self.player.dash_cd,.42)
                    self.player.vx = 0.0
                else:
                    self.player.vx = min(0.0, self.player.vx) * .35
            if self.player.y - half_h < 10:
                self.player.y = 10 + half_h
                self.player.vy = max(0.0, self.player.vy) * .25
                self.player.on_ground = False
            elif self.player.y + half_h > HEIGHT - 10:
                self.player.y = HEIGHT - 10 - half_h
                if self.player.vy >= 0:
                    self.player.vy = 0.0
                    self.player.on_ground = True
                    self.player.coyote = COYOTE_TIME
                    self.player.jumps_used = 0
                else:
                    self.player.on_ground = False
        else:
            target_cam=self.player.y-HEIGHT*.64
            self.camera_y=lerp(self.camera_y,target_cam,clamp(dt*7.5,0,1))
            self.score=max(self.score,int((self.start_y-self.player.y)/8))
            if not self.progress_locked:
                self.best=max(self.best,self.score)
                self.best_style=max(self.best_style,int(self.style_score))
            self.generate_until(self.player.y-1800)
            self.platforms=[p for p in self.platforms if p.y<self.player.y+1100]

        if self.sandbox_mode:
            rank_difficulty = 1.0
        else:
            rank_now = rank_for_score(self.style_score,self.game_mode)
            rank_index = RANK_ORDER.index(rank_now)
            rank_progress = rank_index / max(1, len(RANK_ORDER) - 1)
            self.entity_timer+=dt
            if self.hardcore_mode:
                rank_difficulty = 3.25 + rank_progress * 1.10
                spawn_interval=max(.24,.38-rank_progress*.12)
                max_entities=12
                if self.entity_timer>=spawn_interval and len([e for e in self.entities if e.kind not in ('monster','monster5d')])<max_entities:
                    self.entity_timer=0
                    self.spawn_entity()
                if self.elapsed>=HARDCORE_5D_APPEAR_TIME and not self.monster_spawned:
                    self.spawn_bob()
            else:
                rank_difficulty = 1.08 + rank_progress * 0.98
                base_spawn_interval=max(.70,1.95-self.score/3800)
                spawn_interval=max(.50, base_spawn_interval * (1.0 - rank_progress * .29))
                base_max_entities=min(7,2+self.score//900)
                max_entities=min(9, base_max_entities + int(rank_progress * 2))
                if self.entity_timer>=spawn_interval and len(self.entities)<max_entities:
                    self.entity_timer=0
                    self.spawn_entity()
                if self.elapsed>=BOB_APPEAR_TIME and not self.monster_spawned:
                    self.spawn_bob()
        for e in self.entities:e.update(dt,self.player,self.elapsed,rank_difficulty)
        self.handle_entity_collisions()
        for pt in self.particles:pt.update(dt,self.elapsed)
        self.particles=[pt for pt in self.particles if pt.life>0]
        for sw in self.shockwaves:sw.update(dt)
        self.shockwaves=[sw for sw in self.shockwaves if sw.life>0]
        self.vfx_flash=max(0.0,self.vfx_flash-dt)
        for b in self.blood:b.update(dt,self.elapsed)
        self.blood=[b for b in self.blood if b.life>0]
        particle_cap=[260,220,180,140,90,55][GRAPHICS_QUALITY]
        blood_cap=[190,160,130,100,70,45][GRAPHICS_QUALITY]
        shock_cap=[28,24,20,16,12,8][GRAPHICS_QUALITY]
        if PORTABLE_FAST_MODE:
            particle_cap=min(particle_cap,82)
            blood_cap=min(blood_cap,58)
            shock_cap=min(shock_cap,10)
        if self.hardcore_mode:
            particle_cap=int(particle_cap*.82)
            blood_cap=int(blood_cap*.82)
            shock_cap=int(shock_cap*.82)
        if len(self.particles)>particle_cap:
            self.particles=self.particles[-particle_cap:]
        if len(self.blood)>blood_cap:
            self.blood=self.blood[-blood_cap:]
        if len(self.shockwaves)>shock_cap:
            self.shockwaves=self.shockwaves[-shock_cap:]
        for item in self.action_feed:item[2]-=dt
        self.action_feed=[x for x in self.action_feed if x[2]>0]
        self.shake=max(0,self.shake-28*dt)
        if self.player.y-self.camera_y>HEIGHT+160:
            if self.cheat_god or self.cheat_noclip:
                self.player.y=self.camera_y+HEIGHT*.48
                self.player.vy=0
            else:
                self.dead=True
                start_death_tone()
                start_death_music_pitch(self.game_mode)
                self.add_action('FALL',0)

    def draw_sandbox_desktop_background(self):
        t = self.elapsed
        screen.fill((7,9,15))

        glow=self.reusable_layer("fx")
        cx = WIDTH*.5 + math.sin(t*.55)*WIDTH*.12
        cy = HEIGHT*.42 + math.cos(t*.7)*HEIGHT*.08
        for i in range(max(1,int(7*graphics_bg_factor())),0,-1):
            r = int(min(WIDTH,HEIGHT) * (.08 + i*.055))
            alpha = max(3, 16-i)
            pygame.draw.circle(glow,(38,126,255,alpha),(int(cx),int(cy)),r)
        screen.blit(glow,(0,0))

        horizon = int(HEIGHT*.64 + math.sin(t*.8)*5)
        pygame.draw.line(screen,(34,58,92),(0,horizon),(WIDTH,horizon),1)

        for i in range(max(5,int(18*graphics_bg_factor()))):
            bg_lines=max(5,int(18*graphics_bg_factor()))
            f = i/max(1,bg_lines-1)
            x = int(f*WIDTH)
            pull = (f-.5)*WIDTH*.72
            top_x = WIDTH*.5 + pull*.18
            pygame.draw.line(screen,(20,35,57),(x,HEIGHT),(int(top_x),horizon),1)

        for j in range(1,max(4,int(13*graphics_bg_factor()))):
            bg_depth=max(4,int(13*graphics_bg_factor()))
            depth = j/max(1,bg_depth-1)
            yy = horizon + (depth**1.75)*(HEIGHT-horizon)
            pygame.draw.line(screen,(20,35,57),(0,int(yy)),(WIDTH,int(yy)),1)

        for i in range(max(6,int(36*graphics_bg_factor()))):
            phase = i*1.913
            x = (i*157 + math.sin(t*.4+phase)*42) % (WIDTH+80)-40
            y = (i*103 + math.cos(t*.5+phase)*30) % (HEIGHT+80)-40
            size = 1 + i%3
            pulse = .5+.5*math.sin(t*2.4+phase)
            c = int(55+65*pulse)
            pygame.draw.circle(screen,(c,c+22,min(210,c+70)),(int(x),int(y)),size)

        for i in range(max(1,int(5*graphics_bg_factor()))):
            a = t*(.18+i*.035)+i*1.17
            r = 95+i*44
            px = WIDTH*.5 + math.cos(a)*r*1.7
            py = HEIGHT*.35 + math.sin(a*1.3)*r*.55
            s = 22+i*7
            pts=[]
            for k in range(4):
                aa = a*.7 + math.pi/4 + k*math.pi/2
                pts.append((px+math.cos(aa)*s,py+math.sin(aa)*s))
            pygame.draw.polygon(screen,(28,50,84),pts,2)

        stamp_scale=1.0+math.sin(t*1.8)*.018
        draw_cursive_text("CUBED // SANDBOX",font_mid,(52,70,96),WIDTH//2,42,True,stamp_scale)
        draw_cursive_text("i dont fucking know what to put here",font_small,(42,58,78),WIDTH//2,72,True,1.0)

    def draw_background(self):
        if self.sandbox_mode:
            self.draw_sandbox_desktop_background()
            return
        t = self.elapsed
        cam = self.camera_y
        speed = clamp(abs(self.player.vx) / max(1.0, MAX_X_SPEED), 0.0, 1.0)
        bg_factor=graphics_bg_factor()*(.62 if self.hardcore_mode else .78)
        if self.hardcore_mode:
            pulse = .5 + .5*math.sin(t*2.7)
            screen.fill((18+int(8*pulse),2,5))
            atmosphere=self.reusable_layer("fx")
            cx = WIDTH*.5 + math.sin(t*.63)*WIDTH*.17
            cy = HEIGHT*.38 + math.sin(t*.91+1.3)*HEIGHT*.07
            for ring in range(max(1,int(6*bg_factor)),0,-1):
                radius = int(min(WIDTH,HEIGHT)*(.09+ring*.065))
                alpha = max(4,23-ring*2)
                pygame.draw.circle(atmosphere,(255,18,38,alpha),(int(cx),int(cy)),radius)
            screen.blit(atmosphere,(0,0))
        else:
            screen.fill(BG)

        for i in range(max(7,int(44*bg_factor))):
            phase = i * 1.731
            depth = 0.25 + (i % 7) * 0.105
            x = (i * 193.0 + math.sin(t * (0.35 + depth) + phase) * (18 + 32 * depth)) % (WIDTH + 120) - 60
            y = (i * 137.0 - cam * depth * .10 + math.sin(t * (0.55 + depth) + phase * .7) * 22) % (HEIGHT + 100) - 50
            r = 1 + (i % 3)
            pulse = (math.sin(t * 2.0 + phase) + 1.0) * .5
            c = int(30 + 40 * depth + 24 * pulse)
            dot_color = (min(210,c+85),max(8,int(c*.20)),max(12,int(c*.25))) if self.hardcore_mode else (c,c+8,min(120,c+24))
            pygame.draw.circle(screen,dot_color,(int(x),int(y)),r)

        horizon = int(HEIGHT * .67 + math.sin(t * .9) * 7)

        for layer in range(max(1,int(3*bg_factor))):
            base = horizon + layer * 45
            pts = []
            amp = 18 + layer * 11
            freq = .010 + layer * .003
            drift = t * (1.2 + layer * .28)
            parallax = cam * (.025 + layer * .018)
            for x in range(-40, WIDTH + 60, 18):
                y = base + math.sin(x * freq + drift + layer * 1.7) * amp
                y += math.sin(x * freq * 2.3 - t * 1.7 + layer) * amp * .28
                y += parallax % 42
                pts.append((x, y))
            col = (46+layer*15,5+layer*3,9+layer*5) if self.hardcore_mode else (16+layer*5,22+layer*7,38+layer*11)
            pygame.draw.lines(screen,col,False,pts,2)

        grid_top = horizon + 20
        grid_bottom = HEIGHT + 45
        center_x = WIDTH * .5 + math.sin(t * .7) * 14
        grid_color = (78,8,15) if self.hardcore_mode else (18,28,48)
        for i in range(-12, 13):
            spread = i / 12.0
            x_bottom = center_x + spread * WIDTH * .82
            x_top = center_x + spread * WIDTH * .10
            wobble = math.sin(t * 1.8 + i * .45) * (2 + speed * 4)
            pygame.draw.line(screen,grid_color,(x_top+wobble,grid_top),(x_bottom,grid_bottom),1)

        for j in range(13):
            f = j / 12.0
            eased = f * f
            y = grid_top + eased * (grid_bottom - grid_top)
            y += math.sin(t * 2.2 + j * .8) * (1.2 + speed * 2.0)
            pygame.draw.line(screen,grid_color,(0,int(y)),(WIDTH,int(y)),1)

        band_color = (62,7,13) if self.hardcore_mode else DARK2
        for band in range(4 if not self.hardcore_mode else 3):
            y0 = 70 + band * 88 + math.sin(t * .8 + band) * 10
            pts = []
            for x in range(-20, WIDTH + 40, 18):
                y = y0 + math.sin(t * (1.4 + band * .09) + x * .019 + band) * (7 + band * 1.5)
                y += math.sin(t * 3.0 - x * .007 + band * 2.0) * 3
                pts.append((x, y))
            pygame.draw.lines(screen,band_color,False,pts,1)

        if self.hardcore_mode and GRAPHICS_QUALITY < 5:
            danger=self.reusable_layer("fx")
            danger_alpha = int(8+10*(.5+.5*math.sin(t*3.4)))
            danger.fill((255,0,28,danger_alpha))
            screen.blit(danger,(0,0))

        screen.blit(self.vignette_layer(),(0,0))

    def draw_power_status(self):
        p=self.player;t=self.elapsed
        active=[]
        if p.infinite_jumps>0:active.append(('∞ JUMPS',p.infinite_jumps,CYAN))
        if p.shield>0 and p.shield_hits>0:active.append(('SHIELD',p.shield,BLUE))
        if p.angel>0:active.append(('ANGEL',p.angel,YELLOW))
        if p.flight>0:active.append(('FLIGHT',p.flight,PINK))
        x=24;y=190
        for name,time_left,c in active:
            yy=y+math.sin(t*5+len(name)) * 2
            pygame.draw.rect(screen,DARK,pygame.Rect(x,yy,170,26),0,border_radius=5)
            pygame.draw.rect(screen,c,pygame.Rect(x,yy,170,26),2,border_radius=5)
            draw_text(f'{name}  {time_left:0.1f}s',font_small,c,x+8,yy+4)
            y+=31


    def draw_health_bar(self):
        t=self.elapsed
        p=self.player
        pulse=.5+.5*math.sin(t*5.2)
        x=28+math.sin(t*2.7)*4
        if self.sandbox_mode:
            y=HEIGHT-64+math.sin(t*3.4+1.2)*4
        else:
            y=HEIGHT-112+math.sin(t*3.4+1.2)*4
        w=250
        h=28
        scale=1.0+math.sin(t*3.1)*.018
        tilt=math.sin(t*2.45)*1.25
        bg=pygame.Surface((w+18,h+40),pygame.SRCALPHA)
        pygame.draw.rect(bg,(5,7,12,225),(3,25,w+12,h+10),border_radius=8)
        pygame.draw.rect(bg,(245,247,252,220),(3,25,w+12,h+10),2,border_radius=8)
        ratio=clamp(p.health/max(1,p.max_health),0.0,1.0)
        fill=max(0,int(w*ratio))
        if fill>0:
            pulse_fill=max(0,min(w,int(fill+math.sin(t*7.2)*2)))
            pygame.draw.rect(bg,(255,75,92,235),(9,31,pulse_fill,h-2),border_radius=5)
            shine=max(1,int(pulse_fill*.72))
            pygame.draw.rect(bg,(255,145,155,100),(9,31,shine,5),border_radius=3)
        for i in range(1,p.max_health):
            xx=9+int(w*i/p.max_health)
            pygame.draw.line(bg,(8,10,16,210),(xx,32),(xx,56),3)
        if GRAPHICS_QUALITY <= 1:
            bg=pygame.transform.rotozoom(bg,tilt,scale)
            screen.blit(bg,bg.get_rect(center=(int(x+w*.5+3),int(y+20))))
        else:
            screen.blit(bg,(int(x-6),int(y-5)))
        label_y=y-25+math.sin(t*4.3)*2.2
        label_x=x+math.sin(t*3.8)*2
        draw_text(PLAYER_NAME,font_small,LIGHT,label_x,label_y)
        draw_text(f'{p.health} / {p.max_health}',font_small,WHITE,x+w-48+math.sin(t*4.6+1.4)*2,label_y)
        for i in range(p.max_health):
            cx=x+13+i*25+math.sin(t*4.1+i*.7)*1.8
            cy=y+14+math.sin(t*5+i*.8)*2.4
            active=i<p.health
            c=RED if active else DARK2
            rr=7+int((.5+.5*math.sin(t*6+i))*1.5)
            pygame.draw.circle(screen,c,(int(cx),int(cy)),rr)
            pygame.draw.circle(screen,WHITE if active else LIGHT,(int(cx),int(cy)),rr,1)
        if p.health==1:
            warning=pygame.Surface((w+12,h+10),pygame.SRCALPHA)
            pygame.draw.rect(warning,(255,75,92,int(35+55*pulse)),(0,0,w+12,h+10),3,border_radius=8)
            warning=pygame.transform.rotozoom(warning,math.sin(t*5.5)*.8,1.0+math.sin(t*7)*.02)
            screen.blit(warning,warning.get_rect(center=(int(x+w*.5),int(y+19))))

    def draw_hud(self):
        t=self.elapsed
        ui_wave = .5 + .5*math.sin(t*3.2)
        ui_slide = 6*math.sin(t*2.1)
        if self.sandbox_mode:
            draw_text('SANDBOX MODE',font_mid,YELLOW,28+math.sin(t*4)*3+ui_slide*.25,26+ui_wave*2)
            draw_text('TOUCH SPAWNER BUTTON = EDITOR' if PORTABLE_TOUCH else 'TAB = SANDBOX SPAWNER',font_small,LIGHT,28,66)
            draw_text(f'ENTITIES: {len(self.entities)}',font_small,WHITE,28,92)
            draw_text('RANK IS SESSION ONLY',font_small,RED,28,118)
        rank=rank_for_score(self.style_score,self.game_mode)
        saved_rank=rank_for_score(self.best_style,self.game_mode)
        if self.hardcore_mode:
            draw_text('MARDCORE MODE • 1 LIFE • VAS A ESTAR 5 MTS BAJO TIERRA YURI',font_small,RED,WIDTH/2,24+math.sin(t*4.2)*3,center=True)
        rank_color=RANK_COLORS[rank]
        sway=math.sin(t*3.6)*5;bob=math.sin(t*5+1)*4

                                         
        x1,y1,w1,h1=24+sway+ui_slide*.2,24+bob+ui_wave*2,230,70
        pulse1=1.0+math.sin(t*3.6)*.018
        tilt1=math.sin(t*2.2)*1.2
        panel1=pygame.Surface((w1+18,h1+18),pygame.SRCALPHA)
        pts1=[(18,9),(w1+9,9),(w1-13,h1+9),(9,h1+9)]
        pygame.draw.polygon(panel1,DARK,pts1);pygame.draw.polygon(panel1,CYAN,pts1,3)
        if GRAPHICS_QUALITY <= 1:
            panel1=pygame.transform.rotozoom(panel1,tilt1,pulse1)
            screen.blit(panel1,panel1.get_rect(center=(int(x1+w1*.5),int(y1+h1*.5))))
        else:
            screen.blit(panel1,(int(x1-9),int(y1-9)))
        draw_text('HEIGHT',font_small,LIGHT,x1+24+math.sin(t*4.4)*2,y1+10+math.sin(t*3.5)*2)
        draw_text(str(self.score),font_mid,WHITE,x1+24+math.sin(t*4.9+1)*3,y1+31+math.sin(t*5.1)*2)

        x2,y2,w2,h2=24-sway*.7-ui_slide*.15,102-bob*.6-ui_wave*2,230,70
        pulse2=1.0+math.sin(t*3.1+1.7)*.018
        tilt2=math.sin(t*2.0+1.4)*-1.2
        panel2=pygame.Surface((w2+18,h2+18),pygame.SRCALPHA)
        pts2=[(9,9),(w2-11,9),(w2+9,h2+9),(31,h2+9)]
        pygame.draw.polygon(panel2,DARK,pts2);pygame.draw.polygon(panel2,PURPLE,pts2,3)
        if GRAPHICS_QUALITY <= 1:
            panel2=pygame.transform.rotozoom(panel2,tilt2,pulse2)
            screen.blit(panel2,panel2.get_rect(center=(int(x2+w2*.5),int(y2+h2*.5))))
        else:
            screen.blit(panel2,(int(x2-9),int(y2-9)))
        draw_text('RECORD',font_small,LIGHT,x2+24+math.sin(t*4.0+1)*2,y2+10+math.sin(t*3.1+1.2)*2)
        draw_text(str(self.best),font_mid,WHITE,x2+24+math.sin(t*4.6+2)*3,y2+31+math.sin(t*5.0+1.3)*2)
        self.draw_health_bar()
        self.draw_power_status()

        rank_index = RANK_ORDER.index(rank)
        card_w = min(350, int(WIDTH*.34))
        card_h = 154
        card_x = WIDTH-card_w-24+math.sin(t*2.25)*2.5
        card_y = 20+math.sin(t*2.85+1.1)*2.0
        card_pulse = 1.0+math.sin(t*3.6+rank_index*.4)*.008
        card_tilt = math.sin(t*2.0+rank_index*.3)*.32

        rank_panel = pygame.Surface((card_w+24,card_h+24),pygame.SRCALPHA)
        panel_alpha = 208
        panel_pts = [(18,8),(card_w+14,8),(card_w+6,card_h+16),(8,card_h+16)]
        pygame.draw.polygon(rank_panel,(*DARK,panel_alpha),panel_pts)
        pygame.draw.polygon(rank_panel,(*rank_color,235),panel_pts,3)
        inner_pts = [(25,17),(card_w+5,17),(card_w-1,card_h+7),(17,card_h+7)]
        pygame.draw.polygon(rank_panel,(*DARKER,150),inner_pts,1)

        sweep_x = int((math.sin(t*2.4)*.5+.5)*(card_w-70))+35
        pygame.draw.line(rank_panel,(*rank_color,55),(sweep_x,18),(sweep_x-24,card_h+5),5)

        if GRAPHICS_QUALITY <= 1:
            rank_panel = pygame.transform.rotozoom(rank_panel,card_tilt,card_pulse)
            screen.blit(rank_panel,rank_panel.get_rect(center=(int(card_x+card_w*.5),int(card_y+card_h*.5))))
        else:
            screen.blit(rank_panel,(int(card_x-12),int(card_y-12)))

        badge_x = card_x+card_w-72+math.sin(t*4.2+rank_index)*3
        badge_y = card_y+48+math.sin(t*5.0+rank_index*.7)*2
        badge_r = 29+math.sin(t*4.4+rank_index)*2
        badge_layer=self.reusable_layer("fx")
        pygame.draw.circle(badge_layer,(*rank_color,26),(int(badge_x),int(badge_y)),int(badge_r+13),3)
        pygame.draw.circle(badge_layer,(*rank_color,62),(int(badge_x),int(badge_y)),int(badge_r+5),2)
        screen.blit(badge_layer,(0,0))

        pop_scale = 1.0
        if self.rank_pop_timer > 0.0:
            progress = 1.0 - self.rank_pop_timer / self.rank_pop_duration
            expo_out = 1.0 if progress >= 1.0 else 1.0 - math.pow(2.0, -10.0 * progress)
            pop_scale = .35 + expo_out*.65
            burst_r = int(28+expo_out*92)
            burst_alpha = int((1.0-progress)*190)
            rank_fx=self.reusable_layer("fx")
            for ring in range(3):
                rr=burst_r+ring*13+math.sin(t*10+ring)*4
                pygame.draw.circle(rank_fx,(*rank_color,max(0,burst_alpha-ring*45)),(int(badge_x),int(badge_y)),rr,max(1,5-ring))
            screen.blit(rank_fx,(0,0))

        title_x = card_x+28+math.sin(t*3.2)*1.5
        title_y = card_y+16+math.sin(t*3.8+.7)*1.2
        draw_text('STYLE RANK',font_small,LIGHT,title_x,title_y)

        rotation_amp = 1.2 + rank_index*.18
        rotation = math.sin(t*(4.0+rank_index*.12)+rank_index*.65)*rotation_amp
        rank_text_left = card_x+28
        rank_text_right = badge_x-badge_r-14
        rank_center_x = (rank_text_left+rank_text_right)*.5
        rank_center_y = card_y+58+math.sin(t*4.6+rank_index*.4)*2.5

        if rank == "CUBE":
            draw_rank_cube(badge_x,badge_y,t+math.sin(t*2.2)*.08,rank_color,pop_scale*.72)

        max_rank_width = max(110,int(rank_text_right-rank_text_left))
        procedural_height = (42 if len(rank) < 10 else 34 if len(rank) < 17 else 27) * pop_scale
        draw_sine_font(rank,rank_color,rank_center_x,rank_center_y,max_rank_width,procedural_height,True)

        rank_scores=rank_scores_for_mode(self.game_mode)
        current_threshold = rank_scores[rank]
        if rank_index < len(RANK_ORDER)-1:
            next_rank = RANK_ORDER[rank_index+1]
            next_threshold = rank_scores[next_rank]
            span = max(1,next_threshold-current_threshold)
            rank_progress = clamp((self.style_score-current_threshold)/span,0.0,1.0)
            next_text = f'NEXT  {next_rank}'
            remain = max(0,int(next_threshold-self.style_score))
        else:
            next_rank = 'MAX'
            rank_progress = 1.0
            next_text = 'MAX RANK'
            remain = 0

        info_y = card_y+88
        draw_text(f'STYLE {int(self.style_score)}',font_small,WHITE,title_x+math.sin(t*4.1)*1.2,info_y)
        best_label = 'SESSION ONLY' if self.sandbox_mode else f'BEST {saved_rank}'
        best_width = cursive_text_width(best_label,font_small)
        best_x = card_x+card_w-28-best_width+math.sin(t*3.4+1.2)*1.2
        draw_text(best_label,font_small,LIGHT,best_x,info_y)

        bar_x = int(card_x+28)
        bar_y = int(card_y+118)
        bar_w = max(120,int(card_w-56))
        bar_h = 10
        pygame.draw.rect(screen,DARK2,(bar_x,bar_y,bar_w,bar_h),border_radius=5)
        fill_w = int(bar_w*rank_progress)
        if fill_w > 0:
            pygame.draw.rect(screen,rank_color,(bar_x,bar_y,fill_w,bar_h),border_radius=5)
        marker_x = bar_x+fill_w
        marker_r = 3+int((math.sin(t*7.5)+1)*1.5)
        pygame.draw.circle(screen,WHITE,(int(marker_x),int(bar_y+bar_h*.5)),marker_r)

        next_y = card_y+134
        draw_text(next_text,font_small,rank_color,title_x+math.sin(t*3.7+.4)*1.0,next_y)
        if remain > 0:
            remain_label=f'{remain} TO GO'
            remain_width=cursive_text_width(remain_label,font_small)
            remain_x=card_x+card_w-28-remain_width+math.sin(t*3.1+2.0)*1.0
            draw_text(remain_label,font_small,LIGHT,remain_x,next_y)

        if self.sandbox_mode:
            draw_text('SANDBOX • NO PROGRESS',font_small,YELLOW,card_x+28+math.sin(t*4.4)*2,card_y+card_h+10)
        elif self.progress_locked:
            draw_text('CHEATED RUN • NO PROGRESS',font_small,RED,card_x+28+math.sin(t*4.4)*2,card_y+card_h+10)

                                                        
        feed_x=WIDTH-330;feed_y=196
        for i,(name,pts,life) in enumerate(self.action_feed):
            alpha_wave=math.sin(t*6+i*.8)*5
            bob_wave=math.sin(t*4.2+i*1.1)*2
            c=rank_color if i==0 else LIGHT
            prefix=f'+{pts}  ' if pts>0 else ''
            draw_text(prefix+name,font_small,c,feed_x+alpha_wave,feed_y+i*25+bob_wave)

                    
        warning_x=WIDTH-300+math.sin(t*3.8)*4
        warning_y=382+math.sin(t*4.6+1.2)*3
        special_time=HARDCORE_5D_APPEAR_TIME if self.hardcore_mode else BOB_APPEAR_TIME
        special_name='PENTARACT' if self.hardcore_mode else 'TESSERACT'
        special_color=WHITE if self.hardcore_mode else RED
        if not self.monster_spawned:
            rem=max(0,int(special_time-self.elapsed))
            draw_text(special_name+' APPEARS IN...',font_small,special_color,warning_x,warning_y)
            timer_scale=1.0+math.sin(t*5.5)*.05
            draw_cursive_text(f'{rem}s',font_mid,special_color,warning_x+32,warning_y+35,True,timer_scale)
        else:
            active_scale=1.0+math.sin(t*7.0)*.035
            draw_cursive_text(special_name+' ACTIVE',font_small,special_color,warning_x,warning_y,False,active_scale)

                            
        bar_y=HEIGHT-48+math.sin(t*5)*3
                                                          
        wave=[]
        for i in range(48):
            f=i/47
            xx=18+f*500
            yy=bar_y-8+math.sin(t*7+f*math.tau*3)*2.5
            wave.append((xx,yy))
        pygame.draw.lines(screen,DARK2,False,wave,2)
        if PORTABLE_TOUCH:
            draw_text('TOUCH CONTROLS ACTIVE',font_small,CYAN,24+math.sin(t*4.4)*2,bar_y)
        elif self.hardcore_mode or (self.sandbox_mode and self.weapon_active_timer>0):
            draw_text('SPACE = JUMP',font_small,WHITE,24+math.sin(t*4.4)*2,bar_y)
            draw_text('Q = DASH',font_small,CYAN,185+math.sin(t*4.7+1)*2,bar_y)
            draw_text('E = PARRY',font_small,GREEN,280+math.sin(t*5.0+2)*2,bar_y)
            draw_text('M1 = FIRE',font_small,ORANGE,385+math.sin(t*5.3+3)*2,bar_y)
        else:
            draw_text('SPACE / M1 = JUMP',font_small,WHITE,24+math.sin(t*4.4)*2,bar_y)
            draw_text('Q = DASH',font_small,CYAN,205+math.sin(t*4.7+1)*2,bar_y)
            draw_text('E = PARRY',font_small,GREEN,300+math.sin(t*5.0+2)*2,bar_y)
            draw_text('M = MUSIC',font_small,LIGHT,405+math.sin(t*5.3+3)*2,bar_y)

        self.draw_weapon_hud()
        if self.audio_notice_time>0:
            col=GREEN if self.music_name else RED
            draw_text('AUDIO: '+self.audio_status,font_small,col,WIDTH/2,18,center=True)

    def draw_impact_frame(self):
        screen.fill(WHITE)
        cam = self.camera_y
        p = self.player
        py = p.y - cam

        hw, hh = p.w*.55, p.h*.55
        ang = p.anim_spin
        ca, sa = math.cos(ang), math.sin(ang)
        pts=[]
        for px,py0 in [(-hw,-hh),(hw,-hh),(hw,hh),(-hw,hh)]:
            rx=px*ca-py0*sa
            ry=px*sa+py0*ca
            pts.append((p.x+rx,py+ry))
        pygame.draw.polygon(screen,(0,0,0),pts)

        e = self.impact_entity
        if e is None:
            return

        ey = e.y - cam
        t = self.elapsed
        pulse = 1.0 + math.sin(t * 8 + e.phase) * 0.12
        r = e.radius * pulse
        black = (0,0,0)

        if e.kind == "monster5d":
            verts=project_5d_cube(e.x,ey,r,t,e.phase)
            for a,b in HYPERCUBE5D_EDGES:
                pygame.draw.line(screen,black,verts[a],verts[b],4)
            pygame.draw.circle(screen,black,(int(e.x),int(ey)),11)
        elif e.kind == "monster":
            angle_a = t * 1.7 + math.sin(t * 1.2) * .35
            angle_b = t * 1.15 + math.sin(t * 2.1 + 1.4) * .28
            scale = r * .52
            verts = []
            for w in (-1, 1):
                for z in (-1, 1):
                    for y in (-1, 1):
                        for x in (-1, 1):
                            x1 = x * math.cos(angle_a) - z * math.sin(angle_a)
                            z1 = x * math.sin(angle_a) + z * math.cos(angle_a)
                            y1 = y * math.cos(angle_b) - w * math.sin(angle_b)
                            w1 = y * math.sin(angle_b) + w * math.cos(angle_b)
                            perspective4 = 1.0 / (2.8 - w1 * .45)
                            perspective3 = 1.0 / (2.4 - z1 * .32)
                            px = e.x + x1 * scale * perspective4 * perspective3 * 4.2
                            py2 = ey + y1 * scale * perspective4 * perspective3 * 4.2
                            verts.append((px, py2))
            for i in range(16):
                for bit in (1, 2, 4, 8):
                    j = i ^ bit
                    if i < j:
                        pygame.draw.line(screen, black, verts[i], verts[j], 4)
            pygame.draw.circle(screen, black, (int(e.x), int(ey)), 9)
            for i in range(4):
                a = t * (1.8 + i * .22) + i * math.pi / 2
                rr = r + 16 + math.sin(t * 5 + i) * 6
                pygame.draw.circle(screen, black, (int(e.x + math.cos(a) * rr), int(ey + math.sin(a * 1.3) * rr * .45)), 5)

        elif e.kind == "drone":
            pts2 = []
            for i in range(8):
                a = i * math.tau / 8 + t * 2.8
                rr = r if i % 2 == 0 else r * .42
                pts2.append((e.x + math.cos(a) * rr, ey + math.sin(a) * rr))
            pygame.draw.polygon(screen, black, pts2)
            pygame.draw.circle(screen, WHITE, (int(e.x), int(ey)), 5)

        elif e.kind == "wraith":
            pts2 = []
            for i in range(12):
                a = i * math.tau / 12
                rr = r * (1.0 + math.sin(t * 7 + e.phase + i * 1.4) * .28)
                pts2.append((e.x + math.cos(a) * rr, ey + math.sin(a) * rr))
            pygame.draw.polygon(screen, black, pts2)
            for i in range(3):
                off = math.sin(t * 6 + i * 2) * 5
                pygame.draw.line(screen, WHITE, (e.x-r*.6, ey+off+i*6-6), (e.x+r*.6, ey-off+i*6-6), 2)

        elif e.kind == "hunter":
            ang = math.atan2(e.vy, e.vx)
            tip = (e.x + math.cos(ang) * r * 1.45, ey + math.sin(ang) * r * 1.45)
            left = (e.x + math.cos(ang + 2.45) * r, ey + math.sin(ang + 2.45) * r)
            right = (e.x + math.cos(ang - 2.45) * r, ey + math.sin(ang - 2.45) * r)
            pygame.draw.polygon(screen, black, [tip, left, right])

        elif e.kind == "orbiter":
            pygame.draw.circle(screen, black, (int(e.x), int(ey)), int(r * .62))
            for i in range(3):
                a = t * (3.5 + i * .4) + e.phase + i * math.tau / 3
                ox = e.x + math.cos(a) * r * 1.15
                oy = ey + math.sin(a) * r * .7
                pygame.draw.circle(screen, black, (int(ox), int(oy)), 6)
                pygame.draw.line(screen, black, (e.x, ey), (ox, oy), 3)

        elif e.kind == "dasher":
            ang = math.atan2(e.vy, e.vx)
            pts2 = []
            for offset, dist_mul in ((0,1.55),(2.5,.85),(math.pi,.55),(-2.5,.85)):
                a = ang + offset
                pts2.append((e.x + math.cos(a) * r * dist_mul, ey + math.sin(a) * r * dist_mul))
            pygame.draw.polygon(screen, black, pts2)
            tail = 28 + abs(math.sin(t * 10 + e.phase)) * 18
            pygame.draw.line(screen, black, (e.x-math.cos(ang)*r*.5, ey-math.sin(ang)*r*.5), (e.x-math.cos(ang)*tail, ey-math.sin(ang)*tail), 6)

    def draw_sandbox_bounds(self):
        if not self.sandbox_mode:
            return
        t = self.elapsed
        inset = 10
        pulse = .5 + .5*math.sin(t*6.7)
        outer = 3 + int(pulse*2)

        frame=self.reusable_layer("fx")
        pygame.draw.rect(frame,(70,230,255,150),(inset,inset,WIDTH-inset*2,HEIGHT-inset*2),outer)

        inner = inset + 6
        pygame.draw.rect(frame,(120,160,210,58),(inner,inner,WIDTH-inner*2,HEIGHT-inner*2),1)

        corner = 34
        thick = 4
        c = (245,247,252,210)
        pygame.draw.line(frame,c,(inset,inset),(inset+corner,inset),thick)
        pygame.draw.line(frame,c,(inset,inset),(inset,inset+corner),thick)
        pygame.draw.line(frame,c,(WIDTH-inset,inset),(WIDTH-inset-corner,inset),thick)
        pygame.draw.line(frame,c,(WIDTH-inset,inset),(WIDTH-inset,inset+corner),thick)
        pygame.draw.line(frame,c,(inset,HEIGHT-inset),(inset+corner,HEIGHT-inset),thick)
        pygame.draw.line(frame,c,(inset,HEIGHT-inset),(inset,HEIGHT-inset-corner),thick)
        pygame.draw.line(frame,c,(WIDTH-inset,HEIGHT-inset),(WIDTH-inset-corner,HEIGHT-inset),thick)
        pygame.draw.line(frame,c,(WIDTH-inset,HEIGHT-inset),(WIDTH-inset,HEIGHT-inset-corner),thick)

        for x in range(52,WIDTH-52,84):
            w = 12 + int(8*math.sin(t*5.5+x*.025))
            pygame.draw.line(frame,(70,230,255,110),(x,inset),(x+w,inset),2)
            pygame.draw.line(frame,(70,230,255,110),(x,HEIGHT-inset),(x+w,HEIGHT-inset),2)

        screen.blit(frame,(0,0))

    def draw(self):
        global screen
        if self.impact_timer > 0:
            self.draw_impact_frame()
            return
        self.draw_background()
        sx=random.uniform(-self.shake,self.shake) if self.shake>0 and SCREEN_SHAKE_ENABLED and GRAPHICS_QUALITY<5 else 0
        sy=random.uniform(-self.shake,self.shake) if self.shake>0 and SCREEN_SHAKE_ENABLED and GRAPHICS_QUALITY<5 else 0
        cam=self.camera_y-sy
        for plat in self.platforms:
            plat.draw(cam,self.elapsed,self.hardcore_mode)
        for pu in self.powerups:
            pu.draw(cam,self.elapsed)
        for orb in self.orbs:
            orb.draw(cam,self.elapsed)
        for e in self.entities:
            e.draw(cam,self.elapsed)
        for b in self.bullets:
            b.draw(cam)
        effect_step=graphics_particle_step()
        if GRAPHICS_QUALITY < 5:
            for sw in self.shockwaves[::max(1,effect_step//2)]:
                if -180 <= sw.y-cam <= HEIGHT+180:
                    sw.draw(cam,self.elapsed)
        for pt in self.particles[::effect_step]:
            if -90 <= pt.y-cam <= HEIGHT+90:
                pt.draw(cam,self.elapsed)
        for b in self.blood[::max(1,effect_step//2)]:
            if -90 <= b.y-cam <= HEIGHT+90:
                b.draw(cam,self.elapsed)
        self.draw_sandbox_clear_button()
        ox=self.player.x;self.player.x+=sx;self.player.draw(cam,self.elapsed);self.player.x=ox
        self.draw_player_weapon(cam)
        self.draw_sandbox_bounds()
        if self.vfx_flash > 0 and IMPACT_FLASH_ENABLED and GRAPHICS_QUALITY<5:
            flash=self.reusable_layer("fx")
            alpha = int(clamp(self.vfx_flash / .14, 0.0, 1.0) * 70)
            flash.fill((255,255,255,alpha))
            screen.blit(flash,(0,0))
        base_screen=screen
        ui_layer=self.reusable_layer("ui")
        screen=ui_layer
        self.draw_hud()
        screen=base_screen
        ui_dx=math.sin(self.elapsed*2.35)*2.5
        ui_dy=math.sin(self.elapsed*2.9+1.1)*2.0
        if self.ui_shake_strength>0.01:
            power=4.5*self.ui_shake_strength
            ui_dx+=random.uniform(-power,power)
            ui_dy+=random.uniform(-power,power)
        base_screen.blit(ui_layer,(int(ui_dx),int(ui_dy)))
        if self.dead:
            ov=self.reusable_layer("fx");ov.fill((5,5,10,180));screen.blit(ov,(0,0))
            draw_text(self.death_message,font_big,RED,WIDTH/2,HEIGHT/2-70,center=True)
            draw_text(f'HEIGHT {self.score}  •  STYLE {self.style_score}',font_mid,WHITE,WIDTH/2,HEIGHT/2,center=True)
            retry_text='TOUCH RETRY' if PORTABLE_TOUCH else 'T = RETRY   ENTER = RETRY   ESC = QUIT'
            draw_text(retry_text,font_ui,LIGHT,WIDTH/2,HEIGHT/2+55+math.sin(self.elapsed*4)*3,center=True)
        touch_controller.draw_game_controls(self)

    def on_display_change(self, old_w, old_h, new_w, new_h):
                                                            
        if old_w <= 0:
            return
        ratio = new_w / old_w
        self.player.x = clamp(self.player.x * ratio, 24, new_w - 24)
        for plat in self.platforms:
            plat.x = clamp(plat.x * ratio, 60, new_w - 60)
        for e in self.entities:
            e.x = clamp(e.x * ratio, 30, new_w - 30)
        for pu in self.powerups:
            pu.x = clamp(pu.x * ratio, 30, new_w - 30)
        for orb in self.orbs:
            orb.x = clamp(orb.x * ratio, 30, new_w - 30)
        for pt in self.particles:
            pt.x *= ratio
        for sw in self.shockwaves:
            sw.x *= ratio
        for b in self.blood:
            b.x *= ratio
        self.camera_y = self.player.y - new_h * .64
        self._ui_layer=None
        self._fx_layer=None
        self._vignette_cache={}
        self._panel_cache={}

    def restart(self, cheated=False, sandbox=False, hardcore=None, game_mode=None):
        self.save_best(count_run=not self.progress_locked and not self.sandbox_mode)
        if game_mode is None:
            game_mode=getattr(self,"game_mode","main")
        if sandbox:
            game_mode="sandbox"
        elif hardcore is True:
            game_mode="mardcore"
        elif hardcore is False and game_mode not in ("main","sandbox"):
            game_mode="main"
        if game_mode not in ("main","mardcore","sandbox"):
            game_mode="main"
        sandbox = game_mode == "sandbox"
        hardcore = game_mode == "mardcore"
        if not cheated and not sandbox:
            self.clear_cheat_state()
        self.game_mode = game_mode
        self.progress_locked = bool(cheated or sandbox)
        self.sandbox_mode = sandbox
        self.hardcore_mode = hardcore
        self.reset()
        if not cheated and not sandbox:
            self.cheat_noclip = False
            self.cheat_god = False
        self.game_mode = game_mode
        self.progress_locked = bool(cheated or sandbox)
        self.sandbox_mode = sandbox
        self.hardcore_mode = hardcore


                                                       
MENU_MAIN = "main"
MENU_PLAY = "play"
MENU_OPTIONS = "options"
MENU_PAUSE = "pause"
MENU_HACKS = "hacks"
MENU_PERMANENT_POWERS = "permanent_powers"
MENU_SPAWNER = "spawner"
CHEATS_ENABLED = False
RANK_ORDER = ["FUCK","Efficient","Dull","Cool","Bold","Agreeable","Sensational","SUPER Sensational","HYPER Sensational","HELL YEAH!","CUBE"]
RANK_SCORE_SANDBOX = {"FUCK":0,"Efficient":250,"Dull":500,"Cool":800,"Bold":1200,"Agreeable":1700,"Sensational":2300,"SUPER Sensational":3000,"HYPER Sensational":3900,"HELL YEAH!":5000,"CUBE":6500}
RANK_SCORE_MAIN = {"FUCK":0,"Efficient":350,"Dull":700,"Cool":1100,"Bold":1650,"Agreeable":2300,"Sensational":3100,"SUPER Sensational":4050,"HYPER Sensational":5250,"HELL YEAH!":6750,"CUBE":8750}
RANK_SCORE_MARDCORE = {"FUCK":0,"Efficient":500,"Dull":1000,"Cool":1600,"Bold":2400,"Agreeable":3400,"Sensational":4600,"SUPER Sensational":6000,"HYPER Sensational":7800,"HELL YEAH!":10000,"CUBE":13000}
RANK_SCORE = RANK_SCORE_MAIN

class MenuSystem:
    def __init__(self):
        self.state = MENU_MAIN
        self.index = 0
        self.t = 0.0
        self.main_items = ["PLAY", "OPTIONS", "QUIT"]
        self.play_items = ["MAIN", "MARDCORE", "SANDBOX", "BACK"]
        self.pause_items = ["RESUME", "OPTIONS", "MAIN MENU", "QUIT"]
        self.options_items = ["FULLSCREEN", "GRAPHICS", "MENU SONG", "GAMEPLAY SONG", "SOUNDS", "MUSIC", "SCREEN SHAKE", "IMPACT FLASH", "BACK"]
        self.hacks_items = ["NOCLIP", "GOD", "GET RANK", "ALL POWERUPS", "PERMANENT POWERS", "CLEAR ENTITIES", "BACK"]
        self.permanent_power_items = ["INFINITE JUMPS", "SHIELD", "ANGEL", "FLIGHT", "BACK"]
        self.spawner_kinds = ["drone","wraith","hunter","orbiter","dasher","monster","m_drone","m_wraith","m_hunter","m_orbiter","m_dasher","monster5d"]
        self.spawner_orbs = list(Orb.KINDS)
        self.spawner_powerups = list(PowerUp.NAMES)
        self.spawner_weapons = list(PowerUp.WEAPON_NAMES)
        self.spawner_platforms = ["CUSTOM PLATFORM"]
        self.spawner_sections = ["ENTITIES","ORBS","POWERUPS","WEAPONS","PLATFORMS"]
        self.spawner_section_index = 0
        self.spawner_entity_index = 0
        self.spawner_orb_index = 0
        self.spawner_powerup_index = 0
        self.spawner_weapon_index = 0
        self.spawner_platform_index = 0
        self.spawner_platform_w = 180
        self.spawner_platform_h = 18
        self.hack_rank_index = 0
        self.return_menu = MENU_MAIN
        self.mouse_rects = []
        self.menu_anim = 0.0
        self.menu_anim_target = 1.0
        self.ui_breathe = 0.0
        self.click_lock_until = 0

    def items(self):
        if self.state == MENU_MAIN:
            return self.main_items
        if self.state == MENU_PLAY:
            return self.play_items
        if self.state == MENU_PAUSE:
            return self.pause_items
        if self.state == MENU_HACKS:
            return self.hacks_items
        if self.state == MENU_PERMANENT_POWERS:
            return self.permanent_power_items
        return self.options_items

    def set_state(self, state):
        self.state = state
        self.index = 0
        self.menu_anim = 0.0
        self.menu_anim_target = 1.0

    def open_options(self, return_menu):
        self.return_menu = return_menu
        self.set_state(MENU_OPTIONS)

    def move(self, amount):
        items = self.items()
        self.index = (self.index + amount) % len(items)

    def selected_label(self):
        return self.items()[self.index]

    def current_spawner_section(self):
        return self.spawner_sections[self.spawner_section_index]

    def current_spawner_items(self):
        section=self.current_spawner_section()
        if section=="ORBS":
            return self.spawner_orbs
        if section=="POWERUPS":
            return self.spawner_powerups
        if section=="WEAPONS":
            return self.spawner_weapons
        if section=="PLATFORMS":
            return self.spawner_platforms
        return self.spawner_kinds

    def selected_spawner_kind(self):
        section=self.current_spawner_section()
        if section=="ORBS":
            return self.spawner_orbs[self.spawner_orb_index]
        if section=="POWERUPS":
            return self.spawner_powerups[self.spawner_powerup_index]
        if section=="WEAPONS":
            return self.spawner_weapons[self.spawner_weapon_index]
        if section=="PLATFORMS":
            return self.spawner_platforms[self.spawner_platform_index]
        return self.spawner_kinds[self.spawner_entity_index]

    def selected_spawner_type(self):
        section=self.current_spawner_section()
        if section=="ORBS":
            return "orb"
        if section=="POWERUPS":
            return "powerup"
        if section=="WEAPONS":
            return "weapon"
        if section=="PLATFORMS":
            return "platform"
        return "entity"

    def move_spawner(self, amount):
        section=self.current_spawner_section()
        if section=="ORBS":
            self.spawner_orb_index=(self.spawner_orb_index+amount)%len(self.spawner_orbs)
        elif section=="POWERUPS":
            self.spawner_powerup_index=(self.spawner_powerup_index+amount)%len(self.spawner_powerups)
        elif section=="WEAPONS":
            self.spawner_weapon_index=(self.spawner_weapon_index+amount)%len(self.spawner_weapons)
        elif section=="PLATFORMS":
            self.spawner_platform_index=0
        else:
            self.spawner_entity_index=(self.spawner_entity_index+amount)%len(self.spawner_kinds)

    def move_spawner_section(self, amount):
        self.spawner_section_index=(self.spawner_section_index+amount)%len(self.spawner_sections)

    def resize_spawner_platform(self, axis, amount):
        if axis=="x":
            self.spawner_platform_w=int(clamp(self.spawner_platform_w+amount*20,40,680))
        else:
            self.spawner_platform_h=int(clamp(self.spawner_platform_h+amount*6,8,220))
        game.resize_sandbox_active_platform(self.spawner_platform_w,self.spawner_platform_h)

    def draw_spawner_overlay(self):
        if not hasattr(self,"portable_spawner_shade") or self.portable_spawner_shade.get_size()!=(WIDTH,HEIGHT):
            self.portable_spawner_shade=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
            self.portable_spawner_shade.fill((0,0,0,78))
        screen.blit(self.portable_spawner_shade,(0,0))
        panel_w=min(760,WIDTH*.72)
        x=24
        y=28
        row_h=34
        items=self.current_spawner_items()
        h=min(HEIGHT-56,176+len(items)*row_h)
        if self.current_spawner_section()=="PLATFORMS":
            h=min(HEIGHT-56,334)
        panel=pygame.Surface((int(panel_w),int(h)),pygame.SRCALPHA)
        panel.fill((8,10,16,220))
        screen.blit(panel,(x,y))
        pygame.draw.rect(screen,CYAN,(x,y,panel_w,h),2)
        draw_text("SANDBOX SPAWNER",font_mid,WHITE,x+18,y+12)
        section=self.current_spawner_section()
        entity_active=section=="ENTITIES"
        orb_active=section=="ORBS"
        powerup_active=section=="POWERUPS"
        weapon_active=section=="WEAPONS"
        platform_active=section=="PLATFORMS"
        tab_wave=math.sin(self.t*5.2)*2
        tabs=[
            ("[ ENTITIES ]",entity_active,YELLOW,x+18+tab_wave),
            ("[ ORBS ]",orb_active,CYAN,x+160),
            ("[ POWERUPS ]",powerup_active,GREEN,x+254),
            ("[ WEAPONS ]",weapon_active,ORANGE,x+400),
            ("[ PLATFORMS ]",platform_active,WHITE,x+536-tab_wave)
        ]
        for label,active,color,tx in tabs:
            draw_text(label,font_small,color if active else LIGHT,tx,y+48)
        draw_text("A / D = SECTION",font_small,LIGHT,x+18,y+78)
        if entity_active:
            draw_text("NORMAL + MARDCORE",font_small,PINK,x+18,y+104)
            for i,kind in enumerate(self.spawner_kinds):
                yy=y+132+i*row_h
                selected=i==self.spawner_entity_index
                is_mard=kind in HARDCORE_ENTITY_KINDS or kind=="monster5d"
                c=RED if selected and is_mard else YELLOW if selected else PINK if is_mard else LIGHT
                prefix="> " if selected else "  "
                suffix="  [M]" if is_mard else ""
                draw_text(prefix+ENTITY_NAMES[kind]+suffix,font_small,c,x+20+math.sin(self.t*5+i)*3,yy)
        elif orb_active:
            draw_text("JUMP ORBS",font_small,CYAN,x+18,y+104)
            for i,kind in enumerate(self.spawner_orbs):
                yy=y+132+i*row_h
                selected=i==self.spawner_orb_index
                c=WHITE if selected else YELLOW if kind=="YELLOW" else CYAN
                prefix="> " if selected else "  "
                jump_text="HIGH JUMP" if kind=="YELLOW" else "SUPER JUMP"
                draw_text(prefix+kind+" ORB  -  "+jump_text,font_small,c,x+20+math.sin(self.t*5+i)*3,yy)
        elif powerup_active:
            draw_text("PLAYER POWERUPS",font_small,GREEN,x+18,y+104)
            for i,kind in enumerate(self.spawner_powerups):
                yy=y+132+i*row_h
                selected=i==self.spawner_powerup_index
                c=WHITE if selected else {
                    "INFINITE JUMPS":CYAN,
                    "SHIELD":BLUE,
                    "ANGEL":YELLOW,
                    "FLIGHT":PINK
                }[kind]
                prefix="> " if selected else "  "
                draw_text(prefix+kind,font_small,c,x+20+math.sin(self.t*5+i)*3,yy)
        elif weapon_active:
            draw_text("WEAPON POWER-UPS  -  60.00s",font_small,ORANGE,x+18,y+104)
            for i,kind in enumerate(self.spawner_weapons):
                yy=y+132+i*row_h
                selected=i==self.spawner_weapon_index
                c=WHITE if selected else MARDCORE_WEAPONS[kind]["color"]
                prefix="> " if selected else "  "
                draw_text(prefix+kind+"  -  60.00s",font_small,c,x+20+math.sin(self.t*5+i)*3,yy)
        elif platform_active:
            draw_text("CUSTOM COLLIDABLE PLATFORM",font_small,CYAN,x+18,y+104)
            draw_text("CLICK ANYWHERE = SPAWN / SELECT NEW PLATFORM",font_small,LIGHT,x+18,y+134)
            draw_text(f"X AXIS  {self.spawner_platform_w}px",font_small,WHITE,x+18,y+170)
            draw_text(f"Y AXIS  {self.spawner_platform_h}px",font_small,WHITE,x+270,y+170)
            preview_w=clamp(self.spawner_platform_w*.54,40,panel_w-80)
            preview_h=clamp(self.spawner_platform_h*.54,8,96)
            px=x+panel_w*.5
            py=y+236
            preview=pygame.Rect(int(px-preview_w*.5),int(py-preview_h*.5),int(preview_w),int(preview_h))
            pygame.draw.rect(screen,DARK,preview,border_radius=4)
            pygame.draw.rect(screen,CYAN,preview,2,border_radius=4)
            wave_y=preview.centery+math.sin(self.t*7.0)*2
            pygame.draw.line(screen,WHITE,(preview.left+8,wave_y),(preview.right-8,wave_y),2)
            draw_text("ARROWS = SCALE",font_small,YELLOW,x+18,y+286)
            draw_text("LEFT / RIGHT = X   UP / DOWN = Y",font_small,LIGHT,x+18,y+310)
        draw_text("CLICK = SPAWN   C = CHEATS   X = CLEAR",font_small,CYAN,x+18,y+h-28)

    def draw_sine_background(self):
                                                              
        screen.fill(BG)
        t = self.t
        for row in range(12):
            pts=[]
            base = (row + 1) * HEIGHT / 13
            amp = 10 + row * 1.1
            speed = 1.2 + row * .08
            for x in range(-30, WIDTH+31, 24):
                y = base + math.sin(x*.014 + t*speed + row*.65) * amp
                pts.append((x,y))
            pygame.draw.lines(screen, DARK2 if row % 2 == 0 else DARK, False, pts, 2)

                                                             
        cx, cy = WIDTH*.5, HEIGHT*.42
        for ring in range(4):
            rr = 90 + ring*46 + math.sin(t*2.6 + ring)*9
            pts=[]
            for i in range(64):
                a=i/63*math.tau
                wobble=math.sin(a*5+t*3+ring)*7
                pts.append((cx+math.cos(a)*(rr+wobble), cy+math.sin(a)*(rr+wobble)))
            pygame.draw.lines(screen, (22+ring*5,32+ring*6,52+ring*7), True, pts, 2)

    def draw_title(self, title="CUBED"):
        t=self.t
        y=105+math.sin(t*2.4)*9
        draw_text(title,font_title,WHITE,WIDTH/2,y,center=True)
                                         
        pts=[]
        width=min(520, WIDTH*.55)
        for i in range(60):
            f=i/59
            x=WIDTH/2-width/2+f*width
            yy=y+55+math.sin(t*6+f*math.tau*3)*4
            pts.append((x,yy))
        pygame.draw.lines(screen,CYAN,False,pts,3)

    def draw_items(self):
        self.mouse_rects=[]
        items=self.items()
        self.menu_anim = sine_tween(self.menu_anim, self.menu_anim_target, 8.0, 1.0/FPS)
        ease = clamp(self.menu_anim,0.0,1.0)
        start_y=HEIGHT*.35 if self.state==MENU_OPTIONS else HEIGHT*.48
        spacing=54 if self.state==MENU_OPTIONS else 66
        for i,label in enumerate(items):
            selected=(i==self.index)
            phase=self.t*4+i*.8
            mardcore_button=self.state==MENU_PLAY and label=="MARDCORE"
            if mardcore_button:
                dx=math.sin(self.t*18.0+i*.8)*10
                dy=math.sin(self.t*23.0+i*1.1)*4
            else:
                dx=math.sin(phase)*(14 if selected else 5)
                dy=math.sin(phase*1.17)*(5 if selected else 2)
            slide=(1.0-ease)*(90+i*18)
            dx+=slide if i%2==0 else -slide
            w=min(430, WIDTH*.48)
            h=48
            x=WIDTH/2-w/2+dx
            y=start_y+i*spacing+dy
            rect=pygame.Rect(int(x),int(y),int(w),h)
            self.mouse_rects.append(rect)

                                                   
            cut=18+math.sin(self.t*21.0+i)*5 if mardcore_button else 18+math.sin(phase)*4
            pts=[(x+cut,y),(x+w,y),(x+w-cut,y+h),(x,y+h)]
            pygame.draw.polygon(screen,DARK,pts)
            if mardcore_button:
                mix=.5+.5*math.sin(self.t*7.5)
                color=(
                    int(255),
                    int(35+(255-35)*mix),
                    int(55+(255-55)*mix)
                )
            else:
                color=CYAN if selected else LIGHT
            pygame.draw.polygon(screen,color,pts,3 if selected else 1)

            shown=label
            if self.state==MENU_OPTIONS and label=="FULLSCREEN":
                shown=f"FULLSCREEN: {'ON' if FULLSCREEN else 'OFF'}"
            elif self.state==MENU_OPTIONS and label=="GRAPHICS":
                shown=f"GRAPHICS: {graphics_value()}"
            elif self.state==MENU_OPTIONS and label=="MENU SONG":
                song = "AUTO" if MENU_MUSIC_FILE is None else MENU_MUSIC_FILE
                shown=f"MENU SONG: {song if len(song) <= 28 else song[:25]+'...'}"
            elif self.state==MENU_OPTIONS and label=="GAMEPLAY SONG":
                shown="GAMEPLAY SONG: BY MODE"
            elif self.state==MENU_OPTIONS and label=="SOUNDS":
                shown=f"SOUNDS: {int(SOUND_VOLUME*100)}%"
            elif self.state==MENU_OPTIONS and label=="MUSIC":
                shown=f"MUSIC: {int(MUSIC_VOLUME*100)}%"
            elif self.state==MENU_OPTIONS and label=="SCREEN SHAKE":
                shown=f"SCREEN SHAKE: {'ON' if SCREEN_SHAKE_ENABLED else 'OFF'}"
            elif self.state==MENU_OPTIONS and label=="IMPACT FLASH":
                shown=f"IMPACT FLASH: {'ON' if IMPACT_FLASH_ENABLED else 'OFF'}"
            elif self.state==MENU_HACKS and label=="NOCLIP":
                shown=f"NOCLIP: {'ON' if game.cheat_noclip else 'OFF'}"
            elif self.state==MENU_HACKS and label=="GOD":
                shown=f"GOD: {'ON' if game.cheat_god else 'OFF'}"
            elif self.state==MENU_HACKS and label=="GET RANK":
                shown=f"GET RANK: {RANK_ORDER[self.hack_rank_index]}"
            elif self.state==MENU_PERMANENT_POWERS and label!="BACK":
                shown=f"{label}: {'ON' if label in game.player.permanent_powers else 'OFF'}"
            idle_scale=1.0+math.sin(self.t*2.8+i*.7)*.008
            local_scale=(1.04+math.sin(self.t*16.0)*.018) if mardcore_button else (1.0 + (0.05 + 0.035*math.sin(self.t*7+i))*ease) if selected else idle_scale
            if mardcore_button:
                tx=WIDTH/2+dx+math.sin(self.t*25.0+i*.6)*2.5
                ty=y+h/2+math.sin(self.t*19.0+i*.9)*2.0
            else:
                tx=WIDTH/2+dx+math.sin(self.t*3.1+i*.6)*(3 if selected else 1)
                ty=y+h/2+math.sin(self.t*4.3+i*.9)*(2.5 if selected else .8)
            text_color=color if mardcore_button else WHITE if selected else LIGHT
            draw_cursive_text(shown,font_ui,text_color,tx,ty,True,local_scale)

            if selected:
                                                             
                pulse=8+math.sin(self.t*(18.0 if mardcore_button else 8.0))*5
                pygame.draw.circle(screen,color,(int(x-18-pulse),int(y+h/2)),4)
                pygame.draw.circle(screen,color,(int(x+w+18+pulse),int(y+h/2)),4)

    def draw_footer(self):
        t=self.t
        self.ui_breathe = sine_tween(self.ui_breathe, 1.0, 5.0, 1.0/FPS)
        y=HEIGHT-52+math.sin(t*4)*3
        controls = '↑ ↓ / W S = SELECT    ← → = CHANGE    ENTER / M1 = CONFIRM' if self.state == MENU_OPTIONS else '↑ ↓ / W S = SELECT    ENTER / M1 = CONFIRM'
        footer_x=WIDTH/2+math.sin(t*3.7)*5
        footer_y=y+math.sin(t*2.6+1.3)*2
        draw_text(controls,font_small,LIGHT,footer_x,footer_y,center=True)
        if self.state == MENU_MAIN and CHEATS_ENABLED:
            draw_text('CHEATS ENABLED • PROGRESS DISABLED',font_small,RED,WIDTH/2+math.sin(t*5.2)*6,y-28,center=True)
        if self.state == MENU_PAUSE:
            draw_text('ESC = RESUME',font_small,CYAN,WIDTH/2,y+24,center=True)
        elif self.state == MENU_PLAY:
            draw_text('ESC = BACK',font_small,CYAN,WIDTH/2,y+24,center=True)
        elif self.state == MENU_OPTIONS:
            draw_text('ESC = BACK',font_small,CYAN,WIDTH/2,y+24,center=True)
        elif self.state == MENU_HACKS:
            draw_text('TAB / ESC = BACK    ← → = RANK',font_small,CYAN,WIDTH/2,y+24,center=True)

    def draw(self):
        self.draw_sine_background()
        if self.state == MENU_PLAY:
            self.draw_title('PLAY')
        elif self.state == MENU_PAUSE:
            self.draw_title('PAUSED')
        elif self.state == MENU_OPTIONS:
            self.draw_title('OPTIONS')
        elif self.state == MENU_HACKS:
            self.draw_title('HACKS')
        elif self.state == MENU_PERMANENT_POWERS:
            self.draw_title('PERMANENT POWERS')
        else:
            self.draw_title('CUBED')
        self.draw_items()
        self.draw_footer()

    def hover(self, pos):
        for i,r in enumerate(self.mouse_rects):
            if r.collidepoint(pos):
                self.index=i
                break

    def activate_hack(self, label):
        game.progress_locked = True
        if label == "NOCLIP":
            game.cheat_noclip = not game.cheat_noclip
            game.add_action("NOCLIP ON" if game.cheat_noclip else "NOCLIP OFF",0)
        elif label == "GOD":
            game.cheat_god = not game.cheat_god
            game.add_action("GOD ON" if game.cheat_god else "GOD OFF",0)
        elif label == "GET RANK":
            target=RANK_ORDER[self.hack_rank_index]
            game.style_score=rank_scores_for_mode(game.game_mode)[target]
            game.style_decay_delay=4.0
            game.add_action("GET RANK: "+target,0)
        elif label == "ALL POWERUPS":
            for kind in POWERUP_DURATION:
                game.player.give_powerup(kind)
            game.add_action("ALL POWERUPS",0)
        elif label == "PERMANENT POWERS":
            game.player.permanent_powers.clear()
            self.set_state(MENU_PERMANENT_POWERS)
            self.click_lock_until = pygame.time.get_ticks() + 180
            return
        elif label == "CLEAR ENTITIES":
            game.entities=[e for e in game.entities if e.kind in ('monster','monster5d')]
            game.add_action("ENTITIES CLEARED",0)
        elif label == "BACK":
            self.set_state(MENU_PAUSE)



                                                                               
    def activate_permanent_power(self, label):
        game.progress_locked = True
        if label == "BACK":
            self.set_state(MENU_HACKS)
            return
        if label not in POWERUP_DURATION:
            return
        if label in game.player.permanent_powers:
            game.player.permanent_powers.remove(label)
            if label == "INFINITE JUMPS":
                game.player.infinite_jumps = 0.0
            elif label == "SHIELD":
                game.player.shield = 0.0
                game.player.shield_hits = 0
            elif label == "ANGEL":
                game.player.angel = 0.0
            elif label == "FLIGHT":
                game.player.flight = 0.0
            game.add_action(label+" PERMANENT OFF",0)
        else:
            game.player.permanent_powers.add(label)
            game.player.give_powerup(label)
            if label == "SHIELD":
                game.player.shield_hits = 1
            game.add_action(label+" PERMANENT ON",0)


PLAY_LENS_DURATION = 0.82
play_lens_t = 0.0
play_lens_active = False

def begin_play_transition(game_mode="main"):
    global mode, play_lens_t, play_lens_active
    if game_mode not in ("main","mardcore","sandbox"):
        game_mode="main"
    sandbox = game_mode == "sandbox"
    hardcore = game_mode == "mardcore"
    game.restart(CHEATS_ENABLED or sandbox, sandbox, hardcore, game_mode)
    if sandbox:
        game.platforms = []
    if hardcore:
        game.add_action('VAS A ESTAR 5 MTS BAJO TIERRA YURI',0)
    game.start_music()
    play_lens_t = 0.0
    play_lens_active = True
    mode = "playing"

def draw_lens_circle(progress):
                                                                                  
    progress = clamp(progress, 0.0, 1.0)
    eased = math.sin(progress * math.pi * 0.5)
    cx = WIDTH * 0.5 + math.sin(menu.t * 4.0) * 5
    cy = HEIGHT * 0.48 + math.sin(menu.t * 5.0 + 1.2) * 5
    max_r = math.hypot(WIDTH, HEIGHT) * 0.72
    radius = 18 + eased * max_r

                                                                                  
    mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 245))
    pygame.draw.circle(mask, (0, 0, 0, 0), (int(cx), int(cy)), int(radius))
    screen.blit(mask, (0, 0))

                                          
    for ring in range(5):
        rr = radius + ring * 14 + math.sin(menu.t * 14 + ring * 1.15) * 6
        if rr > 3:
            pts=[]
            for i in range(96):
                a=i/96*math.tau
                wobble=math.sin(a*8 + menu.t*11 + ring)*4
                r2=rr+wobble
                pts.append((cx+math.cos(a)*r2, cy+math.sin(a)*r2))
            col = WHITE if ring == 0 else (90, 210, 255)
            pygame.draw.lines(screen, col, True, pts, 3 if ring == 0 else 1)

                                              
    flash = max(0.0, math.sin(progress * math.pi))
    if flash > 0:
        glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        alpha = int(80 * flash)
        pygame.draw.circle(glow, (255,255,255,alpha), (int(cx),int(cy)), int(max(10, radius*.35)))
        screen.blit(glow,(0,0))

                                                      
touch_controller = TouchController()
game = Game()
menu = MenuSystem()
running = True
mode = "menu"
game.start_menu_music()

def portable_menu_activate_at(pos):
    global mode,running,GRAPHICS_QUALITY,MENU_MUSIC_FILE,GAME_MUSIC_FILE,SOUND_VOLUME,MUSIC_VOLUME,MENU_MUSIC_VOLUME,SCREEN_SHAKE_ENABLED,IMPACT_FLASH_ENABLED
    menu.hover(pos)
    if not (0 <= menu.index < len(menu.items())):
        return
    label=menu.selected_label()
    if menu.state==MENU_MAIN:
        if label=="PLAY":
            menu.set_state(MENU_PLAY)
        elif label=="OPTIONS":
            menu.open_options(MENU_MAIN)
        elif label=="QUIT":
            running=False
    elif menu.state==MENU_PLAY:
        if label=="MAIN":
            begin_play_transition("main")
        elif label=="MARDCORE":
            begin_play_transition("mardcore")
        elif label=="SANDBOX":
            begin_play_transition("sandbox")
        elif label=="BACK":
            menu.set_state(MENU_MAIN)
    elif menu.state==MENU_PAUSE:
        if label=="RESUME":
            mode="playing"
        elif label=="OPTIONS":
            menu.open_options(MENU_PAUSE)
            mode="menu"
        elif label=="MAIN MENU":
            game.save_best()
            touch_controller.reset()
            game.start_menu_music()
            menu.set_state(MENU_MAIN)
            mode="menu"
        elif label=="QUIT":
            running=False
    elif menu.state==MENU_HACKS:
        menu.activate_hack(label)
    elif menu.state==MENU_PERMANENT_POWERS:
        menu.activate_permanent_power(label)
    elif menu.state==MENU_OPTIONS:
        if label=="FULLSCREEN":
            old_w,old_h,new_w,new_h=apply_display(not FULLSCREEN)
            game.on_display_change(old_w,old_h,new_w,new_h)
        elif label=="GRAPHICS":
            GRAPHICS_QUALITY=(GRAPHICS_QUALITY+1)%len(GRAPHICS_LEVELS)
            save_settings()
        elif label=="MENU SONG":
            MENU_MUSIC_FILE=cycle_song(MENU_MUSIC_FILE,1)
            save_settings()
            game.start_menu_music()
        elif label=="GAMEPLAY SONG":
            GAME_MUSIC_FILE="BY_MODE"
            save_settings()
        elif label=="SOUNDS":
            SOUND_VOLUME=0.0 if SOUND_VOLUME>0 else .7
            save_settings()
        elif label=="MUSIC":
            MUSIC_VOLUME=0.0 if MUSIC_VOLUME>0 else .75
            MENU_MUSIC_VOLUME=MUSIC_VOLUME
            save_settings()
            if AUDIO_OK:
                pygame.mixer.music.set_volume(MUSIC_VOLUME)
        elif label=="SCREEN SHAKE":
            SCREEN_SHAKE_ENABLED=not SCREEN_SHAKE_ENABLED
            save_settings()
        elif label=="IMPACT FLASH":
            IMPACT_FLASH_ENABLED=not IMPACT_FLASH_ENABLED
            save_settings()
        elif label=="BACK":
            menu.set_state(menu.return_menu)
            mode="paused" if menu.return_menu==MENU_PAUSE else "menu"

def portable_spawn_at(pos):
    spawner_type=menu.selected_spawner_type()
    if spawner_type=="orb":
        game.spawn_sandbox_orb(menu.selected_spawner_kind(),pos[0],pos[1])
    elif spawner_type=="powerup":
        game.spawn_sandbox_powerup(menu.selected_spawner_kind(),pos[0],pos[1])
    elif spawner_type=="weapon":
        game.spawn_sandbox_weapon(menu.selected_spawner_kind(),pos[0],pos[1])
    elif spawner_type=="platform":
        game.spawn_sandbox_platform(pos[0],pos[1],menu.spawner_platform_w,menu.spawner_platform_h)
    else:
        game.spawn_sandbox_entity(menu.selected_spawner_kind(),pos[0],pos[1])

def portable_handle_spawner_tap(pos):
    global mode
    rects=touch_controller.spawner_rects()
    if rects["close"].collidepoint(pos):
        mode="playing"
        touch_controller.reset()
        return True
    if rects["clear"].collidepoint(pos):
        game.clear_sandbox_world()
        return True
    if rects["section_prev"].collidepoint(pos):
        menu.move_spawner_section(-1)
        return True
    if rects["section_next"].collidepoint(pos):
        menu.move_spawner_section(1)
        return True
    if rects["item_prev"].collidepoint(pos):
        menu.move_spawner(-1)
        return True
    if rects["item_next"].collidepoint(pos):
        menu.move_spawner(1)
        return True
    if menu.current_spawner_section()=="PLATFORMS":
        if rects["x_minus"].collidepoint(pos):
            menu.resize_spawner_platform("x",-1)
            return True
        if rects["x_plus"].collidepoint(pos):
            menu.resize_spawner_platform("x",1)
            return True
        if rects["y_minus"].collidepoint(pos):
            menu.resize_spawner_platform("y",-1)
            return True
        if rects["y_plus"].collidepoint(pos):
            menu.resize_spawner_platform("y",1)
            return True
    panel_w=min(760,WIDTH*.72)
    panel_rect=pygame.Rect(24,28,int(panel_w),HEIGHT-56)
    if not panel_rect.collidepoint(pos):
        portable_spawn_at(pos)
        return True
    return False

def portable_handle_game_tap(action):
    global mode
    if action=="retry":
        start_retry_music_recovery(game.game_mode)
        game.restart(game.progress_locked,game.sandbox_mode)
        return
    if action=="pause":
        touch_controller.reset()
        mode="paused"
        menu.set_state(MENU_PAUSE)
        return
    if action=="spawner":
        touch_controller.reset()
        mode="spawner"
        menu.set_state(MENU_SPAWNER)
        return
    if game.dead:
        return
    if action=="jump":
        game.player.request_jump()
    elif action=="dash":
        if game.player.dash(touch_controller.keys(pygame.key.get_pressed())):
            game.add_action("DASH",55)
            game.burst(game.player.x,game.player.y,CYAN,10,230)
            game.action_vfx("DASH")
    elif action=="parry":
        if game.player.parry(game.hardcore_mode):
            game.ui_shake_timer=.16
            game.ui_shake_strength=1.0
            game.add_action("PARRY READY",35)
            game.burst(game.player.x,game.player.y,GREEN,12,200)
            game.action_vfx("PARRY")
    elif action=="fire":
        game.fire_weapon()

                                                   
while running:
    dt = min(clock.tick(FPS) / 1000.0, 0.033)
    menu.t += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue

        finger_down_type=getattr(pygame,"FINGERDOWN",-10001)
        finger_motion_type=getattr(pygame,"FINGERMOTION",-10002)
        finger_up_type=getattr(pygame,"FINGERUP",-10003)

        if PORTABLE_TOUCH and event.type==finger_down_type:
            pos=(int(event.x*WIDTH),int(event.y*HEIGHT))
            finger_id=getattr(event,"finger_id",getattr(event,"fingerId",0))
            if mode=="playing":
                action=touch_controller.begin_finger(finger_id,pos,game)
                portable_handle_game_tap(action)
            elif mode=="spawner":
                touch_controller.last_finger_ms=pygame.time.get_ticks()
                portable_handle_spawner_tap(pos)
            else:
                touch_controller.last_finger_ms=pygame.time.get_ticks()
                portable_menu_activate_at(pos)
            continue

        if PORTABLE_TOUCH and event.type==finger_motion_type:
            pos=(int(event.x*WIDTH),int(event.y*HEIGHT))
            finger_id=getattr(event,"finger_id",getattr(event,"fingerId",0))
            if mode=="playing":
                touch_controller.move_finger(finger_id,pos,game)
            continue

        if PORTABLE_TOUCH and event.type==finger_up_type:
            finger_id=getattr(event,"finger_id",getattr(event,"fingerId",0))
            touch_controller.end_finger(finger_id)
            continue

        if event.type == pygame.MOUSEMOTION and mode not in ("playing","spawner"):
            menu.hover(event.pos)

        if event.type == pygame.KEYDOWN:
                                                       
            if mode == "playing":
                if event.key == pygame.K_t:
                    if game.dead:
                        start_retry_music_recovery(game.game_mode)
                        game.restart(game.progress_locked, game.sandbox_mode)
                        continue
                    game.restart(game.progress_locked, game.sandbox_mode)
                    if game.sandbox_mode:
                        game.platforms = []
                    continue
                if game.sandbox_mode and event.key == pygame.K_TAB:
                    mode = "spawner"
                    menu.set_state(MENU_SPAWNER)
                    continue
                if game.sandbox_mode and event.key == pygame.K_t:
                    game.platforms = []
                    game.add_action("SANDBOX CLEARED",0)
                    continue
                if event.key == pygame.K_ESCAPE:
                    touch_controller.reset()
                    mode = "paused"
                    menu.set_state(MENU_PAUSE)
                    continue

                if game.dead and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_t):
                    start_retry_music_recovery(game.game_mode)
                    game.restart(game.progress_locked, game.sandbox_mode)
                    if game.sandbox_mode:
                        game.platforms = []
                    continue

                if event.key == pygame.K_m:
                    if not AUDIO_OK:
                        init_audio(); game.music_name, game.audio_status = music_setup(game.game_mode)
                    elif game.music_name is None:
                        game.music_name, game.audio_status = music_setup(game.game_mode)
                    elif pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause(); game.audio_status='PAUSED'
                    else:
                        pygame.mixer.music.unpause()
                        if not pygame.mixer.music.get_busy():
                            game.music_name, game.audio_status = music_setup(game.game_mode)
                    game.audio_notice_time = 5.0

                if not game.dead:
                    if event.key == pygame.K_SPACE:
                        game.player.request_jump()
                    elif event.key == pygame.K_q:
                        if game.player.dash(touch_controller.keys(pygame.key.get_pressed())):
                            game.add_action('DASH',55)
                            game.burst(game.player.x,game.player.y,CYAN,10,230)
                            game.action_vfx("DASH")
                    elif event.key == pygame.K_e:
                        if game.player.parry(game.hardcore_mode):
                            game.ui_shake_timer=.16
                            game.ui_shake_strength=1.0
                            game.add_action('PARRY READY',35)
                            game.burst(game.player.x,game.player.y,GREEN,12,200)
                            game.action_vfx("PARRY")
                continue

                                                               
            if mode == "spawner":
                if event.key in (pygame.K_TAB, pygame.K_ESCAPE):
                    touch_controller.reset()
                    mode = "playing"
                    continue
                platform_tab=menu.current_spawner_section()=="PLATFORMS"
                if event.key == pygame.K_t:
                    game.platforms = []
                    game.sandbox_active_platform=None
                    game.add_action("SANDBOX PLATFORMS CLEARED",0)
                    continue
                if platform_tab and event.key == pygame.K_LEFT:
                    menu.resize_spawner_platform("x",-1)
                    continue
                if platform_tab and event.key == pygame.K_RIGHT:
                    menu.resize_spawner_platform("x",1)
                    continue
                if platform_tab and event.key == pygame.K_UP:
                    menu.resize_spawner_platform("y",1)
                    continue
                if platform_tab and event.key == pygame.K_DOWN:
                    menu.resize_spawner_platform("y",-1)
                    continue
                if event.key in (pygame.K_UP, pygame.K_w):
                    menu.move_spawner(-1)
                    continue
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    menu.move_spawner(1)
                    continue
                if event.key == pygame.K_a:
                    menu.move_spawner_section(-1)
                    continue
                if event.key == pygame.K_d:
                    menu.move_spawner_section(1)
                    continue
                if event.key == pygame.K_LEFT:
                    menu.move_spawner_section(-1)
                    continue
                if event.key == pygame.K_RIGHT:
                    menu.move_spawner_section(1)
                    continue
                if event.key == pygame.K_c:
                    mode = "paused"
                    menu.set_state(MENU_HACKS)
                    continue
                if event.key == pygame.K_x:
                    game.entities.clear()
                    game.orbs.clear()
                    game.powerups.clear()
                    game.platforms.clear()
                    game.sandbox_active_platform=None
                    game.bullets.clear()
                    game.particles.clear()
                    game.blood.clear()
                    game.shockwaves.clear()
                    game.weapon_active_timer=0.0
                    game.monster_spawned = False
                    desktop_entities.clear()
                    game.add_action("SANDBOX CLEARED",0)
                    continue
                continue

            if mode == "starting":
                continue

            if mode == "menu" and menu.state == MENU_MAIN and event.key == pygame.K_m:
                CHEATS_ENABLED = not CHEATS_ENABLED
                if not CHEATS_ENABLED:
                    game.clear_cheat_state()
                    menu.set_state(MENU_MAIN)
                continue

            if mode == "paused" and (CHEATS_ENABLED or game.sandbox_mode) and event.key == pygame.K_TAB:
                menu.set_state(MENU_HACKS)
                continue

            if menu.state == MENU_HACKS and event.key in (pygame.K_TAB, pygame.K_ESCAPE):
                menu.set_state(MENU_PAUSE)
                mode = "paused"
                continue

            if menu.state == MENU_PERMANENT_POWERS and event.key in (pygame.K_TAB, pygame.K_ESCAPE):
                menu.set_state(MENU_HACKS)
                continue

            if menu.state == MENU_HACKS and event.key in (pygame.K_LEFT, pygame.K_a):
                if menu.selected_label() == "GET RANK":
                    menu.hack_rank_index=(menu.hack_rank_index-1)%len(RANK_ORDER)
                    continue
            if menu.state == MENU_HACKS and event.key in (pygame.K_RIGHT, pygame.K_d):
                if menu.selected_label() == "GET RANK":
                    menu.hack_rank_index=(menu.hack_rank_index+1)%len(RANK_ORDER)
                    continue

            if menu.state == MENU_OPTIONS and event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d):
                delta = -1 if event.key in (pygame.K_LEFT, pygame.K_a) else 1
                label = menu.selected_label()
                if label == "GRAPHICS":
                    GRAPHICS_QUALITY=(GRAPHICS_QUALITY+delta)%len(GRAPHICS_LEVELS)
                    save_settings()
                elif label == "MENU SONG":
                    MENU_MUSIC_FILE = cycle_song(MENU_MUSIC_FILE, delta)
                    save_settings()
                    game.start_menu_music()
                elif label == "GAMEPLAY SONG":
                    GAME_MUSIC_FILE = "BY_MODE"
                    save_settings()
                elif label == "SOUNDS":
                    SOUND_VOLUME = clamp(round((SOUND_VOLUME + delta * .1) * 10) / 10, 0.0, 1.0)
                    save_settings()
                    None
                elif label == "MUSIC":
                    MUSIC_VOLUME = clamp(round((MUSIC_VOLUME + delta * .1) * 10) / 10, 0.0, 1.0)
                    MENU_MUSIC_VOLUME = MUSIC_VOLUME
                    save_settings()
                    if AUDIO_OK:
                        pygame.mixer.music.set_volume(MUSIC_VOLUME)
                elif label == "SCREEN SHAKE":
                    SCREEN_SHAKE_ENABLED = not SCREEN_SHAKE_ENABLED
                    save_settings()
                elif label == "IMPACT FLASH":
                    IMPACT_FLASH_ENABLED = not IMPACT_FLASH_ENABLED
                    save_settings()
                continue

            if event.key in (pygame.K_UP, pygame.K_w):
                menu.move(-1)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                menu.move(1)
            elif event.key == pygame.K_ESCAPE:
                if menu.state == MENU_OPTIONS:
                    menu.set_state(menu.return_menu)
                    mode = "paused" if menu.return_menu == MENU_PAUSE else "menu"
                elif menu.state == MENU_PAUSE:
                    touch_controller.reset()
                    mode = "playing"
                elif menu.state == MENU_PLAY:
                    menu.set_state(MENU_MAIN)
                elif menu.state == MENU_MAIN:
                    running = False
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                label=menu.selected_label()
                if menu.state == MENU_MAIN:
                    if label == "PLAY":
                        menu.set_state(MENU_PLAY)
                    elif label == "OPTIONS":
                        menu.open_options(MENU_MAIN)
                    elif label == "QUIT":
                        running=False
                elif menu.state == MENU_PLAY:
                    if label == "MAIN":
                        begin_play_transition("main")
                    elif label == "MARDCORE":
                        begin_play_transition("mardcore")
                    elif label == "SANDBOX":
                        begin_play_transition("sandbox")
                    elif label == "BACK":
                        menu.set_state(MENU_MAIN)
                elif menu.state == MENU_PAUSE:
                    if label == "RESUME":
                        touch_controller.reset()
                        mode="playing"
                    elif label == "OPTIONS":
                        menu.open_options(MENU_PAUSE)
                        mode="menu"
                    elif label == "MAIN MENU":
                        game.save_best()
                        game.start_menu_music()
                        menu.set_state(MENU_MAIN)
                        mode="menu"
                    elif label == "QUIT":
                        running=False
                elif menu.state == MENU_HACKS:
                    menu.activate_hack(label)
                elif menu.state == MENU_PERMANENT_POWERS:
                    menu.activate_permanent_power(label)
                elif menu.state == MENU_OPTIONS:
                    if label == "FULLSCREEN":
                        old_w,old_h,new_w,new_h=apply_display(not FULLSCREEN)
                        game.on_display_change(old_w,old_h,new_w,new_h)
                    elif label == "GRAPHICS":
                        GRAPHICS_QUALITY=(GRAPHICS_QUALITY+1)%len(GRAPHICS_LEVELS)
                        save_settings()
                    elif label == "MENU SONG":
                        MENU_MUSIC_FILE = cycle_song(MENU_MUSIC_FILE, 1)
                        game.start_menu_music()
                    elif label == "GAMEPLAY SONG":
                        GAME_MUSIC_FILE = "BY_MODE"
                    elif label == "SOUNDS":
                        SOUND_VOLUME = 0.0 if SOUND_VOLUME > 0 else .7
                        None
                    elif label == "MUSIC":
                        MUSIC_VOLUME = 0.0 if MUSIC_VOLUME > 0 else .75
                        MENU_MUSIC_VOLUME = MUSIC_VOLUME
                        if AUDIO_OK:
                            pygame.mixer.music.set_volume(MUSIC_VOLUME)
                    elif label == "SCREEN SHAKE":
                        SCREEN_SHAKE_ENABLED = not SCREEN_SHAKE_ENABLED
                    elif label == "IMPACT FLASH":
                        IMPACT_FLASH_ENABLED = not IMPACT_FLASH_ENABLED
                    elif label == "BACK":
                        menu.set_state(menu.return_menu)
                        mode = "paused" if menu.return_menu == MENU_PAUSE else "menu"
                elif menu.state == MENU_HACKS:
                    menu.activate_hack(label)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if PORTABLE_TOUCH and pygame.time.get_ticks()-touch_controller.last_finger_ms<140:
                continue
            if pygame.time.get_ticks() < menu.click_lock_until:
                continue
            if mode == "playing":
                if not game.dead:
                    if game.hardcore_mode or (game.sandbox_mode and game.weapon_active_timer>0):
                        game.fire_weapon()
                    else:
                        game.player.request_jump()
            elif mode == "spawner":
                spawner_type=menu.selected_spawner_type()
                if spawner_type=="orb":
                    game.spawn_sandbox_orb(menu.selected_spawner_kind(),event.pos[0],event.pos[1])
                elif spawner_type=="powerup":
                    game.spawn_sandbox_powerup(menu.selected_spawner_kind(),event.pos[0],event.pos[1])
                elif spawner_type=="weapon":
                    game.spawn_sandbox_weapon(menu.selected_spawner_kind(),event.pos[0],event.pos[1])
                elif spawner_type=="platform":
                    game.spawn_sandbox_platform(event.pos[0],event.pos[1],menu.spawner_platform_w,menu.spawner_platform_h)
                else:
                    game.spawn_sandbox_entity(menu.selected_spawner_kind(),event.pos[0],event.pos[1])
            elif mode != "starting":
                                                                           
                menu.hover(event.pos)
                if 0 <= menu.index < len(menu.items()):
                    label=menu.selected_label()
                    if menu.state == MENU_MAIN:
                        if label == "PLAY":
                            menu.set_state(MENU_PLAY)
                        elif label == "OPTIONS":
                            menu.open_options(MENU_MAIN)
                        elif label == "QUIT":
                            running=False
                    elif menu.state == MENU_PLAY:
                        if label == "MAIN":
                            begin_play_transition("main")
                        elif label == "MARDCORE":
                            begin_play_transition("mardcore")
                        elif label == "SANDBOX":
                            begin_play_transition("sandbox")
                        elif label == "BACK":
                            menu.set_state(MENU_MAIN)
                    elif menu.state == MENU_PAUSE:
                        if label == "RESUME":
                            mode="playing"
                        elif label == "OPTIONS":
                            menu.open_options(MENU_PAUSE)
                            mode="menu"
                        elif label == "MAIN MENU":
                            game.save_best(); game.start_menu_music(); menu.set_state(MENU_MAIN); mode="menu"
                        elif label == "QUIT":
                            running=False
                    elif menu.state == MENU_HACKS:
                        menu.activate_hack(label)
                    elif menu.state == MENU_PERMANENT_POWERS:
                        menu.activate_permanent_power(label)
                    elif menu.state == MENU_OPTIONS:
                        if label == "FULLSCREEN":
                            old_w,old_h,new_w,new_h=apply_display(not FULLSCREEN)
                            game.on_display_change(old_w,old_h,new_w,new_h)
                        elif label == "GRAPHICS":
                            GRAPHICS_QUALITY=(GRAPHICS_QUALITY+1)%len(GRAPHICS_LEVELS)
                            save_settings()
                        elif label == "MENU SONG":
                            MENU_MUSIC_FILE = cycle_song(MENU_MUSIC_FILE, 1)
                            save_settings()
                            game.start_menu_music()
                        elif label == "GAMEPLAY SONG":
                            GAME_MUSIC_FILE = "BY_MODE"
                            save_settings()
                        elif label == "SOUNDS":
                            SOUND_VOLUME = 0.0 if SOUND_VOLUME > 0 else .7
                            save_settings()
                            None
                        elif label == "MUSIC":
                            MUSIC_VOLUME = 0.0 if MUSIC_VOLUME > 0 else .75
                            MENU_MUSIC_VOLUME = MUSIC_VOLUME
                            save_settings()
                            if AUDIO_OK:
                                pygame.mixer.music.set_volume(MUSIC_VOLUME)
                        elif label == "SCREEN SHAKE":
                            SCREEN_SHAKE_ENABLED = not SCREEN_SHAKE_ENABLED
                            save_settings()
                        elif label == "IMPACT FLASH":
                            IMPACT_FLASH_ENABLED = not IMPACT_FLASH_ENABLED
                            save_settings()
                        elif label == "BACK":
                            menu.set_state(menu.return_menu)
                            mode="paused" if menu.return_menu == MENU_PAUSE else "menu"
                    elif menu.state == MENU_HACKS:
                        menu.activate_hack(label)

        elif event.type == pygame.VIDEORESIZE and not FULLSCREEN:
            if pygame.time.get_ticks() >= DISPLAY_SWITCH_UNTIL:
                old_w, old_h = WIDTH, HEIGHT
                WIDTH, HEIGHT = max(800,event.w), max(600,event.h)
                WINDOWED_SIZE[0], WINDOWED_SIZE[1] = WIDTH, HEIGHT
                screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE|pygame.DOUBLEBUF)
                WIDTH, HEIGHT = screen.get_size()
                save_settings()
                game.on_display_change(old_w,old_h,WIDTH,HEIGHT)

    desktop_entities.update()
    if mode == "spawner" and game.sandbox_mode and not FULLSCREEN:
        gm = desktop_entities.global_mouse()
        if gm is not None:
            gx, gy, left_down = gm
            rect = desktop_entities.window_rect()
            outside = rect is not None and not (rect[0] <= gx <= rect[2] and rect[1] <= gy <= rect[3])
            if left_down and not desktop_entities.last_left and outside and menu.selected_spawner_type()=="entity":
                desktop_entities.spawn(menu.selected_spawner_kind(), gx, gy)
            desktop_entities.last_left = left_down
    else:
        gm = desktop_entities.global_mouse()
        if gm is not None:
            desktop_entities.last_left = gm[2]

    if mode == "starting":
        play_lens_t += dt
                                                                            
        game.draw()
        draw_lens_circle(play_lens_t / PLAY_LENS_DURATION)
        if play_lens_t >= PLAY_LENS_DURATION:
            play_lens_active = False
            mode = "playing"
    elif mode == "playing":
        update_death_music_pitch(dt)
        game.update(dt)
        game.draw()
        if play_lens_active:
            play_lens_t += dt
            draw_lens_circle(play_lens_t / PLAY_LENS_DURATION)
            if play_lens_t >= PLAY_LENS_DURATION:
                play_lens_active = False
    elif mode == "spawner":
        game.draw()
        menu.draw_spawner_overlay()
        touch_controller.draw_spawner_controls(menu)
    elif mode == "paused":
                                                                                    
        game.draw()
        shade=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        shade.fill((0,0,0,150))
        screen.blit(shade,(0,0))
                                                                                   
        if menu.state not in (MENU_PAUSE, MENU_HACKS):
            menu.set_state(MENU_PAUSE)
        menu.draw_items()
        y=95+math.sin(menu.t*2.6)*8
        draw_text('HACKS' if menu.state == MENU_HACKS else 'PAUSED',font_title,WHITE,WIDTH/2,y,center=True)
        pts=[]
        for i in range(60):
            f=i/59; x=WIDTH*.32+f*WIDTH*.36
            yy=y+55+math.sin(menu.t*6+f*math.tau*3)*4
            pts.append((x,yy))
        pygame.draw.lines(screen,CYAN,False,pts,3)
        menu.draw_footer()
    else:
        menu.draw()

    pygame.display.flip()

game.save_best()
save_settings()
desktop_entities.clear()
pygame.quit()
sys.exit()
