from manim import *

MAX_HISTORY = 6
ROW_GAP = 0.35

class ScrollTest(Scene):
    def construct(self):
        # Title
        title = Text("Move History:", font_size=32, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        # Header
        header = Text("R#: M vs P Result", font_size=20, color=GRAY)
        header.next_to(title, DOWN, buff=0.3)
        self.add(header)

        # Container for rows
        move_history = VGroup()

        for n in range(1, 13):   # 12 rounds to see multiple scrolls
            entry = Text(f"R{n}: R vs P (lose)", font_size=20, color=WHITE)

            if len(move_history) < MAX_HISTORY:
                # Build-up phase: just stack under header
                idx = len(move_history)
                entry.next_to(
                    header,
                    DOWN,
                    buff=0.15 + idx * ROW_GAP,
                )
                move_history.add(entry)
                self.play(FadeIn(entry), run_time=0.25)

            else:
                # At capacity - smooth scroll with simultaneous fade in/out
                old_entry = move_history[0]

                # Start the new entry just *below* the visible block
                start_buff = 0.15 + MAX_HISTORY * ROW_GAP
                entry.next_to(header, DOWN, buff=start_buff)
                entry.set_opacity(0)  # invisible at start

                move_history.add(entry)
                self.add(entry)

                animations = []

                # Entries that will remain visible: move_history[1:]
                # (old second row ... new last row)
                for i, e in enumerate(move_history[1:], start=0):
                    e.generate_target()
                    e.target.next_to(
                        header,
                        DOWN,
                        buff=0.15 + i * ROW_GAP,  # same spacing as build-up
                    )

                    # New row: fade in while moving into its slot
                    if e is entry:
                        e.target.set_opacity(1)

                    animations.append(MoveToTarget(e))

                # Old top row: fade out (slight upward shift is optional)
                animations.append(FadeOut(old_entry, shift=UP * 0.05))

                # Play everything together -> smooth vertical scroll
                self.play(*animations, run_time=0.3)

                # Remove old top from group + scene
                move_history.remove(old_entry)
                self.remove(old_entry)

            self.wait(0.15)
