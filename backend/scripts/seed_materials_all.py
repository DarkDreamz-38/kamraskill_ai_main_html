"""Seed learning materials for all competencies (prototype demo data).

The MCQ engine splits material into numbered sections ("1. Title") and
generates exactly one question per section; the frontend requests 20
questions, so each material contains exactly 20 numbered sections.

Idempotent: re-running updates existing rows instead of duplicating.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models import Competency, LearningMaterial, MaterialCompetency


def build_material(title, sections):
    """sections: list of 20 (heading, body) tuples -> formatted material text."""
    assert len(sections) == 20, f"{title}: needs 20 sections, got {len(sections)}"
    parts = [title, ""]
    for i, (h, body) in enumerate(sections, 1):
        parts.append(f"{i}. {h}")
        parts.append(body)
        parts.append("")
    return "\n".join(parts).strip()


DATA_ANALYSIS_SECTIONS = [
    ("Data Collection Instruments", "Survey instruments must be pre-tested before fielding to catch ambiguous wording. Enumerator training and continuous monitoring of response rates protect data quality from the start."),
    ("Data Cleaning Workflows", "Data cleaning identifies outliers, resolves missing values, and validates entries against logical constraints. Every cleaning step must be documented so the dataset remains reproducible."),
    ("Outlier Detection Methods", "Z-scores and the interquartile range method flag observations that deviate strongly from the bulk of the data. Values beyond three standard deviations from the mean warrant investigation rather than automatic deletion."),
    ("Missing Data Imputation", "Deletion is acceptable when fewer than five percent of records are affected. Mean, median, and regression imputation preserve sample size for structured datasets, but the chosen method must be reported."),
    ("Measures of Central Tendency", "The arithmetic mean, median, and mode summarize typical values. The median is robust to extreme values and is preferred for skewed distributions such as income data."),
    ("Measures of Dispersion", "Variance and standard deviation quantify the spread around the mean. The coefficient of variation enables comparison across datasets measured in different units."),
    ("Distribution Shape", "Histograms and box plots reveal skewness, modality, and tail behavior. Skewness measures asymmetry while kurtosis measures tail heaviness relative to a normal distribution."),
    ("Sampling Theory Basics", "Probability sampling gives every population unit a known, nonzero selection chance. A current sampling frame is the prerequisite for unbiased estimates."),
    ("Stratified Sampling", "Stratification divides the population into homogeneous strata and samples within each. It improves precision when strata differ sharply on the study variable."),
    ("Cluster and Multistage Designs", "Cluster sampling selects groups first, which reduces field cost but inflates variance; the design effect quantifies the loss. National surveys typically combine clustering and stratification in multistage designs."),
    ("Hypothesis Testing Framework", "Testing begins with a null hypothesis of no effect and a chosen significance level, conventionally 0.05. A p-value below the threshold leads to rejection of the null hypothesis."),
    ("Type I and Type II Errors", "A Type I error rejects a true null; a Type II error fails to reject a false null. Statistical power above 0.8 is recommended before fielding a study."),
    ("Confidence Intervals", "A 95 percent confidence interval means the estimation procedure captures the true parameter in 95 percent of repeated samples. Intervals communicate precision that point estimates hide."),
    ("Correlation Analysis", "The Pearson correlation coefficient ranges from minus one to plus one and measures linear association. Correlation never establishes causation on its own."),
    ("Simple Linear Regression", "Simple regression models a dependent variable as a linear function of one predictor. The slope coefficient gives the expected change in the outcome for a unit change in the predictor."),
    ("Multiple Regression", "Multiple regression extends the model to several predictors, with each coefficient interpreted holding the others constant. Residual diagnostics check linearity, homoscedasticity, and normality."),
    ("Model Fit and R-Squared", "R-squared reports the proportion of outcome variance explained by the model. A high R-squared alone does not guarantee a valid model; diagnostics and theory must agree."),
    ("Chi-Square Tests", "The chi-square test evaluates association between categorical variables using observed versus expected frequencies. Expected counts below five in any cell weaken the approximation."),
    ("Time Series Components", "Time series decompose into trend, seasonal, cyclical, and irregular components. Year-on-year growth neutralizes seasonality and is standard in official releases."),
    ("Official Statistics Practice", "Government data analysis supports policy evaluation, resource allocation, and national indicator monitoring. Officers must follow the Fundamental Principles of Official Statistics: impartiality, rigor, and respondent confidentiality."),
]

STATISTICAL_REASONING_SECTIONS = [
    ("Population and Sample", "A population includes every unit of interest; a sample is the observed subset. Conclusions about the population are valid only when the sample is representative."),
    ("Probability Foundations", "Probability quantifies uncertainty on a zero-to-one scale. Addition and multiplication rules combine event probabilities and underpin all inferential methods."),
    ("Random Variables", "A random variable assigns numerical outcomes to random processes. Distributions describe the probabilities of its possible values."),
    ("The Normal Distribution", "The normal distribution is symmetric and fully described by its mean and standard deviation. Many estimators are approximately normal for large samples by the Central Limit Theorem."),
    ("Sampling Distributions", "The sampling distribution of a statistic describes its variability across repeated samples. The standard error shrinks with the square root of the sample size."),
    ("The Central Limit Theorem", "For large random samples, the sampling distribution of the mean is approximately normal regardless of the population's shape. This justifies interval construction and hypothesis tests."),
    ("Point Estimation", "An estimator is a rule for computing a population value from a sample. Unbiasedness means the estimator's expected value equals the true parameter."),
    ("Efficiency and Consistency", "Efficiency favors the estimator with the smallest variance among unbiased options. Consistency means the estimator converges to the truth as the sample grows."),
    ("Simple Random Sampling", "Simple random sampling gives equal selection probability to all units. It is conceptually clean but often inefficient when the population is heterogeneous."),
    ("Systematic Sampling", "Systematic sampling selects units at fixed intervals from a random start. It is operationally simple but risky when the list has periodic structure."),
    ("Stratification Logic", "Strata should be internally homogeneous and externally heterogeneous. Gains in precision are largest when strata differ strongly on the study variable."),
    ("Cluster Sampling Tradeoffs", "Clustering reduces travel cost but increases variance because units within a cluster resemble each other. The design effect measures the effective loss of sample size."),
    ("Non-Sampling Errors", "Coverage gaps, nonresponse, and measurement error cause non-sampling errors that grow with poor procedure, not with small samples. Documentation and follow-up are the main defenses."),
    ("Significance Levels", "The significance level defines the tolerated probability of a Type I error. Conventionally 0.05, it should reflect the real cost of a false alarm."),
    ("One and Two Tailed Tests", "One-tailed tests are used for directional hypotheses; two-tailed tests detect deviations in either direction. The choice must be made before seeing the data."),
    ("Power Analysis", "Power, one minus the Type II error probability, depends on sample size, effect size, and significance level. Underpowered studies waste resources and produce inconclusive results."),
    ("Index Numbers", "Laspeyres indices use base-period weights and Paasche indices use current-period weights. The Consumer Price Index tracks retail price changes for a fixed basket."),
    ("Seasonal Adjustment", "Seasonal adjustment removes recurring calendar effects so underlying movements become visible. Adjusted series must be clearly labeled to avoid confusing users."),
    ("Interpreting Non-Significance", "A non-significant result means absence of evidence, not evidence of absence. Officers should report confidence intervals rather than binary verdicts."),
    ("Principles of Official Statistics", "Statistical reasoning in government demands objectivity, transparency of methods, and prudent interpretation. Uncertainty is reported alongside every estimate."),
]

DATA_VISUALIZATION_SECTIONS = [
    ("Visual Encoding Channels", "Position along a common scale is the most accurately perceived visual channel, followed by length, angle, and area. Choosing the right channel prevents misreading."),
    ("Bar Charts", "Bar charts encode magnitude by length and are the default for comparing categories. Ordering bars by value rather than alphabetically speeds comprehension."),
    ("Line Charts", "Line charts encode trends over continuous time. Too many series create spaghetti plots; highlight the relevant line and mute the rest."),
    ("Pie and Donut Charts", "Pie charts encode parts of a whole through angle and work only with a few slices. When precise comparison matters, a bar chart is safer."),
    ("Scatter Plots", "Scatter plots reveal relationships between two quantitative variables. Adding trend lines or encodings for a third variable must remain legible."),
    ("Heatmaps", "Heatmaps use color intensity for values in a matrix. Sequential color scales suit ordered data; diverging scales suit values around a neutral midpoint."),
    ("The Data-Ink Ratio", "Maximize the share of ink that carries information. Gridlines, borders, and decoration that add nothing should be removed."),
    ("Axis Integrity", "Bar charts must start at zero so length comparisons remain truthful. Truncated axes exaggerate change and mislead readers."),
    ("Color and Accessibility", "Use high-contrast palettes and avoid red-green pairs that colorblind readers cannot distinguish. WCAG guidance applies to charts as much as text."),
    ("Labels and Annotations", "Axes need units and charts need titles that state the takeaway. Direct annotation beats forcing readers through a legend lookup."),
    ("Small Multiples", "Small multiples repeat the same chart across categories or time slices. Consistent scales across panels make comparison honest."),
    ("Dashboard Layout", "Place the most important indicator top-left, where reading starts. Consistent color meanings across panels build trust."),
    ("Interactivity with Purpose", "Filtering, highlighting, and drill-down should answer real questions. Gimmicks that add clicks without insight reduce usability."),
    ("Context and Benchmarks", "A number becomes a judgment only with context. Targets, prior periods, or peer comparisons turn raw values into decisions."),
    ("Data Storytelling", "Pair each chart with context, insight, and implication. One message per chart keeps the audience oriented."),
    ("Charting for Publication", "Official charts must be reproducible: cite the data source, reference period, and any adjustments. Styling should follow the publishing institution's standards."),
    ("Dual Axis Risks", "Dual axes invite spurious correlation readings and should be avoided. Two series with different units are better shown as separate panels."),
    ("Three-Dimensional Effects", "3D effects distort areas and angles, corrupting the very encodings readers rely on. Flat design is the professional standard."),
    ("Showing Uncertainty", "Error bands and interval annotations communicate uncertainty honestly. Omitting uncertainty overstates confidence in the finding."),
    ("Common Pitfalls Review", "Truncated axes, cherry-picked windows, and rainbow palettes are the most common visualization failures. Always ask what a chart hides as well as what it shows."),
]

COMMUNICATION_SECTIONS = [
    ("Structure of Official Letters", "Official letters follow a fixed structure: reference number, date, salutation, subject line, body, and closing authority. The subject line states the purpose in a single line."),
    ("Noting and Drafting on Files", "File notations separate facts, analysis, and recommendation so decision makers can follow the reasoning. Clarity and brevity are obligations, not stylistic choices."),
    ("Plain Language Policy", "Short sentences, active voice, and no unexplained jargon make government communication accessible. Plain language reduces misinterpretation and follow-up queries."),
    ("The BLUF Principle", "Briefings to senior leadership lead with the bottom line up front, followed by supporting evidence and caveats. Busy readers should get the answer in the first line."),
    ("Facts Versus Opinion", "Written analysis must distinguish facts, assumptions, and opinion explicitly. Blurring them erodes credibility and invites challenge."),
    ("Communicating Numbers", "Lead with the finding, not the method: what changed, by how much, and why it matters. Always attach the reference period and the data source."),
    ("Tables and Charts in Reports", "Use tables for exact values and charts for patterns. Every exhibit needs a self-explanatory title and source note."),
    ("Statistical Press Notes", "Press notes must be factual, neutral, and cleared by competent authority. Only aggregates consistent with statistical confidentiality may be published."),
    ("Handling Errors Transparently", "Errors should be corrected quickly and visibly, with the correction dated. Transparent correction preserves institutional trust."),
    ("Meeting Discipline", "Circulate agendas in advance and record decisions with owners and deadlines. Minutes should go out promptly while memories are fresh."),
    ("Presentation Structure", "Structure presentations as situation, complication, question, answer. One idea per slide with visuals preferred over text blocks."),
    ("Anticipating Questions", "Prepare a backup annex for likely challenges before the meeting. Anticipation converts hostile questions into planned answers."),
    ("Interdepartmental Correspondence", "Requests to other ministries must cite the relevant rules and state exactly what is sought with a deadline. Courtesy and precision travel together."),
    ("Mentoring Junior Staff", "Feedback should be specific, timely, and behavioral rather than personal. Good mentors confirm understanding in writing."),
    ("Listening and Clarification", "Listening first, clarifying expectations, and confirming agreements in writing prevent most workplace conflict. Written trails protect both officer and institution."),
    ("Public Grievance Responses", "Grievance replies must address the specific complaint, cite the action taken, and offer an escalation path. Generic replies invite escalation."),
    ("Media Interaction Rules", "Officers speak to media only within their delegated mandate. Speculation on unpublished data is a confidentiality breach."),
    ("Social Media Standards", "Social posts follow the same accuracy standards as formal releases. Institutional accounts never express personal opinions."),
    ("Cross-Cultural Communication", "Working with state offices and field staff requires sensitivity to regional languages and norms. Translations of key material widen reach."),
    ("Ethics in Communication", "Never misrepresent data, overstate certainty, or conceal unfavorable findings. Honest communication is the foundation of official credibility."),
]

POLICY_SECTIONS = [
    ("The Policy Cycle", "Public policy moves through agenda setting, formulation, adoption, implementation, and evaluation. Data officers contribute baselines, monitoring indicators, and outcome measurement at each stage."),
    ("Evidence-Based Policy", "Evidence-based policy requires clearly stated objectives, measurable indicators, and credible counterfactuals. Without a counterfactual, attribution of impact is guesswork."),
    ("India's Statistical System", "The statistical system spans MoSPI, the National Statistical Office, state bureaus, and line ministries. The National Statistical Commission recommends standards and coordinates."),
    ("Constitutional Assignment", "Union, State, and Concurrent lists determine which governments collect which data. Understanding assignment explains many data-flow frictions."),
    ("Centrally Sponsored Schemes", "Centrally sponsored and central sector schemes carry distinct funding and monitoring requirements. Physical and financial progress are tracked against approved targets."),
    ("Logical Framework Analysis", "The logframe links inputs, activities, outputs, outcomes, and impact in one matrix. It forces schemes to state their causal logic explicitly."),
    ("SMART Indicators", "Key performance indicators must be specific, measurable, achievable, relevant, and time-bound. Vague indicators make monitoring theater."),
    ("Monitoring Versus Evaluation", "Monitoring tracks ongoing delivery; evaluation judges design and impact periodically. Both are needed, and neither substitutes for the other."),
    ("Evaluation Designs", "Designs range from before-after comparisons to randomized controlled trials. The choice balances rigor, cost, feasibility, and ethics."),
    ("Baseline Studies", "Baselines fix the starting values against which change is measured. Skipping baselines makes later evaluation nearly worthless."),
    ("Data in Policy Formulation", "Options memos need costed scenarios with explicit assumptions. Data officers supply the analytical backbone and flag data gaps early."),
    ("Stakeholder Mapping", "Map stakeholders by interest and influence to plan consultations. Documenting dissent honestly strengthens, not weakens, the final decision."),
    ("Consultation Processes", "Consultations must give genuine weight to feedback, with a published summary of responses. Token consultation breeds cynicism."),
    ("The DPDP Act", "The Digital Personal Data Protection Act governs processing of personal data with purpose limitation and consent requirements. Officers must know when statistical exceptions apply and when they do not."),
    ("Statistical Confidentiality", "Respondent identity is protected in all publications; only aggregates are released. Cell suppression and rounding rules prevent re-identification."),
    ("Right to Information Duties", "Records must be maintained and disclosed per the Right to Information Act, with defined exceptions. Timely publication reduces RTI burden."),
    ("Records Retention", "Retention schedules define how long records live and when they are archived or destroyed. Good retention practice protects both accountability and privacy."),
    ("Forecasting and Uncertainty", "Forecasts must communicate uncertainty to prevent false precision from anchoring decisions. Ranges and scenario framing are standard tools."),
    ("Program Dashboards", "Dashboards for flagship schemes track physical and financial progress in near real time. Data quality checks must run before publication, not after."),
    ("Fundamental Principles of Official Statistics", "The Principles bind agencies to impartiality, scientific standards, and transparency of method. Adherence is what makes official statistics trustworthy."),
]

MATERIALS = {
    "Data Analysis": ("data_analysis_fundamentals.pdf", "Data Analysis Fundamentals for Public Sector Officers", DATA_ANALYSIS_SECTIONS),
    "Statistical Reasoning": ("statistical_reasoning_handbook.pdf", "Statistical Reasoning Handbook", STATISTICAL_REASONING_SECTIONS),
    "Data Visualization": ("data_visualization_fundamentals.pdf", "Data Visualization Fundamentals", DATA_VISUALIZATION_SECTIONS),
    "Communication": ("official_communication_guide.pdf", "Official Communication Guide for Statistical Officers", COMMUNICATION_SECTIONS),
    "Policy Understanding": ("policy_fundamentals_notes.pdf", "Public Policy Fundamentals for Data Officers", POLICY_SECTIONS),
}

db = SessionLocal()
try:
    for comp_name, (filename, title, sections) in MATERIALS.items():
        comp = db.query(Competency).filter(Competency.name == comp_name).first()
        if not comp:
            print(f"! Competency '{comp_name}' not found, skipping")
            continue

        text = build_material(title, sections)

        material = db.query(LearningMaterial).filter(LearningMaterial.title == title).first()
        if material:
            material.extracted_text = text
            material.filename = filename
            material.pages = 1
            action = "updated"
        else:
            material = LearningMaterial(
                filename=filename,
                title=title,
                extracted_text=text,
                pages=1,
            )
            db.add(material)
            db.flush()
            action = "created"

        mapping = db.query(MaterialCompetency).filter(
            MaterialCompetency.material_id == material.id,
            MaterialCompetency.competency_id == comp.id,
        ).first()
        if mapping:
            mapping.relevance = 100.0
        else:
            db.add(MaterialCompetency(
                material_id=material.id,
                competency_id=comp.id,
                relevance=100.0,
            ))

        print(f"OK {comp_name}: {action} material #{material.id} (20 sections)")
    db.commit()
    print("Seeding complete.")
finally:
    db.close()
