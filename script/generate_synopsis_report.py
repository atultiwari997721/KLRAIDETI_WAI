import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=200, right=200):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout(doc, text, title="NOTE / ARCHITECTURAL PRINCIPLE", color_hex="00A8B5", bg_hex="F0FBFC"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=160, bottom=160, left=240, right=200)
    
    # Left border
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:left w:val="single" w:sz="36" w:space="0" w:color="{color_hex}"/>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"✦ {title}\n")
    run_t.font.name = "Arial"
    run_t.font.size = Pt(9.5)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor.from_string(color_hex)
    
    run_b = p.add_run(text)
    run_b.font.name = "Calibri"
    run_b.font.size = Pt(10)
    run_b.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    
    # Empty space after table
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(4)
    p_after.paragraph_format.space_after = Pt(6)

def style_heading(heading, space_before=16, space_after=6):
    heading.paragraph_format.space_before = Pt(space_before)
    heading.paragraph_format.space_after = Pt(space_after)
    heading.paragraph_format.keep_with_next = True

print("Initializing document...")
doc = docx.Document()

# Page Margins: 1 inch all around
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Colors
C_NAVY = RGBColor(0x0C, 0x1E, 0x3D)
C_CYAN = RGBColor(0x00, 0x8F, 0xA8)
C_PURPLE = RGBColor(0x6A, 0x22, 0xAA)
C_DARK = RGBColor(0x22, 0x22, 0x22)
C_GRAY = RGBColor(0x55, 0x55, 0x55)

# --- COVER / TITLE BLOCK ---
title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(24)
title_p.paragraph_format.space_after = Pt(4)
title_run = title_p.add_run("KritiAI Architecture & Technical Synopsis")
title_run.font.name = "Arial"
title_run.font.size = Pt(26)
title_run.font.bold = True
title_run.font.color.rgb = C_NAVY

subtitle_p = doc.add_paragraph()
subtitle_p.paragraph_format.space_before = Pt(0)
subtitle_p.paragraph_format.space_after = Pt(18)
sub_run = subtitle_p.add_run("Full Architectural Blueprint, Internal State Machines, and Comprehensive Operations Report")
sub_run.font.name = "Calibri"
sub_run.font.size = Pt(13)
sub_run.font.italic = True
sub_run.font.color.rgb = C_CYAN

# Meta Table
meta_table = doc.add_table(rows=4, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Application Name:", "KritiAI (Autonomous AI Coding Studio & Desktop IDE)"),
    ("Target Platform:", "Windows Desktop (x64 Native), Web Portal, Headless CLI / Server"),
    ("System Release Version:", "Version 1.0.0 (Production Release)"),
    ("Report Classification:", "Complete Engineering Specification & Architectural Deep Dive"),
]
for i, (k, v) in enumerate(meta_data):
    row = meta_table.rows[i]
    cell_k, cell_v = row.cells[0], row.cells[1]
    cell_k.width = Inches(2.2)
    cell_v.width = Inches(4.3)
    
    set_cell_background(cell_k, "F4F6F9")
    set_cell_background(cell_v, "FFFFFF")
    
    pk = cell_k.paragraphs[0]
    pk.paragraph_format.space_before = Pt(3)
    pk.paragraph_format.space_after = Pt(3)
    rk = pk.add_run(k)
    rk.font.name = "Arial"
    rk.font.size = Pt(9.5)
    rk.font.bold = True
    rk.font.color.rgb = C_NAVY
    
    pv = cell_v.paragraphs[0]
    pv.paragraph_format.space_before = Pt(3)
    pv.paragraph_format.space_after = Pt(3)
    rv = pv.add_run(v)
    rv.font.name = "Calibri"
    rv.font.size = Pt(9.5)
    rv.font.color.rgb = C_DARK

p_space = doc.add_paragraph()
p_space.paragraph_format.space_before = Pt(14)
p_space.paragraph_format.space_after = Pt(6)

