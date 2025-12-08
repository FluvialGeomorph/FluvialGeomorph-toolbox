# Getting Started with FluvialGeomorph
Presenter: Michael Dougherty, Geographer, USACE
Branding: FluvialGeomorph (FG hex logo included in PPTX)

Slide 1 — Title & Welcome
Title: Getting Started with FluvialGeomorph
Subtitle: Practical ArcGIS workflows used by USACE
Presenter: Michael Dougherty, Geographer, USACE
Speaker notes:
- Welcome the GIS user group. Briefly state purpose: introduce FluvialGeomorph toolbox and manuals so GIS practitioners can understand applied USACE GIS projects and evaluate adoption.

Slide 2 — Agenda
Bullets:
- What is FluvialGeomorph?
- Applied USACE GIS projects (examples)
- User & Technical Manuals (how to use / how to interpret)
- ArcGIS toolbox demo (short)
- Interpreting outputs & limitations
- Next steps & resources
Speaker notes:
- Explain structure and that demo uses example data & user manual steps.

Slide 3 — What is FluvialGeomorph?
Bullets:
- A collection of GIS tools, documented workflows, and supporting data used by USACE for river geomorphology analysis.
- Goal: reproducible, defensible analyses in ArcGIS workflows.
- Focus areas: cross-section processing, OHWM mapping, regional curves, tiered assessment.
Speaker notes:
- Emphasize it’s not a single monolithic app but a toolbox + manuals + data packages.

Slide 4 — Typical USACE applied GIS projects
List of concrete project examples (one-line each):
- OHWM mapping from terrain for permitting and reach delineation
- Cross-section extraction & metrics for restoration design and stability assessment
- Hydraulic regional curve generation and screening
- Tiered assessments for programmatic screening
- Documentation & model certification for regulatory acceptance
Speaker notes:
- For each, include one sentence about GIS role (DEM prep, batch processing, QA/QC outputs for reporting).

Slide 5 — Role of the User Manual (FG-User-Manual)
Bullets:
- Installation & toolbox setup
- Step-by-step tool usage, inputs/outputs, example workflows
- Worked examples and troubleshooting tips
Speaker notes:
- Point to specific sections: installation, demo datasets, example workflows. Encourage reading before running tools.

Slide 6 — Role of the Technical Manual (FG-Tech-Manual)
Bullets:
- Underlying methods and algorithms
- Assumptions, validation, uncertainty
- Guidance for interpreting results and documenting methods for reviews
Speaker notes:
- Stress the importance of the tech manual when presenting results to regulators or stakeholders.

Slide 7 — Key components for GIS users
Bullets:
- FluvialGeomorph ArcGIS toolbox (primary entry point for ArcGIS users)
- Example datasets & stepwise vignettes in the User Manual
- Supporting R packages and API (for advanced/batch workflows)
- ModelCertification & Tech Manual for regulatory acceptance
Speaker notes:
- Reinforce that toolbox + manuals = reproducible workflow. R packages exist but are optional for ArcGIS users.

Slide 8 — Live demo (ArcGIS Toolbox workflow)
Bullets (demo plan):
- Add toolbox to ArcGIS Pro (User Manual install steps)
- Load example dataset provided in the User Manual
- Run cross-section extraction / metric generation tool
- Inspect outputs: feature classes, attribute tables, plots
Speaker notes:
- Use pre-run outputs or screenshots as failover. Show exactly which User Manual pages to follow for this demo.

Slide 9 — Interpreting outputs & limitations
Bullets:
- Outputs: standardized geomorphic metrics, GIS feature classes, CSVs, plots for QA/QC
- Limitations: DEM resolution, algorithm assumptions, need for local calibration
- Where to find more: Tech Manual sections on uncertainty and validation
Speaker notes:
- Give a brief example: DEM error affects bankfull width estimation; refer to Tech Manual guidance.

Slide 10 — Adoption checklist for GIS teams
Bullets:
- Confirm ArcGIS Pro version & dependencies (see User Manual)
- Start with example datasets and replicate the demo
- Use Tech Manual to document assumptions & QA
- Integrate outputs into your GIS deliverables (maps, shapefiles, tables)
Speaker notes:
- Recommend piloting a small project and documenting differences with local methods.

Slide 11 — Resources & next steps
Bullets with links:
- User Manual: https://fluvialgeomorph.github.io/FG-User-Manual/
- Tech Manual: https://fluvialgeomorph.github.io/FG-Tech-Manual/
- Toolbox repo: https://github.com/FluvialGeomorph/FluvialGeomorph-toolbox
- ModelCertification: https://github.com/FluvialGeomorph/ModelCertification
- Contact: Michael Dougherty, Geographer, USACE
Speaker notes:
- Offer a follow-up: 60-min pilot session or installation help. Provide contact details and preferred next steps.

Appendix — Demo runbook & failovers (short)
- Pre-run demo and save outputs
- If network or ArcGIS issues: show screenshots and pre-exported maps
- Exact User Manual pages to follow for installation and the demo tools (list page titles):
  - Installation & Setup
  - Cross-section Extraction example
  - OHWM workflow example

---