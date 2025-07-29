from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === Configuration ===
DATA_DIR = Path.home() / "Downloads" / "Stochastic Vote Data"
TREATMENT_FILES = [
    (DATA_DIR / "VR_C_r_part2_2025-07-28.csv", "OnlyRisk"),
    (DATA_DIR / "VR_C_s_plus1_part2_2025-07-28.csv", "OnlySafe"),
    (DATA_DIR / "VR_T1a_plus1_part2_2025-07-28.csv", "T1a"),
    (DATA_DIR / "VR_T1b_part2_2025-07-28.csv", "T1b"),
    (DATA_DIR / "VR_Yoked_T1a_all_apps_wide_2025-07-29.csv", "Yoked_on_T1a"),
]

# === 1. Load & tag datasets ===
def load_and_tag(files):
    df_list = []
    for path, treatment in files:
        temp = pd.read_csv(path)
        temp['treatment'] = treatment
        df_list.append(temp)
    combined = pd.concat(df_list, ignore_index=True)
    return combined, df_list

# === 2. Filtering ===
def filter_data(df, min_round=20):
    df = df[df['player.action'].notna()]
    # remove flagged participants
    if 'player.remove' in df.columns:
        flagged = df.loc[df['player.remove'] == 1, 'participant.code'].unique()
        df = df[~df['participant.code'].isin(flagged)]
    # drop if never reached min_round
    if 'subsession.round_number' in df.columns:
        df = df.groupby('participant.code').filter(lambda d: d['subsession.round_number'].max() >= min_round)
    # ensure at least one non-na total_money
    if 'player.total_money' in df.columns:
        df = df.groupby('participant.code').filter(lambda d: d['player.total_money'].notna().any())
    return df.reset_index(drop=True)

