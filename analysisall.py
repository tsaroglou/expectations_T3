import pandas as pd
import matplotlib.pyplot as plt
import os

# === STEP 1: Load and combine all datasets ===
treatment_files = [
    ("/Users/theo/Downloads/Pilot results/VR_T1a_part2_2025-06-24 (6).csv", "T1a"),
    ("/Users/theo/Downloads/Pilot results/Pilot - Only Safe Part 2.csv", "OnlySafe"),
    ("/Users/theo/Downloads/Pilot results/Pilot - Only Risk Part 1.csv", "OnlyRisk")
]

df_list = []
for path, treatment in treatment_files:
    temp = pd.read_csv(path)
    temp['treatment'] = treatment
    df_list.append(temp)

df = pd.concat(df_list, ignore_index=True)

# === STEP 2: Filter relevant rows ===
df = df[df['player.action'].notna()]  # Only where action is not empty
if 'player.remove' in df.columns:
    to_remove = df[df['player.remove'] == 1]['participant.code'].unique()
    df = df[~df['participant.code'].isin(to_remove)]

# === STEP 3: Create variables ===
df['Cooperated'] = df['player.action'].map({'C': 1, 'D': 0})
if 'player.vote' in df.columns:
    df['Chose_Risk'] = df['player.vote'].map({'Matrix B': 1, 'Matrix A': 0})
else:
    df['Chose_Risk'] = None

df = df.reset_index(drop=True)

# === STEP 4: Bar chart - Mean Cooperation by Treatment ===
plt.figure(figsize=(8, 5))
mean_coop = df.groupby('treatment')['Cooperated'].mean()
mean_coop.plot(kind='bar', color='steelblue', edgecolor='black')
plt.ylabel("Average Cooperation")
plt.title("Mean Cooperation by Treatment")
plt.ylim(0, 1.05)
plt.tight_layout()
plt.savefig("mean_cooperation_by_treatment.png")
plt.show()

# === STEP 5: Bar chart - Mean Chose Risk by Treatment (if exists) ===
if df['Chose_Risk'].notna().any():
    plt.figure(figsize=(8, 5))
    mean_risk = df.dropna(subset=['Chose_Risk']).groupby('treatment')['Chose_Risk'].mean()
    mean_risk.plot(kind='bar', color='darkorange', edgecolor='black')
    plt.ylabel("Mean Chose Risk (Matrix B)")
    plt.title("Mean Risk Preference by Treatment")
    plt.ylim(0, 1.05)
    plt.tight_layout()
    plt.savefig("mean_risk_by_treatment.png")
    plt.show()

# === STEP 6: Line plot - Cooperation over time per treatment ===
plt.figure(figsize=(10, 6))
for treatment, sub in df.groupby('treatment'):
    coop_by_round = sub.groupby('subsession.round_number')['Cooperated'].mean()
    plt.plot(coop_by_round.index, coop_by_round.values, label=f"{treatment}", linewidth=2)

plt.xlabel("Round Number")
plt.ylabel("Mean Cooperation")
plt.title("Cooperation Over Time by Treatment")
plt.ylim(0, 1.05)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("cooperation_over_time_by_treatment.png")
plt.show()

# === STEP 6b: Split by treatment and current_game ===
if 'group.current_game' in df.columns:
    game_split_df = df.dropna(subset=['group.current_game'])
    if game_split_df['group.current_game'].nunique() > 1:
        plt.figure(figsize=(10, 6))
        for (treatment, game), sub in game_split_df.groupby(['treatment', 'group.current_game']):
            avg = sub.groupby('subsession.round_number')['Cooperated'].mean()
            plt.plot(avg.index, avg.values,
                     label=f"{treatment} - Game {game}",
                     linestyle='--' if game == 'B' else '-', linewidth=2)
        plt.xlabel("Round Number")
        plt.ylabel("Mean Cooperation")
        plt.title("Cooperation Over Time by Treatment and Game Type")
        plt.ylim(0, 1.05)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig("cooperation_by_treatment_and_game.png")
        plt.show()

# === STEP 6c: Line plot - Risk choice over time per treatment ===
risk_data = df.dropna(subset=['Chose_Risk'])
if not risk_data.empty:
    plt.figure(figsize=(10, 6))
    for treatment, sub in risk_data.groupby('treatment'):
        risk_by_round = sub.groupby('subsession.round_number')['Chose_Risk'].mean()
        plt.plot(risk_by_round.index, risk_by_round.values, label=f"{treatment}", linewidth=2)
    plt.xlabel("Round Number")
    plt.ylabel("Mean Chose Risk")
    plt.title("Risk Preference Over Time by Treatment")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("risk_by_treatment_over_time.png")
    plt.show()

# === STEP 7: Excel Export ===

# Prepare filtered selected data with filled columns
selected_columns = [
    'participant.code', 'participant.label', 'subsession.round_number',
    'player.total_money', 'player.investment',
    'player.decision_1', 'player.decision_2',
    'player.decision_3', 'player.decision_4',
    'player.treatment', 'group.current_game',
    'treatment', 'Cooperated', 'Chose_Risk'
]
filtered_selected_df = df[selected_columns].copy()

# Fill columns that only appear in the final round
one_time_fields = [
    'player.total_money', 'player.investment',
    'player.decision_1', 'player.decision_2',
    'player.decision_3', 'player.decision_4'
]
last_rows = (filtered_selected_df
             .sort_values('subsession.round_number')
             .groupby('participant.code', as_index=False)
             .last()[['participant.code'] + one_time_fields])

filtered_selected_df = filtered_selected_df.merge(last_rows, on='participant.code', suffixes=('', '_filled'))
for col in one_time_fields:
    filtered_selected_df[col] = filtered_selected_df[col].combine_first(filtered_selected_df[col + '_filled'])
    filtered_selected_df.drop(columns=[col + '_filled'], inplace=True)

# Remove prefixes
filtered_selected_df.columns = (
    filtered_selected_df.columns
    .str.replace('participant\.', '', regex=True)
    .str.replace('subsession\.', '', regex=True)
    .str.replace('player\.', '', regex=True)
    .str.replace('group\.', '', regex=True)
)

# Prepare additional summary tables
mean_coop_by_treatment = df.groupby('treatment')['Cooperated'].mean().reset_index()
mean_risk_by_treatment = df.dropna(subset=['Chose_Risk']).groupby('treatment')['Chose_Risk'].mean().reset_index()
overall_means = pd.DataFrame({
    'Metric': ['Cooperated', 'Chose_Risk'],
    'Mean': [df['Cooperated'].mean(), df['Chose_Risk'].mean()]
})

# Export to Excel
with pd.ExcelWriter("summary_analysis.xlsx") as writer:
    overall_means.to_excel(writer, sheet_name='Overall Averages', index=False)
    mean_coop_by_treatment.to_excel(writer, sheet_name='Mean Coop by Treatment', index=False)
    mean_risk_by_treatment.to_excel(writer, sheet_name='Mean Risk by Treatment', index=False)
    df.to_excel(writer, sheet_name='Filtered Data', index=False)
    filtered_selected_df.to_excel(writer, sheet_name='Filtered Selected', index=False)

print("\nAll tables and graphs saved.")
