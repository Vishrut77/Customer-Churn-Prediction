import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette Definitions
    DARK_BG = RGBColor(15, 23, 42)       # Slate 900
    DARK_CARD = RGBColor(30, 41, 59)     # Slate 800
    LIGHT_BG = RGBColor(248, 250, 252)   # Slate 50
    CARD_BG = RGBColor(255, 255, 255)    # White
    CARD_BORDER = RGBColor(226, 232, 240)# Slate 200
    BORDER_DARK = RGBColor(51, 65, 85)   # Slate 700

    PRIMARY = RGBColor(79, 70, 229)      # Indigo 600
    PRIMARY_LIGHT = RGBColor(99, 102, 241) # Indigo 500
    PRIMARY_BG = RGBColor(238, 242, 255) # Indigo 50

    TEXT_DARK = RGBColor(15, 23, 42)     # Slate 900
    TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500
    TEXT_LIGHT = RGBColor(241, 245, 249) # Slate 100
    TEXT_LIGHT_MUTED = RGBColor(148, 163, 184) # Slate 400

    EMERALD = RGBColor(16, 185, 129)     # Emerald 500
    EMERALD_BG = RGBColor(236, 253, 245) # Emerald 50
    AMBER = RGBColor(245, 158, 11)       # Amber 500
    AMBER_BG = RGBColor(254, 243, 199)   # Amber 50
    ROSE = RGBColor(239, 68, 68)         # Rose 500
    ROSE_BG = RGBColor(254, 242, 242)    # Rose 50

    FONT_MAIN = "Calibri"

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.color.rgb = color
        return bg

    def add_header(slide, tag_text, title_text, subtitle_text, slide_num):
        # Category Tag
        tag_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(3.2), Inches(0.32))
        tag_box.fill.solid()
        tag_box.fill.fore_color.rgb = PRIMARY_BG
        tag_box.line.color.rgb = PRIMARY_LIGHT
        tag_box.line.width = Pt(1)
        tf = tag_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = tag_text.upper()
        run.font.name = FONT_MAIN
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = PRIMARY

        # Title
        tbox = slide.shapes.add_textbox(Inches(0.8), Inches(0.78), Inches(10.5), Inches(0.55))
        tf = tbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = title_text
        run.font.name = FONT_MAIN
        run.font.size = Pt(22)
        run.font.bold = True
        run.font.color.rgb = TEXT_DARK

        # Subtitle
        sbox = slide.shapes.add_textbox(Inches(0.8), Inches(1.36), Inches(11.0), Inches(0.35))
        tf = sbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = subtitle_text
        run.font.name = FONT_MAIN
        run.font.size = Pt(12)
        run.font.color.rgb = TEXT_MUTED

        # Slide Number Badge
        nbox = slide.shapes.add_textbox(Inches(11.8), Inches(7.05), Inches(1.0), Inches(0.3))
        tf = nbox.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.RIGHT
        run = p.add_run()
        run.text = f"Slide {slide_num:02d} / 10"
        run.font.name = FONT_MAIN
        run.font.size = Pt(10)
        run.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 1: Title Slide (Dark Theme)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, DARK_BG)

    # Accent decorative banner top
    banner = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
    banner.fill.solid()
    banner.fill.fore_color.rgb = PRIMARY
    banner.line.color.rgb = PRIMARY

    # Badge Pill
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.0), Inches(4.5), Inches(0.36))
    badge.fill.solid()
    badge.fill.fore_color.rgb = DARK_CARD
    badge.line.color.rgb = PRIMARY_LIGHT
    badge.line.width = Pt(1.2)
    tf = badge.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = "MACHINE LEARNING CAPSTONE PROJECT | SEM-7"
    run.font.name = FONT_MAIN
    run.font.size = Pt(10)
    run.font.bold = True
    run.font.color.rgb = PRIMARY_LIGHT

    # Main Title
    tbox = s1.shapes.add_textbox(Inches(0.9), Inches(1.5), Inches(11.5), Inches(1.4))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "Customer Churn Prediction System"
    run.font.name = FONT_MAIN
    run.font.size = Pt(40)
    run.font.bold = True
    run.font.color.rgb = TEXT_LIGHT

    # Subtitle
    sub_box = s1.shapes.add_textbox(Inches(0.9), Inches(2.95), Inches(11.5), Inches(0.7))
    tf = sub_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "An End-to-End ML Intelligence Dashboard, REST API & Automated Retention Recommender"
    run.font.name = FONT_MAIN
    run.font.size = Pt(17)
    run.font.color.rgb = TEXT_LIGHT_MUTED

    # 4 Tech Stack Cards
    cards_data = [
        ("FASTAPI & UVICORN", "High-Performance Backend", "Asynchronous Python server with automatic OpenAPI Swagger docs and strict request handling."),
        ("RANDOM FOREST ML", "Scikit-Learn Classifier", "Ensemble of 100 decision trees fitted with ColumnTransformer & OneHotEncoder for 78.6% accuracy."),
        ("INTERACTIVE UI", "Vanilla JS & Chart.js", "Full-featured web dashboard with 4 KPI cards, 3 visual charts, and a 21-column customer explorer."),
        ("AUTOMATED QA", "13 Pytest Test Cases", "100% test coverage across endpoints, query filtering, pagination, and zero-value edge cases.")
    ]

    card_w = Inches(2.7)
    card_h = Inches(2.2)
    card_y = Inches(4.0)

    for i, (pill, title, desc) in enumerate(cards_data):
        cx = Inches(0.9 + i * 2.93)
        cshape = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, card_y, card_w, card_h)
        cshape.fill.solid()
        cshape.fill.fore_color.rgb = DARK_CARD
        cshape.line.color.rgb = BORDER_DARK
        cshape.line.width = Pt(1)

        tf = cshape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
        tf.margin_bottom = Inches(0.1)

        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = pill
        run.font.name = FONT_MAIN
        run.font.size = Pt(9.5)
        run.font.bold = True
        run.font.color.rgb = PRIMARY_LIGHT

        p2 = tf.add_paragraph()
        p2.space_before = Pt(6)
        run2 = p2.add_run()
        run2.text = title
        run2.font.name = FONT_MAIN
        run2.font.size = Pt(13)
        run2.font.bold = True
        run2.font.color.rgb = TEXT_LIGHT

        p3 = tf.add_paragraph()
        p3.space_before = Pt(8)
        run3 = p3.add_run()
        run3.text = desc
        run3.font.name = FONT_MAIN
        run3.font.size = Pt(10.5)
        run3.font.color.rgb = TEXT_LIGHT_MUTED

    # Footer Metadata
    ft_box = s1.shapes.add_textbox(Inches(0.9), Inches(6.8), Inches(11.5), Inches(0.4))
    tf = ft_box.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "Dataset: IBM Telco Customer Churn (7,043 Records)  |  Architecture: Production ML Pipeline + REST API + Modern Web UI"
    run.font.name = FONT_MAIN
    run.font.size = Pt(10)
    run.font.color.rgb = TEXT_LIGHT_MUTED

    # ==========================================
    # SLIDE 2: Business Context & Project Motivation
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, LIGHT_BG)
    add_header(s2, "01 | Problem Statement & Context", "The Telecom Churn Dilemma & Project Motivation", "Addressing revenue leakage and shifting from reactive cancellation handling to proactive retention", 2)

    # 3 Stat Cards across top
    stats_data = [
        ("5x - 7x", "Acquisition vs. Retention Cost", "Acquiring a new subscriber costs drastically more than retaining an existing customer.", ROSE, ROSE_BG),
        ("26.54%", "Portfolio Churn Baseline", "Over 1 in 4 customers churn historically (1,869 out of 7,043 accounts).", AMBER, AMBER_BG),
        ("15% - 25%", "Annual Telecom Industry Attrition", "Average yearly customer loss in telecommunications without predictive intervention.", PRIMARY, PRIMARY_BG)
    ]

    for i, (stat, label, detail, color, bg) in enumerate(stats_data):
        cx = Inches(0.8 + i * 3.98)
        box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.85), Inches(3.75), Inches(1.3))
        box.fill.solid()
        box.fill.fore_color.rgb = bg
        box.line.color.rgb = color
        box.line.width = Pt(1)

        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.12)
        tf.margin_bottom = Inches(0.05)

        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = stat
        run.font.name = FONT_MAIN
        run.font.size = Pt(26)
        run.font.bold = True
        run.font.color.rgb = color

        p2 = tf.add_paragraph()
        run2 = p2.add_run()
        run2.text = label.upper()
        run2.font.name = FONT_MAIN
        run2.font.size = Pt(9.5)
        run2.font.bold = True
        run2.font.color.rgb = TEXT_DARK

        p3 = tf.add_paragraph()
        run3 = p3.add_run()
        run3.text = detail
        run3.font.name = FONT_MAIN
        run3.font.size = Pt(9)
        run3.font.color.rgb = TEXT_MUTED

    # Left Column: The Business Problem
    lp = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.3), Inches(5.7), Inches(3.55))
    lp.fill.solid()
    lp.fill.fore_color.rgb = CARD_BG
    lp.line.color.rgb = CARD_BORDER
    lp.line.width = Pt(1)
    tf = lp.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "THE CORE BUSINESS PROBLEM"
    run.font.name = FONT_MAIN
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = ROSE

    prob_bullets = [
        ("High Revenue Depletion: ", "Customer cancellations reduce recurring Monthly Recurring Revenue (MRR) and shorten Customer Lifetime Value (CLV)."),
        ("Late Detection Trap: ", "Traditional methods detect churn only after customers request cancellation, making save-attempts costly and low-yield."),
        ("Lack of Granular Risk Scoring: ", "Customer success teams lack real-time visibility into which specific accounts carry immediate flight risk."),
        ("Untargeted Marketing Spend: ", "Without precise risk probabilities, retention budgets are misallocated to safe customers or lost causes.")
    ]
    for b_title, b_text in prob_bullets:
        p_b = tf.add_paragraph()
        p_b.space_before = Pt(8)
        r1 = p_b.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p_b.add_run()
        r2.text = b_text
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_MUTED

    # Right Column: Project Objectives & Solution Scope
    rp = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.3), Inches(5.7), Inches(3.55))
    rp.fill.solid()
    rp.fill.fore_color.rgb = CARD_BG
    rp.line.color.rgb = CARD_BORDER
    rp.line.width = Pt(1)
    tf = rp.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "PROJECT OBJECTIVES & TECHNICAL SCOPE"
    run.font.name = FONT_MAIN
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = PRIMARY

    sol_bullets = [
        ("Robust ML Classification Pipeline: ", "Train a Scikit-Learn Random Forest model that evaluates 18 customer attributes to predict churn probability."),
        ("Production REST API with FastAPI: ", "Expose high-throughput, type-safe endpoints validated by Pydantic v2 schemas and documented via OpenAPI."),
        ("Interactive Intelligence Dashboard: ", "Develop a responsive single-page web app with real-time KPI metrics, dynamic Chart.js charts, and customer explorer."),
        ("Actionable Retention Recommender: ", "Translate raw probabilities into categorized risk tiers (Low/Moderate/High) with tailored retention action plans.")
    ]
    for b_title, b_text in sol_bullets:
        p_b = tf.add_paragraph()
        p_b.space_before = Pt(8)
        r1 = p_b.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p_b.add_run()
        r2.text = b_text
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 3: Dataset Analysis & Exploratory Insights
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, LIGHT_BG)
    add_header(s3, "02 | Dataset & Exploratory Analysis", "IBM Telco Dataset Analysis & Churn Drivers", "Detailed inspection of 7,043 subscriber records and foundational exploratory findings", 3)

    # 4 Quick Stat Badges
    pills = [
        ("7,043 Records", "Total Dataset Rows"),
        ("21 Columns", "Original Attributes"),
        ("18 Features", "Model Input Predictors"),
        ("26.54% Churn", "Class Imbalance Baseline")
    ]
    for i, (stat, desc) in enumerate(pills):
        cx = Inches(0.8 + i * 2.98)
        pbox = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.85), Inches(2.78), Inches(0.7))
        pbox.fill.solid()
        pbox.fill.fore_color.rgb = CARD_BG
        pbox.line.color.rgb = CARD_BORDER
        pbox.line.width = Pt(1)
        tf = pbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r1 = p.add_run()
        r1.text = stat + "  •  "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = PRIMARY
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_MUTED

    # 3 Deep Dive Column Cards
    col_cards = [
        ("Contract Type Dynamics", "Highest Single Risk Predictor", [
            ("Month-to-Month: ", "42.71% churn rate (severe flight risk due to zero lock-in)."),
            ("One-Year Contract: ", "11.27% churn rate (almost 4x safer than month-to-month)."),
            ("Two-Year Contract: ", "2.83% churn rate (15x safer; highest customer retention)."),
            ("Key Takeaway: ", "Incentivizing long-term contracts is the most potent churn antidote.")
        ], ROSE),
        ("Tenure Lifespan Pattern", "The Onboarding Vulnerability Curve", [
            ("0–12 Months Tenure: ", "47.44% churn rate (critical first-year attrition cliff)."),
            ("13–24 Months Tenure: ", "Stabilizes down to ~28% churn rate."),
            ("25–48 Months Tenure: ", "Decreases significantly to ~16% churn rate."),
            ("49–72 Months Tenure: ", "Drops to <7% churn rate; high brand loyalty and stickiness.")
        ], AMBER),
        ("Financial & Service Factors", "Price Sensitivity & Service Types", [
            ("Average Spend Gap: ", "Churned users average $74.44/mo vs. $61.27/mo for retained."),
            ("Fiber Optic Vulnerability: ", ">40% churn rate due to premium pricing & competitive offers."),
            ("Electronic Check: ", "Highest churn payment method (paperless, unautomated friction)."),
            ("Support Services: ", "Online Security & Tech Support reduce churn by >50%.")
        ], PRIMARY)
    ]

    for i, (title, sub, bullets, accent) in enumerate(col_cards):
        cx = Inches(0.8 + i * 3.98)
        cbox = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(2.7), Inches(3.75), Inches(4.15))
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = CARD_BG
        cbox.line.color.rgb = CARD_BORDER
        cbox.line.width = Pt(1)

        # Top accent bar on card
        bar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(2.7), Inches(3.75), Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent
        bar.line.color.rgb = accent

        tf = cbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.2)

        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title
        r.font.name = FONT_MAIN
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = TEXT_DARK

        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = sub
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = accent

        for b_lbl, b_val in bullets:
            pb = tf.add_paragraph()
            pb.space_before = Pt(8)
            r_l = pb.add_run()
            r_l.text = "• " + b_lbl
            r_l.font.bold = True
            r_l.font.size = Pt(9.5)
            r_l.font.color.rgb = TEXT_DARK
            r_v = pb.add_run()
            r_v.text = b_val
            r_v.font.size = Pt(9)
            r_v.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 4: Data Preprocessing & Pipeline Engineering
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, LIGHT_BG)
    add_header(s4, "03 | Preprocessing & Pipelines", "Data Cleaning & Scikit-Learn ColumnTransformer", "End-to-end data transformation pipeline ensuring reproducible preprocessing and zero leakage", 4)

    # 5 Horizontal Pipeline Steps
    steps = [
        ("1. Raw Ingestion", "Telco CSV (7,043 rows)\n21 initial attributes", PRIMARY_BG, PRIMARY),
        ("2. Data Cleaning", "Coerce blank TotalCharges\nDrop customerID & gender", PRIMARY_BG, PRIMARY),
        ("3. Binary Encoding", "Map 'No service' / 'No' -> 0\nMap 'Yes' -> 1", PRIMARY_BG, PRIMARY),
        ("4. ColumnTransformer", "OneHotEncoder on 3 cols\nRemainder passthrough", EMERALD_BG, EMERALD),
        ("5. Joblib Bundle", "Save encoder, model &\ncolumn order bundle", PRIMARY_BG, PRIMARY)
    ]

    for i, (stitle, sdesc, bg, color) in enumerate(steps):
        sx = Inches(0.8 + i * 2.38)
        sbox = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, Inches(1.85), Inches(2.15), Inches(1.2))
        sbox.fill.solid()
        sbox.fill.fore_color.rgb = bg
        sbox.line.color.rgb = color
        sbox.line.width = Pt(1)

        tf = sbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.12)
        tf.margin_top = Inches(0.12)

        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = stitle
        r.font.name = FONT_MAIN
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        p2.space_before = Pt(4)
        r2 = p2.add_run()
        r2.text = sdesc
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(9)
        r2.font.color.rgb = TEXT_DARK

        # Arrow connector (if not last)
        if i < 4:
            abox = s4.shapes.add_textbox(sx + Inches(2.15), Inches(2.2), Inches(0.23), Inches(0.4))
            tf_a = abox.text_frame
            tf_a.margin_left = tf_a.margin_right = tf_a.margin_top = tf_a.margin_bottom = 0
            p_a = tf_a.paragraphs[0]
            p_a.alignment = PP_ALIGN.CENTER
            ra = p_a.add_run()
            ra.text = "→"
            ra.font.size = Pt(16)
            ra.font.bold = True
            ra.font.color.rgb = PRIMARY

    # Lower Left Box: OneHotEncoder Strategy
    ll = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.25), Inches(5.7), Inches(3.6))
    ll.fill.solid()
    ll.fill.fore_color.rgb = CARD_BG
    ll.line.color.rgb = CARD_BORDER
    ll.line.width = Pt(1)

    tf = ll.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.22)

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "TARGETED ONE-HOT ENCODING (COLUMNTRANSFORMER)"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = PRIMARY

    ohe_points = [
        ("Why Targeted OHE? ", "Standard get_dummies() blows up dimensionality to 43+ columns. By converting binary services (e.g., TechSupport) to 0/1 in cleaning, only 3 multi-class columns require OneHotEncoder."),
        ("1. InternetService: ", "Encoded to 3 categories ('0' / No Internet, 'DSL', 'Fiber optic')."),
        ("2. Contract: ", "Encoded to 3 categories ('Month-to-month', 'One year', 'Two year')."),
        ("3. PaymentMethod: ", "Encoded to 4 categories ('Electronic check', 'Mailed check', 'Bank transfer auto', 'Credit card auto')."),
        ("Feature Space Result: ", "18 input features are cleanly mapped to exactly 25 binary/numeric model columns, reducing matrix sparsity and training time.")
    ]
    for b_t, b_d in ohe_points:
        pb = tf.add_paragraph()
        pb.space_before = Pt(6)
        rl = pb.add_run()
        rl.text = "• " + b_t
        rl.font.bold = True
        rl.font.size = Pt(9.5)
        rl.font.color.rgb = TEXT_DARK
        rd = pb.add_run()
        rd.text = b_d
        rd.font.size = Pt(9)
        rd.font.color.rgb = TEXT_MUTED

    # Lower Right Box: Data Leakage Prevention & Handling
    lr = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.25), Inches(5.7), Inches(3.6))
    lr.fill.solid()
    lr.fill.fore_color.rgb = CARD_BG
    lr.line.color.rgb = CARD_BORDER
    lr.line.width = Pt(1)

    tf = lr.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.22)

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "DATA HYGIENE & LEAKAGE PREVENTION"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = EMERALD

    leak_points = [
        ("Removal of Index Column (Unnamed: 0): ", "During notebook EDA, an arbitrary CSV row index column was inadvertently generated. If left in, tree models overfit on row index. Both train.py and prediction_service.py strictly strip Unnamed: 0."),
        ("Handling Missing TotalCharges: ", "11 new customers had tenure=0 and empty TotalCharges. Used pd.to_numeric(errors='coerce') to properly handle empty strings and prevent type corruption."),
        ("ID & Gender Dropped: ", "customerID (random hash) and gender (50/50 split with zero churn correlation) were removed to prevent spurious statistical correlations."),
        ("Stratified Split (80/20): ", "Used stratify=Y in train_test_split() to preserve the 26.54% churn ratio in both training and test sets, avoiding class distribution skew.")
    ]
    for b_t, b_d in leak_points:
        pb = tf.add_paragraph()
        pb.space_before = Pt(6)
        rl = pb.add_run()
        rl.text = "• " + b_t
        rl.font.bold = True
        rl.font.size = Pt(9.5)
        rl.font.color.rgb = TEXT_DARK
        rd = pb.add_run()
        rd.text = b_d
        rd.font.size = Pt(9)
        rd.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 5: Machine Learning Model Architecture & Training
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, LIGHT_BG)
    add_header(s5, "04 | Machine Learning Model", "Random Forest Classifier Architecture & Training", "Ensemble bagging strategy combining 100 decorrelated decision trees for robust classification", 5)

    # Left Column: Model Configuration & Specs
    ml_left = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(5.7), Inches(5.0))
    ml_left.fill.solid()
    ml_left.fill.fore_color.rgb = CARD_BG
    ml_left.line.color.rgb = CARD_BORDER
    ml_left.line.width = Pt(1)

    tf = ml_left.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "MODEL SPECIFICATIONS & HYPERPARAMETERS"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = PRIMARY

    specs = [
        ("Algorithm: ", "RandomForestClassifier (Scikit-Learn ensemble)"),
        ("Number of Estimators: ", "n_estimators = 100 decision trees"),
        ("Split Quality Criterion: ", "Gini Impurity for optimal node splitting"),
        ("Random State: ", "random_state = 42 (ensures 100% reproducibility)"),
        ("Train/Test Partition: ", "80% Training (5,592 rows) / 20% Testing (1,399 rows)"),
        ("Stratification: ", "stratify = Y (preserves 26.54% churn ratio)"),
        ("Probability Estimation: ", "predict_proba() computes class=1 soft vote probability"),
        ("Serialization: ", "joblib.dump() bundle storing model, encoder & input columns")
    ]
    for s_label, s_val in specs:
        pb = tf.add_paragraph()
        pb.space_before = Pt(8)
        rl = pb.add_run()
        rl.text = s_label
        rl.font.bold = True
        rl.font.size = Pt(10)
        rl.font.color.rgb = TEXT_DARK
        rv = pb.add_run()
        rv.text = s_val
        rv.font.size = Pt(9.5)
        rv.font.color.rgb = TEXT_MUTED

    # Lower callout inside left card
    cbox = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(5.5), Inches(5.3), Inches(1.15))
    cbox.fill.solid()
    cbox.fill.fore_color.rgb = PRIMARY_BG
    cbox.line.color.rgb = PRIMARY_LIGHT
    cbox.line.width = Pt(1)
    tf_c = cbox.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = Inches(0.12)
    p_c = tf_c.paragraphs[0]
    rc1 = p_c.add_run()
    rc1.text = "Pipeline Deployment Bundle (churn_pipeline.joblib)\n"
    rc1.font.bold = True
    rc1.font.size = Pt(10)
    rc1.font.color.rgb = PRIMARY
    rc2 = p_c.add_run()
    rc2.text = "Saved dictionary: {'encoder': ColumnTransformer, 'model': RandomForest, 'input_columns': list}. Ensures exact feature alignment between training and REST API inference."
    rc2.font.size = Pt(8.5)
    rc2.font.color.rgb = TEXT_DARK

    # Right Column: Why Random Forest?
    ml_right = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.85), Inches(5.7), Inches(5.0))
    ml_right.fill.solid()
    ml_right.fill.fore_color.rgb = CARD_BG
    ml_right.line.color.rgb = CARD_BORDER
    ml_right.line.width = Pt(1)

    tf = ml_right.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "WHY RANDOM FOREST OUTPERFORMS ALTERNATIVES"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = EMERALD

    rf_advantages = [
        ("Non-Linear Interaction Modeling: ", "Customer churn is heavily governed by non-linear interactions (e.g., high MonthlyCharges + low tenure = extreme churn risk). Decision trees capture these cross-features naturally without polynomial expansions."),
        ("Resistance to Overfitting: ", "Individual decision trees have high variance. Random Forest applies Bootstrap Aggregation (bagging) and random feature subsets at each split (sqrt(p)), averaging out individual tree errors."),
        ("Scale Invariance: ", "Numeric features like tenure (0–72 months) and TotalCharges ($0–$8,600) do not require MinMax or Standard scaling, eliminating scaling artifacts during inference."),
        ("Smooth Probability Outputs: ", "Averaging class predictions across 100 trees yields a continuous, well-calibrated churn probability suitable for business risk thresholds."),
        ("Intrinsic Feature Interpretability: ", "Provides built-in MDI (Mean Decrease in Impurity) feature importances to explain which factors drive customer churn.")
    ]
    for adv_t, adv_d in rf_advantages:
        pb = tf.add_paragraph()
        pb.space_before = Pt(8)
        rl = pb.add_run()
        rl.text = "• " + adv_t
        rl.font.bold = True
        rl.font.size = Pt(9.5)
        rl.font.color.rgb = TEXT_DARK
        rd = pb.add_run()
        rd.text = adv_d
        rd.font.size = Pt(9)
        rd.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 6: Model Evaluation, Performance & Feature Importance
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, LIGHT_BG)
    add_header(s6, "05 | Evaluation & Interpretability", "Model Performance Metrics & Feature Importance", "Rigorous evaluation on holdout test set and identification of primary churn drivers", 6)

    # 4 Metric Cards across top
    metrics_data = [
        ("78.63%", "Holdout Test Accuracy", "Correct classification across unseen test set", PRIMARY, PRIMARY_BG),
        ("0.823", "ROC-AUC Score", "Strong discriminative capability between classes", EMERALD, EMERALD_BG),
        ("0.86 F1", "Class 0 (Retained)", "90% recall on loyal/retained customers", PRIMARY, PRIMARY_BG),
        ("0.63 Prec", "Class 1 (Churned)", "High precision when predicting customer churn", AMBER, AMBER_BG)
    ]
    for i, (mval, mtitle, mdesc, col, bg) in enumerate(metrics_data):
        cx = Inches(0.8 + i * 2.98)
        box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.85), Inches(2.78), Inches(1.2))
        box.fill.solid()
        box.fill.fore_color.rgb = bg
        box.line.color.rgb = col
        box.line.width = Pt(1)

        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.15)
        tf.margin_top = Inches(0.1)

        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = mval
        r.font.name = FONT_MAIN
        r.font.size = Pt(24)
        r.font.bold = True
        r.font.color.rgb = col

        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = mtitle.upper()
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(9)
        r2.font.bold = True
        r2.font.color.rgb = TEXT_DARK

        p3 = tf.add_paragraph()
        r3 = p3.add_run()
        r3.text = mdesc
        r3.font.name = FONT_MAIN
        r3.font.size = Pt(8.5)
        r3.font.color.rgb = TEXT_MUTED

    # Left Box: Confusion Matrix Analysis
    ev_left = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.2), Inches(5.7), Inches(3.65))
    ev_left.fill.solid()
    ev_left.fill.fore_color.rgb = CARD_BG
    ev_left.line.color.rgb = CARD_BORDER
    ev_left.line.width = Pt(1)

    tf = ev_left.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.22)

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "TEST CONFUSION MATRIX & CLASSIFICATION REPORT"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = PRIMARY

    cm_data = [
        ("True Negatives (TN): ", "929 customers correctly identified as Retained (90% Recall)."),
        ("False Positives (FP): ", "100 retained customers incorrectly flagged (Low False Alarm)."),
        ("True Positives (TP): ", "174 churning customers successfully detected (63% Precision)."),
        ("False Negatives (FN): ", "196 churn cases missed due to class imbalance threshold."),
        ("ROC-AUC Analysis: ", "Score of 0.823 proves the model effectively separates churners from non-churners across decision thresholds, far surpassing random guessing (0.50).")
    ]
    for k, v in cm_data:
        pb = tf.add_paragraph()
        pb.space_before = Pt(6)
        rl = pb.add_run()
        rl.text = "• " + k
        rl.font.bold = True
        rl.font.size = Pt(9.5)
        rl.font.color.rgb = TEXT_DARK
        rv = pb.add_run()
        rv.text = v
        rv.font.size = Pt(9)
        rv.font.color.rgb = TEXT_MUTED

    # Right Box: Top Feature Importances (MDI)
    ev_right = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.2), Inches(5.7), Inches(3.65))
    ev_right.fill.solid()
    ev_right.fill.fore_color.rgb = CARD_BG
    ev_right.line.color.rgb = CARD_BORDER
    ev_right.line.width = Pt(1)

    tf = ev_right.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.22)

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "TOP PREDICTIVE FEATURE IMPORTANCES"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = EMERALD

    top_feats = [
        ("TotalCharges (19.48%): ", "Cumulative financial footprint & tenure proxy."),
        ("MonthlyCharges (17.87%): ", "Immediate pricing burden; primary churn catalyst."),
        ("tenure (15.42%): ", "Customer relationship lifespan; tenure decays churn."),
        ("Contract: Month-to-month (7.40%): ", "Absence of commitment enables swift churn."),
        ("InternetService: Fiber optic (4.31%): ", "High price tier correlates with competitor migration."),
        ("PaymentMethod: Electronic check (3.26%): ", "Friction and lack of automated billing.")
    ]
    for feat, fdesc in top_feats:
        pb = tf.add_paragraph()
        pb.space_before = Pt(5)
        rl = pb.add_run()
        rl.text = "• " + feat
        rl.font.bold = True
        rl.font.size = Pt(9.5)
        rl.font.color.rgb = TEXT_DARK
        rv = pb.add_run()
        rv.text = fdesc
        rv.font.size = Pt(9)
        rv.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 7: Full-Stack System Architecture & FastAPI Backend
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, LIGHT_BG)
    add_header(s7, "06 | System Architecture & Backend", "Full-Stack System Architecture & FastAPI REST API", "Asynchronous, modular backend architecture serving analytics and real-time inference", 7)

    # 4 Architecture Flow Tiers (Horizontal layout on Left side)
    arch_left = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(5.7), Inches(5.0))
    arch_left.fill.solid()
    arch_left.fill.fore_color.rgb = CARD_BG
    arch_left.line.color.rgb = CARD_BORDER
    arch_left.line.width = Pt(1)

    tf = arch_left.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.22)

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "SYSTEM ARCHITECTURE & DATA FLOW"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = PRIMARY

    layers = [
        ("Layer 1: Client Browser (Frontend UI)", "HTML5 + Vanilla CSS + Vanilla JS (ES6) + Chart.js 4.4.\nResponsive dashboard with live KPI cards and prediction form."),
        ("Layer 2: FastAPI Routing & Static Mounts", "app/main.py mounts /css, /js, and serves index.html at /.\nIncludes routers for dashboard and prediction endpoints."),
        ("Layer 3: Schema Validation Layer (Pydantic v2)", "CustomerInput & PredictionResponse schemas enforce strict type validation (0/1 integers, ge=0 floats, Literals)."),
        ("Layer 4: Service Layer & Model Cache", "analytics_service.py parses CSV with Pandas for dashboard stats.\nprediction_service.py uses @lru_cache for fast bundle loading."),
        ("Layer 5: Machine Learning Pipeline", "Pre-trained churn_pipeline.joblib applies ColumnTransformer\nand feeds 25 features to RandomForestClassifier.")
    ]
    for l_title, l_desc in layers:
        pb = tf.add_paragraph()
        pb.space_before = Pt(7)
        rl = pb.add_run()
        rl.text = "• " + l_title + "\n"
        rl.font.bold = True
        rl.font.size = Pt(9.5)
        rl.font.color.rgb = TEXT_DARK
        rd = pb.add_run()
        rd.text = l_desc
        rd.font.size = Pt(8.5)
        rd.font.color.rgb = TEXT_MUTED

    # Right Column: REST API Endpoints Specification
    arch_right = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.85), Inches(5.7), Inches(5.0))
    arch_right.fill.solid()
    arch_right.fill.fore_color.rgb = CARD_BG
    arch_right.line.color.rgb = CARD_BORDER
    arch_right.line.width = Pt(1)

    tf = arch_right.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.22)

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "REST API ENDPOINTS SPECIFICATION"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = EMERALD

    endpoints = [
        ("POST /api/predict", "Core ML Inference", "Receives 18 customer attributes via CustomerInput JSON body. Transforms input using fitted encoder and returns churn_probability and predicted_churn (Yes/No)."),
        ("GET /api/dashboard", "Portfolio KPIs & Visual Data", "Computes portfolio stats (total, churned, retained, rate) and pre-aggregates chart datasets (churn by contract, tenure tiers, and monthly charges)."),
        ("GET /api/customers", "Paginated Customer Explorer", "Supports query parameters: search (text search), churn (Yes/No), contract, offset, limit (1–100). Returns filtered records and pagination metadata."),
        ("GET /health & /", "Healthcheck & Web UI", "/health returns {'status': 'ok'} for load balancer monitoring. / serves the single-page HTML interface directly.")
    ]
    for ep_method, ep_title, ep_desc in endpoints:
        pb = tf.add_paragraph()
        pb.space_before = Pt(8)
        rl = pb.add_run()
        rl.text = "• " + ep_method + "  (" + ep_title + ")\n"
        rl.font.bold = True
        rl.font.size = Pt(9.5)
        rl.font.color.rgb = PRIMARY
        rd = pb.add_run()
        rd.text = ep_desc
        rd.font.size = Pt(9)
        rd.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 8: Interactive Web Dashboard & Real-Time Analytics UI
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, LIGHT_BG)
    add_header(s8, "07 | Frontend Dashboard UI", "Interactive Analytics UI & Customer Explorer", "Unified, responsive dashboard with real-time portfolio metrics, Chart.js visuals, and data table", 8)

    # 3 Large Feature Highlight Cards
    ui_cards = [
        ("Real-Time KPI Ribbon", "Live Portfolio Health", [
            ("Total Customers: ", "7,043 subscriber accounts indexed."),
            ("Churned / Retained: ", "1,869 Churned vs. 5,174 Retained accounts."),
            ("Churn Rate Metric: ", "26.54% overall portfolio attrition rate."),
            ("Connection Pill: ", "Dynamic status badge displaying live backend health (Connected / Offline)."),
            ("Skeleton States: ", "Animated skeleton loaders during asynchronous data fetching.")
        ], PRIMARY),
        ("Visual Retention Charts", "Chart.js Visualizations", [
            ("Churn by Contract: ", "Grouped bar chart illustrating Month-to-Month (42.7%) vs. 1-Yr (11.3%) & 2-Yr (2.8%)."),
            ("Churn by Tenure: ", "Visual risk curve across customer lifespans (0–12m, 13–24m, 25–48m, 49–72m)."),
            ("Average Monthly Spend: ", "Side-by-side comparison showing churned users spend $13.17 more per month."),
            ("Canvas Optimization: ", "Responsive Chart.js configuration with custom tooltips.")
        ], EMERALD),
        ("Customer Explorer & Modal", "Full 21-Attribute Browser", [
            ("Search & Filtering: ", "Instant text search + Churn status & Contract dropdown filters."),
            ("Pagination Controls: ", "10, 25, 50, 100 rows per page with offset/limit query handling."),
            ("Inspection Modal: ", "Deep-dive dialog displaying all 21 demographic & service fields."),
            ("1-Click Predictor: ", "'Test' button loads any table record directly into Predictor."),
            ("Export to CSV: ", "Download filtered table view directly to client CSV file.")
        ], AMBER)
    ]

    for i, (title, sub, bullets, accent) in enumerate(ui_cards):
        cx = Inches(0.8 + i * 3.98)
        cbox = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.85), Inches(3.75), Inches(5.0))
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = CARD_BG
        cbox.line.color.rgb = CARD_BORDER
        cbox.line.width = Pt(1)

        # Top accent bar on card
        bar = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(1.85), Inches(3.75), Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent
        bar.line.color.rgb = accent

        tf = cbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.22)

        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title
        r.font.name = FONT_MAIN
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = TEXT_DARK

        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = sub
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = accent

        for b_lbl, b_val in bullets:
            pb = tf.add_paragraph()
            pb.space_before = Pt(8)
            r_l = pb.add_run()
            r_l.text = "• " + b_lbl
            r_l.font.bold = True
            r_l.font.size = Pt(9.5)
            r_l.font.color.rgb = TEXT_DARK
            r_v = pb.add_run()
            r_v.text = b_val
            r_v.font.size = Pt(9)
            r_v.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 9: Real-Time Churn Predictor & Retention Recommender
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, LIGHT_BG)
    add_header(s9, "08 | Prediction & Recommender", "Real-Time Churn Predictor & Retention Guidance", "Interactive inference interface translating probability into color-coded risk tiers and action plans", 9)

    # Left Column: Predictor Input Form & Presets
    pr_left = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(5.7), Inches(5.0))
    pr_left.fill.solid()
    pr_left.fill.fore_color.rgb = CARD_BG
    pr_left.line.color.rgb = CARD_BORDER
    pr_left.line.width = Pt(1)

    tf = pr_left.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "INTERACTIVE INPUT FORM & QUICK PRESETS"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = PRIMARY

    p_points = [
        ("Structured Form Sections: ", "18 input fields cleanly organized into Account Information, Demographics, and Internet/Phone Services."),
        ("High-Risk Preset Button: ", "Loads Month-to-month contract, Fiber optic, Electronic check, tenure=2, MonthlyCharges=$85 -> Instantly triggers >75% High Risk score."),
        ("Loyal Customer Preset Button: ", "Loads Two-year contract, DSL, Automatic bank transfer, tenure=48, MonthlyCharges=$55 -> Triggers <15% Low Risk score."),
        ("Asynchronous API Invocation: ", "Form submission asynchronously triggers POST /api/predict without page refresh, rendering results in under 50 milliseconds.")
    ]
    for pt, pd in p_points:
        pb = tf.add_paragraph()
        pb.space_before = Pt(8)
        rl = pb.add_run()
        rl.text = "• " + pt
        rl.font.bold = True
        rl.font.size = Pt(9.5)
        rl.font.color.rgb = TEXT_DARK
        rd = pb.add_run()
        rd.text = pd
        rd.font.size = Pt(9)
        rd.font.color.rgb = TEXT_MUTED

    # Lower sample box on Left
    sbox = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(5.2), Inches(5.3), Inches(1.4))
    sbox.fill.solid()
    sbox.fill.fore_color.rgb = PRIMARY_BG
    sbox.line.color.rgb = PRIMARY_LIGHT
    sbox.line.width = Pt(1)
    tf_s = sbox.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = Inches(0.12)
    ps = tf_s.paragraphs[0]
    rs1 = ps.add_run()
    rs1.text = "Live Probability Gauge Meter\n"
    rs1.font.bold = True
    rs1.font.size = Pt(10)
    rs1.font.color.rgb = PRIMARY
    rs2 = ps.add_run()
    rs2.text = "Visual probability bar dynamically transitions color based on score:\n• < 35%: Emerald (Low Risk / Safe Relationship)\n• 35% - 65%: Amber (Moderate Risk / Watchlist)\n• > 65%: Rose (High Risk / Critical Flight Hazard)"
    rs2.font.size = Pt(8.5)
    rs2.font.color.rgb = TEXT_DARK

    # Right Column: Automated Retention Recommendations
    pr_right = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.85), Inches(5.7), Inches(5.0))
    pr_right.fill.solid()
    pr_right.fill.fore_color.rgb = CARD_BG
    pr_right.line.color.rgb = CARD_BORDER
    pr_right.line.width = Pt(1)

    tf = pr_right.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "ACTIONABLE RETENTION RECOMMENDATIONS"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = EMERALD

    recs = [
        ("Long-Term Contract Incentives: ", "For Month-to-Month high-risk subscribers, offer a 15% discount voucher conditioned on a 1-year or 2-year contract migration."),
        ("Tech Support & Security Bundling: ", "Customers with Online Security and Tech Support churn 50% less. Provide a complimentary 90-day trial of premium cybersecurity services."),
        ("Automated Payment Migration: ", "Subscribers using Electronic Check exhibit high churn. Offer a one-time $10 bill credit for switching to Credit Card or Bank Transfer auto-pay."),
        ("Onboarding Concierge (Tenure < 12m): ", "For accounts under 1-year tenure with high monthly charges, schedule a proactive customer success call to ensure service satisfaction."),
        ("Targeted Loyalty Perks (Low Risk): ", "For accounts with >48-month tenure, provide milestone rewards (e.g., speed upgrades) to maintain brand advocacy and prevent competitor switching.")
    ]
    for r_title, r_desc in recs:
        pb = tf.add_paragraph()
        pb.space_before = Pt(7)
        rl = pb.add_run()
        rl.text = "• " + r_title
        rl.font.bold = True
        rl.font.size = Pt(9.5)
        rl.font.color.rgb = TEXT_DARK
        rd = pb.add_run()
        rd.text = r_desc
        rd.font.size = Pt(9)
        rd.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 10: Testing, Quality Assurance & Future Roadmap
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, LIGHT_BG)
    add_header(s10, "09 | QA Verification & Roadmap", "Automated QA Verification & Strategic Roadmap", "Complete automated test coverage, key architectural conclusions, and future evolution", 10)

    # Left Column: Pytest Automated QA Suite
    qa_box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(5.7), Inches(5.0))
    qa_box.fill.solid()
    qa_box.fill.fore_color.rgb = CARD_BG
    qa_box.line.color.rgb = CARD_BORDER
    qa_box.line.width = Pt(1)

    tf = qa_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.22)

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "AUTOMATED TESTING & QUALITY GATES (13/13 PASSED)"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = EMERALD

    tests = [
        ("Server & Asset Delivery: ", "Validates /health (200 OK), root / (HTML home), /css/style.css, and /js/app.js static asset delivery."),
        ("Dashboard Calculations: ", "Verifies total = churned + retained, rate between 0-100%, and valid grouped contract/tenure arrays."),
        ("Pagination & Query Bounds: ", "Tests offset/limit pagination, search keyword queries, and confirms HTTP 422 for limit>100 or offset<0."),
        ("Inference Schema Validation: ", "Asserts valid churn_probability ∈ [0,1], predicted_churn ∈ {Yes,No}, and validates HTTP 422 on missing/invalid fields."),
        ("Robust Edge Case Handling: ", "Handles non-standard strings (InternetService='No' -> '0') and extreme edge cases (tenure=0, TotalCharges=0.0).")
    ]
    for t_t, t_d in tests:
        pb = tf.add_paragraph()
        pb.space_before = Pt(7)
        rl = pb.add_run()
        rl.text = "• " + t_t
        rl.font.bold = True
        rl.font.size = Pt(9.5)
        rl.font.color.rgb = TEXT_DARK
        rd = pb.add_run()
        rd.text = t_d
        rd.font.size = Pt(9)
        rd.font.color.rgb = TEXT_MUTED

    # Lower pass badge
    pbadge = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(5.65), Inches(5.3), Inches(0.95))
    pbadge.fill.solid()
    pbadge.fill.fore_color.rgb = EMERALD_BG
    pbadge.line.color.rgb = EMERALD
    pbadge.line.width = Pt(1)
    tf_pb = pbadge.text_frame
    tf_pb.word_wrap = True
    tf_pb.margin_left = tf_pb.margin_right = tf_pb.margin_top = Inches(0.12)
    p_pb = tf_pb.paragraphs[0]
    p_pb.alignment = PP_ALIGN.CENTER
    r_pb1 = p_pb.add_run()
    r_pb1.text = "✓  13 / 13 Pytest Test Cases Passed (0 Failures, 0 Errors)\n"
    r_pb1.font.bold = True
    r_pb1.font.size = Pt(11)
    r_pb1.font.color.rgb = EMERALD
    r_pb2 = p_pb.add_run()
    r_pb2.text = "Validated across Starlette TestClient with full HTTP simulation."
    r_pb2.font.size = Pt(9)
    r_pb2.font.color.rgb = TEXT_DARK

    # Right Column: Future Roadmap & Enhancements
    rm_box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.85), Inches(5.7), Inches(5.0))
    rm_box.fill.solid()
    rm_box.fill.fore_color.rgb = CARD_BG
    rm_box.line.color.rgb = CARD_BORDER
    rm_box.line.width = Pt(1)

    tf = rm_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.22)

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "PROJECT CONCLUSIONS & FUTURE ROADMAP"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = PRIMARY

    roadmap = [
        ("SHAP Explainability Layer: ", "Integrate TreeSHAP to generate individual feature attribution waterfall charts, showing customers exactly why their risk is high."),
        ("Hyperparameter Tuning with Optuna: ", "Conduct automated Bayesian optimization across n_estimators, max_depth, and min_samples_split to maximize churn recall."),
        ("Gradient Boosting Comparison: ", "Benchmark LightGBM and XGBoost against Random Forest for potential accuracy gains on tabular data."),
        ("Database Persistence (PostgreSQL): ", "Transition from static CSV files to a transactional database to support historical prediction logging and customer audit trails."),
        ("Containerization & CI/CD: ", "Package the application into a Docker container and set up GitHub Actions for continuous integration, testing, and cloud deployment.")
    ]
    for rm_t, rm_d in roadmap:
        pb = tf.add_paragraph()
        pb.space_before = Pt(7)
        rl = pb.add_run()
        rl.text = "• " + rm_t
        rl.font.bold = True
        rl.font.size = Pt(9.5)
        rl.font.color.rgb = TEXT_DARK
        rd = pb.add_run()
        rd.text = rm_d
        rd.font.size = Pt(9)
        rd.font.color.rgb = TEXT_MUTED

    output_path = "Customer_Churn_Prediction_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path} with {len(prs.slides)} slides!")

if __name__ == "__main__":
    create_deck()
