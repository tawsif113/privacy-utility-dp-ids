from __future__ import annotations

import json
from pathlib import Path

NOTEBOOK = Path("notebooks/05_dp_sgd_privacy_utility_sweep.ipynb")

with NOTEBOOK.open("r", encoding="utf-8") as file:
    nb = json.load(file)

cells = {cell.get("id"): cell for cell in nb["cells"]}


def source(cell_id: str) -> str:
    value = cells[cell_id]["source"]
    return "".join(value) if isinstance(value, list) else value


def set_source(cell_id: str, text: str) -> None:
    cells[cell_id]["source"] = text.splitlines(keepends=True)


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise RuntimeError(
            f"Expected one match, found {text.count(old)} for:\n{old[:120]}"
        )
    return text.replace(old, new, 1)


# Mark the corrected protocol and preserve accepted target caches.
text = source("5e3b8cee")
text = replace_once(
    text,
    "SAVE_INTERMEDIATE_ATTACK_DATA = True\n",
    "SAVE_INTERMEDIATE_ATTACK_DATA = True\n"
    "SHADOW_PROTOCOL_VERSION = \"epsilon_delta_matched_v2\"\n",
)
set_source("5e3b8cee", text)

set_source(
    "57cad817",
    """### Fair-comparison controls

Target training remains fixed. Each DP shadow now receives the same requested
`(epsilon, delta)` as its corresponding target condition. Opacus may calculate
a different shadow noise multiplier because the shadow dataset and sampling rate
are different. Every shadow's actual epsilon is recorded and checked.
""",
)

# Add strict JSON helpers so missing non-private values become null, not NaN.
text = source("57e111e6")
anchor = '''def load_json(path: Path) -> dict:
    with path.open("r") as file:
        return json.load(file)
'''
helpers = '''
def to_json_safe(value):
    if isinstance(value, dict):
        return {str(key): to_json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_json_safe(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def write_strict_json(path: Path, payload: dict) -> None:
    with path.open("w") as file:
        json.dump(
            to_json_safe(payload),
            file,
            indent=2,
            allow_nan=False,
        )
'''
text = replace_once(text, anchor, anchor + "\n" + helpers)
set_source("57e111e6", text)

# Use strict JSON for target cache configs.
text = source("a0d541cb")
text = replace_once(
    text,
    '''    with paths["config"].open("w") as file:
        json.dump(target_config, file, indent=2, default=str)
''',
    '''    write_strict_json(paths["config"], target_config)
''',
)
set_source("a0d541cb", text)

# Correct DP-shadow cache isolation and privacy-budget calibration.
text = source("72fc47e4")
old_paths = '''def shadow_output_path(condition: str, shadow_seed: int) -> Path:
    shadow_dir = INTERMEDIATE_DIR / condition / "shadow_outputs"
    shadow_dir.mkdir(parents=True, exist_ok=True)
    return shadow_dir / f"shadow_{shadow_seed}_mia_features.csv"


def shadow_config_path(condition: str, shadow_seed: int) -> Path:
    shadow_dir = INTERMEDIATE_DIR / condition / "shadow_outputs"
    shadow_dir.mkdir(parents=True, exist_ok=True)
    return shadow_dir / f"shadow_{shadow_seed}_config.json"
'''
new_paths = '''def shadow_cache_directory(condition: str) -> Path:
    cache_name = (
        "shadow_outputs"
        if condition == "non_private"
        else f"shadow_outputs_{SHADOW_PROTOCOL_VERSION}"
    )
    shadow_dir = INTERMEDIATE_DIR / condition / cache_name
    shadow_dir.mkdir(parents=True, exist_ok=True)
    return shadow_dir


def shadow_output_path(condition: str, shadow_seed: int) -> Path:
    return shadow_cache_directory(condition) / f"shadow_{shadow_seed}_mia_features.csv"


def shadow_config_path(condition: str, shadow_seed: int) -> Path:
    return shadow_cache_directory(condition) / f"shadow_{shadow_seed}_config.json"
'''
text = replace_once(text, old_paths, new_paths)