# Divider line
p_div = doc.add_paragraph()
p_div.paragraph_format.space_before = Pt(0)
p_div.paragraph_format.space_after = Pt(14)
r_div = p_div.add_run("―" * 55)
r_div.font.color.rgb = RGBColor(0xDD, 0xDD, 0xDD)

# --- SECTION 1 ---
h1 = doc.add_heading("1. Executive Summary & Core Purpose", level=1)
style_heading(h1, 14, 6)
h1.runs[0].font.name = "Arial"
h1.runs[0].font.color.rgb = C_NAVY

p1 = doc.add_paragraph(
    "KritiAI is an enterprise-grade autonomous AI coding environment and desktop integrated development studio. "
    "Unlike conventional autocomplete extensions or chatbot sidebars that merely offer isolated snippets, KritiAI "
    "operates as a self-driving engineering agent. It possesses process-level awareness of the developer's entire workspace, "
    "executes surgical multi-file edits, runs terminal verification commands, analyzes compile-time diagnostics, and loops "
    "autonomously until user-defined software engineering goals are verified and complete."
)
p1.paragraph_format.space_before = Pt(0)
p1.paragraph_format.space_after = Pt(8)
p1.runs[0].font.name = "Calibri"
p1.runs[0].font.size = Pt(11)

p2 = doc.add_paragraph(
    "The application is engineered to bridge the critical gap between frontier AI reasoning models and local file-system reality. "
    "By maintaining an ACID-compliant durable state machine in SQLite, decoupling prompt admission from LLM execution, "
    "and embedding deep Language Server Protocol (LSP) intelligence, KritiAI guarantees absolute workspace integrity, "
    "zero state corruption across process crashes, and complete local privacy."
)
p2.paragraph_format.space_before = Pt(0)
p2.paragraph_format.space_after = Pt(10)
p2.runs[0].font.name = "Calibri"
p2.runs[0].font.size = Pt(11)

add_callout(
    doc,
    "Core Paradigm: Durable State Preservation\n"
    "In KritiAI, model execution is strictly separated from durable prompt admission. User prompts are admitted into a persistent "
    "inbox table (session_input) before any model work begins. Even if a network disconnects or the machine restarts mid-stream, "
    "the session resumes predictably without losing user intent or corrupting transaction boundaries.",
    title="FOUNDATIONAL INVARIANT: DURABLE ADMISSION",
    color_hex="0C1E3D",
    bg_hex="F0F4FA"
)

# --- SECTION 2 ---
h2 = doc.add_heading("2. High-Level System Architecture & Package Topology", level=1)
style_heading(h2, 18, 6)
h2.runs[0].font.name = "Arial"
h2.runs[0].font.color.rgb = C_NAVY

p_arch = doc.add_paragraph(
    "KritiAI is structured as an ultra-modular monorepo governed by strict, directed runtime dependencies. "
    "The architectural invariant dictates that runtime dependencies flow unidirectionally from Schema to Core and Protocol, "
    "and then from Core and Protocol to Server. Client and Web UI runtime code may depend on Schema and Protocol, but never directly on Core or Server. "
    "The package breakdown is as follows:"
)
p_arch.paragraph_format.space_after = Pt(8)
p_arch.runs[0].font.name = "Calibri"
p_arch.runs[0].font.size = Pt(11)

