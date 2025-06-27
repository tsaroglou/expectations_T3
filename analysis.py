import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load your CSV file
file_path = "/Users/theo/Downloads/VR_T1a_part2_2025-06-24 (6).csv"
df = pd.read_csv(file_path)

# Drop all rows for any participant where any row has player.remove == 1
remove_ids = df.loc[df['player.remove'] == 1, 'participant.code'].unique()
df = df[~df['participant.code'].isin(remove_ids)].copy()

# Step 1: Keep only rows where player.played == 1
df = df[df['player.action'].notna()].copy()
df = df.reset_index(drop=True)  # ✅ Add this line

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

# Step 7: Line plot of mean cooperation per round
overall_mean_by_round = df.groupby('subsession.round_number')['Cooperated'].mean().reset_index()

plt.figure(figsize=(10, 6))
plt.plot(overall_mean_by_round['subsession.round_number'],
         overall_mean_by_round['Cooperated'],
         label='Mean Cooperation',
         color='gray', linewidth=2)

plt.xlabel('Round Number', fontsize=12)
plt.ylabel('Mean Cooperation', fontsize=12)
plt.title('Mean Cooperation per Round', fontsize=14, weight='bold')
plt.xticks(range(1, 21), fontsize=10)
plt.yticks(fontsize=10)
plt.xlim(1, 20)
plt.ylim(0, 1.05)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11, loc='lower right')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("mean_cooperation_by_round.png")
plt.show()


# Step 7c: Line plot of mean risk choice per round (across both games)
mean_risk_by_round = df.groupby('subsession.round_number')['Chose_Risk'].mean().reset_index()

plt.figure(figsize=(10, 6))
plt.plot(mean_risk_by_round['subsession.round_number'],
         mean_risk_by_round['Chose_Risk'],
         label='Mean Risk Choice (Matrix B)',
         color='orange', linewidth=2, linestyle='-')

plt.xlabel('Round Number', fontsize=12)
plt.ylabel('Proportion Voting Risk', fontsize=12)
plt.title('Mean Risk Choice per Round', fontsize=14, weight='bold')
plt.xticks(range(1, 21), fontsize=10)
plt.yticks(fontsize=10)
plt.xlim(1, 20)
plt.ylim(0, 1.05)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11, loc='lower right')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("mean_risk_choice_by_round.png")
plt.show()

# Step 7b: Line plot of cooperation by round split by game type
mean_coop_by_game_round = df.groupby(['subsession.round_number', 'group.current_game'])['Cooperated'].mean().reset_index()

plt.figure(figsize=(10, 6))

# Line for Game A (Safe)
game_a = mean_coop_by_game_round[mean_coop_by_game_round['group.current_game'] == 'A']
plt.plot(game_a['subsession.round_number'], game_a['Cooperated'],
         label='Safe Game (A)', color='blue', linewidth=2)

# Line for Game B (Risky)
game_b = mean_coop_by_game_round[mean_coop_by_game_round['group.current_game'] == 'B']
plt.plot(game_b['subsession.round_number'], game_b['Cooperated'],
         label='Risky Game (B)', color='red', linewidth=2, linestyle='--')

# Styling
plt.xlabel('Round Number', fontsize=12)
plt.ylabel('Mean Cooperation', fontsize=12)
plt.title('Mean Cooperation per Round by Game Type', fontsize=14, weight='bold')
plt.xticks(range(1, 21), fontsize=10)
plt.yticks(fontsize=10)
plt.xlim(1, 20)
plt.ylim(0, 1.05)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11, loc='lower right')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("mean_cooperation_by_round_by_game.png")
plt.show()

# Graph 1: Mean Cooperation per Round by Game Type (side-by-side lines)
mean_coop_by_game_round = df.groupby(['subsession.round_number', 'group.current_game'])['Cooperated'].mean().reset_index()

plt.figure(figsize=(10, 6))

# Safe Game (A)
game_a = mean_coop_by_game_round[mean_coop_by_game_round['group.current_game'] == 'A']
plt.plot(game_a['subsession.round_number'], game_a['Cooperated'],
         label='Safe Game (A)', color='blue', linewidth=2)

# Risky Game (B)
game_b = mean_coop_by_game_round[mean_coop_by_game_round['group.current_game'] == 'B']
plt.plot(game_b['subsession.round_number'], game_b['Cooperated'],
         label='Risky Game (B)', color='red', linewidth=2, linestyle='--')

plt.xlabel('Round Number', fontsize=12)
plt.ylabel('Mean Cooperation', fontsize=12)
plt.title('Mean Cooperation per Round by Game Type', fontsize=14, weight='bold')
plt.xticks(range(1, 21), fontsize=10)
plt.yticks(fontsize=10)
plt.xlim(1, 20)
plt.ylim(0, 1.05)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11, loc='lower right')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("mean_cooperation_by_round_split_by_game.png")
plt.show()