old_resume = '''    if RESUME and output_path.exists() and config_path.exists():
        print(f"Resuming {condition}, shadow {shadow_seed}")
        return pd.read_csv(output_path), load_json(config_path), []
'''
new_resume = '''    if RESUME and output_path.exists() and config_path.exists():
        saved_config = load_json(config_path)
        current = (
            not target_result.formal_dp
            or (
                saved_config.get("shadow_protocol_version")
                == SHADOW_PROTOCOL_VERSION
                and np.isclose(
                    float(saved_config["requested_epsilon"]),
                    float(target_result.target_epsilon),
                )
                and np.isclose(
                    float(saved_config["requested_delta"]),
                    TARGET_DELTA,
                )
            )
        )
        if current:
            print(f"Resuming {condition}, shadow {shadow_seed}")
            return pd.read_csv(output_path), saved_config, []
        print(f"Ignoring stale cache for {condition}, shadow {shadow_seed}")
'''
text = replace_once(text, old_resume, new_resume)

text = replace_once(
    text,
    '''    shadow_delta = None
    shadow_actual_epsilon = None
    shadow_sample_rate = None
''',
    '''    requested_epsilon = None
    requested_delta = None
    shadow_actual_epsilon = None
    shadow_noise_multiplier = None
    shadow_sample_rate = None
''',
)

old_private = '''    if target_result.formal_dp:
        shadow_delta = 1.0 / len(X_shadow_members)
        privacy_engine = PrivacyEngine(accountant=ACCOUNTANT, secure_mode=SECURE_MODE)

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("once")
            model, optimizer, train_loader = privacy_engine.make_private(
                module=model,
                optimizer=optimizer,
                criterion=criterion,
                data_loader=train_loader,
                noise_multiplier=target_result.noise_multiplier,
                max_grad_norm=MAX_GRAD_NORM,
                poisson_sampling=POISSON_SAMPLING,
                clipping="flat",
                loss_reduction="mean",
            )
'''
new_private = '''    if target_result.formal_dp:
        requested_epsilon = float(target_result.target_epsilon)
        requested_delta = float(TARGET_DELTA)
        privacy_engine = PrivacyEngine(accountant=ACCOUNTANT, secure_mode=SECURE_MODE)

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("once")
            model, optimizer, train_loader = privacy_engine.make_private_with_epsilon(
                module=model,
                optimizer=optimizer,
                criterion=criterion,
                data_loader=train_loader,
                target_epsilon=requested_epsilon,
                target_delta=requested_delta,
                epochs=EPOCHS,
                max_grad_norm=MAX_GRAD_NORM,
                poisson_sampling=POISSON_SAMPLING,
                clipping="flat",
                loss_reduction="mean",
            )
'''
text = replace_once(text, old_private, new_private)

text = replace_once(
    text,
    '''        shadow_sample_rate = float(
            getattr(train_loader, "sample_rate", 1.0 / len(train_loader))
        )
''',
    '''        shadow_noise_multiplier = float(optimizer.noise_multiplier)
        shadow_sample_rate = float(
            getattr(train_loader, "sample_rate", 1.0 / len(train_loader))
        )
''',
)

text = text.replace(
    "privacy_engine.get_epsilon(shadow_delta)",
    "privacy_engine.get_epsilon(requested_delta)",
)
text = text.replace(
    '"shadow_delta": shadow_delta,',
    '"shadow_delta": requested_delta,',
)

text = replace_once(
    text,
    '''    if target_result.formal_dp:
        shadow_actual_epsilon = float(
            privacy_engine.get_epsilon(requested_delta)
        )
''',
    '''    if target_result.formal_dp:
        shadow_actual_epsilon = float(
            privacy_engine.get_epsilon(requested_delta)
        )
        assert abs(shadow_actual_epsilon - requested_epsilon) <= 0.10
''',
)