packages_info = [
    ("packages/core", "The central business logic engine. Houses SessionV2, prompt execution state machines, tool orchestrators, provider stream processors, and permission gatekeepers."),
    ("packages/schema", "The single source of truth for durable data structures. Implements SQLite tables via Drizzle ORM using snake_case columns, transaction schemas, and migration registries."),
    ("packages/protocol", "Type-safe communication contracts defining IPC messages, WebSocket event streams, RPC endpoints, and Model Context Protocol (MCP) tool interfaces."),
    ("packages/desktop", "The native Windows, macOS, and Linux shell. Powered by Electron 42, it manages native OS windows, custom titlebars, hardware acceleration, background worker spawns, and NSIS installers."),
    ("packages/app", "The high-performance reactive GUI built on SolidJS. Operates with zero virtual DOM overhead, fine-grained signal reactivity, syntax highlighted editors, and virtualized diff streams."),
    ("packages/opencode (CLI/TUI)", "The terminal engineering environment. Built with Bun and OpenTUI, providing terminal user interfaces, keyboard shortcuts, diff viewports, and interactive terminal loops."),
    ("packages/server", "Embedded Hono HTTP and WebSocket server. Bridges native desktop processes with external tools, editor extensions, and remote browser clients."),
    ("packages/llm", "Frontier model adaptation layer. Normalizes streaming APIs across Google Gemini, Anthropic Claude, OpenAI GPT, DeepSeek, and local offline models via Ollama."),
    ("packages/system-context", "Workspace observation algebra. Tracks file system epochs, git commit differentials, terminal outputs, and symbol definitions into prompt context."),
]

table_pkg = doc.add_table(rows=len(packages_info) + 1, cols=2)
table_pkg.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_row = table_pkg.rows[0]
hdr_row.cells[0].width = Inches(2.0)
hdr_row.cells[1].width = Inches(4.5)
set_cell_background(hdr_row.cells[0], "0C1E3D")
set_cell_background(hdr_row.cells[1], "0C1E3D")

for idx, h_text in enumerate(["Package Layer", "Core Architectural Responsibility"]):
    p = hdr_row.cells[idx].paragraphs[0]
    r = p.add_run(h_text)
    r.font.name = "Arial"
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

for i, (pkg, desc) in enumerate(packages_info):
    row = table_pkg.rows[i + 1]
    cell_p, cell_d = row.cells[0], row.cells[1]
    cell_p.width = Inches(2.0)
    cell_d.width = Inches(4.5)
    
    bg = "F9FAFC" if i % 2 == 0 else "FFFFFF"
    set_cell_background(cell_p, bg)
    set_cell_background(cell_d, bg)
    
    pp = cell_p.paragraphs[0]
    pp.paragraph_format.space_before = Pt(3)
    pp.paragraph_format.space_after = Pt(3)
    rp = pp.add_run(pkg)
    rp.font.name = "Consolas"
    rp.font.size = Pt(9.5)
    rp.font.bold = True
    rp.font.color.rgb = C_CYAN
    
    pd = cell_d.paragraphs[0]
    pd.paragraph_format.space_before = Pt(3)
    pd.paragraph_format.space_after = Pt(3)
    rd = pd.add_run(desc)
    rd.font.name = "Calibri"
    rd.font.size = Pt(9.5)
    rd.font.color.rgb = C_DARK

p_space2 = doc.add_paragraph()
p_space2.paragraph_format.space_before = Pt(12)

# --- SECTION 3 ---
h3 = doc.add_heading("3. The V2 Session Core & State Machine Mechanics", level=1)
style_heading(h3, 16, 6)
h3.runs[0].font.name = "Arial"
h3.runs[0].font.color.rgb = C_NAVY

p3_1 = doc.add_paragraph(
    "The beating heart of KritiAI is the V2 Session Core (`SessionV2`). Unlike naive agent loops that hold state exclusively "
    "in ephemeral JavaScript heap memory, KritiAI enforces durable state transitions that mirror database transaction logs:"
)
p3_1.runs[0].font.name = "Calibri"
p3_1.runs[0].font.size = Pt(11)

