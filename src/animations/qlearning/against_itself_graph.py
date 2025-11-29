import pandas as pd
import matplotlib.pyplot as plt

# -------- CONFIG ----------------------------------------------------
CSV_PATH = "results/results_qlearning_vs_qlearning.csv"
ROLLING_WINDOW = 500
# --------------------------------------------------------------------

def main():
    repdf = pd.read_csv(CSV_PATH)

    dfs = [
        ("QLearning", repdf),
    ]

    # Compute rolling winrates
    for _, df in dfs:
        df["is_win"] = df["result"] == "win"
        df["rolling_winrate"] = df["is_win"].rolling(ROLLING_WINDOW).mean()

    plt.figure(figsize=(12, 7))  # slightly taller for table room

    DOWNSAMPLE = 100  # plot every Nth point to reduce clutter

    # Plot lines
    for name, df in dfs:
        plt.plot(
            df["round"].iloc[::DOWNSAMPLE],
            df["rolling_winrate"].iloc[::DOWNSAMPLE],
            label=name,
            linewidth=2
        )

    plt.title(f"QLearning Results Rolling Win Rate (window={ROLLING_WINDOW})")
    plt.xlabel("Round")
    plt.ylabel("Win Rate")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.legend()

    # ---- Ending rolling winrate table ----
    # Build table data
    table_data = []
    for name, df in dfs:
        overall_winrate = df["is_win"].mean()
        overall_tierate = (df["result"] == "tie").mean()
        table_data.append([name, f"{overall_winrate:.3f}", f"{overall_tierate:.3f}"])

    # Add table to plot
    table = plt.table(
        cellText=table_data,
        colLabels=["Opponent", "Overall Winrate", "Overall Tie Rate"],
        loc="lower center",
        cellLoc="center",
        bbox=[0.25, -0.60, 0.5, 0.35]
    )

    plt.subplots_adjust(bottom=0.45)  # make room for table

    plt.show()

if __name__ == "__main__":
    main()
