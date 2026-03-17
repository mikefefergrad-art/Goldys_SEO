from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import re

doc = Document()

# --- Styles ---
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)

def set_heading(paragraph, text, level=1):
    paragraph.clear()
    run = paragraph.add_run(text)
    run.bold = True
    if level == 1:
        run.font.size = Pt(18)
        run.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
    elif level == 2:
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x2E, 0x74, 0xB5)
    elif level == 3:
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x40, 0x40, 0x40)

def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    set_heading(p, text, level)
    return p

def add_bold_para(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    return p

def shade_row(row, color_hex):
    for cell in row.cells:
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:fill'), color_hex)
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:val'), 'clear')
        tcPr.append(shd)

def add_table(doc, headers, rows, header_color='1F497D'):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    # Header row
    hdr = table.rows[0]
    shade_row(hdr, header_color)
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        cell.text = h
        run = cell.paragraphs[0].runs[0]
        run.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        run.font.size = Pt(10)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    # Data rows
    for r_idx, row in enumerate(rows):
        tr = table.rows[r_idx + 1]
        if r_idx % 2 == 0:
            shade_row(tr, 'DEEAF1')
        for c_idx, cell_text in enumerate(row):
            cell = tr.cells[c_idx]
            cell.text = str(cell_text)
            cell.paragraphs[0].runs[0].font.size = Pt(10)
    doc.add_paragraph()
    return table

def add_quote_box(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.right_indent = Inches(0.4)
    run = p.add_run(f'"{text}"')
    run.italic = True
    run.font.color.rgb = RGBColor(0x40, 0x40, 0x40)
    run.font.size = Pt(11)

# ============================================================
# TITLE
# ============================================================
title = doc.add_heading("Goldy's Competitive Battle Cards & Pricing Comparison", 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in title.runs:
    run.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
meta.add_run("Category: Instant Oatmeal & Hot Cereal · Superseed Cereal  |  Market: Canada  |  Last Updated: March 2026\nAll prices in CAD").font.size = Pt(10)

doc.add_paragraph()

# ============================================================
# TARGET CUSTOMER
# ============================================================
add_heading(doc, "Our Target Customer", 1)
doc.add_paragraph(
    "Family-friendly shoppers — parents who want clean, nutritious, convenient breakfasts they feel great "
    "feeding their kids and eating themselves. They read labels, care about what goes into their family's food, "
    "and are willing to pay more for real ingredients over fillers and refined sugar. They shop at grocery stores, "
    "natural food retailers, and online — and they're looking for a product the whole family can enjoy at the breakfast table."
)

# ============================================================
# OUR STAR SKUs
# ============================================================
add_heading(doc, "Our Star SKUs", 1)
add_table(doc,
    headers=["SKU", "Key Stats", "Price"],
    rows=[
        ["Instant Superseed Oatmeal",
         "Glyphosate-free Canadian oats + chia, hemp, pumpkin, buckwheat · freeze-dried fruit · sweetened with organic date powder · 0g refined sugar",
         "$6.99 / box (6 × 35g bags)"],
        ["Protein+ Instant Superseed Oatmeal",
         "10g plant-based protein · 5g fibre · oats + chia, pumpkin, sunflower seeds · 0g refined sugar · 100% vegan",
         "$7.99 / box (5 × 50g bags)"],
        ["Superseed Cereal",
         "Grain-free · chia, hemp, pumpkin, buckwheat + freeze-dried fruit · 0g added sugar",
         "$10.99 / 225g"],
    ]
)

add_bold_para(doc, "What sets every Goldy's product apart for families:")
bullets = [
    "Glyphosate-free Canadian oats (oatmeal line) — parents can trust what they're feeding their kids",
    "Superseeds blended in — not plain oats — so the whole family gets more nutrition per bowl",
    "Sweetened only with organic date powder — zero refined sugar (no morning sugar crashes for kids)",
    "Freeze-dried whole fruit (retains nutrients + flavor better than dried — kids love the taste)",
    "Non-GMO · Gluten-Free · Dairy-Free · Vegan · Made in Canada",
    "Ready in under 5 minutes — realistic for busy family mornings",
]
for b in bullets:
    p = doc.add_paragraph(style='List Bullet')
    p.add_run(b).font.size = Pt(11)

# ============================================================
# PROTEIN HEAD-TO-HEAD
# ============================================================
add_heading(doc, "Protein Per Serving: Head-to-Head", 1)
add_table(doc,
    headers=["Brand", "Product", "Protein/serving", "Protein Source", "Added Sugar", "Vegan?"],
    rows=[
        ["Goldy's Protein+", "Instant Superseed Oatmeal", "10g", "Chia, pumpkin, sunflower seeds", "0g", "Yes"],
        ["Goldy's Standard", "Instant Superseed Oatmeal", "~5–6g", "Oats + seeds", "0g", "Yes"],
        ["Quaker Protein", "Instant Oatmeal (Maple Brown Sugar)", "10–12g", "Whey isolate + whey concentrate", "11g", "No (dairy)"],
        ["Bob's Red Mill", "Protein Oats", "9–10g", "High-protein oat variety (no isolates)", "0g", "Yes"],
        ["One Degree", "Protein Instant Oatmeal", "~10–12g", "Sprouted oats + faba beans", "Low", "Yes"],
        ["Nature's Path", "Instant Oatmeal", "~6g", "Oats", "6–8g (flavored)", "Yes"],
        ["Yumi Organics", "Morning Oats (instant)", "3g", "Oats", "Low", "Yes"],
        ["Yumi Organics", "Overnight Oats", "6g", "Oats", "Low", "Yes"],
        ["Seven Sundays", "Muesli (eaten hot)", "~8g", "Oats + seeds", "0g refined", "Yes"],
    ]
)

# ============================================================
# PRICING COMPARISON
# ============================================================
add_heading(doc, "Pricing Comparison: Instant Oatmeal / Hot Cereal (all CAD)", 1)
add_table(doc,
    headers=["Brand", "Product", "Size", "Price (CAD)", "Per Serving (CAD, est.)"],
    rows=[
        ["Goldy's", "Instant Superseed Oatmeal", "6 × 35g bags", "$6.99", "~$1.17"],
        ["Goldy's", "Protein+ Oatmeal", "5 × 50g bags", "$7.99", "~$1.60"],
        ["Yumi Organics", "Morning Oats (8 pkts)", "box", "~$9.60", "~$1.20"],
        ["Yumi Organics", "Overnight Oats (5 pkts)", "box", "~$10.00", "~$2.00"],
        ["Nature's Path", "Instant Oatmeal (8 pkts)", "14oz", "~$6.90–9.65", "~$0.87–1.21"],
        ["Quaker Protein", "Instant Oatmeal (6 pkts)", "12.7oz", "~$6.90–8.30", "~$1.15–1.38"],
        ["Bob's Red Mill", "Protein Oats", "64oz", "~$12.25 (Costco)", "~$0.61"],
        ["One Degree", "Sprouted Instant Oatmeal", "18oz", "~$9.65–12.40", "~$1.38–1.79"],
        ["Seven Sundays", "Muesli", "12oz", "~$12.40–13.80", "~$2.07–2.76"],
    ]
)

# ============================================================
# BATTLE CARDS
# ============================================================
battle_cards = [
    {
        "title": "Battle Card 1: vs. Yumi Organics (closest Canadian competitor)",
        "about": "Canadian brand. Organic instant oatmeal and overnight oats. Enriched with 27 vitamins & minerals. "
                 "Morning Oats: 3g protein, ~$1.20/serving. Overnight Oats: 6g protein, ~$2.00/serving. "
                 "Available at Healthy Planet Canada, My Healthy Planet, Well.ca, Amazon.ca.",
        "table_headers": ["", "Goldy's", "Yumi Organics"],
        "table_rows": [
            ["Star format", "Instant + Protein+ oatmeal", "Instant (Morning Oats) + Overnight Oats"],
            ["Protein/serving", "5–6g (standard) · 10g (Protein+)", "3g (instant) · 6g (overnight)"],
            ["Protein source", "Whole-food seeds", "Oats (enriched, not seed-based)"],
            ["Sugar", "0g refined · date powder only", "Low sugar, some added"],
            ["Glyphosate-free oats?", "Yes", "Not specified"],
            ["Superseeds included?", "Yes (chia, hemp, pumpkin, buckwheat)", "No"],
            ["Freeze-dried fruit?", "Yes", "No"],
            ["Vitamins enriched?", "Naturally nutrient-dense (seeds)", "Yes – 27 added vitamins & minerals"],
            ["Made in Canada?", "Yes", "Yes"],
            ["Price per serving", "~$2.50–3.00", "~$1.20–$2.00"],
        ],
        "win_angles": [
            "Goldy's Protein+ delivers 10g protein vs. Yumi's 3g (instant) — more than 3x more protein to keep kids and parents fuelled through the morning.",
            "Goldy's protein is seed-based whole food; Yumi Organics' protein comes from oats + fortification. Parents want real food, not lab-added vitamins.",
            "Superseeds in every serving = omega-3s, healthy fats, and fibre that Yumi Organics can't match — nutrients growing bodies need.",
            "Glyphosate-free certification is a powerful differentiator — parents actively worry about pesticide residue in oats (Yumi Organics does not claim this).",
            "Freeze-dried real fruit means kids get real fruit taste without parents adding sugar or toppings.",
        ],
        "their_strengths": [
            "Cheaper per serving (~$1.20 vs. our ~$2.50) — for budget-conscious families, we must sell on value per nutrient ('what's actually in the bowl').",
            "27 added vitamins & minerals is a compelling claim for parents — counter with: Goldy's gets its nutrients from real seeds, not synthetic fortification.",
            "Overnight oats format is trendy for busy parents — Goldy's cold-soak potential for Superseed Cereal is a story worth telling.",
        ],
    },
    {
        "title": "Battle Card 2: vs. Quaker Protein",
        "about": "PepsiCo-owned mass-market giant. Protein Instant Oatmeal: 10–12g protein/serving from whey isolate + whey concentrate. "
                 "Flavors: Maple & Brown Sugar, Banana Nut, Cranberry Almond, Apples & Cinnamon. 11g added sugar (Maple Brown Sugar). "
                 "Price: ~$6.90–8.30 / 6-packet box. Available at Walmart, Loblaws, Sobeys, Costco, etc.",
        "table_headers": ["", "Goldy's Protein+", "Quaker Protein"],
        "table_rows": [
            ["Protein/serving", "10g", "10–12g"],
            ["Protein source", "Chia, pumpkin, sunflower seeds", "Whey isolate + whey concentrate (dairy)"],
            ["Vegan?", "Yes", "No"],
            ["Added sugar", "0g (date powder only)", "11g per packet"],
            ["Glyphosate-free oats?", "Yes", "Not claimed"],
            ["Superseeds?", "Yes", "No"],
            ["Freeze-dried fruit?", "Yes", "No – dried fruit / flavorings"],
            ["Price/serving", "~$2.50–3.00", "~$1.15–1.40"],
        ],
        "win_angles": [
            "Same protein count (10g), but Goldy's protein is 100% plant-based whole-food seeds — no dairy, no isolates. Parents don't need to add whey powder to their kids' breakfast.",
            "Quaker Protein Maple Brown Sugar has 11g of added sugar per packet — that's almost 3 teaspoons of sugar per bowl before the kids even leave for school. Goldy's has zero.",
            "Goldy's oats are glyphosate-free; Quaker oats have faced scrutiny over glyphosate residue in testing. This matters to parents who read the news.",
            "Whole-food seeds deliver omega-3s, healthy fats, and additional micronutrients beyond just protein — a more complete breakfast for growing kids.",
        ],
        "key_message": "You wouldn't add 3 teaspoons of sugar to your child's breakfast — but that's what's in every packet of Quaker Protein. Goldy's matches the protein with real seeds and zero refined sugar. A breakfast the whole family can feel good about.",
        "their_strengths": [
            "Price: Quaker is ~2–3x cheaper per serving — for families watching grocery budgets, this is real.",
            "Ubiquity: sold in every grocery store in Canada — parents grab what's easy and available.",
            "Brand trust: Quaker has been the family breakfast default for generations. We're the new option that has to earn trust.",
        ],
    },
    {
        "title": "Battle Card 3: vs. Nature's Path",
        "about": "BC-based Canadian brand. USDA Organic, Non-GMO Project Verified. Instant Oatmeal: ~6g protein, sweetened with cane sugar "
                 "(6–8g added sugar in flavored varieties). Flavors: Apple Cinnamon, Maple Nut, Blueberry Cinnamon Flax, Original. "
                 "Price: ~$6.90–9.65 / 8-packet box. Available at Whole Foods, Walmart, Loblaws, Costco.",
        "table_headers": ["", "Goldy's Instant Oatmeal", "Nature's Path Instant Oatmeal"],
        "table_rows": [
            ["Protein/serving", "~5–6g (standard) · 10g (Protein+)", "~6g"],
            ["Added sugar", "0g (date powder only)", "6–8g (cane sugar in flavored pkts)"],
            ["Glyphosate-free oats?", "Yes", "Not specifically claimed"],
            ["USDA Organic?", "Non-GMO / clean", "Yes"],
            ["Superseeds included?", "Yes", "Partial (Flax Plus variety only)"],
            ["Freeze-dried fruit?", "Yes", "No – dried fruit"],
            ["Made in Canada?", "Yes", "Yes (BC)"],
            ["Price/serving", "~$2.50–3.00", "~$0.87–1.21"],
        ],
        "win_angles": [
            "Goldy's has zero refined sugar; Nature's Path flavored oatmeal uses cane sugar as the second ingredient. Parents buying 'organic' don't expect sugar-loaded oatmeal.",
            "Glyphosate-free certification on our oats is a specific, verifiable claim — parents concerned about pesticide residue have a clear answer with Goldy's.",
            "Superseeds in every serving = more complete nutrition per bowl for kids and parents, not just empty-calorie oats.",
            "Protein+ SKU delivers nearly double the protein of Nature's Path — keeping kids fuller and focused through the morning.",
        ],
        "their_strengths": [
            "USDA Organic certification carries weight with family shoppers — our clean label story must be told loudly and specifically.",
            "Mass distribution across Canada and US — families buy what's on their shelf, and Nature's Path is everywhere.",
            "Price per serving is significantly lower — matters for families buying breakfast for 3–5 people daily.",
        ],
    },
    {
        "title": "Battle Card 4: vs. One Degree Organics",
        "about": "BC-based Canadian brand. Sprouted oats for better nutrient absorption. Protein Instant Oatmeal uses faba beans for added protein. "
                 "USDA Organic, Non-GMO, Glyphosate-Free (3rd-party tested). Farm traceable via QR code. "
                 "Price: ~$9.65–12.40 / 18oz instant oatmeal. Available at Whole Foods, Costco, Thrive Market, Amazon.",
        "table_headers": ["", "Goldy's", "One Degree Organics"],
        "table_rows": [
            ["Origin", "Canadian (Made in Canada)", "Canadian (BC-based)"],
            ["Star differentiator", "Superseeds + glyphosate-free oats", "Sprouted oats + farm traceability"],
            ["Protein source", "Chia, pumpkin, sunflower seeds", "Sprouted oats + faba beans (Protein line)"],
            ["Glyphosate-free?", "Yes", "Yes (3rd-party tested)"],
            ["USDA Organic?", "Non-GMO / clean", "Yes"],
            ["Added sugar?", "0g refined (date powder)", "Coconut sugar (low, not zero)"],
            ["Superseeds?", "Yes — multiple per SKU", "No (oat-focused)"],
            ["Freeze-dried fruit?", "Yes", "No – dried fruit"],
            ["Price/serving", "~$2.50–3.00", "~$1.38–1.79"],
        ],
        "win_angles": [
            "Both are Canadian, clean, glyphosate-free — this is a close fight. Goldy's wins on the superseed nutrition story and zero refined sugar.",
            "Goldy's freeze-dried fruit vs. One Degree's dried fruit = better flavor and nutrient retention — and kids actually want to eat it.",
            "Goldy's seeds add omega-3s, healthy fats, and multi-source protein One Degree's plain oat base can't deliver.",
            "One Degree's faba bean protein is a novel ingredient that may confuse families — Goldy's whole-food seed protein (chia, pumpkin, sunflower) is familiar and kid-friendly.",
            "Goldy's is truly instant — add hot water and it's done. One Degree's rolled/quick oats require more stovetop time on busy mornings.",
        ],
        "their_strengths": [
            "Farm-to-table QR traceability is a compelling transparency story for ingredient-conscious parents — Goldy's should develop its own sourcing narrative.",
            "USDA Organic is a gap for us — and 'organic' is often the first filter for family shoppers.",
            "Stronger US distribution (Whole Foods, Costco).",
        ],
    },
    {
        "title": "Battle Card 5: vs. Bob's Red Mill Protein Oats",
        "about": "Employee-owned (founded 1978). Protein Oats = a special high-protein oat variety — no protein powders added. "
                 "9–10g protein/serving. Gluten-Free, Non-GMO, 0g added sugar. Price: ~$12.25 / 64oz at Costco. "
                 "Available at Costco, Walmart, Amazon, Whole Foods.",
        "table_headers": ["", "Goldy's Protein+", "Bob's Red Mill Protein Oats"],
        "table_rows": [
            ["Protein/serving", "10g", "9–10g"],
            ["Protein source", "Chia, pumpkin, sunflower seeds", "High-protein oat variety (just oats)"],
            ["Added sugar", "0g", "0g"],
            ["Vegan?", "Yes", "Yes"],
            ["Gluten-Free?", "Yes", "Yes"],
            ["Glyphosate-free oats?", "Yes", "Not specifically claimed"],
            ["Omega-3s / healthy fats?", "Yes (seeds)", "Minimal (oats only)"],
            ["Flavored / ready-to-eat?", "Yes (Cinnamon Spice, Original)", "No – plain, requires prep and toppings"],
            ["Freeze-dried fruit?", "Yes", "No"],
            ["Price/serving", "~$2.50–3.00", "~$0.61 (bulk Costco)"],
        ],
        "win_angles": [
            "Goldy's Protein+ delivers the same protein count, but from seeds not just oats — the whole family gets omega-3s, healthy fats, and a broader micronutrient profile in every bowl.",
            "Bob's Protein Oats are plain and unflavored — parents have to add toppings, sweetener, and fruit to make kids eat it. Goldy's is ready-to-eat with real flavors and freeze-dried fruit.",
            "Glyphosate-free oats is a claim Bob's doesn't specifically make — matters to parents watching for pesticide residue.",
            "Goldy's is a complete, grab-and-go family breakfast; Bob's is a bulk pantry ingredient that requires prep and customization.",
        ],
        "their_strengths": [
            "Price: Bob's Costco 64oz is dramatically cheaper per serving (~$0.61 vs. ~$2.50) — families feeding multiple kids feel this.",
            "Deep brand trust and loyalty in the natural/health grocery channel — parents already know and trust Bob's.",
            "60% more protein than regular oats is a very clean, simple claim.",
        ],
    },
    {
        "title": "Battle Card 6: vs. Seven Sundays",
        "about": "B-Corp certified muesli brand (Minneapolis, 2011). Gluten-free, Non-GMO, no refined sugar. "
                 "Oats + sorghum + buckwheat + seeds + fruit. ~8g protein/serving. Can be eaten hot or cold. "
                 "Price: ~$12.40–13.80 / 12oz bag. Available DTC and specialty retail including Walmart.",
        "table_headers": ["", "Goldy's Instant Oatmeal", "Seven Sundays Muesli"],
        "table_rows": [
            ["Format", "True instant oatmeal (add hot water)", "Muesli (eaten cold, or prepared hot)"],
            ["Protein/serving", "5–6g · 10g (Protein+)", "~8g"],
            ["Grain-free option?", "Yes – Superseed Cereal SKU", "No"],
            ["No refined sugar?", "Yes", "Yes"],
            ["Superseeds?", "Yes — multiple", "Partial (some varieties)"],
            ["Freeze-dried fruit?", "Yes", "No – dried fruit"],
            ["B-Corp?", "Not certified", "Yes – B-Corp certified"],
            ["Made in Canada?", "Yes", "No – US brand"],
            ["Price/bag", "~$9.99", "~$12.40–13.80"],
            ["Price/serving", "~$2.50–3.00", "~$2.07–2.76"],
        ],
        "win_angles": [
            "Goldy's Protein+ beats Seven Sundays on protein (10g vs. 8g) with a cleaner seed-only source.",
            "Goldy's is Canadian — local sourcing story resonates with families who care about where their food comes from.",
            "Freeze-dried whole fruit vs. dried fruit = better nutrition and more vibrant flavor that kids actually enjoy.",
            "True instant format (hot water + done) is more convenient for rushed family mornings than muesli prep.",
            "Goldy's Superseed Cereal covers the grain-free space for families with gluten sensitivities.",
        ],
        "their_strengths": [
            "B-Corp certification adds credibility with values-driven family shoppers — worth pursuing for Goldy's.",
            "Seven Sundays has a strong US DTC following and brand story.",
        ],
    },
    {
        "title": "Battle Card 7: vs. Magic Spoon (Cereal SKU only)",
        "about": "Grain-free, high-protein adult cold cereal. 13–14g protein/serving from whey isolate. Zero added sugar. "
                 "~$12.40–13.80 / 7oz box. In 6,800 US stores. Not a hot cereal competitor — relevant only against Goldy's Superseed Cereal.",
        "table_headers": ["", "Goldy's Superseed Cereal", "Magic Spoon"],
        "table_rows": [
            ["Format", "Hot or cold (transforms to pudding)", "Cold only (crunchy, stays crunchy)"],
            ["Protein/serving", "~6–8g (seeds)", "13–14g (whey isolate)"],
            ["Vegan?", "Yes", "No (whey = dairy)"],
            ["Whole-food ingredients?", "Yes — real seeds + freeze-dried fruit", "No – processed whey + allulose + monk fruit"],
            ["Added sugar?", "0g", "0g"],
            ["Grain-free?", "Yes", "Yes"],
            ["Price/oz", "~$1.14/oz", "~$1.78–1.97/oz"],
            ["Market", "Canada", "US (mass retail)"],
        ],
        "win_angles": [
            "Goldy's is cheaper, vegan, and made with real whole-food ingredients.",
            "Magic Spoon is a processed novelty product; Goldy's is real food.",
            "Most relevant if/when Goldy's expands to US retail.",
        ],
        "their_strengths": [],
    },
]

for bc in battle_cards:
    doc.add_page_break()
    add_heading(doc, bc["title"], 2)
    add_bold_para(doc, "About")
    doc.add_paragraph(bc["about"])
    doc.add_paragraph()
    add_table(doc, bc["table_headers"], bc["table_rows"])

    if bc.get("key_message"):
        add_bold_para(doc, "Key Message:")
        add_quote_box(doc, bc["key_message"])
        doc.add_paragraph()

    add_bold_para(doc, "Our Win Angle (for families):")
    for wa in bc["win_angles"]:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(wa).font.size = Pt(11)

    if bc["their_strengths"]:
        doc.add_paragraph()
        add_bold_para(doc, "Their Strengths We Must Address:")
        for ts in bc["their_strengths"]:
            p = doc.add_paragraph(style='List Bullet')
            p.add_run(ts).font.size = Pt(11)

# ============================================================
# KEY GAPS
# ============================================================
doc.add_page_break()
add_heading(doc, "Key Gaps to Address", 1)
add_table(doc,
    headers=["Gap", "Recommended Action"],
    rows=[
        ["No USDA Organic certification", "Pursue certification or clearly communicate glyphosate-free + non-GMO sourcing — 'organic' is the first filter for many family shoppers"],
        ["Protein+ protein claim needs on-pack prominence", "Lead with '10g plant-based protein' front-of-pack — parents scanning the shelf need to see this instantly"],
        ["Price premium vs. Yumi Organics / Nature's Path", "Build cost-per-nutrient comparison (protein, omega-3, fibre per dollar) — reframe as 'what are you actually feeding your family per dollar?'"],
        ["Family-friendly messaging on pack", "Ensure packaging and website speak to families, not just health enthusiasts — 'the whole family' language, kid-friendly flavor names, family breakfast imagery"],
        ["Limited retail distribution in Canada", "Family shoppers buy at Loblaws, Metro, Sobeys — specialty-only limits reach. Prioritize Canadian grocery chain expansion."],
        ["No B-Corp certification", "Consider pursuing — values-driven family shoppers notice this"],
    ]
)

# ============================================================
# CORE MESSAGING
# ============================================================
add_heading(doc, "Goldy's Core Messaging by SKU (Family-First)", 1)

add_heading(doc, "Instant Superseed Oatmeal", 3)
add_quote_box(doc, "Breakfast the whole family can feel good about. Glyphosate-free Canadian oats loaded with chia, hemp, pumpkin, and buckwheat — plus real freeze-dried fruit and zero refined sugar. Ready in 5 minutes, loved by kids and parents alike.")

add_heading(doc, "Protein+ Instant Superseed Oatmeal", 3)
add_quote_box(doc, "10 grams of plant-based protein from real seeds — not whey powder, not sugar. Keeps kids fuelled and focused through the morning. Keeps parents feeling great about what they put on the table. Done in 5 minutes.")

add_heading(doc, "Against Quaker Protein:", 3)
add_quote_box(doc, "You wouldn't add 3 teaspoons of sugar to your child's oatmeal — but Quaker Protein does it for you. Goldy's matches the protein with real seeds and zero refined sugar. A breakfast the whole family deserves.")

add_heading(doc, "Against the 'just oats' category:", 3)
add_quote_box(doc, "Most instant oatmeal is just oats. Goldy's starts with glyphosate-free Canadian oats and adds superseeds for omega-3s, protein, and healthy fats — a more complete breakfast for growing kids and busy parents. No toppings required.")

# ============================================================
# SOURCES
# ============================================================
doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run("Sources: goldys.ca · healthyplanetcanada.com · yumi-organics.ca · quakeroats.com · naturespath.com · "
                "onedegreeorganics.com · bobsredmill.com · sevensundays.com · magicspoon.com · amazon.ca · walmart.com · "
                "costco.com · naturamarket.ca · well.ca")
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)

output_path = "/home/user/Goldys_SEO/competitive-intel/Goldys_Competitive_Battle_Cards.docx"
doc.save(output_path)
print(f"Saved: {output_path}")