# Graph 2: Mean Vote (Risk Choice) per Round by Game Type
mean_vote_by_game_round = df.groupby(['subsession.round_number', 'group.current_game'])['Chose_Risk'].mean().reset_index()

plt.figure(figsize=(10, 6))

# Safe Game (A)
vote_a = mean_vote_by_game_round[mean_vote_by_game_round['group.current_game'] == 'A']
plt.plot(vote_a['subsession.round_number'], vote_a['Chose_Risk'],
         label='Safe Game (A)', color='blue', linewidth=2)

# Risky Game (B)
vote_b = mean_vote_by_game_round[mean_vote_by_game_round['group.current_game'] == 'B']
plt.plot(vote_b['subsession.round_number'], vote_b['Chose_Risk'],
         label='Risky Game (B)', color='red', linewidth=2, linestyle='--')

plt.xlabel('Round Number', fontsize=12)
plt.ylabel('Proportion Voting Risk', fontsize=12)
plt.title('Mean Risk Vote per Round by Game Type', fontsize=14, weight='bold')
plt.xticks(range(1, 21), fontsize=10)
plt.yticks(fontsize=10)
plt.xlim(1, 20)
plt.ylim(0, 1.05)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11, loc='lower right')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("mean_vote_by_round_split_by_game.png")
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

# Prepare total money sheet
money_df = df[['participant.label', 'player.total_money']].copy()
money_df = money_df[money_df['player.total_money'].notna()]
money_df['participant.label'] = money_df['participant.label'].astype(str) + ','

# Prepare selected filtered data for export
# Step X: Prepare selected filtered data with cleaned values
selected_columns = [
    'participant.code', 'participant.label', 'subsession.round_number',
    'player.total_money', 'player.investment',
    'player.decision_1', 'player.decision_2',
    'player.decision_3', 'player.decision_4',
    'player.treatment', 'group.current_game',
    'Cooperated', 'Chose_Risk', 'player.matrix_sequence'
]
filtered_selected_df = df[selected_columns].copy()

# Step X.1: Fill one-time fields from the last round for each participant
one_time_fields = [
    'player.total_money', 'player.investment',
    'player.decision_1', 'player.decision_2',
    'player.decision_3', 'player.decision_4'
]

# Get last-round values per participant
last_rows = (
    filtered_selected_df
    .sort_values('subsession.round_number')
    .groupby('participant.code', as_index=False)
    .last()[['participant.code'] + one_time_fields]
)

# Merge last-round values into the full dataset
filtered_selected_df = filtered_selected_df.merge(
    last_rows,
    on='participant.code',
    suffixes=('', '_filled')
)

# Fill missing values using last-round values
for col in one_time_fields:
    filled_col = col + '_filled'
    filtered_selected_df[col] = filtered_selected_df[col].combine_first(filtered_selected_df[filled_col])
    filtered_selected_df.drop(columns=[filled_col], inplace=True)

# Step X.2: Remove prefixes from column names
filtered_selected_df.columns = (
    filtered_selected_df.columns
    .str.replace('participant\\.', '', regex=True)
    .str.replace('subsession\\.', '', regex=True)
    .str.replace('player\\.', '', regex=True)
    .str.replace('group\\.', '', regex=True)
)

# Format matrix_sequence: convert string to list, reformat using single quotes + trailing comma
import ast

def format_sequence(seq):
    try:
        # Safely parse the string back to list
        sequence_list = ast.literal_eval(seq)
        # Convert to desired format: single-quoted items and trailing comma
        formatted = "[" + ", ".join(f"'{x}'" for x in sequence_list) + "],"
        return formatted
    except:
        return seq  # fallback if parsing fails

# Apply formatting to player.matrix_sequence column
filtered_selected_df['matrix_sequence'] = filtered_selected_df['matrix_sequence'].apply(format_sequence)

## Step 10: Export all tables to a single Excel file
with pd.ExcelWriter("summary_analysis.xlsx") as writer:
    overall_means.to_excel(writer, sheet_name='Overall Averages', index=False)
    mean_coop_by_game.to_excel(writer, sheet_name='Mean Coop by Game', index=False)
    mean_coop_by_game_vote.to_excel(writer, sheet_name='Mean Coop by Game+Vote', index=False)
    mean_vote.to_excel(writer, sheet_name='Mean Vote', index=False)
    df.to_excel(writer, sheet_name='Filtered Data', index=False)
    money_df.to_excel(writer, sheet_name='Total Money', index=False)
    filtered_selected_df.to_excel(writer, sheet_name='Filtered Selected', index=False)  # ✅ New sheet

# Save all unique matrix sequences to a .txt file in desired format
unique_sequences = filtered_selected_df['matrix_sequence'].dropna().unique()

with open("matrix_sequences.txt", "w") as f:
    for seq in unique_sequences:
        f.write(seq + "\n")

print("\nAll tables saved to 'summary_analysis.xlsx'.")