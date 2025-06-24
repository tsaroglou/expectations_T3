import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load your CSV file
file_path = "/Users/theo/Downloads/VR_T1a_part2_2025-06-24 (4).csv"
df = pd.read_csv(file_path)

# Step 1: Keep only rows where player.played == 1
df = df[df['player.played'] == 1]

# Step 2: Sort by participant.code and subsession.round_number
df = df.sort_values(by=['participant.code', 'subsession.round_number'])

# Step 3: Create "Cooperated" column
df['Cooperated'] = df['player.action'].map({'C': 1, 'D': 0})

# Step 4: Create "Chose_Risk" column
df['Chose_Risk'] = df['player.vote'].map({'Matrix B': 1, 'Matrix A': 0})

# Step 5: Bar chart - average cooperation by group.current_game
plt.figure(figsize=(8, 5))
bar_data = df.groupby('group.current_game')['Cooperated'].mean()
bars = bar_data.plot(kind='bar', color=['blue', 'red'], edgecolor='black')

plt.xlabel('Game Type', fontsize=12)
plt.ylabel('Average Cooperation', fontsize=12)
plt.title('Average Cooperation by Game Type', fontsize=14, weight='bold')
plt.xticks(rotation=0)
plt.ylim(0, 1.1)
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i in bars.patches:
    bars.annotate(f"{i.get_height():.2f}",
                  (i.get_x() + i.get_width() / 2, i.get_height() + 0.02),
                  ha='center', fontsize=10)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("average_cooperation_by_game.png")
plt.show()

# Step 6: Overall averages
mean_cooperated = df['Cooperated'].mean()
mean_chose_risk = df['Chose_Risk'].mean()

# Step 7: Line plot with colored dots by game
mean_by_round_game = df.groupby(['subsession.round_number', 'group.current_game'])['Cooperated'].mean().reset_index()
overall_mean_by_round = df.groupby('subsession.round_number')['Cooperated'].mean().reset_index()

plt.figure(figsize=(10, 6))
plt.plot(overall_mean_by_round['subsession.round_number'],
         overall_mean_by_round['Cooperated'],
         label='Overall Mean Cooperation', color='gray', linewidth=2, zorder=1)

for _, row in mean_by_round_game.iterrows():
    color = 'blue' if row['group.current_game'] == 'A' else 'red'
    plt.scatter(int(row['subsession.round_number']), row['Cooperated'],
                color=color, s=100, edgecolors='black', linewidth=0.8, zorder=2)

blue_patch = mpatches.Patch(color='blue', label='Safe Game (A)')
red_patch = mpatches.Patch(color='red', label='Risky Game (B)')
gray_line = plt.Line2D([], [], color='gray', label='Overall Mean Cooperation', linewidth=2)
plt.legend(handles=[blue_patch, red_patch, gray_line], fontsize=11, loc='lower right')

plt.xlabel('Round Number', fontsize=12)
plt.ylabel('Mean Cooperation', fontsize=12)
plt.title('Mean Cooperation per Round (Colored by Game)', fontsize=14, weight='bold')
plt.xticks(overall_mean_by_round['subsession.round_number'], fontsize=10)
plt.yticks(fontsize=10)
plt.ylim(0, 1.05)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("mean_cooperation_by_round_and_game.png")
plt.show()

# Step 8: Print overall averages
print(f"\nMean Cooperated: {mean_cooperated:.3f}")
print(f"Mean Chose Risk: {mean_chose_risk:.3f}")

# Step 9: Create summary tables
mean_coop_by_game = df.groupby('group.current_game')['Cooperated'].mean().reset_index()
mean_coop_by_game_vote = df.groupby(['group.current_game', 'player.vote'])['Cooperated'].mean().reset_index()
mean_vote = pd.DataFrame({
    'Metric': ['Chose_Risk'],
    'Mean': [mean_chose_risk]
})
overall_means = pd.DataFrame({
    'Metric': ['Cooperated', 'Chose_Risk'],
    'Mean': [mean_cooperated, mean_chose_risk]
})

# Step 10: Export all tables to a single Excel file
with pd.ExcelWriter("summary_analysis.xlsx") as writer:
    overall_means.to_excel(writer, sheet_name='Overall Averages', index=False)
    mean_coop_by_game.to_excel(writer, sheet_name='Mean Coop by Game', index=False)
    mean_coop_by_game_vote.to_excel(writer, sheet_name='Mean Coop by Game+Vote', index=False)
    mean_vote.to_excel(writer, sheet_name='Mean Vote', index=False)

print("\nAll tables saved to 'summary_analysis.xlsx'.")