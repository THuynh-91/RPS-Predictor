from manim import *

class TestLatexAlignment(Scene):
    def construct(self):
        # Test 1: Simple {l r} array
        test1 = MathTex(
            r"\frac{"
            r"\begin{array}{l r}"
            r"\text{Total Wins:} & 2"
            r"\end{array}"
            r"}{"
            r"\begin{array}{l r}"
            r"\text{Total Loss:} & 1"
            r"\end{array}"
            r"}",
            font_size=40
        ).shift(UP * 2.5)
        
        # Test 2: Just text without array
        test2 = MathTex(
            r"\frac{"
            r"\text{Total Wins: } 2"
            r"}{"
            r"\text{Total Loss: } 1"
            r"}",
            font_size=40
        ).shift(UP * 0.5)
        
        # Test 3: Using \quad for spacing
        test3 = MathTex(
            r"\frac{"
            r"\text{Total Wins:}\quad 2"
            r"}{"
            r"\text{Total Loss:}\quad 1"
            r"}",
            font_size=40
        ).shift(DOWN * 1.5)
        
        label1 = Text("Test 1: array {l r}", font_size=20).next_to(test1, LEFT, buff=0.5)
        label2 = Text("Test 2: plain text", font_size=20).next_to(test2, LEFT, buff=0.5)
        label3 = Text("Test 3: \\quad spacing", font_size=20).next_to(test3, LEFT, buff=0.5)
        
        self.add(test1, test2, test3, label1, label2, label3)
        self.wait(2)