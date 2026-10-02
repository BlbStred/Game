# Provides video function, where
# Right mouse button starts video
# Left  mouse button stops video and advances 1 frame

# See integrals.py for an example of usage

# User specifies what objects to display --
# polygons, lines, text
# He specifies sizes and positions in his own x-y coordinates.
# For that he needs to provide a window dimensions in his x-y coordinates.
# These dimensions are mapped on physical window, which that allow
# translation from x-y coordimates to physical coordinates


import pygame
import mylib


class Video:

    def __init__(self, speed,
                 xmin, xmax, ymin, ymax):  # dimensions of total window 

        pygame.init()

        # Set screen to almost fill in existing display,
        # but making the aspect ration same
        aspectRatio = (ymax - ymin)/(xmax - xmin)

        # height/width = aspectRatio

        # Try maximum width
        width  = 1200
        height =  width * aspectRatio
        if height > 600:
            height = 600
            width = height/aspectRatio

        margin = 30
        self.screen = pygame.display.set_mode((width+margin, height+margin))

        # Prepare translation from x-y coordinates to self.screen coordinates
        # These three numbers are used in the function scale() 
        self.xscale = width/(xmax-xmin)
        self.yscale = height/(ymax-ymin)        
        self.origin = ((0-xmin)*self.xscale, (ymax-0)*self.yscale)  # where to place origin of x-y coordinates
        
        self.font = pygame.font.SysFont('couriernew', 20)
        
        self.speed = speed   # initial value, increased by scrolling up, decreased by scrolling down


    # translate pos in x-y coordinates to screen coordinates
    def scale(self, pos):
        x, y = pos
        return (self.origin[0] + x*self.xscale,
                self.origin[1] - y*self.yscale)

    
    # translate screen coordinates to in x-y coordinates
    def unscale(self, pos):
        s, t = pos
        return ((s - self.origin[0])/self.xscale,
                -(t - self.origin[1])/self.yscale)


    # draw line from point0 to point1
    def line(self, point0, point1, color, width):
        if mylib.isNone((point0, point1)) == False:
            pygame.draw.line(self.screen, color, self.scale(point0), self.scale(point1), width)
        

    # draw polygon from a list of points
    # if with == 0 then it will be filled with given color,
    # otherwise it just draws the outline with given color
    def polygon(self, points, color, width):
        pygame.draw.polygon(self.screen, color, [self.scale(p) for p in points], width)


    def circle(self, center, radius, color, width):
        pygame.draw.circle(self.screen, color, self.scale(center), radius, width=width)
        

    # Place give string data as given position
    def text(self, data, pos, color): 
        text_surface = self.font.render(data, True, color)
        text_rect = text_surface.get_rect()
        text_rect.x, text_rect.y = self.scale(pos)
        self.screen.blit(text_surface, text_rect)


    def textWithBackground(self, data, pos, color):
        x, y = self.scale(pos)
        pygame.draw.polygon(self.screen, 'white', [(x-10,              y-10),
                                                   (x-10,              y+25),
                                                   (x+10+len(data)*14, y+25),
                                                   (x+10+len(data)*14, y-10)], 0)
        self.text(data, pos, color)

    # Start the video
    # it calls application.run() to provided contents
    # the application can use the above utilities
    
    def video(self, application):
    
        state = 'wait'   # do not change picture until a mouse is clicked

        # The variable time keeps incrementing accoring to specified speed
        # It is passed to the application, which can use it do decide
        # wheter to provide a changed frame, or redisplay previous frame
        time = -1
        
        running = True
        while running:
            
            mouse = 'none'  # set below is any mouse event

            # Check if any event happened
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                
                if event.type == pygame.MOUSEWHEEL:
                    if (event.y > 0): self.speed = self.speed * 1.1 #roll up   to increase by 10%
                    if (event.y < 0): self.speed = self.speed / 1.1 #roll down to decrease by 10%
                                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    match(event.button):
                        case 1:       # Left click -- make only one step until next mouse click
                            mouse = 'left'
                            state = 'step'
                            time  = time + 1
                        case 3:        # Right click -- keeps updating screen with any new picture from application
                            mouse = 'right'
                            state = 'steps'
            
            if state == 'wait': continue        # Wait from a mouse click
            if state == 'step': state = 'wait'  # Redisplay screen below, then wait for a mouse click
    
            self.screen.fill("white")           # Discard what was there before


            
            application.run(time, mouse, self.unscale((mouse_x, mouse_y)))  # application provides a picture

        

            time  = time + self.speed

            pygame.display.flip()               # actually display
    
    
        pygame.quit()

