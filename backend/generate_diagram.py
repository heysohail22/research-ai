import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_architecture_diagram():
    # Setup high-res figure with dark modern theme
    fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')
    
    # Hide axes
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title & Subtitle
    ax.text(8, 9.5, "AUTONOMOUS AI RESEARCH AGENT - ARCHITECTURE", 
            fontsize=20, fontweight='bold', color='#F8FAFC', ha='center', va='center')
    ax.text(8, 9.08, "End-to-End Information Retrieval, Algorithmic Deduplication & LLM Synthesis Pipeline", 
            fontsize=11, color='#94A3B8', ha='center', va='center')

    # Helper function for drawing rounded boxes
    def draw_card(x, y, w, h, bg_color, border_color, title, subtitle="", badge="", badge_color="#38BDF8"):
        # Shadow
        shadow = patches.FancyBboxPatch(
            (x + 0.06, y - 0.06), w, h,
            boxstyle="round,pad=0.1,rounding_size=0.2",
            fc='#030712', ec='none', alpha=0.5, zorder=2
        )
        ax.add_patch(shadow)
        
        # Main card
        card = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.1,rounding_size=0.2",
            fc=bg_color, ec=border_color, lw=1.5, zorder=3
        )
        ax.add_patch(card)
        
        # Badge
        if badge:
            badge_box = patches.FancyBboxPatch(
                (x + w - 1.6, y + h - 0.35), 1.5, 0.28,
                boxstyle="round,pad=0.05,rounding_size=0.1",
                fc='#0F172A', ec=badge_color, lw=1, zorder=4
            )
            ax.add_patch(badge_box)
            ax.text(x + w - 0.85, y + h - 0.21, badge, fontsize=7.5, fontweight='bold', 
                    color=badge_color, ha='center', va='center', zorder=5)

        # Title
        ax.text(x + 0.3, y + h - 0.45, title, fontsize=12, fontweight='bold', 
                color='#F1F5F9', ha='left', va='center', zorder=4)
        
        # Subtitle / content
        if subtitle:
            ax.text(x + 0.3, y + (h - 0.4) / 2, subtitle, fontsize=9, 
                    color='#CBD5E1', ha='left', va='center', zorder=4, linespacing=1.4)

    # 1. Presentation Layer (Top Left)
    draw_card(
        x=0.8, y=6.2, w=3.4, h=2.2,
        bg_color='#111827', border_color='#38BDF8',
        title="1. Presentation Layer",
        subtitle="• Next.js Web Dashboard\n  (React 19, Tailwind CSS)\n• CLI Terminal Runner\n  (main.py via uv)\n• Real-time progress tracker",
        badge="UI / CLIENT", badge_color="#38BDF8"
    )

    # 2. Orchestration & API Layer (Top Center)
    draw_card(
        x=5.2, y=6.2, w=4.0, h=2.2,
        bg_color='#111827', border_color='#818CF8',
        title="2. API & Orchestrator",
        subtitle="• FastAPI REST Backend (:8000)\n• Endpoint: POST /api/research\n• Pydantic schema validation\n• Session & CORS handler",
        badge="FASTAPI", badge_color="#818CF8"
    )

    # 3. External Ingestion (Top Right)
    draw_card(
        x=10.2, y=6.2, w=4.8, h=2.2,
        bg_color='#111827', border_color='#F59E0B',
        title="3. Live Data Ingestion",
        subtitle="• Tavily Search API Client\n• Advanced depth web retrieval\n• Neural page reranking\n• Returns 8 raw candidates + excerpts",
        badge="TAVILY SEARCH", badge_color="#F59E0B"
    )

    # 4. Processing & Deduplication Pipeline (Middle spanning)
    # Background container for pipeline
    pipe_bg = patches.FancyBboxPatch(
        (0.8, 3.2), 14.2, 2.3,
        boxstyle="round,pad=0.15,rounding_size=0.25",
        fc='#0F172A', ec='#334155', lw=1.2, zorder=2
    )
    ax.add_patch(pipe_bg)
    ax.text(1.2, 5.15, "4. Relevance Filtering & Lexical Deduplication Engine (Zero LLM Overhead)", 
            fontsize=11, fontweight='bold', color='#38BDF8', zorder=3)

    # 4 Sub-stages inside the pipeline
    sub_stages = [
        ("Step 4A", "Relevance Scoring", "Filters Tavily score < 0.72\nEnsures topical signal"),
        ("Step 4B", "Quality Filter", "Min length > 80 chars\nDiscards cookie fluff"),
        ("Step 4C", "URL Normalization", "Strips UTM/tracking tags\nCaps 2 links per domain"),
        ("Step 4D", "Lexical Dedupe", "Jaccard word-set overlap\nDiscards duplicate articles")
    ]
    
    for i, (tag, stitle, sdesc) in enumerate(sub_stages):
        sx = 1.2 + i * 3.45
        draw_card(
            x=sx, y=3.45, w=3.1, h=1.45,
            bg_color='#1E293B', border_color='#475569',
            title=f"{tag}: {stitle}",
            subtitle=sdesc,
            badge="", badge_color="#94A3B8"
        )
        if i < 3:
            ax.annotate("", xy=(sx + 3.35, 4.15), xytext=(sx + 3.1, 4.15),
                        arrowprops=dict(arrowstyle="-|>", color='#64748B', lw=1.8), zorder=5)

    # 5. Synthesis Engine (Bottom Left)
    draw_card(
        x=0.8, y=0.5, w=6.8, h=2.2,
        bg_color='#111827', border_color='#10B981',
        title="5. LLM Synthesis Engine (Gemini)",
        subtitle="• Google Gemini 3.5 Flash Lite\n• Structured analytical prompt with ground-truth constraint\n• Guarantees inline citations referencing source IDs [1], [2]\n• Eliminates hallucinated assertions",
        badge="GEMINI 3.5", badge_color="#10B981"
    )

    # 6. Structured Deliverables (Bottom Right)
    draw_card(
        x=8.4, y=0.5, w=6.6, h=2.2,
        bg_color='#111827', border_color='#EC4899',
        title="6. Final Structured Deliverables",
        subtitle="• Key Points: 3-5 executive takeaways\n• Important Findings: In-depth analysis with citations [1], [2]\n• Actionable Insights: Strategic next steps\n• References & Sources: Verified URLs & descriptions\n• Auto-saved to outputs/*.md & rendered on UI",
        badge="DELIVERABLES", badge_color="#EC4899"
    )

    # Connecting Arrows
    def draw_arrow(x1, y1, x2, y2, color='#38BDF8', rad=0.0):
        connectionstyle = f"arc3,rad={rad}" if rad != 0 else "arc3"
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>", 
                color=color, 
                lw=2.2, 
                mutation_scale=15, 
                connectionstyle=connectionstyle
            ),
            zorder=6
        )

    # 1 -> 2
    draw_arrow(4.2, 7.3, 5.2, 7.3, color='#38BDF8')
    # 2 -> 3
    draw_arrow(9.2, 7.3, 10.2, 7.3, color='#818CF8')
    # 3 -> 4
    draw_arrow(12.6, 6.2, 12.6, 5.5, color='#F59E0B')
    # 4 -> 5
    draw_arrow(4.2, 3.2, 4.2, 2.7, color='#10B981')
    # 5 -> 6
    draw_arrow(7.6, 1.6, 8.4, 1.6, color='#EC4899')

    # Save to file
    out_path = "/home/sohail/Desktop/research-ai/architecture_diagram.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"✅ Architecture diagram saved successfully: {out_path}")

if __name__ == "__main__":
    create_architecture_diagram()