points_v2 = [
    ("Durable Input Admission:", "When a developer submits a prompt (via GUI, keyboard, or API), SessionV2.prompt(...) first inserts a row into the session_input database table. Only after the row is committed is an advisory SessionExecution.wake(sessionID) event dispatched. This ensures zero prompt loss regardless of execution status."),
    ("Process-Global Coordination:", "SessionExecution is managed as a process-global singleton keyed by sessionID. Multiple calls to run or wake the same session join a coalesced execution drain (SessionRunCoordinator), preventing concurrent model races on the same workspace."),
    ("Steering vs. Queuing Mechanics:", "By default, prompts are admitted in 'steer' mode—they are promoted into the model turn allowance at the next safe provider boundary. Alternatively, 'queue' prompts remain pending until the current session reaches a resting idle state, at which point exactly one queued message is promoted."),
    ("Single-Turn LLM Stream Execution:", "Each turn preserves exactly one explicit llm.stream(request) invocation. Projected historical messages are re-read and validated from the database before durable continuation. KritiAI strictly forbids unbounded in-memory recursive tool loops."),
    ("Turn Allowance Reset:", "Promoting any new user input resets the agent's provider-turn allowance counter, allowing long multi-step investigations without hitting arbitrary hard stop thresholds."),
]

for title, body in points_v2:
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    r1 = p.add_run(f"{title} ")
    r1.font.name = "Arial"
    r1.font.size = Pt(10)
    r1.font.bold = True
    r1.font.color.rgb = C_PURPLE
    r2 = p.add_run(body)
    r2.font.name = "Calibri"
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = C_DARK

# --- SECTION 4 ---
h4 = doc.add_heading("4. Technology Stack & Framework Justifications", level=1)
style_heading(h4, 16, 6)
h4.runs[0].font.name = "Arial"
h4.runs[0].font.color.rgb = C_NAVY

p_tech = doc.add_paragraph(
    "Every technology in the KritiAI stack was selected to maximize deterministic execution speed, memory efficiency, and developer ergonomics:"
)
p_tech.runs[0].font.name = "Calibri"
p_tech.runs[0].font.size = Pt(11)

tech_stack = [
    ("Bun Runtime", "Used for package orchestration, lightning-fast compilation, native file I/O (Bun.file), and high-throughput script execution."),
    ("Effect-TS (Algebraic Effects)", "Powers core domain services, layered dependency injection, typed error handling, and robust concurrency control without messy try/catch chains."),
    ("SolidJS & Solid-Start", "Eliminates the performance overhead of the Virtual DOM. Provides surgical reactivity where only modified DOM text nodes and diff spans re-render during token streams."),
    ("Drizzle ORM & SQLite", "Embedded transactional storage. SQLite WAL (Write-Ahead Logging) mode allows concurrent reader processes while maintaining sub-millisecond durable writes."),
    ("Electron 42 & NSIS", "Provides native desktop capability on Windows with custom frameless window styling, GPU-accelerated canvas rendering, and zero browser sandbox constraints."),
    ("OpenTUI", "Delivers high-performance terminal UI rendering for developers working directly in headless SSH, WSL, or console environments."),
]

for name, desc in tech_stack:
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    r1 = p.add_run(f"{name}: ")
    r1.font.name = "Arial"
    r1.font.size = Pt(10)
    r1.font.bold = True
    r1.font.color.rgb = C_NAVY
    r2 = p.add_run(desc)
    r2.font.name = "Calibri"
    r2.font.size = Pt(10.5)

# --- SECTION 5 ---
h5 = doc.add_heading("5. Operational Workflow: How KritiAI Works End-to-End", level=1)
style_heading(h5, 16, 6)
h5.runs[0].font.name = "Arial"
h5.runs[0].font.color.rgb = C_NAVY

p5_intro = doc.add_paragraph(
    "To understand the power of KritiAI, consider the typical lifecycle when a developer requests a complex feature:"
)
p5_intro.runs[0].font.name = "Calibri"
p5_intro.runs[0].font.size = Pt(11)