# === 3. Feature engineering ===
def engineer_features(df):
    df = df.copy()
    df['Cooperated'] = df['player.action'].map({'C': 1, 'D': 0})
    if 'player.vote' in df.columns:
        df['Chose_Risk'] = df['player.vote'].map({'Matrix B': 1, 'Matrix A': 0})
    else:
        df['Chose_Risk'] = np.nan
    # 5-round bins
    df['round_bin'] = ((df['subsession.round_number'] - 1) // 5 + 1) * 5
    return df

# === Plot helpers ===
def annotate_bars(ax, dy=0.02, fmt="{:.2f}"):
    for p in ax.patches:
        ax.annotate(fmt.format(p.get_height()),
                    (p.get_x() + p.get_width() / 2., p.get_height() + dy),
                    ha='center', va='bottom', fontsize=9)


def plot_line(df, group_cols, value_col, title, xlabel, ylabel,
              bins=None, linestyle_map=None, save_path=None):
    fig, ax = plt.subplots(figsize=(10, 6))
    if bins:
        df = df.copy()
        df['bin'] = ((df['subsession.round_number'] - 1) // bins + 1) * bins
        x_col = 'bin'
        ax.axhline(0.5, color='gray', linestyle='--', linewidth=1)
    else:
        x_col = 'subsession.round_number'
    for name, sub in df.groupby(group_cols):
        series = sub.groupby(x_col)[value_col].mean()
        label = ' – '.join(map(str, name)) if isinstance(name, tuple) else name
        linestyle = '-' if not linestyle_map else None
        if linestyle_map and isinstance(name, tuple):
            game = name[group_cols.index('group.current_game')]
            linestyle = linestyle_map.get(game, '-')
        marker = 'o' if bins else None
        ax.plot(series.index, series.values,
                label=label, marker=marker, linestyle=linestyle)
        for x, y in zip(series.index, series.values):
            ax.text(x, y + 0.02, f"{y:.2f}", ha='center', fontsize=9)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_ylim(0, 1.05)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    plt.xticks(sorted(df[x_col].unique()))
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()


def plot_bar(df, index_cols, value_col, title, xlabel, ylabel,
              save_path=None, color_map=None):
    summary = df.groupby(index_cols)[value_col].mean().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(10, 6) if len(index_cols) > 1 else (8, 5))
    summary.plot(kind='bar', color=color_map, edgecolor='black', ax=ax)
    annotate_bars(ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_ylim(0, 1.05)
    ax.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()

# === 4. Corrected Risk-Combo chart ===
def plot_risk_combo(df, save_path=None):
    # subset T1a/T1b with valid risk choice
    sub = df[df['treatment'].isin(['T1a', 'T1b']) & df['Chose_Risk'].notna()].copy()
    cols = ['group.id_in_subsession', 'subsession.round_number',
            'participant.code', 'Chose_Risk', 'Cooperated',
            'group.current_game', 'treatment']
    sub = sub[cols]
    # merge to align partner rows
    partner = sub.rename(columns={
        'participant.code': 'participant.code_partner',
        'Chose_Risk': 'Chose_Risk_partner',
        'Cooperated': 'Cooperated_partner',
        'group.current_game': 'group.current_game_partner'
    })
    merged = sub.merge(partner,
                       on=['group.id_in_subsession', 'subsession.round_number'],
                       suffixes=('', '_p'))
    merged = merged[merged['participant.code'] != merged['participant.code_partner']]
    # classify combos
    def classify(row):
        s, p = row['Chose_Risk'], row['Chose_Risk_partner']
        if s == 0 and p == 0: return 'NoRisk-NoRisk'
        if s == 1 and p == 1: return 'Risk-Risk'
        if s == 0 and p == 1: return 'NoRisk-Risk'
        if s == 1 and p == 0: return 'Risk-NoRisk'
        return 'Other'
    merged['RiskCombo'] = merged.apply(classify, axis=1)
    merged['Game'] = merged['group.current_game']  # same for both
    # summary by combo, treatment, game
    summary = merged.groupby(['RiskCombo', 'treatment', 'Game'])['Cooperated'] \
                     .mean().reset_index()
    combos = ['NoRisk-NoRisk', 'Risk-Risk', 'NoRisk-Risk', 'Risk-NoRisk']
    treatments = ['T1a', 'T1b']
    games = ['A', 'B']
    width = 0.2
    fig, ax = plt.subplots(figsize=(15, 6))
    for i, combo in enumerate(combos):
        for j, t in enumerate(treatments):
            for k, g in enumerate(games):
                row = summary[ (summary['RiskCombo'] == combo) &
                               (summary['treatment'] == t) &
                               (summary['Game'] == g) ]
                if row.empty: continue
                val = row['Cooperated'].values[0]
                xpos = i + (j - 0.5) * width
                hatch = '///' if g == 'B' else None
                ax.bar(xpos, val, width,
                       label=f"{t}" if (i == 0 and g == 'A') else "",
                       edgecolor='black', hatch=hatch)
                ax.text(xpos, val + 0.02, f"{val:.2f}", ha='center', fontsize=9)
    ax.set_xticks(range(len(combos)))
    ax.set_xticklabels(combos)
    ax.set_ylabel('Mean Cooperation')
    ax.set_title('Cooperation by Risk Combo and Treatment\n(Hatched = Game B)')
    ax.set_ylim(0, 1.05)
    ax.grid(True, axis='y', linestyle='--', alpha=0.6)
    # custom legend
    handles = [plt.Rectangle((0, 0), 1, 1, color='skyblue', edgecolor='black', label='T1a'),
               plt.Rectangle((0, 0), 1, 1, color='orange', edgecolor='black', label='T1b'),
               plt.Rectangle((0, 0), 1, 1, facecolor='white', hatch='///', edgecolor='black', label='Game B')]
    ax.legend(handles=handles)
    plt.tight_layout()
    if save_path: plt.savefig(save_path)
    plt.show()

# === 5. Export to Excel ===
def export_all(df, original_list, out_file="summary_analysis.xlsx"):
    # overall means
    overall = pd.DataFrame({
        'Metric': ['Cooperated', 'Chose_Risk'],
        'Mean': [df['Cooperated'].mean(), df['Chose_Risk'].mean()]
    })
    # participant counts
    pc = df.groupby('treatment')['participant.code'].nunique().reset_index()
    pc.columns = ['Treatment', 'Unique Participants']
    # mean coop & risk
    mc = df.groupby('treatment')['Cooperated'].mean().reset_index()
    mr = df.dropna(subset=['Chose_Risk']).groupby('treatment')['Chose_Risk'].mean().reset_index()
    # filtered selected
    sel_cols = [
        'participant.code', 'participant.label', 'subsession.round_number',
        'player.total_money', 'player.investment',
        'player.decision_1','player.decision_2','player.decision_3','player.decision_4',
        'player.treatment','group.current_game','group.id_in_subsession',
        'treatment','Cooperated','Chose_Risk'
    ]
    sel = df[sel_cols].copy()
    # fill one-time fields
    one_time = ['player.total_money','player.investment',
                'player.decision_1','player.decision_2',
                'player.decision_3','player.decision_4']
    last = pd.concat(original_list, ignore_index=True) \
             .sort_values('subsession.round_number') \
             .groupby('participant.code', as_index=False).last()[['participant.code'] + one_time]
    sel = sel.merge(last, on='participant.code', suffixes=('','_filled'))
    for col in one_time:
        sel[col] = sel[col].combine_first(sel[f"{col}_filled"])
        sel.drop(columns=[f"{col}_filled"] , inplace=True)
    sel.columns = (sel.columns
                   .str.replace('participant\.', '', regex=True)
                   .str.replace('subsession\.', '', regex=True)
                   .str.replace('player\.', '', regex=True)
                   .str.replace('group\.', '', regex=True))
    # write
    with pd.ExcelWriter(out_file) as writer:
        overall.to_excel(writer, sheet_name='Overall Averages', index=False)
        pc.to_excel(writer, sheet_name='Participant Counts', index=False)
        mc.to_excel(writer, sheet_name='Mean Coop by Treatment', index=False)
        mr.to_excel(writer, sheet_name='Mean Risk by Treatment', index=False)
        df.to_excel(writer, sheet_name='Filtered Data', index=False)
        sel.to_excel(writer, sheet_name='Filtered Selected', index=False)

# === 6. Strategy export ===
def export_strategy(files):
    strategy_list = []
    for path, treatment in files:
        temp = pd.read_csv(path)
        temp.columns = temp.columns.str.strip()
        if all(col in temp.columns for col in ['player.strategy','player.factors','player.belief']):
            sub = temp[['participant.code','player.strategy','player.factors','player.belief']].copy()
            sub['treatment'] = treatment
            strategy_list.append(sub)
    if strategy_list:
        pd.concat(strategy_list, ignore_index=True).to_excel(
            "strategy_factors_belief.xlsx", index=False
        )
        print("Exported strategy_factors_belief.xlsx with available columns.")
    else:
        print("No datasets contained all of: player.strategy, player.factors, player.belief")

# === 7. Main pipeline ===
def main():
    df, raw_list = load_and_tag(TREATMENT_FILES)
    df = filter_data(df)
    df = engineer_features(df)
    # restrict for time-series plots
    df20 = df[df['subsession.round_number'] <= 20]
    # plots
    plot_line(df20, ['treatment'], 'Cooperated',
              'Cooperation Over Time by Treatment', 'Round Number', 'Mean Cooperation', save_path='cooperation_over_time.png')
    plot_line(df20, ['treatment'], 'Cooperated',
              'Cooperation per 5-Round Bin by Treatment', 'Round Bin', 'Avg Cooperation', bins=5, save_path='cooperation_binned_by_treatment.png')
    plot_line(df20, ['treatment','group.current_game'], 'Cooperated',
              'T1a vs Yoked_on_T1a: Cooperation by Game', 'Round Number', 'Mean Cooperation',
              linestyle_map={'A':'-','B':'--'}, save_path='T1a_Yoked_by_game.png')
    plot_bar(df, ['treatment'], 'Cooperated',
             'Mean Cooperation by Treatment', '', 'Average Cooperation', save_path='mean_cooperation_by_treatment.png')
    if 'group.current_game' in df.columns:
        plot_bar(df[df['group.current_game'].notna()], ['treatment','group.current_game'], 'Cooperated',
                 'Mean Cooperation by Treatment and Game', '', 'Average Cooperation', save_path='mean_coop_by_treatment_and_game.png')
    if df['Chose_Risk'].notna().any():
        plot_bar(df.dropna(subset=['Chose_Risk']), ['treatment'], 'Chose_Risk',
                 'Mean Risk Preference by Treatment', '', 'Mean Chose Risk', save_path='mean_risk_by_treatment.png')
        plot_line(df20.dropna(subset=['Chose_Risk']), ['treatment'], 'Chose_Risk',
                  'Risk Choice Over Time by Treatment', 'Round Number', 'Mean Chose Risk', save_path='risk_choice_over_time.png')
        plot_risk_combo(df20, save_path='coop_by_vote_combo_treatment.png')
    # exports
    export_all(df, raw_list)
    export_strategy(TREATMENT_FILES)

if __name__ == "__main__":
    main()
