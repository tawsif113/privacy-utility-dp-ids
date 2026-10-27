#!/usr/bin/env python3
"""Check manuscript tables and accepted seed summaries without retraining models.

Run from any directory. --write-tables updates only delimited manuscript tables.
This checks committed aggregates, not original predictions or external model bundles.
"""
import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / 'results/final_analysis/tables'
UNSW = ROOT / 'results/unsw_nb15_external_validation'
LABEL = {'non_private': 'Non-private', 'dp_eps_4': 'DP epsilon about 4', 'dp_eps_2': 'DP epsilon about 2'}
THREAT = {'score_only_black_box': 'Score-only', 'label_aware_audit': 'Label-aware'}
T95 = 2.7764451051977987


def stats(values):
    a = np.asarray(values, dtype=float)
    assert len(a) == 5 and np.isfinite(a).all()
    mean, sd = a.mean(), a.std(ddof=1)
    return np.array([mean, sd, mean - T95 * sd / np.sqrt(5), mean + T95 * sd / np.sqrt(5)])


def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                      '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(row) + ' |' for row in rows])


def evidence_tables():
    primary = pd.read_csv(FINAL / 'final_primary_privacy_utility.csv')
    u = pd.read_csv(UNSW / 'unsw_nb15_ids_results.csv')
    m = pd.read_csv(UNSW / 'unsw_nb15_mia_results.csv')
    result = {}
    rows = []
    for condition in LABEL:
        r = primary[(primary.condition == condition) & (primary.threat_model == 'score_only_black_box')].iloc[0]
        rows.append([LABEL[condition], '—' if pd.isna(r.actual_epsilon) else f'{r.actual_epsilon:.4f}'] +
                    [f'{r[f"ids_{k}_mean"]:.4f} ± {r[f"ids_{k}_standard_deviation"]:.4f}' for k in ['recall', 'fnr', 'f1', 'fpr', 'pr_auc']])
    result['nsl-utility'] = table(['Condition', 'Actual epsilon', 'Recall', 'FNR', 'F1', 'FPR', 'Average precision'], rows)
    rows, rates = [], []
    for _, r in primary.iterrows():
        rows.append([LABEL[r.condition], THREAT[r.threat_model]] +
                    [f'{r[f"{k}_mean"]:.5f} [{r[f"{k}_ci_low"]:.5f}, {r[f"{k}_ci_high"]:.5f}]' for k in ['mia_auc', 'mia_advantage']])
        rates.append([LABEL[r.condition], THREAT[r.threat_model]] +
                     [f'{r[f"{k}_mean"]:.6f}' for k in ['mia_balanced_accuracy', 'tpr_at_1pct_fpr', 'tpr_at_5pct_fpr']])
    result['nsl-mia'] = table(['Condition', 'Threat model', 'AUC [95% CI]', 'Advantage [95% CI]'], rows)
    result['nsl-low-fpr'] = table(['Condition', 'Threat model', 'Balanced accuracy', 'TPR at 1% FPR', 'TPR at 5% FPR'], rates)
    rows = []
    for condition in LABEL:
        r = u[(u.condition == condition) & (u.threshold_policy == 'validation_selected_F2')].iloc[0]
        rows.append([LABEL[condition], '—' if pd.isna(r.actual_epsilon) else f'{r.actual_epsilon:.6f}', f'{r.threshold:.2f}'] +
                    [f'{r[k]:.6f}' for k in ['recall', 'f1', 'fpr', 'pr_auc']])
    result['unsw-utility'] = table(['Condition', 'Actual epsilon', 'Threshold', 'Recall', 'F1', 'FPR', 'Average precision'], rows)
    rows, rates = [], []
    for _, r in m.iterrows():
        rows.append([LABEL[r.condition], THREAT[r.threat_model],
                     f'{r.mia_advantage:.6f} [{r.mia_advantage_ci_low:.6f}, {r.mia_advantage_ci_high:.6f}]',
                     f'{r.mia_balanced_accuracy:.6f}'])
        rates.append([LABEL[r.condition], THREAT[r.threat_model], f'{r.tpr_at_1pct_fpr:.6f}', f'{r.tpr_at_5pct_fpr:.6f}'])
    result['unsw-advantage'] = table(['Condition', 'Threat model', 'Advantage [95% CI]', 'Balanced accuracy'], rows)
    result['unsw-low-fpr'] = table(['Condition', 'Threat model', 'TPR at 1% FPR', 'TPR at 5% FPR'], rates)
    return result


def check_seed_summaries():
    ids = pd.read_csv(FINAL / 'ids_default_and_tuned_per_seed.csv')
    ids = ids[ids.threshold_policy == 'validation_selected_F2']
    primary = pd.read_csv(FINAL / 'primary_mia_per_seed.csv')
    secondary = pd.read_csv(FINAL / 'secondary_mia_per_seed.csv')
    accounting = pd.read_csv(FINAL / 'privacy_accounting_per_seed.csv')
    count = 0
    for _, r in pd.read_csv(FINAL / 'five_seed_summary.csv').iterrows():
        if r.domain == 'IDS':
            values = ids[ids.condition == r.condition][r.metric]
        elif r.domain == 'MIA':
            values = primary[(primary.condition == r.condition) & (primary.threat_model == r.threat_model)][r.metric]
        elif r.domain == 'privacy_accounting':
            values = accounting[accounting.condition == r.condition][r.metric]
        else:
            raise AssertionError(f'Unknown domain: {r.domain}')
        assert r.n_seeds == 5
        np.testing.assert_allclose(stats(values), r[['mean', 'standard_deviation', 'ci_low', 'ci_high']].to_numpy(dtype=float), atol=1e-10, rtol=1e-9)
        count += 1
    for filename, mia in [('primary_paired_differences_summary.csv', primary), ('secondary_paired_differences_summary.csv', secondary)]:
        for _, r in pd.read_csv(FINAL / filename).iterrows():
            source = ids if r.get('domain') == 'IDS' else mia[mia.threat_model == r.threat_model]
            ref = source[source.condition == r.reference_condition].set_index('seed')[r.metric]
            cmp = source[source.condition == r.comparison_condition].set_index('seed')[r.metric]
            assert set(ref.index) == set(cmp.index) == {42, 52, 62, 72, 82}
            np.testing.assert_allclose(stats(cmp - ref), r[['mean', 'standard_deviation', 'ci_low', 'ci_high']].to_numpy(dtype=float), atol=1e-10, rtol=1e-9)
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-tables', action='store_true')
    args = parser.parse_args()
    checked = check_seed_summaries()
    path = ROOT / 'paper/manuscript.md'
    text = path.read_text()
    tables = evidence_tables()
    for name, value in tables.items():
        pattern = rf'(<!-- evidence:{name}:start -->\n).*?(\n<!-- evidence:{name}:end -->)'
        match = re.search(pattern, text, re.S)
        assert match, f'Missing table block: {name}'
        if args.write_tables:
            text = re.sub(pattern, lambda m: m[1] + value + m[2], text, flags=re.S)
        else:
            assert match[0] == match[1] + value + match[2], f'Table differs from evidence: {name}'
    if args.write_tables:
        path.write_text(text)
    print(f'Passed: {checked} seed/paired summary rows recomputed; {len(tables)} manuscript tables matched to committed CSV evidence.')
    print('Scope: aggregate consistency only; no model retraining, prediction replay, or new bootstrap run.')


if __name__ == '__main__':
    main()