old_config_fields = '''        "noise_multiplier": (
            target_result.noise_multiplier
            if target_result.formal_dp
            else None
        ),
'''
new_config_fields = '''        "shadow_protocol_version": (
            SHADOW_PROTOCOL_VERSION
            if target_result.formal_dp
            else "accepted_non_private_v1"
        ),
        "requested_epsilon": requested_epsilon,
        "requested_delta": requested_delta,
        "target_actual_epsilon": target_result.actual_epsilon,
        "target_noise_multiplier": target_result.noise_multiplier,
        "shadow_noise_multiplier": shadow_noise_multiplier,
        "absolute_epsilon_error": (
            abs(shadow_actual_epsilon - requested_epsilon)
            if target_result.formal_dp
            else None
        ),
'''
text = replace_once(text, old_config_fields, new_config_fields)
text = replace_once(
    text,
    '''    with config_path.open("w") as file:
        json.dump(shadow_config, file, indent=2, default=str)
''',
    '''    write_strict_json(config_path, shadow_config)
''',
)
set_source("72fc47e4", text)

# Add a hard shadow-budget gate.
text = source("10fbbb16")
text += '''

dp_shadow_configs = shadow_configs[
    shadow_configs["formal_dp"] == True
].copy()

shadow_budget_gate = bool(
    (dp_shadow_configs["absolute_epsilon_error"].astype(float) <= 0.10).all()
    and np.allclose(
        dp_shadow_configs["shadow_delta"].astype(float),
        TARGET_DELTA,
    )
)

display(dp_shadow_configs[[
    "condition",
    "shadow_seed",
    "requested_epsilon",
    "shadow_actual_epsilon",
    "absolute_epsilon_error",
    "requested_delta",
    "target_noise_multiplier",
    "shadow_noise_multiplier",
]])

assert shadow_budget_gate
print("DP shadow epsilon/delta matching gate:", shadow_budget_gate)
'''
set_source("10fbbb16", text)

# Add paired bootstrap helper.
text = source("660f39a8")
text += '''


def paired_bootstrap_metric_difference(
    labels: np.ndarray,
    reference_scores: np.ndarray,
    comparison_scores: np.ndarray,
    metric_function: Callable,
    seed: int,
) -> tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    estimate = float(
        metric_function(labels, comparison_scores)
        - metric_function(labels, reference_scores)
    )
    values = []
    for _ in range(BOOTSTRAP_N):
        indices = rng.integers(0, len(labels), len(labels))
        sampled_labels = labels[indices]
        if len(np.unique(sampled_labels)) < 2:
            continue
        values.append(
            metric_function(sampled_labels, comparison_scores[indices])
            - metric_function(sampled_labels, reference_scores[indices])
        )
    low, high = np.quantile(values, [0.025, 0.975])
    return estimate, float(low), float(high)
'''
set_source("660f39a8", text)

