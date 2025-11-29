import pandas as pd
import matplotlib.pyplot as plt

# -------- CONFIG ----------------------------------------------------
REPEATER_CSV_PATH = "results/training_qlearning_vs_repeater.csv"
FIZZBUZZ_CSV_PATH = "results/training_qlearning_vs_fizzbuzz.csv"
COUNTER_CSV_PATH = "results/training_qlearning_vs_counter.csv"
RANDOM_CSV_PATH = "results/training_qlearning_vs_random.csv"
SLIGHTBIAS_CSV_PATH = "results/training_qlearning_vs_slightbias.csv"
ROLLING_WINDOW = 500
# --------------------------------------------------------------------

def main():
    repdf = pd.read_csv(REPEATER_CSV_PATH)
    fbdf = pd.read_csv(FIZZBUZZ_CSV_PATH)
    codf = pd.read_csv(COUNTER_CSV_PATH)
    randf = pd.read_csv(RANDOM_CSV_PATH)
    sbdf = pd.read_csv(SLIGHTBIAS_CSV_PATH)

    dfs = [
        ("Repeater", repdf),
        ("FizzBuzz", fbdf),
        ("Counter", codf),
        ("Random", randf),
        ("SlightBias", sbdf)
    ]

    # Compute rolling winrates excluding ties
    for _, df in dfs:
        df["is_win"] = (df["result"] == "win").astype(int)
        df["is_loss"] = (df["result"] == "lose").astype(int)
        df["is_tie"] = (df["result"] == "tie").astype(int)

        df["is_wl"] = df["is_win"] + df["is_loss"]

        # Rolling winrate = wins / (wins+losses)
        wins_roll = df["is_win"].rolling(ROLLING_WINDOW).sum()
        wl_roll = df["is_wl"].rolling(ROLLING_WINDOW).sum()
        df["rolling_winrate"] = wins_roll / wl_roll

        # Rolling tie rate
        df["rolling_tierate"] = df["is_tie"].rolling(ROLLING_WINDOW).mean()

    plt.figure(figsize=(14, 8))

    # Plot rolling winrates
    for name, df in dfs:
        plt.plot(df["round"], df["rolling_winrate"], linewidth=2, label=name)

    plt.title(f"QLearning Training Rolling Win Rate (wins vs losses only, window={ROLLING_WINDOW})")
    plt.xlabel("Round")
    plt.ylabel("Win Rate")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.legend()

    # ---- TABLE 1: Final Rolling Winrate (W / (W+L)) ----
    win_table_data = []
    for name, df in dfs:
        final_w = df["rolling_winrate"].iloc[-1]
        win_table_data.append([name, f"{final_w:.3f}"])

    win_table = plt.table(
        cellText=win_table_data,
        colLabels=["Opponent", "Final Winrate (W / (W+L))"],
        loc="lower left",
        cellLoc="center",
        bbox=[0.05, -0.55, 0.4, 0.35]
    )

    # ---- TABLE 2: Final Rolling Tie Rate ----
    tie_table_data = []
    for name, df in dfs:
        final_t = df["rolling_tierate"].iloc[-1]
        tie_table_data.append([name, f"{final_t:.3f}"])

    tie_table = plt.table(
        cellText=tie_table_data,
        colLabels=["Opponent", "Final Tie Rate"],
        loc="lower right",
        cellLoc="center",
        bbox=[0.55, -0.55, 0.4, 0.35]
    )

    plt.subplots_adjust(bottom=0.45)
    plt.show()

if __name__ == "__main__":
    main()