steps = [
    ("Step 1: Workspace Ingestion & Epoch Projection", "KritiAI examines git branch state, active editor tabs, and indexed symbol maps. A System Context Epoch is generated, packing current diffs, relevant file excerpts, and environment variables into model context."),
    ("Step 2: Frontier Model Turn & Tool Proposal", "The prompt is passed to the configured model (e.g. Gemini 2.5 Pro or Claude 3.7 Sonnet). The model analyzes the request and outputs a structured tool invocation, such as `edit_file` or `run_command`."),
    ("Step 3: Surgical Sandboxed Execution", "KritiAI validates security policies and runs the proposed action. For file edits, modifications are performed with strict character-sequence matching and syntax integrity checks. For commands, tests and linters execute in an isolated subshell."),
    ("Step 4: Feedback Loop & Autonomous Error Correction", "If the edit introduces a compiler error, syntax failure, or test break, KritiAI captures the stdout/stderr stream directly into the conversation transcript. Rather than halting, the agent automatically examines the error diagnostic, formulates a repair diff, and verifies the fix."),
    ("Step 5: Completion & User Presentation", "Once all tests pass and changes are validated, the session completes. The user is presented with a unified Git diff and an executive summary of completed actions."),
]

for s_num, s_desc in steps:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r_n = p.add_run(f"{s_num}\n")
    r_n.font.name = "Arial"
    r_n.font.size = Pt(10.5)
    r_n.font.bold = True
    r_n.font.color.rgb = C_CYAN
    r_d = p.add_run(s_desc)
    r_d.font.name = "Calibri"
    r_d.font.size = Pt(10.5)
    r_d.font.color.rgb = C_DARK

# --- SECTION 6 ---
h6 = doc.add_heading("6. Comprehensive User Guide: How to Use KritiAI", level=1)
style_heading(h6, 16, 6)
h6.runs[0].font.name = "Arial"
h6.runs[0].font.color.rgb = C_NAVY

p6_text = doc.add_paragraph(
    "KritiAI offers flexible interfaces adapted to different developer preferences and environments:"
)
p6_text.runs[0].font.name = "Calibri"
p6_text.runs[0].font.size = Pt(11)

modes = [
    ("1. Native Windows Desktop Application", "Launch KritiAI from the Desktop shortcut or Start Menu. Enjoy a responsive frameless desktop client complete with full split-pane views, interactive file tree navigation, visual diff review, and local GPU acceleration."),
    ("2. Command-Line & Headless Terminal Mode", "Run `kritiai` from any shell inside your project repository. The Terminal User Interface (TUI) activates immediately, providing full agent capabilities without leaving your terminal workflow."),
    ("3. Web Portal & Interactive Studio", "Visit the deployed Vercel web portal at https://kritiai-web.vercel.app to explore documentation, test prompts in the live browser studio demo, or download the latest Windows desktop installer."),
    ("4. Slash Command Shortcuts", "Use built-in agent shortcuts in chat: `/plan` for multi-step task breakdowns, `/goal` for autonomous long-running execution loops, and `/boost` for multi-agent reasoning tasks."),
]

for m_title, m_desc in modes:
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    r1 = p.add_run(f"{m_title}: ")
    r1.font.name = "Arial"
    r1.font.size = Pt(10)
    r1.font.bold = True
    r1.font.color.rgb = C_NAVY
    r2 = p.add_run(m_desc)
    r2.font.name = "Calibri"
    r2.font.size = Pt(10.5)

# --- SECTION 7 ---
h7 = doc.add_heading("7. Production Deployment & Global Distribution", level=1)
style_heading(h7, 16, 6)
h7.runs[0].font.name = "Arial"
h7.runs[0].font.color.rgb = C_NAVY

p7_text = doc.add_paragraph(
    "The deployment pipeline integrates three world-class infrastructures to ensure blazing speed, zero downtime, and instant global distribution:"
)
p7_text.runs[0].font.name = "Calibri"
p7_text.runs[0].font.size = Pt(11)

