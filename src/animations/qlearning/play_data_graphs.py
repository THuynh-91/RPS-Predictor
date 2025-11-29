import pandas as pd
import matplotlib.pyplot as plt

# -------- CONFIG ----------------------------------------------------
REPEATER_CSV_PATH = "results/results_qlearning_vs_repeater.csv"
FIZZBUZZ_CSV_PATH = "results/results_qlearning_vs_fizzbuzz.csv"
COUNTER_CSV_PATH = "results/results_qlearning_vs_counter.csv"
RANDOM_CSV_PATH = "results/results_qlearning_vs_random.csv"
SLIGHTBIAS_CSV_PATH = "results/results_qlearning_vs_slightbias.csv"
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

    # Compute WIN/LOSS ONLY rolling winrates
    for _, df in dfs:
        df["is_win"]  = (df["result"] == "win").astype(int)
        df["is_loss"] = (df["result"] == "lose").astype(int)
        df["is_tie"]  = (df["result"] == "tie")

        # Correct rolling winrate: W / (W+L), ties excluded
        wins  = df["is_win"].rolling(ROLLING_WINDOW).sum()
        losses = df["is_loss"].rolling(ROLLING_WINDOW).sum()
        denom = wins + losses

        df["rolling_winrate"] = (wins / denom).fillna(0)

    plt.figure(figsize=(14, 8))

    DOWNSAMPLE = 100

    # Plot rolling winrates
    for name, df in dfs:
        y = df["rolling_winrate"].iloc[::DOWNSAMPLE]
        x = df["round"].iloc[y.index]
        plt.plot(x, y, label=name, linewidth=2)

    plt.title(f"QLearning Rolling Win Rate (wins vs losses only, window={ROLLING_WINDOW})")
    plt.xlabel("Round")
    plt.ylabel("Win Rate")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.legend()

    # ---- TABLE 1: Winrate (excluding ties) ----
    win_table_data = []
    for name, df in dfs:
        total_wins = df["is_win"].sum()
        total_losses = df["is_loss"].sum()
        winrate = total_wins / (total_wins + total_losses) if (total_wins + total_losses) > 0 else 0
        win_table_data.append([name, f"{winrate:.3f}"])

    plt.table(
        cellText=win_table_data,
        colLabels=["Opponent", "Winrate (W / (W+L))"],
        loc="lower left",
        cellLoc="center",
        bbox=[0.05, -0.55, 0.4, 0.35]
    )

    # ---- TABLE 2: Tie Rate ----
    tie_table_data = []
    for name, df in dfs:
        tie_rate = df["is_tie"].mean()
        tie_table_data.append([name, f"{tie_rate:.3f}"])

    plt.table(
        cellText=tie_table_data,
        colLabels=["Opponent", "Tie Rate"],
        loc="lower right",
        cellLoc="center",
        bbox=[0.55, -0.55, 0.4, 0.35]
    )

    plt.subplots_adjust(bottom=0.45)

    plt.show()

if __name__ == "__main__":
    main()
