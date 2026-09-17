import os
import time
from typing import List, Dict, Any

def generate_html_report(
    leads: List[Dict[str, Any]],
    job_title: str,
    location: str,
    output_file: str = "leads_report.html"
) -> str:
    """
    Generates a modern, interactive responsive HTML report with cards, filters,
    and 1-click cold outreach message copy buttons for HR, Tech Lead, and CEO.
    """
    out_path = os.path.abspath(output_file)
    timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S")

    cards_html = ""
    for idx, lead in enumerate(leads, 1):
        comp = lead.get("company", "Unknown Company")
        role = lead.get("role", "AI Engineer")
        loc = lead.get("location", location)
        paid = lead.get("paid_status", "Confirmed Paid")
        apply_url = lead.get("apply_url", "#")
        hr = lead.get("hr_contact", "Not Found")
        tech = lead.get("tech_contact", "Not Found")
        ceo = lead.get("ceo_contact", "Not Found")
        why = lead.get("why_fits", "")

        def extract_link(contact_str: str) -> tuple:
            if "http" in contact_str:
                parts = contact_str.split("http")
                title = parts[0].replace("—", "").replace("-", "").strip()
                url = "http" + parts[1].strip()
                return title or "LinkedIn Profile", url
            return contact_str, "#"

        hr_title, hr_url = extract_link(hr)
        tech_title, tech_url = extract_link(tech)
        ceo_title, ceo_url = extract_link(ceo)

        cards_html += f"""
        <div class="job-card" data-company="{comp.lower()}" data-role="{role.lower()}">
            <div class="card-header">
                <div>
                    <span class="badge badge-index">#{idx}</span>
                    <span class="badge badge-paid">💰 {paid}</span>
                </div>
                <span class="badge badge-loc">📍 {loc}</span>
            </div>
            
            <h2 class="company-title">{comp}</h2>
            <h3 class="role-title">{role}</h3>
            
            <div class="why-box">
                <strong>💡 Why it fits for Cold Reach:</strong>
                <p>{why}</p>
            </div>

            <div class="contacts-grid">
                <div class="contact-card hr-card">
                    <div class="contact-label">👤 HR / Talent Acquisition</div>
                    <div class="contact-name">{hr_title}</div>
                    <div class="contact-actions">
                        <a href="{hr_url}" target="_blank" class="btn btn-linkedin">View LinkedIn ↗</a>
                        <button class="btn btn-copy" onclick="copyTemplate('hr', '{comp}', '{role}')">Copy HR Pitch</button>
                    </div>
                </div>

                <div class="contact-card tech-card">
                    <div class="contact-label">💻 Tech / Engineering Lead <span class="badge-rec">Highest Conversion</span></div>
                    <div class="contact-name">{tech_title}</div>
                    <div class="contact-actions">
                        <a href="{tech_url}" target="_blank" class="btn btn-linkedin">View LinkedIn ↗</a>
                        <button class="btn btn-copy" onclick="copyTemplate('tech', '{comp}', '{role}')">Copy Tech Pitch</button>
                    </div>
                </div>

                <div class="contact-card ceo-card">
                    <div class="contact-label">👔 Founder / CEO</div>
                    <div class="contact-name">{ceo_title}</div>
                    <div class="contact-actions">
                        <a href="{ceo_url}" target="_blank" class="btn btn-linkedin">View LinkedIn ↗</a>
                        <button class="btn btn-copy" onclick="copyTemplate('ceo', '{comp}', '{role}')">Copy CEO Pitch</button>
                    </div>
                </div>
            </div>

            <div class="card-footer">
                <a href="{apply_url}" target="_blank" class="btn btn-apply">🚀 Direct Application Link</a>
            </div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Outreach & Cold Reach Leads Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0b0f19;
            --surface: #131b2e;
            --surface-card: #18223c;
            --border: #233152;
            --primary: #3b82f6;
            --accent: #10b981;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            padding: 2rem 1rem;
            line-height: 1.5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5);
        }}
        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 1rem;
        }}
        h1 {{
            font-size: 1.85rem;
            font-weight: 800;
            background: linear-gradient(90deg, #60a5fa, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .meta-pills {{
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-top: 0.5rem;
        }}
        .pill {{
            background: #1e293b;
            border: 1px solid var(--border);
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            color: var(--text-muted);
        }}
        .pill strong {{ color: #fff; }}
        
        .search-bar {{
            margin-top: 1.5rem;
            display: flex;
            gap: 1rem;
        }}
        .search-input {{
            flex: 1;
            padding: 0.85rem 1.25rem;
            background: #0b0f19;
            border: 1px solid var(--border);
            border-radius: 10px;
            color: #fff;
            font-size: 1rem;
            outline: none;
        }}
        .search-input:focus {{
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }}

        .jobs-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(550px, 1fr));
            gap: 1.5rem;
        }}
        @media (max-width: 768px) {{
            .jobs-grid {{ grid-template-columns: 1fr; }}
        }}

        .job-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s, border-color 0.2s;
        }}
        .job-card:hover {{
            transform: translateY(-2px);
            border-color: #3b82f6;
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
        }}
        .badge {{
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.25rem 0.65rem;
            border-radius: 6px;
            display: inline-block;
        }}
        .badge-index {{ background: #334155; color: #f8fafc; }}
        .badge-paid {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }}
        .badge-loc {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }}
        .badge-rec {{ background: #f59e0b; color: #000; font-size: 0.65rem; padding: 2px 6px; border-radius: 4px; margin-left: 4px; }}

        .company-title {{
            font-size: 1.4rem;
            font-weight: 700;
            color: #fff;
        }}
        .role-title {{
            font-size: 1.05rem;
            color: #93c5fd;
            margin-bottom: 1rem;
        }}
        
        .why-box {{
            background: rgba(15, 23, 42, 0.6);
            border-left: 3px solid #3b82f6;
            padding: 0.75rem 1rem;
            border-radius: 0 8px 8px 0;
            font-size: 0.875rem;
            color: #cbd5e1;
            margin-bottom: 1.25rem;
        }}

        .contacts-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 0.75rem;
            margin-bottom: 1.25rem;
        }}
        .contact-card {{
            background: var(--surface-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.75rem 1rem;
        }}
        .contact-label {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 0.25rem;
        }}
        .contact-name {{
            font-size: 0.9rem;
            font-weight: 600;
            color: #f1f5f9;
            margin-bottom: 0.5rem;
        }}
        .contact-actions {{
            display: flex;
            gap: 0.5rem;
        }}

        .btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            font-weight: 600;
            padding: 0.4rem 0.75rem;
            border-radius: 6px;
            text-decoration: none;
            cursor: pointer;
            border: none;
            transition: all 0.15s;
        }}
        .btn-linkedin {{
            background: #0284c7;
            color: #fff;
        }}
        .btn-linkedin:hover {{ background: #0369a1; }}
        .btn-copy {{
            background: #334155;
            color: #cbd5e1;
        }}
        .btn-copy:hover {{ background: #475569; color: #fff; }}
        .btn-apply {{
            width: 100%;
            background: linear-gradient(90deg, #2563eb, #1d4ed8);
            color: #fff;
            padding: 0.65rem;
            font-size: 0.95rem;
        }}
        .btn-apply:hover {{
            background: linear-gradient(90deg, #1d4ed8, #1e40af);
        }}
        
        .toast {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: #10b981;
            color: #000;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.9rem;
            display: none;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5);
            z-index: 999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-top">
                <div>
                    <h1>🎯 Job Outreach & Cold Reach Intelligence</h1>
                    <div class="meta-pills">
                        <div class="pill">Role: <strong>{job_title}</strong></div>
                        <div class="pill">Location: <strong>{location}</strong></div>
                        <div class="pill">Qualified Leads: <strong>{len(leads)}</strong></div>
                        <div class="pill">Updated: <strong>{timestamp_str}</strong></div>
                    </div>
                </div>
            </div>
            
            <div class="search-bar">
                <input type="text" id="searchInput" class="search-input" placeholder="🔍 Filter by company name or role title..." onkeyup="filterCards()">
            </div>
        </header>

        <div class="jobs-grid" id="jobsGrid">
            {cards_html}
        </div>
    </div>

    <div id="toast" class="toast">📋 Pitch template copied to clipboard!</div>

    <script>
        function filterCards() {{
            const query = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.job-card');
            cards.forEach(card => {{
                const comp = card.getAttribute('data-company');
                const role = card.getAttribute('data-role');
                if (comp.includes(query) || role.includes(query)) {{
                    card.style.display = 'flex';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}

        function showToast(text) {{
            const toast = document.getElementById('toast');
            toast.innerText = text;
            toast.style.display = 'block';
            setTimeout(() => {{
                toast.style.display = 'none';
            }}, 2500);
        }}

        function copyTemplate(type, company, role) {{
            let template = "";
            if (type === 'hr') {{
                template = `Hi! I recently submitted my application for the ${{role}} opening at ${{company}}.\\n\\nI specialize in building practical AI systems (LLMs, LangGraph agentic workflows, and RAG pipelines). My GitHub projects and resume are attached for quick review.\\n\\nWould love to know if any further details are required for the initial screening stage. Thank you!`;
            }} else if (type === 'tech') {{
                template = `Hi! Saw the cutting-edge AI work your team is shipping at ${{company}}.\\n\\nI’m an AI engineer focusing on multi-agent workflows and real-time LLM pipelines. I recently built a project tackling sub-second document reasoning and tool-calling agents.\\n\\nHere is the repo & demo: [Your GitHub/Loom link]\\n\\nI've applied for the ${{role}} position and would love 5 minutes to show how I can start contributing to your team's sprint this term!`;
            }} else {{
                template = `Hi! Love what you and the founding team are building at ${{company}}.\\n\\nI saw you're expanding the team with the ${{role}} role. I have hands-on experience building production-grade agentic workflows and LLM applications.\\n\\nWould love 5 minutes to share how I can help accelerate your engineering roadmap this quarter. Either way, cheering on your growth!`;
            }}

            navigator.clipboard.writeText(template).then(() => {{
                showToast("📋 Copied " + type.toUpperCase() + " outreach pitch to clipboard!");
            }});
        }}
    </script>
</body>
</html>
"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[HTML REPORT] Generated interactive report at: {out_path}")
    return out_path