deploy_points = [
    ("Vercel Edge Network (Web Portal):", "The public website is deployed to Vercel (https://kritiai-web.vercel.app). Built with ultra-clean static routing, responsive dark-neon styling, and edge caching, it serves global traffic with sub-100ms latency."),
    ("GitHub Releases Global CDN (Binary Storage):", "The 183 MB Windows installer (KritiAi-desktop-win-x64.exe) is hosted directly on GitHub Releases under tag v1.0.0. This bypasses Vercel Hobby 100MB static upload limits while leveraging GitHub's unlimited-bandwidth worldwide CDN."),
    ("Seamless Dynamic Redirection:", "The Vercel route /download/windows seamlessly issues an HTTP 307 temporary redirect to the latest GitHub Release asset, allowing end users to download the executable with a single click directly from your domain."),
    ("PE Binary Resource Inversion:", "Every generated Windows binary includes the updated glowing crystal 'Ki' logo injected directly into the PE header via rcedit, ensuring that Windows Explorer, Alt+Tab, and the taskbar display pristine branded icons."),
]

for dt, dd in deploy_points:
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    r1 = p.add_run(f"{dt} ")
    r1.font.name = "Arial"
    r1.font.size = Pt(10)
    r1.font.bold = True
    r1.font.color.rgb = C_CYAN
    r2 = p.add_run(dd)
    r2.font.name = "Calibri"
    r2.font.size = Pt(10.5)

# --- SECTION 8 ---
h8 = doc.add_heading("8. Security, Local Privacy & Performance Guarantees", level=1)
style_heading(h8, 16, 6)
h8.runs[0].font.name = "Arial"
h8.runs[0].font.color.rgb = C_NAVY

sec_points = [
    ("Local-First Architecture:", "Source code stays exclusively on the developer's computer. When utilizing local LLM backends (such as Ollama or vLLM), zero tokens leave the local network."),
    ("Granular Permission Boundaries:", "KritiAI enforces strict permissions for tool invocations. Read, write, and command executions can be configured for automatic authorization, interactive prompting, or full restriction per agent."),
    ("Subprocess Isolation:", "Background build tools, test runners, and node-pty terminal processes run in isolated process trees, preventing memory leaks or runaway daemon processes from degrading system performance."),
    ("Deterministic Cache Invalidation:", "Language server ASTs and git status hashes are cached deterministically. Re-indexing occurs incrementally only for files that have suffered modification since the last epoch."),
]

for st, sd in sec_points:
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    r1 = p.add_run(f"{st} ")
    r1.font.name = "Arial"
    r1.font.size = Pt(10)
    r1.font.bold = True
    r1.font.color.rgb = C_PURPLE
    r2 = p.add_run(sd)
    r2.font.name = "Calibri"
    r2.font.size = Pt(10.5)

add_callout(
    doc,
    "Summary of URLs & Access Points:\n"
    "• Production Web Portal: https://kritiai-web.vercel.app\n"
    "• Windows App Download: https://kritiai-web.vercel.app/download/windows\n"
    "• GitHub Code Repository: https://github.com/atultiwari997721/KLRAIDETI_WAI\n"
    "• Direct Release Asset: https://github.com/atultiwari997721/KLRAIDETI_WAI/releases/tag/v1.0.0",
    title="KEY PRODUCTION ENDPOINTS",
    color_hex="008FA8",
    bg_hex="F0FBFC"
)

# Footer note
p_end = doc.add_paragraph()
p_end.paragraph_format.space_before = Pt(20)
p_end.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_end = p_end.add_run("― End of Architectural Synopsis Report • Generated for KritiAI v1.0.0 ―")
r_end.font.name = "Calibri"
r_end.font.size = Pt(9.5)
r_end.font.italic = True
r_end.font.color.rgb = C_GRAY

# Output paths
ROOT_DIR = r"K:\Projects\KLRAIDETI_WAI"
out_paths = [
    os.path.join(ROOT_DIR, "KritiAI_Architecture_and_Synopsis_Report.docx"),
    os.path.join(ROOT_DIR, "deploy", "kritiai-web", "KritiAI_Architecture_and_Synopsis_Report.docx"),
    os.path.join(ROOT_DIR, "deploy", "kritiai-web", "report.docx"),
]

for out_path in out_paths:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc.save(out_path)
    print(f"Report saved successfully to: {out_path}")

print("All reports generated successfully!")