# Insert paired DP-minus-non-private MIA analysis after group diagnostics.
paired_markdown = {
    "cell_type": "markdown",
    "id": "paired-mia-differences-v2",
    "metadata": {},
    "source": [
        "## 17. Paired DP-minus-non-private MIA differences\n",
        "\n",
        "Negative differences indicate lower measured leakage under DP. A reduction is supported only when the complete paired 95% confidence interval is below zero.\n",
    ],
}
paired_code_text = '''def best_attack_by_threat(attacks):
    selected = {}
    for attack in attacks:
        current = selected.get(attack.threat_model)
        if current is None or attack.shadow_calibration_auc > current.shadow_calibration_auc:
            selected[attack.threat_model] = attack
    return selected

keys = ["membership", "partition_position", "row_id"]
reference_data = (
    target_condition_results["non_private"].target_mia_features
    .sort_values(keys)
    .reset_index(drop=True)
)
reference_attacks = best_attack_by_threat(attacks_by_condition["non_private"])
paired_rows = []

for dp_condition in ["dp_eps_8", "dp_eps_4", "dp_eps_2"]:
    comparison_data = (
        target_condition_results[dp_condition].target_mia_features
        .sort_values(keys)
        .reset_index(drop=True)
    )
    pd.testing.assert_frame_equal(
        reference_data[keys],
        comparison_data[keys],
        check_dtype=False,
    )
    comparison_attacks = best_attack_by_threat(attacks_by_condition[dp_condition])

    masks = {"overall": np.ones(len(reference_data), dtype=bool)}
    for column in ["binary_group", "family_group"]:
        for value in sorted(reference_data[column].unique()):
            masks[f"{column}={value}"] = (
                reference_data[column].to_numpy() == value
            )

    for threat_model in ["score_only_black_box", "label_aware_audit"]:
        ref_attack = reference_attacks[threat_model]
        dp_attack = comparison_attacks[threat_model]
        ref_scores_all = ref_attack.score_function(reference_data)
        dp_scores_all = dp_attack.score_function(comparison_data)

        for subset, mask in masks.items():
            labels = reference_data.loc[mask, "membership"].to_numpy(dtype=int)
            counts = pd.Series(labels).value_counts()
            if counts.get(0, 0) < MIN_GROUP_NONMEMBERS or counts.get(1, 0) < MIN_GROUP_MEMBERS:
                continue

            for metric_name, metric_function in {
                "mia_auc": roc_auc_score,
                "mia_advantage": calculate_mia_advantage,
            }.items():
                difference, ci_low, ci_high = paired_bootstrap_metric_difference(
                    labels,
                    ref_scores_all[mask],
                    dp_scores_all[mask],
                    metric_function,
                    stable_seed("paired", dp_condition, threat_model, subset, metric_name),
                )
                paired_rows.append({
                    "reference_condition": "non_private",
                    "comparison_condition": dp_condition,
                    "threat_model": threat_model,
                    "subset": subset,
                    "metric": metric_name,
                    "n": int(mask.sum()),
                    "reference_attack_model": ref_attack.attack_model,
                    "comparison_attack_model": dp_attack.attack_model,
                    "reference_estimate": metric_function(labels, ref_scores_all[mask]),
                    "comparison_estimate": metric_function(labels, dp_scores_all[mask]),
                    "difference_dp_minus_non_private": difference,
                    "difference_ci_low": ci_low,
                    "difference_ci_high": ci_high,
                    "supports_measured_reduction": bool(ci_high < 0),
                    "bootstrap_n": BOOTSTRAP_N,
                })

dp_sgd_paired_mia_differences = pd.DataFrame(paired_rows).merge(
    dp_sgd_configs[[
        "condition",
        "target_epsilon",
        "actual_epsilon",
        "delta",
    ]],
    left_on="comparison_condition",
    right_on="condition",
    how="left",
    validate="many_to_one",
).drop(columns=["condition"])

dp_sgd_paired_mia_differences.to_csv(
    RESULTS_DIR / "dp_sgd_paired_mia_differences.csv",
    index=False,
)

display(dp_sgd_paired_mia_differences[
    (dp_sgd_paired_mia_differences["metric"] == "mia_auc")
    & dp_sgd_paired_mia_differences["subset"].isin(
        ["overall", "family_group=Rare"]
    )
])
'''
paired_code = {
    "cell_type": "code",
    "execution_count": None,
    "id": "paired-mia-analysis-v2",
    "metadata": {},
    "outputs": [],
    "source": paired_code_text.splitlines(keepends=True),
}

group_index = next(
    index
    for index, cell in enumerate(nb["cells"])
    if cell.get("id") == "89119874"
)
nb["cells"][group_index + 1:group_index + 1] = [
    paired_markdown,
    paired_code,
]

