"""Read-only audit of Experiment 06 evidence; no neural-model training.

CLI: python scripts/audit_experiment06.py /path/to/experiment06_evidence.zip
Checks internal integrity and recalculates statistics from per-run tables.
Does not independently reproduce neural predictions or privacy accounting.
"""
import hashlib
import io
import json
from pathlib import Path
import zipfile
import numpy as np
import pandas as pd

SEEDS = [42, 52, 62, 72, 82]
CONDITIONS = ['non_private', 'dp_eps_4', 'dp_eps_2']
THREATS = ['score_only_black_box', 'label_aware_audit']
PRIMARY = dict(zip(THREATS, ['logistic_regression', 'loss_threshold']))
IDS_METRICS = ['recall', 'fnr', 'f1', 'fpr', 'precision', 'pr_auc', 'threshold']
MIA_METRICS = ['mia_auc', 'mia_advantage', 'mia_balanced_accuracy', 'tpr_at_1pct_fpr', 'tpr_at_5pct_fpr']
T_CRITICAL = 2.7764451051977987


def require(test, message):
    if not bool(test):
        raise ValueError(message)


def close(a, b, message, atol=1e-12):
    require(np.allclose(np.asarray(a, dtype=float), np.asarray(b, dtype=float), rtol=0, atol=atol, equal_nan=True), message)


def read_bundle(source):
    source = Path(source)
    if source.is_dir():
        manifest = json.loads((source / 'repeated_runs_manifest.json').read_text())
        names = list(manifest['output_sha256']) + ['repeated_runs_manifest.json']
        require(all(Path(n).name == n for n in names), 'Invalid artifact filename')
        return {n: (source / n).read_bytes() for n in names}
    with zipfile.ZipFile(source) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), 'Duplicate ZIP entries')
        require(all(Path(n).name == n for n in names), 'ZIP must have flat artifact names')
        return {n: archive.read(n) for n in names}


def stats(values):
    values = np.asarray(values, dtype=float)
    require(len(values) == 5 and np.isfinite(values).all(), 'Expected five finite seed values')
    mean = values.mean()
    sd = values.std(ddof=1)
    half = T_CRITICAL * sd / np.sqrt(5)
    return [mean, sd, mean-half, mean+half]


