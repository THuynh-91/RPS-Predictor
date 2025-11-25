from manim import *

class TestVGroupAlignment(Scene):
    def construct(self):
        # Build the fraction manually with VGroups for perfect control
        
        # Create all text elements
        wins_label = Text("Total Wins:", font_size=18, color=WHITE)
        wins_num = Text("2", font_size=18, color=WHITE)
        loss_label = Text("Total Loss:", font_size=18, color=WHITE) 
        loss_num = Text("1", font_size=18, color=WHITE)
        
        # Position numerator: label on left, number on right with fixed gap
        wins_num.next_to(wins_label, RIGHT, buff=0.8)
        numerator = VGroup(wins_label, wins_num)
        
        # Position denominator: match the numerator layout
        loss_num.next_to(loss_label, RIGHT, buff=0.8)
        # Align loss number directly below wins number
        loss_num.align_to(wins_num, RIGHT)
        denominator = VGroup(loss_label, loss_num)
        
        # Create fraction bar
        bar_length = max(numerator.width, denominator.width) * 1.1
        fraction_bar = Line(LEFT * bar_length/2, RIGHT * bar_length/2, color=WHITE, stroke_width=2)
        
        # Stack vertically
        fraction = VGroup(numerator, fraction_bar, denominator).arrange(DOWN, buff=0.15)
        
        # Add Win Rate label
        win_rate_label = Text("Win Rate =", font_size=20, color=YELLOW)
        win_rate_label.next_to(fraction, LEFT, buff=0.3)
        
        full_equation = VGroup(win_rate_label, fraction)
        
        self.add(full_equation)
        self.wait(2)