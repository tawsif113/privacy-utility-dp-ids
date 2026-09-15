# Related-work verification and novelty audit

**Verification date:** 2026-09-14  
**Purpose:** prevent the manuscript from repeating metadata-only assumptions or claiming novelty
that the inspected literature does not support.

## Verification method

The four closest IDS papers were checked against their supplied full texts, not only abstracts:

1. Markovic et al., *Applied Intelligence* 54 (2024), DOI
   [10.1007/s10489-024-05589-6](https://doi.org/10.1007/s10489-024-05589-6).
2. Liu et al., *IEEE Transactions on Artificial Intelligence* 6(2) (2025), DOI
   [10.1109/TAI.2024.3357791](https://doi.org/10.1109/TAI.2024.3357791).
3. Tafreshian and Zhang, arXiv:2502.15561 (2025), accepted to IEEE AI+TrustCom 2024,
   [arXiv record](https://arxiv.org/abs/2502.15561).
4. Sharma and Chen, *Electronics* 13(24) (2024), DOI
   [10.3390/electronics13245030](https://doi.org/10.3390/electronics13245030).

The foundational DP, DP-SGD, MIA, auditing, and dataset statements were checked against the
original papers or official proceedings/dataset pages linked below. “Verified” means the stated
claim appears in the inspected source; it does not mean independent reproduction of that paper.

## Closest IDS papers: corrected evidence matrix

| Paper | Verified datasets and task | Mechanism / attacks | Metrics and scale | Code | Exact relationship to this study |
|---|---|---|---|---|---|
| Markovic et al. (2024) | KDD, NSL-KDD, UNSW-NB15, CIC-IDS-2017; attack detection and multiclass attack classification | Horizontal federated random forests; exponential-mechanism private trees; epsilon values 0.1, 0.5, 1, 5 | Accuracy and F1; local versus merged global forests | Yes: `vujicictijana/RF_FL` | Direct DP+IDS utility neighbor, but different model and federated setting; no MIA audit, DP-SGD, five-seed paired analysis, Recall/FNR focus, or empirical leakage comparison |
| Liu et al. (2025 issue; online 2024) | USTC-TFC2016 traffic classification and CICIDS2017 intrusion detection; 6k/3k and 20k/10k train/test subsets | HierarchicalDP adds Laplace noise to selected input features; MPE and EMI membership attacks; NIFGSM and APGD evasion attacks | Membership-inference rate, adversarial-example escape rate, accuracy; 1,000 attack cases per dataset (500 train, 500 test) | Yes: `liuguangrui-hit/HierarchicalDP` | Closest integrated privacy/robustness neighbor, but not DP-SGD and not NSL-KDD/UNSW-NB15; reports attack success rates rather than our multi-seed paired MIA-AUC protocol |
| Tafreshian & Zhang (2025) | NSL-KDD and UNSW-NB15; adversarially perturbed and unaltered test traffic | Genetic-algorithm attack generation constrained by feature mutability, interdependence, and protocols; adversarial training, balancing, feature engineering, ensembles, fine-tuning | Accuracy, precision, recall; cumulative defense pipeline | No repository identified in the paper | Strong adversarial-realism context, but no formal DP or MIA; adversarial evasion is explicitly outside the present paper’s scope |
| Sharma & Chen (2024) | NSL-KDD; nine ML models | PGD, transfer, PGD-assisted transfer, ZOO, Boundary, HopSkipJump | Accuracy, F1, attack-success rate and perturbation distances | Uses public libraries; no study repository stated in the inspected data-availability section | Shows why NIDS threat models matter, but the attacks are adapted from image settings and feature masking is future work; not evidence about membership privacy or DP |

### Corrections to the earlier shortlist

- Liu et al. does identify its datasets: USTC-TFC2016 and CICIDS2017.
- Liu et al. does identify its evaluated architectures: MLP, DNN and a dataset-appropriate CNN
  or LSTM, yielding four architecture types across the study.
- Liu et al. publishes an evaluation-code URL.
- Liu et al. is not a DP-SGD study. Its defense partitions features by security level and adds
  Laplace noise to selected training or testing features.
- Markovic et al. is not the direct experimental baseline reproduced here. It uses federated
  random forests and a tree-specific exponential mechanism; this repository uses a centralized
  MLP and Opacus DP-SGD.
- Tafreshian and Zhang’s reported gains are cumulative defense-pipeline results under their
  adversarial setting. They are not directly comparable to clean-test DP utility values in this
  repository.
- Sharma and Chen explicitly leave practical feature masking to future work. Their high attack
  success rates must not be generalized to protocol-valid attacks against this project’s MLP.

## Privacy and auditing foundations

| Source | Verified point used in the draft | Boundary imposed on this paper |
|---|---|---|
| Dwork et al. (2006), [DOI](https://doi.org/10.1007/11681878_14) | DP bounds how much an algorithm’s output distribution can change between neighbouring datasets | State the adjacency/privacy scope; do not describe near-chance MIA as the DP guarantee |
| Abadi et al. (2016), [arXiv](https://arxiv.org/abs/1607.00133) | DP-SGD clips per-example gradients, adds Gaussian noise and composes privacy loss | Report clipping, noise, sampling, steps/epochs, epsilon and delta |
| Yousefpour et al. (2021), [arXiv](https://arxiv.org/abs/2109.12298) | Opacus implements per-sample-gradient DP training in PyTorch | Name the software and version; avoid claiming Opacus makes non-private preprocessing private |
| Gopi et al. (2021), [NeurIPS](https://proceedings.neurips.cc/paper/2021/hash/6097d8f3714205740f30debe1166744e-Abstract.html) | Privacy-random-variable composition supports accurate numerical accounting for repeated mechanisms such as DP-SGD | Identify the PRV accountant; do not compare epsilon values produced under unstated accountants |
| Shokri et al. (2017), [arXiv](https://arxiv.org/abs/1610.05820) | A black-box attacker can train shadow models and an attack classifier to distinguish members from non-members using prediction behavior | Define attacker knowledge and keep target outputs out of attacker training/calibration |
| Song & Mittal (2021), [USENIX](https://www.usenix.org/conference/usenixsecurity21/presentation/song) | Weakly configured learned attackers can underestimate membership risk; metric-based and per-sample views can be stronger | Use multiple predeclared attack families and avoid “no leakage” language |
| Carlini et al. (2022), [arXiv](https://arxiv.org/abs/2112.03570) | Average attack accuracy/AUC can obscure high-confidence leakage; low-FPR reporting and stronger likelihood-ratio attacks matter | Report TPR at 1%/5% FPR, and list the absence of LiRA/RMIA/adaptive attacks as a limitation |
| Steinke et al. (2023), [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2023/hash/9a6f6e0d6781d1cb8689192408946d73-Abstract-Conference.html) | Empirical DP auditing can produce privacy lower bounds, including from one training run under a specialized canary protocol | Do not call the project’s ordinary MIA evaluation a lower-bound audit of the claimed epsilon |
| Aerni et al. (2024), [DOI](https://doi.org/10.1145/3658644.3690194) | Population-average, weak or defense-unaware attacks can materially underestimate vulnerable-sample leakage | Frame near-chance MIA as attack-relative evidence and disclose absence of canaries/adaptive attacks |

## Dataset foundations

| Dataset | Source checked | Verified use here | Limitation |
|---|---|---|---|
| NSL-KDD | Tavallaee et al. (2009), [official record](https://publications-cnrc.canada.ca/eng/view/object/?id=1b6ee3b8-0771-44ff-8d79-c4f4a2a7292f); [UNB page](https://www.unb.ca/cic/datasets/nsl.html) | Fixed `KDDTrain+` development source and untouched `KDDTest+` utility test | An older benchmark derived from KDD’99; results are not evidence of contemporary deployment performance |
| UNSW-NB15 | Moustafa & Slay (2015), [DOI](https://doi.org/10.1109/MilCIS.2015.7348942); [official dataset page](https://research.unsw.edu.au/projects/unsw-nb15-dataset) | Official training/testing CSV partitions, with training partition internally split for target/shadow roles | Only one target-training seed in this project; selected-threshold FPR is about 42% |

## Defensible novelty position

The inspected literature supports neither “first DP for IDS” nor “first MIA defense for NIDS.”
Those claims are false or at least undefended. The narrower contribution is methodological and
empirical:

> A reproducible, centralized tabular-NIDS evaluation that combines formally accounted Opacus
> DP-SGD, validation-only IDS operating-point selection, condition-matched shadow MIAs under two
> black-box knowledge settings, five-seed paired uncertainty on NSL-KDD, and a bounded
> single-seed UNSW-NB15 consistency check—while reporting false-positive burden and average
> precision alongside Recall/FNR.

Even this should be described as a contribution of the present study, not an absolute priority
claim over all published and unpublished work.

## Claim-to-source map

| Draft claim | Evidence |
|---|---|
| DP and MIA are distinct evidence types | Dwork et al.; Shokri et al.; Steinke et al. |
| Low-FPR behavior and strong/adaptive attacks matter | Carlini et al.; Aerni et al. |
| Prior DP+IDS work spans tree/federated and feature-perturbation mechanisms | Markovic et al.; Liu et al. |
| Adversarial robustness is a different threat axis | Liu et al.; Tafreshian & Zhang; Sharma & Chen |
| NSL-KDD and UNSW-NB15 results should not be equated | Original dataset papers and the project’s distinct protocols |
| No measured leakage-reduction conclusion is supported | Accepted Experiment 08/09 tables, not an external citation |

## Remaining literature tasks before submission

These are editorial checks, not new experiments:

1. Run a final database search (IEEE Xplore, ACM DL, Scopus/Web of Science if available) using the
   exact conjunction `DP-SGD AND (intrusion detection OR network traffic) AND membership
   inference` and record the search date/query.
2. Confirm the target venue’s policy for citing arXiv versions of accepted papers.
3. Export BibTeX from publisher pages and compare it with `references.bib` for punctuation,
   page ranges and proceedings metadata.
4. Add any supervisor-mandated local or regional citation only after verifying that it changes the
   gap analysis or experimental interpretation.
