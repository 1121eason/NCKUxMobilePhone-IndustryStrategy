# Mobile Phone Industry Competition & Strategy

### Platform knowledge, firm boundaries and competitive advantage

[繁體中文](README.md) · [Full case study in Chinese](docs/industry-strategy.zh-TW.md) · [Strategy playbook](docs/strategy-playbook.zh-TW.md) · [Evidence review](docs/evidence-review.md)

**How can mobile phone brands and contract manufacturers build competitive advantage when a third party controls important technology and development knowledge?**

This repository develops an industry strategy case from a Group H course presentation. It examines the relationship among brand firms, Taiwanese contract manufacturers and platform providers: how knowledge shapes decision rights, how firms choose their boundaries, and how collaboration can protect the value created through specialization.

![Industry structure and strategic choices](assets/competition-map.svg)

## Strategic argument

Brands need enough core component knowledge to translate customer needs into feasible product concepts. Contract manufacturers can move beyond assembly by developing architectural knowledge: integration, testing and implementation problem solving. Platform providers influence both through technology road maps, reference designs and technical support.

The resulting strategic question is how to allocate capabilities and decision rights across partners. Clear specialization requires coordination, incentives and an escalation process for problems that span organizational boundaries.

## What the repository contains

| Deliverable | Analytical purpose |
|---|---|
| [Industry strategy report](docs/industry-strategy.zh-TW.md) | Value chain, competitive pressures, knowledge dependence, firm boundaries and strategic trade-offs |
| [Strategy playbook](docs/strategy-playbook.zh-TW.md) | Actions, risks and proposed measures for brands, manufacturers and platform providers |
| [Evidence review](docs/evidence-review.md) | Published aggregate findings, statistical interpretation and limitations |
| [Source register](docs/sources.md) | Source identities, printed/PDF page references and presentation mapping |
| [Contribution statement](docs/contribution.md) | Group work, personal participation and the scope of this repository |
| [Published summary](data/published-summary.json) | Transcribed aggregate results with no project-level observations |

The five-forces mapping, governance design and performance measures are **new case interpretations and proposals**. They were not tested as interventions in the original study.

## Evidence and limits

The principal source is Shiu and Yasumoto (2018), *The Impact of Platform Providers’ Knowledge on Interfirm Division of Labor: The Case of the Mobile Phone Industry*. The study covers **50 smartphone development projects in 8 Taiwanese contract manufacturers during 2012–2014**, with a questionnaire administered in 2015. The research belongs to the original authors; this repository is a secondary analysis.

![Published aggregate performance](assets/published-performance.svg)

The group combining stronger brand concept rights and stronger manufacturer implementation rights had the highest reported mean PDP, **0.38**, compared with **0.31** in another group. The omnibus ANOVA does not establish a significant pairwise difference between those two groups. PDP is a centered assessment score, not a percentage or financial return.

The final regression reports positive coefficients for concept rights, implementation rights and communication. Early problem solving has only the source's weaker `p < .10` marker; the interaction coefficient is not significant in the final model. Model changes do not establish causal mediation. See the [evidence review](docs/evidence-review.md).

This is a historical case, with no claim to measure the current market, supplier shares or today's company operating models. Apple and Xiaomi references are historical illustrations in the source, not separate company investigations or a claim that every illustration is in the sample.

## Reproducibility

Python 3, standard library only:

```bash
python3 scripts/verify_case_study.py
python3 scripts/build_figures.py --check
```

Checks cover transcription consistency, sample totals, local links and deterministic figures. The underlying questionnaire data are unavailable; the regressions and original project-level analysis cannot be rerun.

## Attribution

The repository owner jointly participated in the full Group H report. The course presentation is a group work; the underlying scholarly research is by Jing-Ming Shiu and Masanori Yasumoto. Full reference PDFs, machine translation and the original slides are retained locally rather than redistributed here. [Sources](docs/sources.md) · [Contribution](docs/contribution.md) · [Notice](NOTICE.md)
