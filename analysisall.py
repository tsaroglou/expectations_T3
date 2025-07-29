import pandas as pd
import matplotlib.pyplot as plt
import os

# === STEP 1: Load and combine all datasets ===
treatment_files = [
    (r"C:\Users\TheodorosSaroglou\Downloads\Stochastic Vote Data\VR_C_r_part2_2025-07-28.csv", "OnlyRisk"),
    (r"C:\Users\TheodorosSaroglou\Downloads\Stochastic Vote Data\VR_C_s_plus1_part2_2025-07-28.csv", "OnlySafe"),
    (r"C:\Users\TheodorosSaroglou\Downloads\Stochastic Vote Data\VR_T1a_plus1_part2_2025-07-28.csv", "T1a"),
    (r"C:\Users\TheodorosSaroglou\Downloads\Stochastic Vote Data\VR_T1b_part2_2025-07-28.csv", "T1b"),
    (r"C:\Users\TheodorosSaroglou\Downloads\VR_Yoked_T1a_all_apps_wide_2025-07-29.csv", "Yoked_on_T1a"),
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

# === NEW: Drop participants who never reached round 20 ===
if 'subsession.round_number' in df.columns:
    df = (
        df
        .groupby('participant.code')
        .filter(lambda d: d['subsession.round_number'].max() >= 20)
        .reset_index(drop=True)
    )

if 'player.total_money' in df.columns:
    df = (
        df
        .groupby('participant.code')
        .filter(lambda d: d['player.total_money'].notna().any())
        .reset_index(drop=True)
    )

# === STEP 3: Create variables ===
df['Cooperated'] = df['player.action'].map({'C': 1, 'D': 0})
if 'player.vote' in df.columns:
    df['Chose_Risk'] = df['player.vote'].map({'Matrix B': 1, 'Matrix A': 0})
else:
    df['Chose_Risk'] = None

df = df.reset_index(drop=True)

# === Filter to rounds <= 20 for line graphs ===
df = df[df['subsession.round_number'] <= 20]

# === Helper function to label bars ===
def label_bars(ax):
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height:.2f}',
                    (p.get_x() + p.get_width() / 2., height + 0.02),
                    ha='center', va='bottom', fontsize=9)

