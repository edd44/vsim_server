import pygame


class Window():
    def __init__(self):
        self.width = 1600
        self.height = 850
        self.center = [int(self.width/2), int(self.height)/2]
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.font = pygame.font.SysFont("calibri", 30)
        self.pitch_label_pos = (self.width / 2, 10)
        self.roll_label_pos = (10, self.height / 2)
        self.lservo_label_pos = (10, self.height-30)
        self.rservo_label_pos = (self.width-70, self.height-30)

    def set_pitch_value(self, value):
        self.screen.blit(self.font.render(str(int(value*100)), True, (255, 255, 255)), self.pitch_label_pos)
        pygame.draw.line(self.screen, (255,0,0), self.center, [self.width/2, self.height/2+int(value*100*20)], 10)

    def set_roll_value(self, value):
        self.screen.blit(self.font.render(str(int(value*100)), True, (255, 255, 255)), self.roll_label_pos)
        pygame.draw.line(self.screen, (255,0,0), self.center, [self.width/2+int(value*100*20), self.height/2], 10)

    def set_rservo_value(self, value):
        self.screen.blit(self.font.render(str(value), True, (255, 255, 255)), self.rservo_label_pos)

    def set_lservo_value(self, value):
        self.screen.blit(self.font.render(str(value), True, (255, 255, 255)), self.lservo_label_pos)
