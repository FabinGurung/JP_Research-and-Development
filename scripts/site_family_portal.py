"""Two-family front door and academic reading-room hub. Legacy URLs stay intact."""
from pathlib import Path
from site_core import ROOT, REPO_URL, esc, load, shell, write

def build_family_home(researchers, folder_roles):
    hero = (ROOT / "web/living-hero.html").read_text(encoding="utf-8")
    hero = hero.replace("THE LIVING RESEARCH LIBRARY", "JP RESEARCH & DEVELOPMENT")
    hero = hero.replace("Where curiosity <em>takes flight.</em>", "One workspace. <em>Two families.</em>")
    hero = hero.replace(
        "An open home for thoughtful research, structural ideas, and reproducible discoveries. Follow every source, revision and careful step from question to knowledge.",
        "Choose Enterprise Documents for governed business records or Academic Writing for research, theses and scientific work. Source code and permissions remain separate for each family."
    )
    hero = hero.replace('href="thesis-infrastructure/index.html"', 'href="academic-writing/index.html"')
    hero = hero.replace("Explore the research library", "Enter Academic Writing")
    hero = hero.replace('href="researchers/index.html"', 'href="enterprise-documents/index.html"')
    hero = hero.replace("Meet the researchers", "Enter Enterprise Documents")
    hero = hero.replace("@@RESEARCHERS@@", str(len(researchers))).replace("@@ROOTS@@", str(folder_roles["verified_root_count"]))
    hero = hero.replace(
        "A working research collection. Indexing does not imply scientific or university approval.",
        "A code-and-evidence portal. A validated template does not by itself certify a contract, manuscript, or scientific result."
    )
    cards = (
        '<article class="card"><h2>Enterprise Documents</h2><p>Fourteen typed document families, private company branding, '
        'semantic controls, payment validation and explicit approval gates.</p>'
        '<p><a href="enterprise-documents/index.html">Open Enterprise Documents →</a></p></article>'
        '<article class="card"><h2>Academic Writing</h2><p>Researchers, thesis infrastructure, research LaTeX and presentations, '
        'scientific evidence, handovers, history and academic controls.</p>'
        '<p><a href="academic-writing/index.html">Open Academic Writing →</a></p></article>'
    )
    return (
        '<main>' + hero +
        '<section class="wrap section" aria-labelledby="family-choice"><h2 id="family-choice">Choose your document family</h2>'
        '<div class="family-grid">' + cards + '</div></section>'
        '<section class="wrap section"><h2>How this portal works</h2>'
        '<p>Humans state the objective and approve when required. Authorized AI workflows consult versioned controls, '
        'deterministic validators and the owning private source records. Missing evidence produces a HOLD, not an invented answer.</p>'
        '<p><a href="' + esc(REPO_URL + '/blob/main/docs/AI_FIRST_FAMILY_ROUTING_READ_FIRST.md') + '">Read the AI-first execution contract →</a></p>'
        '</section></main>'
    )

def build_academic_portal(out):
    nav = load(Path("registry/academic-family-navigation.v0.1.json"))
    tower = load(Path("controls/academic-writing/tower.json"))
    groups = []
    for group in nav["groups"]:
        cards = "".join(
            '<article class="card"><h3>' + esc(item["title"]) + '</h3>'
            '<p>' + esc(item["description"]) + '</p>'
            '<p><a href="../' + esc(item["route"]) + '/index.html">Open workspace →</a></p></article>'
            for item in group["items"]
        )
        groups.append('<section class="section"><h2>' + esc(group["group"]) + '</h2>'
                      '<div class="grid">' + cards + '</div></section>')
    body = (
        '<main class="wrap hero"><div class="eyebrow">Academic Writing · Family Hub</div>'
        '<h1>Research, theses and academic controls</h1>'
        '<p class="lead">The parent workspace for every research-related page: researcher workspaces, thesis folder roles, '
        'manuscripts, presentations, science QA, academic history and supporting demonstrations.</p>'
        '<div class="notice"><strong>Preserved links:</strong> existing researcher and research URLs still work. '
        'Only their navigation has been grouped under Academic Writing; no underlying research source was moved.</div>'
        '<p><a href="control-tower/index.html">Open the separate Academic Family Control Tower →</a></p>'
        + "".join(groups) + '</main>'
    )
    write(out, "academic-writing/index.html", shell("Academic Writing", body, 1))
    children = "".join(
        '<article class="card"><h3>' + esc(c["id"].replace("_", " ").title()) + '</h3>'
        '<p>' + esc(c["role"]) + '</p><p><a href="' + esc(REPO_URL + '/blob/main/' + c["canonical_control"]) +
        '">Read canonical control →</a></p></article>'
        for c in tower["children"]
    )
    tower_body=(
        '<main class="wrap hero"><div class="eyebrow">Academic Family · Control Tower</div>'
        '<h1>Academic Writing Control Tower</h1>'
        '<p class="lead">A family router over existing canonical scientific controls. It is not a second thesis style '
        'tower and it cannot approve unsupported research claims.</p>'
        '<section class="section"><h2>Independent academic control modules</h2>'
        '<div class="grid">' + children + '</div></section>'
        '<section class="section"><h2>Authority boundaries</h2>'
        '<p>Academic proof, institutional approval and manuscript correctness require verified sources and domain review. '
        'Enterprise client-contract semantics remain separate.</p>'
        '<p><a href="' + esc(REPO_URL + '/blob/main/controls/academic-writing/tower.json') +
        '">Read machine-readable academic family control →</a></p></section></main>'
    )
    write(out, "academic-writing/control-tower/index.html", shell("Academic Family Control", tower_body, 2))
    # Expose the public-safe routing map without adding a second source authority.
    write(out, "data/family-router.json",
          (ROOT / "controls/family-router.v0.1.json").read_text(encoding="utf-8"))