# === NEW: Line chart with 5-round bins for all treatments ===
df['round_bin'] = ((df['subsession.round_number'] - 1) // 5 + 1) * 5
plt.figure(figsize=(10, 6))
for treatment, sub in df.groupby('treatment'):
    binned = sub.groupby('round_bin')['Cooperated'].mean()
    plt.plot(binned.index, binned.values, label=treatment, marker='o')
    for x, y in zip(binned.index, binned.values):
        plt.text(x, y + 0.02, f"{y:.2f}", ha='center', fontsize=9)
plt.axhline(0.5, color='gray', linestyle='--', linewidth=1)
plt.xlabel("Round Bin")
plt.ylabel("Avg Cooperation")
plt.title("Cooperation per 5-Round Bin by Treatment")
plt.xticks(sorted(df['round_bin'].unique()))
plt.ylim(0, 1.05)
plt.grid(True, axis='both', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("cooperation_binned_by_treatment.png")
plt.show()

# === NEW: Line chart with 5-round bins for T1a and Yoked ===
subset = df[df['treatment'].isin(['T1a', 'Yoked_on_T1a'])]
plt.figure(figsize=(10, 6))
for treatment, sub in subset.groupby('treatment'):
    binned = sub.groupby('round_bin')['Cooperated'].mean()
    plt.plot(binned.index, binned.values, label=treatment, marker='o')
    for x, y in zip(binned.index, binned.values):
        plt.text(x, y + 0.02, f"{y:.2f}", ha='center', fontsize=9)
plt.axhline(0.5, color='gray', linestyle='--', linewidth=1)
plt.xlabel("Round Bin")
plt.ylabel("Avg Cooperation")
plt.title("Cooperation per 5-Round Bin: T1a vs Yoked")
plt.xticks(sorted(subset['round_bin'].unique()))
plt.ylim(0, 1.05)
plt.grid(True, axis='both', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("cooperation_binned_T1a_Yoked.png")
plt.show()

# === STEP 4: Bar chart - Mean Cooperation by Treatment ===
plt.figure(figsize=(8, 5))
mean_coop = df.groupby('treatment')['Cooperated'].mean()
ax = mean_coop.plot(kind='bar', color='steelblue', edgecolor='black')
label_bars(ax)
plt.ylabel("Average Cooperation")
plt.title("Mean Cooperation by Treatment")
plt.ylim(0, 1.05)
plt.grid(True, axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("mean_cooperation_by_treatment.png")
plt.show()

# === STEP 4b: Bar chart - Mean Cooperation by Treatment and Game (if applicable) ===
if 'group.current_game' in df.columns:
    df_game = df.dropna(subset=['group.current_game'])
    if not df_game.empty:
        bar_data = df_game.groupby(['treatment', 'group.current_game'])['Cooperated'].mean().unstack()
        ax = bar_data.plot(kind='bar', figsize=(10, 6), edgecolor='black')
        for container in ax.containers:
            for bar in container:
                height = bar.get_height()
                ax.annotate(f'{height:.2f}',
                            (bar.get_x() + bar.get_width() / 2., height + 0.02),
                            ha='center', va='bottom', fontsize=9)
        plt.ylabel("Average Cooperation")
        plt.title("Mean Cooperation by Treatment and Game")
        plt.ylim(0, 1.05)
        plt.grid(True, axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig("mean_cooperation_by_treatment_and_game.png")
        plt.show()

# === STEP 5: Bar chart - Mean Chose Risk by Treatment (if exists) ===
if df['Chose_Risk'].notna().any():
    plt.figure(figsize=(8, 5))
    mean_risk = df.dropna(subset=['Chose_Risk']).groupby('treatment')['Chose_Risk'].mean()
    ax = mean_risk.plot(kind='bar', color='darkorange', edgecolor='black')
    label_bars(ax)
    plt.ylabel("Mean Chose Risk (Matrix B)")
    plt.title("Mean Risk Preference by Treatment")
    plt.ylim(0, 1.05)
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("mean_risk_by_treatment.png")
    plt.show()


# === STEP 6: Line plot - Cooperation over time per treatment ===
plt.figure(figsize=(10, 6))
for treatment, sub in df.groupby('treatment'):
    coop_by_round = sub.groupby('subsession.round_number')['Cooperated'].mean()
    coop_by_round = coop_by_round[coop_by_round.index <= 20]
    plt.plot(coop_by_round.index, coop_by_round.values, label=f"{treatment}", linewidth=2)

plt.xlabel("Round Number")
plt.ylabel("Mean Cooperation")
plt.title("Cooperation Over Time by Treatment")
plt.xticks(range(1, 21))
plt.ylim(0, 1.05)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("cooperation_over_time_by_treatment.png")
plt.show()

# === NEW: Cooperation by own/partner risk, split by treatment and marked by game ===
df_risk = df[df['treatment'].isin(['T1a', 'T1b']) & df['Chose_Risk'].notna()]
df_risk = df_risk[['participant.code', 'group.id_in_subsession', 'subsession.round_number', 'Chose_Risk', 'Cooperated', 'treatment', 'group.current_game']]

def label_condition(row_self, row_partner):
    if row_self == 0 and row_partner == 0:
        return "Both no risk"
    elif row_self == 1 and row_partner == 0:
        return "Self yes / Partner no"
    elif row_self == 0 and row_partner == 1:
        return "Self no / Partner yes"
    elif row_self == 1 and row_partner == 1:
        return "Both chose risk"
    return "Unknown"

merged = pd.merge(
    df_risk,
    df_risk,
    on=['group.id_in_subsession', 'subsession.round_number'],
    suffixes=('_self', '_partner')
)

merged = merged[merged['participant.code_self'] != merged['participant.code_partner']]

merged['condition'] = merged.apply(lambda row: label_condition(row['Chose_Risk_self'], row['Chose_Risk_partner']), axis=1)

# Determine bar hatching based on current_game
merged['hatch'] = merged['group.current_game_self'].map({'A': '//', 'B': '..'})

summary = merged.groupby(['treatment_self', 'condition', 'hatch'])['Cooperated_self'].mean().reset_index()
summary = summary.rename(columns={
    'treatment_self': 'Treatment',
    'Cooperated_self': 'Mean Cooperation',
    'hatch': 'Hatch'
})

# Plotting
fig, ax = plt.subplots(figsize=(15, 6))
colors = {'T1a': 'steelblue', 'T1b': 'orange'}
conditions = summary['condition'].unique()
hatch_map = {'//': 'Game A', '..': 'Game B'}

for i, treatment in enumerate(['T1a', 'T1b']):
    subset = summary[summary['Treatment'] == treatment]
    for j, row in subset.iterrows():
        x = list(conditions).index(row['condition']) + i * 0.35
        bar = ax.bar(x, row['Mean Cooperation'], width=0.25, label=f"{treatment}" if j == 0 else "",
                     color=colors[treatment], hatch=row['Hatch'], edgecolor='black')
        ax.text(x, row['Mean Cooperation'] + 0.02, f"{row['Mean Cooperation']:.2f}", ha='center', fontsize=9)

# X-axis setup
ax.set_xticks([i + 0.175 for i in range(len(conditions))])
ax.set_xticklabels(conditions)
ax.set_ylabel("Mean Cooperation")
ax.set_title("Cooperation by Risk Condition and Treatment")
ax.set_ylim(0, 1.05)
ax.grid(True, linestyle='--', alpha=0.6, axis='y')

# Create legend manually
handles = [
    plt.Rectangle((0,0),1,1, color='steelblue', edgecolor='black', label='T1a'),
    plt.Rectangle((0,0),1,1, color='orange', edgecolor='black', label='T1b'),
    plt.Rectangle((0,0),1,1, color='white', hatch='//', edgecolor='black', label='Game A'),
    plt.Rectangle((0,0),1,1, color='white', hatch='..', edgecolor='black', label='Game B')
]
ax.legend(handles=handles)

plt.tight_layout()
plt.savefig("cooperation_by_risk_condition_treatment_and_game.png")
plt.show()


# === STEP 6b: Split by treatment and current_game ===
if 'group.current_game' in df.columns:
    game_split_df = df.dropna(subset=['group.current_game'])
    if game_split_df['group.current_game'].nunique() > 0:
        plt.figure(figsize=(10, 6))
        for (treatment, game), sub in game_split_df.groupby(['treatment', 'group.current_game']):
            avg = sub.groupby('subsession.round_number')['Cooperated'].mean()
            avg = avg[avg.index <= 20]
            plt.plot(avg.index, avg.values,
                     label=f"{treatment} - Game {game}",
                     linestyle='--' if game == 'B' else '-', linewidth=2)
        plt.xlabel("Round Number")
        plt.ylabel("Mean Cooperation")
        plt.title("Cooperation Over Time by Treatment and Game Type")
        plt.xticks(range(1, 21))
        plt.ylim(0, 1.05)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig("cooperation_by_treatment_and_game.png")
        plt.show()

# === NEW STEP: Line plot for T1a and Yoked_on_T1a by game ===
subset_df = df[df['treatment'].isin(['T1a', 'Yoked_on_T1a']) & df['group.current_game'].notna()]
plt.figure(figsize=(10, 6))
for (treatment, game), sub in subset_df.groupby(['treatment', 'group.current_game']):
    avg = sub.groupby('subsession.round_number')['Cooperated'].mean()
    avg = avg[avg.index <= 20]
    plt.plot(avg.index, avg.values, label=f"{treatment} - Game {game}", linestyle='--' if game == 'B' else '-', linewidth=2)
plt.xlabel("Round Number")
plt.ylabel("Mean Cooperation")
plt.title("T1a vs Yoked_on_T1a: Cooperation by Game")
plt.xticks(range(1, 21))
plt.ylim(0, 1.05)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("T1a_Yoked_by_game.png")
plt.show()

# 1) Subset
subset = df[
    df['treatment'].isin(['T1a', 'T1b']) &
    df['group.current_game'].notna()
].copy()

# 2) Define bins of 5 rounds
subset['round_bin'] = ((subset['subsession.round_number'] - 1) // 5 + 1) * 5

# 3) Plot
plt.figure(figsize=(10, 6))
for (treatment, game), sub in subset.groupby(['treatment', 'group.current_game']):
    binned = sub.groupby('round_bin')['Cooperated'].mean()
    plt.plot(
        binned.index,
        binned.values,
        label=f"{treatment} – Game {game}",
        linestyle='--' if game == 'B' else '-',
        marker='o'
    )
    # annotate each point
    for x, y in zip(binned.index, binned.values):
        plt.text(x, y + 0.02, f"{y:.2f}", ha='center', fontsize=9)

plt.xlabel("Round Bin")
plt.ylabel("Mean Cooperation")
plt.title("T1a vs T1b: Cooperation by Game (5-Round Bins)")
plt.xticks(sorted(subset['round_bin'].unique()))
plt.ylim(0, 1.05)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("T1a_T1b_by_game_binned.png")
plt.show()

# === NEW STEP: Line plot for T1a and T1b by game ===
subset_df = df[df['treatment'].isin(['T1a', 'T1b']) & df['group.current_game'].notna()]
plt.figure(figsize=(10, 6))
for (treatment, game), sub in subset_df.groupby(['treatment', 'group.current_game']):
    avg = sub.groupby('subsession.round_number')['Cooperated'].mean()
    avg = avg[avg.index <= 20]
    plt.plot(avg.index, avg.values, label=f"{treatment} - Game {game}", linestyle='--' if game == 'B' else '-', linewidth=2)
plt.xlabel("Round Number")
plt.ylabel("Mean Cooperation")
plt.title("T1a vs T1b: Cooperation by Game")
plt.xticks(range(1, 21))
plt.ylim(0, 1.05)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("T1a_T1b_by_game.png")
plt.show()


# === NEW STEP: Binned cooperation by treatment and game ===
if 'group.current_game' in df.columns:
    game_split_df = df.dropna(subset=['group.current_game'])
    if game_split_df['group.current_game'].nunique() > 0:
        game_split_df['round_bin'] = ((game_split_df['subsession.round_number'] - 1) // 5 + 1) * 5
        plt.figure(figsize=(10, 6))
        for (treatment, game), sub in game_split_df.groupby(['treatment', 'group.current_game']):
            binned = sub.groupby('round_bin')['Cooperated'].mean()
            plt.plot(binned.index, binned.values, label=f"{treatment} - Game {game}",
                     linestyle='--' if game == 'B' else '-', marker='o')
            for x, y in zip(binned.index, binned.values):
                plt.text(x, y + 0.02, f"{y:.2f}", ha='center', fontsize=9)
        plt.xlabel("Round Bin")
        plt.ylabel("Mean Cooperation")
        plt.title("Binned Cooperation by Treatment and Game")
        plt.xticks(sorted(game_split_df['round_bin'].unique()))
        plt.ylim(0, 1.05)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.savefig("binned_cooperation_by_treatment_and_game.png")
        plt.show()

# === NEW STEP: Binned cooperation for T1a vs Yoked_on_T1a by game ===
subset_binned = df[df['treatment'].isin(['T1a', 'Yoked_on_T1a']) & df['group.current_game'].notna()]
subset_binned['round_bin'] = ((subset_binned['subsession.round_number'] - 1) // 5 + 1) * 5
plt.figure(figsize=(10, 6))
for (treatment, game), sub in subset_binned.groupby(['treatment', 'group.current_game']):
    binned = sub.groupby('round_bin')['Cooperated'].mean()
    plt.plot(binned.index, binned.values, label=f"{treatment} - Game {game}",
             linestyle='--' if game == 'B' else '-', marker='o')
    for x, y in zip(binned.index, binned.values):
        plt.text(x, y + 0.02, f"{y:.2f}", ha='center', fontsize=9)
plt.xlabel("Round Bin")
plt.ylabel("Mean Cooperation")
plt.title("Binned Cooperation: T1a vs Yoked_on_T1a by Game")
plt.xticks(sorted(subset_binned['round_bin'].unique()))
plt.ylim(0, 1.05)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("binned_T1a_Yoked_by_game.png")
plt.show()

# === STEP 6c: Line plot - Risk choice over time (if available) ===
if df['Chose_Risk'].notna().any():
    plt.figure(figsize=(10, 6))
    for treatment, sub in df.dropna(subset=['Chose_Risk']).groupby('treatment'):
        risk_by_round = sub.groupby('subsession.round_number')['Chose_Risk'].mean()
        risk_by_round = risk_by_round[risk_by_round.index <= 20]
        plt.plot(risk_by_round.index, risk_by_round.values, label=f"{treatment}", linewidth=2)

    plt.xlabel("Round Number")
    plt.ylabel("Mean Chose Risk")
    plt.title("Risk Choice Over Time by Treatment")
    plt.xticks(range(1, 21))
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("risk_choice_over_time_by_treatment.png")
    plt.show()

    # === NEW: Bar chart of cooperation by participant/partner risk combos, by treatment ===
    subset = df[df['treatment'].isin(['T1a', 'T1b']) & df['Chose_Risk'].notna()]

    # Identify partner's vote
    subset = subset.sort_values(['treatment', 'group.id_in_subsession', 'subsession.round_number'])
    subset['partner_vote'] = (
        subset.groupby(['treatment', 'group.id_in_subsession', 'subsession.round_number'])['Chose_Risk']
        .transform(lambda x: x[::-1].values)
    )


    # Define categories
    def classify_combination(row):
        if row['Chose_Risk'] == 0 and row['partner_vote'] == 0:
            return 'NoRisk-NoRisk'
        elif row['Chose_Risk'] == 1 and row['partner_vote'] == 1:
            return 'Risk-Risk'
        elif row['Chose_Risk'] == 0 and row['partner_vote'] == 1:
            return 'NoRisk-Risk'
        elif row['Chose_Risk'] == 1 and row['partner_vote'] == 0:
            return 'Risk-NoRisk'
        else:
            return 'Other'


    subset['RiskCombo'] = subset.apply(classify_combination, axis=1)

    # Compute mean cooperation
    combo_means = (
        subset.groupby(['RiskCombo', 'treatment'])['Cooperated']
        .mean()
        .unstack()
        .reindex(['NoRisk-NoRisk', 'Risk-Risk', 'NoRisk-Risk', 'Risk-NoRisk'])
    )

    # Set up plot
    fig, ax = plt.subplots(figsize=(15, 6))
    width = 0.2
    x = range(len(combo_means))

    # Mapping from condition + treatment to current_game
    game_map = {
        ('NoRisk-NoRisk', 'T1a'): 'A',
        ('NoRisk-NoRisk', 'T1b'): 'A',
        ('Risk-Risk', 'T1a'): 'B',
        ('Risk-Risk', 'T1b'): 'B',
        ('NoRisk-Risk', 'T1a'): 'A',
        ('NoRisk-Risk', 'T1b'): 'B',
        ('Risk-NoRisk', 'T1a'): 'A',
        ('Risk-NoRisk', 'T1b'): 'B',
    }

    # Bar plots with hatching for game B
    # Pre-define colours so it’s easier to read / extend
    treatment_colors = {
        'T1a': 'skyblue',
        'T1b': 'orange'
    }

    for i, combo in enumerate(combo_means.index):
        for j, treatment in enumerate(['T1a', 'T1b']):
            val = combo_means.loc[combo, treatment]
            xpos = i + (j - 0.5) * width
            is_game_b = (game_map.get((combo, treatment)) == 'B')

            ax.bar(
                xpos,
                val,
                width,
                label=treatment if i == 0 else "",
                edgecolor='black',
                color=treatment_colors.get(treatment, 'gray'),
                hatch='///' if is_game_b else None,
            )

            ax.text(
                xpos,
                val + 0.02,
                f"{val:.2f}",
                ha='center',
                fontsize=9
            )
    # Labels and formatting
    ax.set_xticks(range(len(combo_means)))
    ax.set_xticklabels(['NoRisk-NoRisk', 'Risk-Risk', 'NoRisk-Risk', 'Risk-NoRisk'])
    ax.set_ylabel("Mean Cooperation")
    ax.set_title("Cooperation by Risk Combo and Treatment\n(Hatched bars = Game B)")
    ax.legend()
    ax.set_ylim(0, 1.05)
    ax.grid(True, axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig("coop_by_vote_combo_treatment.png")
    plt.show()

# === STEP 7: Excel Export ===

# Prepare filtered selected data with filled columns
selected_columns = [
    'participant.code', 'participant.label', 'subsession.round_number',
    'player.total_money', 'player.investment',
    'player.decision_1', 'player.decision_2',
    'player.decision_3', 'player.decision_4',
    'player.treatment', 'group.current_game', 'group.id_in_subsession',
    'treatment', 'Cooperated', 'Chose_Risk'
]
filtered_selected_df = df[selected_columns].copy()

# Fill columns that only appear in the final round using the full (unfiltered) dataset
one_time_fields = [
    'player.total_money', 'player.investment',
    'player.decision_1', 'player.decision_2',
    'player.decision_3', 'player.decision_4'
]

last_round_values = (
    pd.concat(df_list, ignore_index=True)  # unfiltered original data
    .sort_values('subsession.round_number')
    .groupby('participant.code', as_index=False)
    .last()[['participant.code'] + one_time_fields]
)

filtered_selected_df = filtered_selected_df.merge(last_round_values, on='participant.code', suffixes=('', '_filled'))
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

# === STEP 8: Participant Counts ===
participant_counts = df.groupby('treatment')['participant.code'].nunique().reset_index()
participant_counts.columns = ['Treatment', 'Unique Participants']


# Export to Excel
with pd.ExcelWriter("summary_analysis.xlsx") as writer:
    overall_means.to_excel(writer, sheet_name='Overall Averages', index=False)
    participant_counts.to_excel(writer, sheet_name='Participant Counts', index=False)
    mean_coop_by_treatment.to_excel(writer, sheet_name='Mean Coop by Treatment', index=False)
    mean_risk_by_treatment.to_excel(writer, sheet_name='Mean Risk by Treatment', index=False)
    df.to_excel(writer, sheet_name='Filtered Data', index=False)
    filtered_selected_df.to_excel(writer, sheet_name='Filtered Selected', index=False)
# === NEW STEP: Export strategy/factors/belief if they exist ===
strategy_data = []

for path, treatment in treatment_files:
    temp = pd.read_csv(path)
    temp.columns = temp.columns.str.strip()  # clean column names just in case
    has_cols = all(col in temp.columns for col in ['player.strategy', 'player.factors', 'player.belief'])
    if has_cols:
        temp_subset = temp[['participant.code', 'player.strategy', 'player.factors', 'player.belief']].copy()
        temp_subset['treatment'] = treatment
        strategy_data.append(temp_subset)

if strategy_data:
    df_strategy = pd.concat(strategy_data, ignore_index=True)
    df_strategy.to_excel("strategy_factors_belief.xlsx", index=False)
    print("Exported strategy_factors_belief.xlsx with available columns.")
else:
    print("No datasets contained all of: player.strategy, player.factors, player.belief")


print("\nAll tables and graphs saved.")

