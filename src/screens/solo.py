import math
import pygame
from src.core.scene import Scene
from src.core.physics import create_space, update_space, reset_body_momentum
from src.levels.map_loader import load_raw_map_data, get_random_map_name
from src.levels.level_factory import build_level
from src.systems.slingshot import Slingshot
from src.systems.renderer import draw_entities, draw_aim_line
from src.utils.ui import draw_text, draw_button, draw_overlay
from src.constants import SHOOT_SPEED_THRESHOLD

class SoloScene(Scene):
    def __init__(self):
        self.next = None
        self.space = create_space()
        self.walls, self.ball, self.hole = build_level(self.space, load_raw_map_data(get_random_map_name()))
        
        self.slingshot = Slingshot()
        
        self.score = 0
        self.is_won = False
        self.win_timer = 0
        self.current_mouse_pos = (0, 0)

        # Panneau latéral de logs / debug dépliable
        self.show_debug_panel = False
        self.btn_toggle_debug = pygame.Rect(20, 60, 90, 30)
        self.logs = ["Système initialisé"]
        self._was_in_cuvette = False
        self._was_stopped = True

    def add_log(self, msg):
        time_str = f"[{pygame.time.get_ticks() // 1000}s]"
        self.logs.append(f"{time_str} {msg}")
        if len(self.logs) > 8:
            self.logs.pop(0)

    def _get_quit_btn(self):
        from src.constants import WIDTH
        return pygame.Rect(WIDTH - 120, 20, 100, 40)

    def process_inputs(self, inputs):
        self.current_mouse_pos = inputs.mouse_pos
        
        if inputs.escape:
            self.next = "MENU"
            
        if inputs.mouse_down:
            panel_rect = pygame.Rect(20, 60, 280, 410) if self.show_debug_panel else self.btn_toggle_debug
            if self._get_quit_btn().collidepoint(inputs.mouse_down):
                self.next = "MENU"
            elif self.btn_toggle_debug.collidepoint(inputs.mouse_down):
                self.show_debug_panel = not self.show_debug_panel
            elif self.show_debug_panel and panel_rect.collidepoint(inputs.mouse_down):
                pass
            elif not self.is_won and self.ball.is_stopped():
                self.slingshot.start(inputs.mouse_down, self.ball)
                
        if inputs.mouse_up and self.slingshot.aiming and not self.is_won:
            if self.slingshot.release(inputs.mouse_up, self.ball):
                self.score += 1
                self.add_log(f"Tir #{self.score} (V: {self.ball.speed:.0f} px/s)")

    def update(self):
        dist = math.hypot(self.hole.pos[0] - self.ball.pos[0], self.hole.pos[1] - self.ball.pos[1])
        in_cuvette = dist < self.hole.influence_radius
        if in_cuvette and not self._was_in_cuvette and not self.is_won:
            self.add_log("Entrée cuvette")
        self._was_in_cuvette = in_cuvette

        is_stopped = self.ball.is_stopped()
        if is_stopped and not self._was_stopped and not self.is_won:
            self.add_log("Balle stabilisée")
        self._was_stopped = is_stopped

        if not self.is_won:
            self.hole.apply_gravity(self.ball)

        update_space(self.space)

        if not self.is_won and self.hole.is_ball_in(self.ball):
            self.is_won = True
            self.win_timer = pygame.time.get_ticks()
            reset_body_momentum(self.ball.body)
            self.add_log("Trou marqué !")

        if self.is_won and pygame.time.get_ticks() - self.win_timer > 2000:
            self.next = "SOLO"

    def _draw_debug_panel(self, screen):
        label = "◀ Logs" if self.show_debug_panel else "▶ Logs"
        draw_button(screen, label, self.btn_toggle_debug, (40, 50, 60), (60, 75, 90), self.current_mouse_pos, 18)

        if not self.show_debug_panel:
            return

        panel_w, panel_h = 280, 360
        panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_surf.fill((20, 25, 32, 225))
        pygame.draw.rect(panel_surf, (70, 85, 100), (0, 0, panel_w, panel_h), 2, border_radius=8)

        dist = math.hypot(self.hole.pos[0] - self.ball.pos[0], self.hole.pos[1] - self.ball.pos[1])
        if dist < self.hole.radius:
            cuvette_str = "Dans le trou"
            cuvette_col = (255, 215, 0)
        elif dist < self.hole.influence_radius:
            cuvette_str = "Attraction cuvette"
            cuvette_col = (80, 200, 255)
        else:
            cuvette_str = "Hors zone"
            cuvette_col = (180, 180, 180)

        ready = self.ball.is_stopped()
        status_str = "Prêt à tirer" if ready else "En mouvement"
        status_col = (100, 255, 100) if ready else (255, 160, 160)

        lines = [
            ("--- ÉTAT PHYSIQUE ---", (220, 220, 220)),
            (f"Pos : ({self.ball.pos[0]}, {self.ball.pos[1]})", (255, 255, 255)),
            (f"Vitesse : {self.ball.speed:.1f} px/s", (255, 255, 255)),
            (f"Vx : {self.ball.body.velocity.x:.1f} | Vy : {self.ball.body.velocity.y:.1f}", (200, 200, 200)),
            (f"Seuil tir : {SHOOT_SPEED_THRESHOLD} px/s", (200, 200, 200)),
            (f"Statut : {status_str}", status_col),
            (f"Dist. trou : {dist:.1f} px", (255, 255, 255)),
            (f"Cuvette : {cuvette_str}", cuvette_col),
            ("--- DERNIERS ÉVÉNEMENTS ---", (220, 220, 220)),
        ]

        y_offset = 12
        for text, col in lines:
            draw_text(panel_surf, text, (14, y_offset), font_size=16, color=col)
            y_offset += 24

        for log in self.logs[-4:]:
            draw_text(panel_surf, log, (14, y_offset), font_size=14, color=(160, 210, 255))
            y_offset += 20

        screen.blit(panel_surf, (20, 100))

    def render(self, screen):
        draw_entities(screen, self.walls, self.ball, self.hole, hide_ball=self.is_won)
        
        aim_vector = self.slingshot.get_aim_vector(self.current_mouse_pos)
        draw_aim_line(screen, self.ball.pos, aim_vector)
        
        draw_text(screen, f"Hits : {self.score}", (20, 20))
        draw_button(screen, "Leave", self._get_quit_btn(), (150, 50, 50), (200, 50, 50), self.current_mouse_pos, 20)

        # Panneau dépliable de logs
        self._draw_debug_panel(screen)

        w, h = screen.get_size()
        ready = self.ball.is_stopped()
        color = (100, 255, 100) if ready else (255, 180, 180)
        draw_text(screen, f"Vitesse: {self.ball.speed:.1f} / {SHOOT_SPEED_THRESHOLD}", (w - 230, h - 35), font_size=20, color=color)

        if self.is_won:
            w, h = screen.get_size()
            draw_overlay(screen)
            draw_text(screen, "Scored !", (w//2, h//2), 50, (255, 215, 0), center=True)

    def get_next_scene(self):
        return self.next