from manim import *
import pandas as pd

DATA_FILE = "../results/results_random_vs_repeater.csv"
SHOW_ROUNDS = 2001  # Process through round 10001
ANIMATED_ROUNDS = 3  # Animate first 5 rounds
FINAL_ROUND = 2001  # Also animate the final round
UPDATE_INTERVAL = 50  # Update visuals every N rounds during fast-forward
ROW_GAP = 0.35
MAX_HISTORY = 6

MOVE_COLOR = {"R": RED, "P": BLUE, "S": GREEN}
RESULT_COLOR = {"win": GREEN, "lose": RED, "tie": GRAY}
LABELS = {"R": "Rock", "P": "Paper", "S": "Scissors"}
ALL_MOVES = ["R", "P", "S"]


class RPSPlayback(Scene):
    def construct(self):
        df = pd.read_csv(DATA_FILE).head(SHOW_ROUNDS)

        # Title
        title = Text("Random vs Repeater (2k rounds)", font_size=36)
        title.to_edge(UP, buff=0.4)
        self.add(title)

        # Score trackers
        win_tracker = ValueTracker(0)
        loss_tracker = ValueTracker(0)
        tie_tracker = ValueTracker(0)

        # Scoreboard
        scoreboard = self._scoreboard(win_tracker, loss_tracker, tie_tracker)
        scoreboard.next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        self.add(scoreboard)

        # Accuracy graph title
        accuracy_title = Text("Prediction Accuracy:", font_size=22, color=YELLOW)
        accuracy_title.next_to(scoreboard, DOWN, buff=0.5).align_to(scoreboard, LEFT)
        self.add(accuracy_title)

        # Axes for accuracy graph
        axes = Axes(
            x_range=[0, SHOW_ROUNDS, SHOW_ROUNDS//10],
            y_range=[0, 100, 20],
            x_length=4,
            y_length=3,
            axis_config={"color": GRAY, "include_numbers": False},
            tips=False,
        )
        axes.next_to(accuracy_title, DOWN, buff=0.3).align_to(accuracy_title, LEFT)

        x_label = Text("Rounds", font_size=16, color=GRAY).next_to(axes, DOWN, buff=0.2)
        y_label = Text("Accuracy %", font_size=16, color=GRAY).next_to(
            axes, LEFT, buff=0.2
        ).rotate(90 * DEGREES)
        self.add(axes, x_label, y_label)

        # Accuracy tracking
        accuracy_data = []
        correct_predictions = 0
        total_predictions = 0

        # Move history setup
        move_history_title, header_entry, move_history = self._setup_move_history(title)

        # Static Win Rate % text
        win_rate_center = Text("Win Rate: --%", font_size=24, color=GREEN)
        win_rate_center.move_to(ORIGIN).shift(UP * 0.7)
        self.add(win_rate_center)

        # Bottom-right Win-Rate block
        def get_win_rate_group():
            wins = int(win_tracker.get_value())
            losses = int(loss_tracker.get_value())

            if wins == 0 and losses == 0:
                wins_str = "--"
                loss_str = "--"
            elif losses == 0:
                wins_str = str(wins) if wins > 0 else "--"
                loss_str = "--"
            else:
                wins_str = str(wins)
                loss_str = str(losses)

            wins_label = Text("Total Wins:", font_size=18, color=WHITE)
            wins_num = Text(wins_str, font_size=18, color=WHITE)
            loss_label = Text("Total Loss:", font_size=18, color=WHITE)
            loss_num = Text(loss_str, font_size=18, color=WHITE)
            
            wins_num.next_to(wins_label, RIGHT, buff=0.8)
            numerator = VGroup(wins_label, wins_num)
            
            loss_num.next_to(loss_label, RIGHT, buff=0.8)
            loss_num.align_to(wins_num, RIGHT)
            denominator = VGroup(loss_label, loss_num)
            
            bar_length = max(numerator.width, denominator.width) * 1.1
            fraction_bar = Line(LEFT * bar_length/2, RIGHT * bar_length/2, color=WHITE, stroke_width=2)
            
            fraction = VGroup(numerator, fraction_bar, denominator).arrange(DOWN, buff=0.15)
            
            win_rate_label_text = Text("Win Rate =", font_size=20, color=YELLOW)
            win_rate_label_text.next_to(fraction, LEFT, buff=0.3)
            
            return VGroup(win_rate_label_text, fraction)

        win_rate_group = get_win_rate_group()
        win_rate_group.to_edge(DOWN + RIGHT, buff=0.4)
        self.add(win_rate_group)

        accuracy_line = None
        
        # Fast forward indicator
        ff_text = Text("Fast Forwarding...", font_size=32, color=YELLOW)
        ff_text.move_to(ORIGIN)

        # Main loop over rounds
        for idx, row in df.iterrows():
            round_num = int(row["round"])
            ai_move = row["model_move"]
            opp_move = row["opponent_move"]
            prediction = row.get("model_prediction", None)
            result = row["result"]
            
            is_animated = (round_num <= ANIMATED_ROUNDS) or (round_num == FINAL_ROUND)
            should_update_visual = is_animated or (round_num % UPDATE_INTERVAL == 0)
            
            if round_num == ANIMATED_ROUNDS + 1:
                self.play(FadeIn(ff_text), run_time=0.3)
            
            if round_num == FINAL_ROUND and FINAL_ROUND > ANIMATED_ROUNDS:
                self.play(FadeOut(ff_text), run_time=0.3)

            if is_animated:
                round_txt = Text(f"Round {round_num}", font_size=30)
                round_txt.next_to(win_rate_center, DOWN, buff=0.5)
                self.play(FadeIn(round_txt), run_time=0.3)
                self._show_selection(round_txt, ai_move, opp_move)
                self.play(FadeOut(round_txt), run_time=0.2)

            if result == "win":
                win_tracker.increment_value(1)
            elif result == "lose":
                loss_tracker.increment_value(1)
            else:
                tie_tracker.increment_value(1)

            if should_update_visual:
                new_scoreboard = self._scoreboard(win_tracker, loss_tracker, tie_tracker)
                new_scoreboard.move_to(scoreboard)
                
                new_group = get_win_rate_group()
                new_group.move_to(win_rate_group)
                
                if is_animated:
                    self.play(
                        Transform(scoreboard, new_scoreboard),
                        Transform(win_rate_group, new_group),
                        run_time=0.1
                    )
                else:
                    scoreboard.become(new_scoreboard)
                    win_rate_group.become(new_group)

                wins_now = int(win_tracker.get_value())
                losses_now = int(loss_tracker.get_value())
                total_games = wins_now + losses_now
                if total_games > 0:
                    rate = (wins_now / total_games) * 100
                    new_center = Text(f"Win Rate: {rate:.1f}%", font_size=24, color=GREEN)
                else:
                    new_center = Text("Win Rate: --%", font_size=24, color=GREEN)
                new_center.move_to(win_rate_center)
                
                if is_animated:
                    self.play(Transform(win_rate_center, new_center), run_time=0.1)
                else:
                    win_rate_center.become(new_center)

            if prediction and pd.notna(prediction):
                total_predictions += 1
                if prediction == opp_move:
                    correct_predictions += 1

                if should_update_visual:
                    accuracy_pct = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0
                    accuracy_data.append((round_num, accuracy_pct))

                    points = [axes.coords_to_point(x, y) for x, y in accuracy_data]
                    new_line = VMobject()
                    new_line.set_points_as_corners(points)
                    new_line.set_color(BLUE)
                    new_line.set_stroke(width=3)

                    if accuracy_line:
                        if is_animated:
                            self.play(Transform(accuracy_line, new_line), run_time=0.2)
                        else:
                            accuracy_line.become(new_line)
                    else:
                        accuracy_line = new_line
                        if is_animated:
                            self.play(Create(accuracy_line), run_time=0.2)
                        else:
                            self.add(accuracy_line)

                    acc_text = Text(f"{accuracy_pct:.1f}%", font_size=18, color=BLUE)
                    acc_text.next_to(accuracy_title, RIGHT, buff=0.3)
                    if hasattr(self, "acc_display"):
                        if is_animated:
                            self.play(Transform(self.acc_display, acc_text), run_time=0.1)
                        else:
                            self.acc_display.become(acc_text)
                    else:
                        self.acc_display = acc_text
                        self.add(acc_text)

            if should_update_visual:
                history_entry = self._create_history_entry(round_num, ai_move, opp_move, result)

                if len(move_history) < MAX_HISTORY:
                    idx = len(move_history)
                    history_entry.next_to(header_entry, DOWN, buff=0.15 + idx * 0.35)
                    move_history.add(history_entry)
                    if is_animated:
                        self.play(FadeIn(history_entry), run_time=0.2)
                    else:
                        self.add(history_entry)
                else:
                    old_entry = move_history[0]
                    start_buff = 0.15 + MAX_HISTORY * ROW_GAP
                    history_entry.next_to(header_entry, DOWN, buff=start_buff)
                    move_history.add(history_entry)
                    self.add(history_entry)

                    if is_animated:
                        animations = []
                        for i, entry in enumerate(move_history[1:], start=0):
                            entry.generate_target()
                            entry.target.next_to(header_entry, DOWN, buff=0.15 + i * ROW_GAP)
                            animations.append(Transform(entry, entry.target))
                        animations.append(FadeOut(old_entry))
                        self.play(*animations, run_time=0.3)
                    else:
                        for i, entry in enumerate(move_history[1:], start=0):
                            entry.next_to(header_entry, DOWN, buff=0.15 + i * ROW_GAP)
                        self.remove(old_entry)

                    move_history.remove(old_entry)

            if not is_animated and should_update_visual:
                self.wait(0.05)
            elif is_animated and round_num <= ANIMATED_ROUNDS:
                self.wait(0.1)
        
        self.wait(2)

    def _setup_move_history(self, title):
        move_history_title = Text("Move History:", font_size=24, color=YELLOW)
        move_history_title.next_to(title, DOWN, buff=0.5).to_edge(RIGHT, buff=0.5)

        hdr_round_text = Text("R#:", font_size=14, color=GRAY)
        hdr_round_box = Rectangle(width=0.4, height=hdr_round_text.height * 1.3, stroke_width=0, fill_opacity=0, fill_color=BLACK)
        hdr_round_text.move_to(hdr_round_box)
        hdr_round_text.align_to(hdr_round_box, LEFT)
        header_round_container = VGroup(hdr_round_box, hdr_round_text)

        m_label = Text("M", font_size=14, color=YELLOW, weight=BOLD)
        vs_header = Text("vs", font_size=12, color=GRAY)
        p_label = Text("P", font_size=14, color=YELLOW, weight=BOLD)
        header_center_inner = VGroup(m_label, vs_header, p_label).arrange(RIGHT, buff=0.1)
        header_center_box = Rectangle(width=1.0, height=header_center_inner.height * 1.3, stroke_width=0, fill_opacity=0, fill_color=BLACK)
        header_center_inner.move_to(header_center_box)
        header_center_container = VGroup(header_center_box, header_center_inner)

        result_header_text = Text("Result", font_size=14, color=GRAY)
        result_header_box = Rectangle(width=0.75, height=result_header_text.height * 1.3, stroke_width=0, fill_opacity=0, fill_color=BLACK)
        result_header_text.move_to(result_header_box)
        result_header_container = VGroup(result_header_box, result_header_text)

        header_entry = VGroup(header_round_container, header_center_container, result_header_container).arrange(RIGHT, buff=0.15)
        header_entry.next_to(move_history_title, DOWN, buff=0.25)

        move_history_title.move_to(header_entry.get_center() + UP * (move_history_title.height/2 + header_entry.height/2 + 0.25))
        
        self.add(move_history_title)
        self.add(header_entry)

        move_history = VGroup()
        self.add(move_history)
        
        return move_history_title, header_entry, move_history

    def _show_selection(self, round_txt, final_ai_move, final_opp_move):
        ai_label = Text("AI (Random):", font_size=24, color=YELLOW).next_to(round_txt, DOWN, buff=0.5)
        opp_label = Text("Opponent (Repeater):", font_size=24, color=YELLOW).next_to(ai_label, DOWN, buff=0.3)
        self.play(FadeIn(ai_label), FadeIn(opp_label), run_time=0.1)

        ai_options = VGroup(*[self._mini_token(move) for move in ALL_MOVES]).arrange(RIGHT, buff=0.2)
        ai_options.next_to(ai_label, RIGHT, buff=0.3)
        opp_options = VGroup(*[self._mini_token(move) for move in ALL_MOVES]).arrange(RIGHT, buff=0.2)
        opp_options.next_to(opp_label, RIGHT, buff=0.3)
        self.play(FadeIn(ai_options), FadeIn(opp_options), run_time=0.1)

      
        self.play(ai_options.animate.set_opacity(0.3), opp_options.animate.set_opacity(0.3), run_time=0.1)
        self.play(ai_options.animate.set_opacity(1), opp_options.animate.set_opacity(1), run_time=0.1)

        ai_selected = self._mini_token(final_ai_move).next_to(ai_label, RIGHT, buff=0.3).scale(1.2)
        opp_selected = self._mini_token(final_opp_move).next_to(opp_label, RIGHT, buff=0.3).scale(1.2)
        self.play(Transform(ai_options, ai_selected), Transform(opp_options, opp_selected), run_time=0.15)

        self.wait(0.1)
        self.play(FadeOut(ai_label), FadeOut(opp_label), FadeOut(ai_options), FadeOut(opp_options), run_time=0.1)

    def _mini_token(self, move):
        circle = Circle(radius=0.25, color=MOVE_COLOR[move], fill_opacity=0.3).set_stroke(width=2)
        text = Text(move, font_size=20, color=WHITE)
        return VGroup(circle, text)

    def _create_history_entry(self, round_num, ai_move, opp_move, result):
        round_text = Text(f"R{round_num}:", font_size=14, color=GRAY)
        round_box = Rectangle(width=0.4, height=round_text.height * 1.3, stroke_width=0, fill_opacity=0, fill_color=BLACK)
        round_text.move_to(round_box)
        round_text.align_to(round_box, LEFT)
        round_col = VGroup(round_box, round_text)

        ai_circle = Circle(radius=0.12, color=MOVE_COLOR[ai_move], fill_opacity=0.4).set_stroke(width=1.5)
        ai_letter = Text(ai_move, font_size=12, color=WHITE)
        ai_token = VGroup(ai_circle, ai_letter)
        vs_text = Text("vs", font_size=12, color=GRAY)
        opp_circle = Circle(radius=0.12, color=MOVE_COLOR[opp_move], fill_opacity=0.4).set_stroke(width=1.5)
        opp_letter = Text(opp_move, font_size=12, color=WHITE)
        opp_token = VGroup(opp_circle, opp_letter)

        mid_inner = VGroup(ai_token, vs_text, opp_token).arrange(RIGHT, buff=0.1)
        mid_box = Rectangle(width=1.0, height=mid_inner.height * 1.3, stroke_width=0, fill_opacity=0, fill_color=BLACK)
        mid_inner.move_to(mid_box)
        mid_col = VGroup(mid_box, mid_inner)

        res_text = Text(f"({result})", font_size=16, color=RESULT_COLOR[result])
        res_box = Rectangle(width=0.75, height=res_text.height * 1.3, stroke_width=0, fill_opacity=0, fill_color=BLACK)
        res_text.move_to(res_box)
        res_col = VGroup(res_box, res_text)

        entry = VGroup(round_col, mid_col, res_col).arrange(RIGHT, buff=0.15)
        return entry

    def _scoreboard(self, w, l, t):
        def make_row(label, tracker, color):
            text_label = Text(label, font_size=26)
            num_text = Text(str(int(tracker.get_value())), font_size=30, color=color)
            return VGroup(text_label, num_text).arrange(RIGHT, buff=0.5)

        wins = make_row("Model wins:", w, GREEN)
        losses = make_row("Player wins:", l, RED)
        ties = make_row("Ties:", t, GRAY)
        return VGroup(wins, losses, ties).arrange(DOWN, aligned_edge=LEFT, buff=0.3)