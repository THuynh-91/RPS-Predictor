from manim import *

MAX_HISTORY = 6
ROW_GAP = 0.35

MOVE_COLOR = {"R": RED, "P": BLUE, "S": GREEN}
RESULT_COLOR = {"win": GREEN, "lose": RED, "tie": GRAY}


class ScrollTest(Scene):
    def construct(self):
        # ---------- Title ----------
        title = Text("Move History:", font_size=32, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        # ============================================================
        #  HEADER: 3 fixed-width columns (R#, M vs P, Result)
        # ============================================================

        # --- Round column (header) ---
        hdr_round_text = Text("R#:", font_size=14, color=GRAY)
        hdr_round_box = Rectangle(
            width=0.4,
            height=hdr_round_text.height * 1.3,
            stroke_width=0,
            fill_opacity=0,       # invisible
            fill_color=BLACK,
        )
        hdr_round_text.move_to(hdr_round_box)
        hdr_round_text.align_to(hdr_round_box, LEFT)   # left-align inside column
        hdr_round_col = VGroup(hdr_round_box, hdr_round_text)

        # --- Middle column: M vs P (header) ---
        m_label = Text("M", font_size=14, color=YELLOW)
        vs_header = Text("vs", font_size=12, color=GRAY)
        p_label = Text("P", font_size=14, color=YELLOW)
        hdr_mid_inner = VGroup(m_label, vs_header, p_label).arrange(RIGHT, buff=0.1)

        hdr_mid_box = Rectangle(
            width=1.0,
            height=hdr_mid_inner.height * 1.3,
            stroke_width=0,
            fill_opacity=0,
            fill_color=BLACK,
        )
        hdr_mid_inner.move_to(hdr_mid_box)
        hdr_mid_col = VGroup(hdr_mid_box, hdr_mid_inner)

        # --- Result column (header) ---
        hdr_result_text = Text("Result", font_size=14, color=GRAY)
        hdr_result_box = Rectangle(
            width=0.75,
            height=hdr_result_text.height * 1.3,
            stroke_width=0,
            fill_opacity=0,
            fill_color=BLACK,
        )
        hdr_result_text.move_to(hdr_result_box)
        hdr_result_col = VGroup(hdr_result_box, hdr_result_text)

        header = VGroup(hdr_round_col, hdr_mid_col, hdr_result_col).arrange(
            RIGHT, buff=0.15
        )
        header.next_to(title, DOWN, buff=0.3)
        self.add(header)

        # ---------- Move history container ----------
        move_history = VGroup()

        # Fake data to test colors + scroll
        rounds = [
            ("R", "S", "win"),
            ("R", "S", "win"),
            ("R", "R", "tie"),
            ("P", "P", "tie"),
            ("P", "S", "lose"),
            ("P", "P", "tie"),
            ("R", "P", "lose"),
            ("R", "R", "tie"),
            ("S", "P", "win"),
            ("S", "S", "tie"),
            ("P", "R", "win"),
            ("R", "S", "win"),
        ]

        def create_entry(idx, ai_move, opp_move, result_key):
            # ---------- Round column ----------
            round_text = Text(f"R{idx}:", font_size=14, color=GRAY)
            round_box = Rectangle(
                width=0.4,
                height=round_text.height * 1.3,
                stroke_width=0,
                fill_opacity=0,
                fill_color=BLACK,
            )
            round_text.move_to(round_box)
            round_text.align_to(round_box, LEFT)  # left-align text like header
            round_col = VGroup(round_box, round_text)

            # ---------- Middle column: M vs P ----------
            ai_circle = Circle(
                radius=0.12,
                color=MOVE_COLOR[ai_move],
                fill_opacity=0.4,
            ).set_stroke(width=1.5)
            ai_letter = Text(ai_move, font_size=12, color=WHITE)
            ai_token = VGroup(ai_circle, ai_letter)

            vs = Text("vs", font_size=12, color=GRAY)

            opp_circle = Circle(
                radius=0.12,
                color=MOVE_COLOR[opp_move],
                fill_opacity=0.4,
            ).set_stroke(width=1.5)
            opp_letter = Text(opp_move, font_size=12, color=WHITE)
            opp_token = VGroup(opp_circle, opp_letter)

            mid_inner = VGroup(ai_token, vs, opp_token).arrange(RIGHT, buff=0.1)

            mid_box = Rectangle(
                width=1.0,
                height=mid_inner.height * 1.3,
                stroke_width=0,
                fill_opacity=0,
                fill_color=BLACK,
            )
            mid_inner.move_to(mid_box)
            mid_col = VGroup(mid_box, mid_inner)

            # ---------- Result column ----------
            res_text = Text(
                f"({result_key})",
                font_size=16,
                color=RESULT_COLOR[result_key],
            )
            res_box = Rectangle(
                width=0.75,
                height=res_text.height * 1.3,
                stroke_width=0,
                fill_opacity=0,
                fill_color=BLACK,
            )
            res_text.move_to(res_box)
            res_col = VGroup(res_box, res_text)

            entry = VGroup(round_col, mid_col, res_col).arrange(RIGHT, buff=0.15)
            return entry

        # ============================================================
        #  Main test loop
        # ============================================================

        for idx, (ai_move, opp_move, result_key) in enumerate(rounds, start=1):
            entry = create_entry(idx, ai_move, opp_move, result_key)

            if len(move_history) < MAX_HISTORY:
                # Build-up phase
                pos_index = len(move_history)
                entry.next_to(
                    header,
                    DOWN,
                    buff=0.15 + pos_index * ROW_GAP,
                )
                move_history.add(entry)
                self.play(FadeIn(entry), run_time=0.25)

            else:
                # Scroll phase
                old_entry = move_history[0]

                # Start new entry just below visible block
                start_buff = 0.15 + MAX_HISTORY * ROW_GAP
                entry.next_to(header, DOWN, buff=start_buff)

                move_history.add(entry)
                self.add(entry)

                animations = []

                # Re-layout remaining rows (1..end) under header
                for i, e in enumerate(move_history[1:], start=0):
                    e.generate_target()
                    e.target.next_to(
                        header,
                        DOWN,
                        buff=0.15 + i * ROW_GAP,
                    )

                    # Use Transform instead of MoveToTarget to fully redraw
                    animations.append(Transform(e, e.target))

                # Top row fades out
                animations.append(FadeOut(old_entry))

                self.play(*animations, run_time=0.3)

                move_history.remove(old_entry)
                self.remove(old_entry)

            self.wait(0.1)
