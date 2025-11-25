from manim import *

MOVE_COLOR = {"R": RED, "P": BLUE, "S": GREEN}
RESULT_COLOR = {"win": GREEN, "lose": RED, "tie": GRAY}

class TestMoveHistory(Scene):
    def construct(self):
        # Title
        move_history_title = Text("Move History:", font_size=24, color=YELLOW)
        move_history_title.shift(UP * 2 + RIGHT * 3)
        
        # Add header row showing M vs P - make columns match entry structure
        # Round number column - use actual text to match width
        header_round = Text("R#:", font_size=14, color=GRAY)
        header_round_container = VGroup(header_round)
        header_round_container.set_width(0.4)
        
        m_label = Text("M", font_size=14, color=YELLOW, weight=BOLD)
        vs_header = Text("vs", font_size=12, color=GRAY)
        p_label = Text("P", font_size=14, color=YELLOW, weight=BOLD)
        
        header_center = VGroup(m_label, vs_header, p_label).arrange(RIGHT, buff=0.1)
        header_center_container = VGroup(header_center)
        header_center_container.set_width(1.0)
        
        result_header = Text("Result", font_size=14, color=GRAY)
        result_header_container = VGroup(result_header)
        result_header_container.set_width(0.75)
        
        header_entry = VGroup(header_round_container, header_center_container, result_header_container).arrange(RIGHT, buff=0.15)
        header_entry.next_to(move_history_title, DOWN, buff=0.25)
        
        # Center align the title above the entire header
        move_history_title.move_to(header_entry.get_center() + UP * 0.6)
        
        self.add(move_history_title)
        self.add(header_entry)
        
        # Create sample entries
        sample_data = [
            (1, "R", "S", "win"),
            (2, "R", "S", "win"),
            (3, "R", "R", "tie"),
            (4, "P", "P", "tie"),
            (5, "P", "S", "lose"),
        ]
        
        for i, (round_num, ai_move, opp_move, result) in enumerate(sample_data):
            entry = self._create_history_entry(round_num, ai_move, opp_move, result)
            entry.next_to(header_entry, DOWN, buff=0.15 + i * 0.35)
            self.add(entry)
        
        self.wait(2)
    
    def _create_history_entry(self, round_num, ai_move, opp_move, result):
        # Round label
        round_label = Text(f"R{round_num}:", font_size=14, color=GRAY)
        round_label_container = VGroup(round_label)
        round_label_container.set_width(0.4)

        # Moves
        ai_circle = Circle(
            radius=0.12, color=MOVE_COLOR[ai_move], fill_opacity=0.4
        ).set_stroke(width=1.5)
        ai_text = Text(ai_move, font_size=12, color=WHITE)
        ai_token = VGroup(ai_circle, ai_text)

        vs_text = Text("vs", font_size=12, color=GRAY)

        opp_circle = Circle(
            radius=0.12, color=MOVE_COLOR[opp_move], fill_opacity=0.4
        ).set_stroke(width=1.5)
        opp_text = Text(opp_move, font_size=12, color=WHITE)
        opp_token = VGroup(opp_circle, opp_text)

        center_group = VGroup(ai_token, vs_text, opp_token).arrange(RIGHT, buff=0.1)
        center_container = VGroup(center_group)
        center_container.set_width(1.0)

        # Result text
        result_text = Text(
            f"({result})",
            font_size=16,
            color=RESULT_COLOR[result],
        )

        box_width = 0.75
        box_height = result_text.height * 1.2
        box = Rectangle(
            width=box_width,
            height=box_height,
            stroke_width=0,
            fill_opacity=0,
        )
        result_text.move_to(box.get_center())
        result_container = VGroup(box, result_text)

        entry = VGroup(
            round_label_container, center_container, result_container
        ).arrange(RIGHT, buff=0.15)

        return entry