# Update config, outputs, strict manifest writing, and gates.
text = source("0af8a519")
text = replace_once(
    text,
    '"protocol_version": "ROADMAP_REVISED_V2",\n',
    '"protocol_version": "ROADMAP_REVISED_V2",\n'
    '    "protocol_revision": SHADOW_PROTOCOL_VERSION,\n',
)
text = replace_once(
    text,
    '''        "dp_shadow_rule": (
            "Reuse target condition noise multiplier, clipping norm, "
            "batch size, and epochs."
        ),
''',
    '''        "dp_shadow_rule": (
            "Match target epsilon and fixed target delta; "
            "derive a shadow-specific noise multiplier."
        ),
        "paired_difference_rule": (
            "Paired bootstrap on identical target records."
        ),
''',
)
text = replace_once(
    text,
    '''with (RESULTS_DIR / "config.json").open("w") as file:
    json.dump(experiment_config, file, indent=2, default=str)
''',
    '''write_strict_json(RESULTS_DIR / "config.json", experiment_config)
''',
)
set_source("0af8a519", text)

text = source("15d8eb24")
text = replace_once(
    text,
    '    RESULTS_DIR / "dp_sgd_group_analysis.csv",\n',
    '    RESULTS_DIR / "dp_sgd_group_analysis.csv",\n'
    '    RESULTS_DIR / "dp_sgd_paired_mia_differences.csv",\n',
)
text = replace_once(
    text,
    '''with manifest_path.open("w") as file:
    json.dump(manifest, file, indent=2, default=str)

with (MANIFEST_DIR / "dp_sgd_sweep_manifest.json").open("w") as file:
    json.dump(manifest, file, indent=2, default=str)
''',
    '''write_strict_json(manifest_path, manifest)
write_strict_json(
    MANIFEST_DIR / "dp_sgd_sweep_manifest.json",
    manifest,
)
''',
)
set_source("15d8eb24", text)

text = source("3ae01621")
text = replace_once(
    text,
    '''final_gate = bool(
    condition_gate
    and epsilon_gate
    and mia_gate
    and not missing_outputs
)
''',
    '''paired_gate = bool(
    not dp_sgd_paired_mia_differences.empty
    and set(dp_sgd_paired_mia_differences["comparison_condition"])
    == {"dp_eps_8", "dp_eps_4", "dp_eps_2"}
)

final_gate = bool(
    condition_gate
    and epsilon_gate
    and shadow_budget_gate
    and mia_gate
    and paired_gate
    and not missing_outputs
)
''',
)
text = replace_once(
    text,
    '''    "mia_gate": mia_gate,
    "all_outputs_saved": not missing_outputs,
''',
    '''    "shadow_budget_gate": shadow_budget_gate,
    "mia_gate": mia_gate,
    "paired_difference_gate": paired_gate,
    "all_outputs_saved": not missing_outputs,
''',
)
set_source("3ae01621", text)

# Renumber the final headings and update the interpretation boundary.
for cell in nb["cells"]:
    if cell["cell_type"] != "markdown":
        continue
    text = "".join(cell["source"])
    text = text.replace(
        "## 17. Bootstrap CI table and privacy–utility summary",
        "## 18. Bootstrap CI table and privacy–utility summary",
    )
    text = text.replace(
        "## 18. Save deduplicated warnings, config, and manifest",
        "## 19. Save deduplicated warnings, config, and manifest",
    )
    text = text.replace(
        "## 19. Final protocol and output gate",
        "## 20. Final protocol and output gate",
    )
    text = text.replace(
        "## 20. Interpretation boundary",
        "## 21. Interpretation boundary",
    )
    cell["source"] = text.splitlines(keepends=True)

set_source(
    "51af6449",
    """## 21. Interpretation boundary

- Reused target models mean target IDS results should remain unchanged.
- Every DP shadow must match its requested epsilon within 0.10 and use the fixed target delta.
- Claim a measured MIA reduction only when the paired confidence interval is fully below zero.
- Keep Rare-group findings exploratory because the subgroup is small and multiple comparisons are made.
- Do not add epsilon approximately 1 before the corrected results are reviewed.
""",
)

with NOTEBOOK.open("w", encoding="utf-8") as file:
    json.dump(nb, file, indent=1, ensure_ascii=False)

print(f"Patched {NOTEBOOK}")