def audit_bundle(blobs):
    m = json.loads(blobs['repeated_runs_manifest.json'])
    require(m['experiment'] == '06_repeated_runs_stability', 'Wrong experiment')
    require(m['protocol_version'] == 'ROADMAP_REVISED_V2', 'Wrong protocol')
    require(m['seeds'] == SEEDS, 'Seeds changed')
    require([c['condition'] for c in m['conditions']] == CONDITIONS, 'Conditions changed')
    require(m['mia']['primary_attacks'] == PRIMARY, 'Primary attacks changed')
    require(m['mia']['new_shadow_models_trained'] == 0 and m['mia']['target_score_tuning'] is False, 'Attack protocol changed')
    require(all(v is True for v in m['protocol_gates'].values()), 'Source protocol gate failed')
    require(len(m['output_sha256']) == 15, 'Incomplete artifact index')
    require(set(blobs) == set(m['output_sha256']) | {'repeated_runs_manifest.json'}, 'Unexpected/missing artifact')
    for name, expected in m['output_sha256'].items():
        require(hashlib.sha256(blobs[name]).hexdigest() == expected, f'Checksum failed: {name}')
    cfg = json.loads(blobs['config.json'])
    for k,v in cfg.items():
        require(m.get(k) == v, f'Manifest/config mismatch: {k}')
    tables = {name: pd.read_csv(io.BytesIO(data)) for name,data in blobs.items() if name.endswith('.csv')}
    ids = tables['repeated_run_ids_results.csv']
    run = tables['repeated_run_configs.csv']
    require(len(ids)==45 and len(run)==15, 'Incomplete run tables')
    expected = {(c,s) for c in CONDITIONS for s in SEEDS}
    require(set(zip(run.condition,run.seed)) == expected and not run.duplicated(['condition','seed']).any(), 'Duplicate/missing run')
    require(run.model_sha256.nunique()==15, 'Model identities are not unique')
    source_by_seed = np.where(run.seed==42, 'accepted_experiment_05', 'trained_experiment_06')
    require((run.run_source == source_by_seed).all(), 'Wrong seed provenance')
    require(run.source_device.eq('cpu').all(), 'Mixed source devices')
    require(run.epochs.eq(30).all() and run.batch_size.eq(256).all() and run.optimizer.eq('Adam').all(), 'Training controls changed')
    close(run.learning_rate,.001,'Learning rate changed');close(run.weight_decay,.0001,'Weight decay changed')
    require((run.formal_dp == run.condition.ne('non_private')).all(), 'Formal DP labels incorrect')
    require(run.secure_mode.eq(False).all(), 'Secure-mode protocol changed')
    for c,e,noise in [('dp_eps_4',4,.6817626953125),('dp_eps_2',2,.88134765625)]:
        r=run[run.condition==c]
        close(r.target_epsilon,e,'Target epsilon mismatch')
        require((r.actual_epsilon-e).abs().le(.1).all(),'Actual epsilon outside accepted tolerance')
        close(r.delta,1/88181,'Delta changed',1e-15)
        close(r.noise_multiplier,noise,'Noise multiplier changed')
        close(r.max_grad_norm,1,'Clipping changed');close(r.sample_rate,1/345,'Sampling rate changed')
        require(r.accountant.eq('prv').all() and r.poisson_sampling.eq(True).all(),'Accountant/sampling mismatch')
    require(run[run.condition=='non_private'].actual_epsilon.isna().all(),'Non-private has finite epsilon')
    manifest_runs={(r['condition'],r['seed']):r for r in m['target_run_configs']}
    for _,r in run.iterrows():
        mr=manifest_runs[(r.condition,int(r.seed))]
        for k in ['model_sha256','cache_fingerprint','run_source']:
            require(r[k]==mr[k],f'Run manifest disagreement: {k}')
        sw=mr['source_software']
        require(sw['torch']=='2.11.0+cpu' and sw['opacus']=='1.6.0' and sw['numpy']=='2.1.3' and sw['pandas']=='2.2.3','Source software mismatch')
        require(sw.get('sklearn',sw.get('scikit-learn'))=='1.6.1','Source sklearn mismatch')
        for k in ['actual_epsilon','noise_multiplier','delta','selected_threshold']:
            close(r[k], np.nan if mr[k] is None else mr[k],f'Run manifest mismatch: {k}')
    require(not ids.duplicated(['condition','seed','split','threshold_policy']).any(),'Duplicate IDS evaluation')
    for _,r in ids.iterrows():
        tn,fp,fn,tp=[float(r[k]) for k in ['tn','fp','fn','tp']]
        require(all(x>=0 and x.is_integer() for x in [tn,fp,fn,tp]), 'Invalid confusion counts')
        den=tn+fp+fn+tp
        metrics={'recall':tp/(tp+fn),'fnr':fn/(tp+fn),'fpr':fp/(fp+tn),'precision':tp/(tp+fp) if tp+fp else 0,'f1':2*tp/(2*tp+fp+fn),'accuracy':(tp+tn)/den}
        for key,value in metrics.items():close(r[key],value,f'IDS count/metric mismatch: {key}')
        if r['split']=='KDDTest+':require(den==22544 and tp+fn==12833 and tn+fp==9711,'Test population changed')
        else:require(r['split']=='target_validation' and den==12597,'Validation population changed')
    tuned=ids[(ids['split']=='KDDTest+') & (ids.threshold_policy=='validation_selected_F2')].copy()
    require(len(tuned)==15 and set(zip(tuned.condition,tuned.seed))==expected,'Tuned IDS rows incomplete')
    for _,r in tuned.iterrows():
        rr=run[(run.condition==r.condition)&(run.seed==r.seed)].iloc[0]
        close(r.threshold,rr.selected_threshold,'Threshold/config mismatch')
    for policy,file in [('primary','repeated_run_mia_results.csv'),('secondary','secondary_mia_results.csv')]:
        d=tables[file]
        require(len(d)==30 and not d.duplicated(['condition','seed','threat_model']).any(),'Incomplete MIA table')
        require(set(zip(d.condition,d.seed,d.threat_model))=={(c,s,t) for c,s in expected for t in THREATS},'MIA key mismatch')
        require(d.analysis_role.eq(policy).all(),'Mixed attacker policy')
        require(d.members.eq(12597).all() and d.nonmembers.eq(12597).all() and d.n.eq(25194).all(),'MIA population changed')
        require(np.isfinite(d[MIA_METRICS]).all().all() and ((d[MIA_METRICS]>=0)&(d[MIA_METRICS]<=1)).all().all(),'Invalid MIA values')
        for (c,t),group in d.groupby(['condition','threat_model']):
            require(group.attack_model.nunique()==1 and group.operating_threshold.nunique()==1,'Attacker changed across seeds')
            if policy=='primary':require(group.attack_model.iloc[0]==PRIMARY[t],'Primary family changed')
    def check_summaries(summary, values_for):
        require(not summary.duplicated([c for c in ['condition','comparison_condition','domain','threat_model','metric'] if c in summary]).any(),'Duplicate summaries')
        for _,r in summary.iterrows():
            require(r.n_seeds==5,'Summary missing seeds')
            close(r[['mean','standard_deviation','ci_low','ci_high']],stats(values_for(r)),f'Summary mismatch: {r.metric}')
    primary=tables['repeated_run_mia_results.csv']
    def primary_values(r):
        data=tuned if r.domain=='IDS' else run if r.domain=='privacy_accounting' else primary
        mask=data.condition.eq(r.condition)
        if r.domain=='MIA':mask &= data.threat_model.eq(r.threat_model)
        return data.loc[mask,r.metric]
    require(len(tables['repeated_run_summary.csv'])==53,'Incomplete primary summary')
    check_summaries(tables['repeated_run_summary.csv'],primary_values)
    secondary=tables['secondary_mia_results.csv']
    require(len(tables['secondary_mia_summary.csv'])==30,'Incomplete secondary summary')
    check_summaries(tables['secondary_mia_summary.csv'],lambda r:secondary.loc[secondary.condition.eq(r.condition)&secondary.threat_model.eq(r.threat_model),r.metric])
    for policy,diffname,sumname in [('primary','repeated_run_paired_differences.csv','repeated_run_paired_summary.csv'),('secondary','secondary_mia_paired_differences.csv','secondary_mia_paired_summary.csv')]:
        diff=tables[diffname];summary=tables[sumname]
        require(len(diff)==(170 if policy=='primary' else 100),'Incomplete paired differences')
        require(len(summary)==(34 if policy=='primary' else 20),'Incomplete paired summary')
        for _,r in diff.iterrows():
            data=tuned if policy=='primary' and r.domain=='IDS' else primary if policy=='primary' else secondary
            mask=data.seed.eq(r.seed)
            if 'threat_model' in data:mask &= data.threat_model.eq(r.threat_model)
            a=data.loc[mask & data.condition.eq('non_private'),r.metric]
            b=data.loc[mask & data.condition.eq(r.comparison_condition),r.metric]
            require(len(a)==len(b)==1,'Unpaired observations')
            close(r.difference_dp_minus_non_private,b.iloc[0]-a.iloc[0],'Paired difference incorrect')
        def paired_values(r):
            mask=diff.comparison_condition.eq(r.comparison_condition)&diff.metric.eq(r.metric)
            if pd.notna(r.threat_model):mask &= diff.threat_model.eq(r.threat_model)
            if 'domain' in diff:mask &= diff.domain.eq(r.domain)
            d=diff.loc[mask]
            require(set(d.seed)==set(SEEDS) and not d.seed.duplicated().any(),'Paired seeds incorrect')
            return d.difference_dp_minus_non_private
        check_summaries(summary,paired_values)
    verification=tables['seed42_import_verification.csv']
    require(len(verification)==24 and verification.verification_passed.eq(True).all(),'Seed-42 verification incomplete')
    for _,r in verification.iterrows():
        tol=1e-8 if r.metric=='mia_auc' else 1e-10
        close(r.absolute_difference,abs(r.recomputed_value-r.accepted_experiment_05_value),'Incorrect saved verification difference')
        require(r.absolute_difference<=tol and r.verification_atol==tol,'Verification tolerance violated')
    fixed=tables['fixed_attacker_verification.csv']
    require(len(fixed)==12 and fixed.verification_passed.eq(True).all(),'Attacker reconstruction failed')
    close(fixed.accepted_operating_threshold,fixed.reconstructed_operating_threshold,'Calibration threshold mismatch',1e-8)
    close(fixed.accepted_shadow_calibration_auc,fixed.reconstructed_shadow_calibration_auc,'Calibration AUC mismatch',1e-10)
    sample=tables['target_mia_sample_manifest.csv']
    require(len(sample)==25194 and sample.membership.value_counts().to_dict()=={0:12597,1:12597},'MIA sample imbalance')
    require(sample.row_id.nunique()==25194,'Overlapping/duplicate MIA records')
    counts=sample.groupby(['membership','true_label']).size().unstack()
    require(counts.loc[0].equals(counts.loc[1]),'MIA class balance differs')
    report={'accepted_for_final_analysis':True,'manifest_sha256':hashlib.sha256(blobs['repeated_runs_manifest.json']).hexdigest(),'verified_artifact_checksums':15,'condition_seed_runs':15,'new_target_runs':12,'primary_mia_rows':30,'secondary_mia_rows':30,'summaries_and_paired_differences_recomputed':True,'neural_predictions_independently_recomputed':False,'source_model_files_available_in_bundle':False,'scope':'Training-seed stability conditional on fixed data and attackers; no universal optimum or leakage-reduction claim.'}
    return m,tables,report

if __name__=='__main__':
    import sys
    _,_,report=audit_bundle(read_bundle(sys.argv[1]))
    print(json.dumps(report,indent=2))
