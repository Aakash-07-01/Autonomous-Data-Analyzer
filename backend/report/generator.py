import markdown
import datetime
from bs4 import BeautifulSoup
import re

def generate_html(markdown_text: str, charts: list, filename: str = "dataset.csv", job_id: str = "") -> str:
    """
    Converts markdown text to a fully styled standalone HTML document.
    Embeds the interactive Plotly HTML snippets instead of static images.
    Features a modern dark-theme dashboard, a left sidebar for dynamic Table of Contents,
    ScrollSpy headings tracking, scroll-reveal animations, responsive layouts, and clean print styling.
    """
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_text, extensions=['extra', 'tables'])
    
    # Process headings and tables with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    toc_items = []
    
    # Add anchor links to headings and build TOC items
    header_index = 0
    for header in soup.find_all(['h1', 'h2', 'h3']):
        header_text = header.text.strip()
        if not header_text:
            continue
        
        # Generate clean ID for headings
        header_id = header.get('id')
        if not header_id:
            clean_text = re.sub(r'[^a-zA-Z0-9\-]', '', header_text.lower().replace(' ', '-').replace('_', '-'))
            header_id = f"section-{header_index}-{clean_text}"
            header['id'] = header_id
        
        # Ensure scroll margin so links align nicely when clicked
        header['class'] = header.get('class', []) + ['scroll-mt-24']
        
        toc_items.append({
            'level': int(header.name[1]),
            'title': header_text,
            'id': header_id
        })
        header_index += 1
        
    # Wrap all tables in a responsive card div for scrolling and layout consistency
    for table in soup.find_all('table'):
        wrapper = soup.new_tag('div', **{
            'class': 'overflow-x-auto my-6 border border-[#222226] rounded-xl bg-[#08080a] shadow-inner max-w-full'
        })
        table.wrap(wrapper)

    processed_html = str(soup)
    
    # Generate Table of Contents HTML
    toc_html = ""
    if toc_items:
        for item in toc_items:
            pl = "pl-2" if item['level'] == 1 else "pl-5 border-l border-neutral-800" if item['level'] == 2 else "pl-8 border-l border-neutral-800"
            font_size = "text-xs font-bold tracking-[0.08em] uppercase text-white mt-4 first:mt-0 font-mono" if item['level'] == 1 else "text-xs text-neutral-400 font-medium" if item['level'] == 2 else "text-[11px] text-neutral-500"
            toc_html += f"""
            <a href="#{item['id']}" class="toc-item block py-1.5 transition-all duration-200 hover:text-white border-l-2 border-transparent hover:border-neutral-600 {pl} {font_size}">
                {item['title']}
            </a>
            """
    else:
        toc_html = "<span class='text-xs text-neutral-600 font-mono pl-2 italic'>No sections indexed</span>"

    # Inject interactive charts
    charts_html = "<div class='grid grid-cols-1 xl:grid-cols-2 gap-8 mt-8'>"
    for idx, chart in enumerate(charts):
        charts_html += f"""
        <div class="bg-[#0c0c0e]/95 border border-[#1f1f23] rounded-2xl p-6 shadow-2xl hover:border-[#22c55e]/30 transition-all duration-300 chart-card-wrap hover:-translate-y-1 relative group overflow-hidden">
            <!-- Corner borders hover indicator -->
            <div class="absolute top-0 left-0 w-3 h-3 border-t border-l border-transparent group-hover:border-[#22c55e]/40 transition-colors"></div>
            <div class="absolute top-0 right-0 w-3 h-3 border-t border-r border-transparent group-hover:border-[#22c55e]/40 transition-colors"></div>
            <h3 class="text-xs font-semibold mb-4 text-[#22c55e] text-center font-mono tracking-widest uppercase chart-title-text flex items-center justify-center space-x-2">
                <span class="w-1.5 h-1.5 rounded-full bg-[#22c55e]/60"></span>
                <span>{chart.get('title', 'Visualization')}</span>
            </h3>
            <div class="chart-wrapper bg-[#040405] rounded-xl p-2 border border-[#151518]/80">
                {chart.get('html', '')}
            </div>
        </div>
        """
    charts_html += "</div>"
    
    # Metadata calculations
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    job_id_short = job_id[:8] + "..." if len(job_id) > 8 else (job_id if job_id else "N/A")
    
    full_html = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Autonomous EDA Report | {filename}</title>
    <!-- Tailwind CSS for utility styles -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        mono: ['JetBrains Mono', 'monospace'],
                        display: ['Orbitron', 'sans-serif'],
                        sans: ['Inter', 'sans-serif'],
                    }},
                    colors: {{
                        brand: {{
                            green: '#22c55e',
                            neon: '#39ff14',
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Orbitron:wght@600;700;800;900&display=swap" rel="stylesheet">
    <!-- Plotly.js for interactive charts -->
    <script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
    <style>
        body {{
            background-color: #030303;
            color: #d4d4d8;
            font-family: 'Inter', sans-serif;
            overflow-x: hidden;
        }}
        
        /* Grid background */
        .cyber-grid {{
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.007) 1px, transparent 1px), 
                linear-gradient(90deg, rgba(255, 255, 255, 0.007) 1px, transparent 1px);
            background-size: 40px 40px;
        }}

        /* Glow effects */
        .radial-glow {{
            background: radial-gradient(circle, rgba(34, 197, 94, 0.06) 0%, rgba(0, 0, 0, 0) 70%);
        }}
        
        .card-glow:hover {{
            box-shadow: 0 0 35px rgba(34, 197, 94, 0.05);
            border-color: rgba(34, 197, 94, 0.2);
        }}

        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        ::-webkit-scrollbar-track {{
            background: #030304;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #1c1c21;
            border-radius: 3px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #22c55e;
        }}

        /* Markdown elements styling */
        .markdown-container h1 {{
            font-size: 2rem;
            font-weight: 800;
            color: #ffffff;
            font-family: 'Orbitron', sans-serif;
            border-bottom: 1px solid #1a1a20;
            padding-bottom: 0.75rem;
            margin-top: 3rem;
            margin-bottom: 1.5rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            display: flex;
            align-items: center;
        }}
        .markdown-container h1::before {{
            content: "";
            display: inline-block;
            width: 4px;
            height: 28px;
            background-color: #22c55e;
            margin-right: 0.75rem;
            border-radius: 2px;
            box-shadow: 0 0 10px rgba(34, 197, 94, 0.6);
        }}
        .markdown-container h2 {{
            font-size: 1.35rem;
            font-weight: 700;
            color: #34d399;
            margin-top: 2rem;
            margin-bottom: 1rem;
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 0.03em;
            border-bottom: 1px solid #15151a;
            padding-bottom: 0.5rem;
        }}
        .markdown-container h3 {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #a7f3d0;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            font-family: 'JetBrains Mono', monospace;
        }}
        .markdown-container p {{
            margin-bottom: 1.25rem;
            line-height: 1.75;
            color: #a1a1aa;
            font-size: 0.925rem;
        }}
        .markdown-container ul {{
            list-style-type: none;
            padding-left: 1.25rem;
            margin-bottom: 1.5rem;
            color: #a1a1aa;
        }}
        .markdown-container ul li {{
            position: relative;
            margin-bottom: 0.5rem;
            padding-left: 1.25rem;
        }}
        .markdown-container ul li::before {{
            content: "▪";
            color: #22c55e;
            position: absolute;
            left: 0;
            font-size: 0.8rem;
            top: -1px;
            text-shadow: 0 0 5px rgba(34, 197, 94, 0.8);
        }}
        .markdown-container ol {{
            list-style-type: decimal;
            padding-left: 1.5rem;
            margin-bottom: 1.5rem;
            color: #a1a1aa;
        }}
        .markdown-container ol li {{
            margin-bottom: 0.5rem;
            padding-left: 0.5rem;
        }}
        .markdown-container strong {{
            color: #ffffff;
            font-weight: 600;
        }}
        .markdown-container blockquote {{
            border-left: 3px solid #22c55e;
            background: rgba(34, 197, 94, 0.02);
            padding: 1.25rem 1.5rem;
            margin: 1.75rem 0;
            border-radius: 0 16px 16px 0;
            font-style: italic;
            color: #cbd5e1;
            border-top: 1px solid rgba(34, 197, 94, 0.05);
            border-bottom: 1px solid rgba(34, 197, 94, 0.05);
            border-right: 1px solid rgba(34, 197, 94, 0.05);
        }}
        .markdown-container code {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.825em;
            background: rgba(255, 255, 255, 0.05);
            padding: 0.15rem 0.35rem;
            border-radius: 6px;
            color: #34d399;
            border: 1px solid rgba(255, 255, 255, 0.02);
        }}
        .markdown-container pre {{
            background: #040405;
            border: 1px solid #1a1a20;
            padding: 1.25rem;
            border-radius: 12px;
            overflow-x: auto;
            margin: 1.5rem 0;
        }}
        .markdown-container pre code {{
            background: transparent;
            padding: 0;
            border: none;
            color: #e4e4e7;
            font-size: 0.85rem;
        }}
        .markdown-container table {{
            width: 100%;
            border-collapse: collapse;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
        }}
        .markdown-container th {{
            background-color: #0c0c0e;
            color: #22c55e;
            border-bottom: 2px solid #1a1a20;
            padding: 0.75rem 1rem;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .markdown-container td {{
            border-bottom: 1px solid #101014;
            padding: 0.75rem 1rem;
            color: #d4d4d8;
        }}
        .markdown-container tr {{
            transition: all 0.2s ease;
            border-left: 2px solid transparent;
        }}
        .markdown-container tr:hover {{
            background-color: rgba(34, 197, 94, 0.015);
            border-left-color: #22c55e;
        }}
        .markdown-container tr:hover td {{
            color: #ffffff;
        }}
        
        @media print {{
            .no-print, #sidebar, #mobile-nav-toggle, #backdrop, header button {{
                display: none !important;
            }}
            body {{
                background-color: white !important;
                color: #0f172a !important;
                background-image: none !important;
            }}
            main {{
                padding-left: 0 !important;
                background-color: white !important;
                border: none !important;
                box-shadow: none !important;
                padding: 0 !important;
            }}
            section, div, header, footer, table, tr, td, th {{
                background-color: transparent !important;
                background-image: none !important;
                color: #0f172a !important;
                border-color: #cbd5e1 !important;
                box-shadow: none !important;
            }}
            .markdown-container h1, 
            .markdown-container h2, 
            .markdown-container h3, 
            .markdown-container h4, 
            .markdown-container h5, 
            .markdown-container h6 {{
                color: #0f172a !important;
                border-bottom: 1px solid #e2e8f0 !important;
                padding-bottom: 0.5rem !important;
                margin-top: 2rem !important;
                margin-bottom: 1rem !important;
            }}
            .markdown-container h1::before {{
                display: none !important;
            }}
            .markdown-container p, 
            .markdown-container ul, 
            .markdown-container li, 
            .markdown-container ol {{
                color: #334155 !important;
            }}
            .markdown-container strong {{
                color: black !important;
            }}
            .markdown-container blockquote {{
                border-left-color: #94a3b8 !important;
                background: #f8fafc !important;
                color: #475569 !important;
                border-top: none !important;
                border-right: none !important;
                border-bottom: none !important;
            }}
            .markdown-container code {{
                color: #047857 !important;
                background-color: #f1f5f9 !important;
                border-color: #cbd5e1 !important;
            }}
            .markdown-container pre {{
                background-color: #f8fafc !important;
                border-color: #cbd5e1 !important;
            }}
            .markdown-container pre code {{
                color: #0f172a !important;
                background-color: transparent !important;
            }}
            .markdown-container table {{
                color: black !important;
                border: 1px solid #cbd5e1 !important;
            }}
            .markdown-container th {{
                background-color: #f1f5f9 !important;
                color: #0f172a !important;
                border: 1px solid #cbd5e1 !important;
            }}
            .markdown-container td {{
                border: 1px solid #e2e8f0 !important;
                color: #334155 !important;
            }}
            .markdown-container tr:hover {{
                background-color: transparent !important;
                border-left-color: transparent !important;
            }}
            .markdown-container tr:hover td {{
                color: #334155 !important;
            }}
            .chart-card-wrap {{
                background-color: white !important;
                border: 1px solid #e2e8f0 !important;
                box-shadow: none !important;
            }}
            .chart-title-text {{
                color: #0f172a !important;
            }}
            .chart-wrapper {{
                background-color: white !important;
                border: 1px solid #cbd5e1 !important;
                filter: none !important;
            }}
            .chart-card-wrap, section, blockquote, pre, table {{
                page-break-inside: avoid;
                break-inside: avoid;
            }}
        }}
    </style>
</head>
<body class="min-h-screen cyber-grid relative">

    <!-- Breathing radial neon glow background -->
    <div class="fixed top-[15%] left-[40%] w-[600px] h-[600px] radial-glow pointer-events-none z-0"></div>
    <div class="fixed bottom-[10%] right-[-10%] w-[450px] h-[450px] radial-glow pointer-events-none z-0 opacity-40"></div>

    <!-- Backdrop for mobile sidebar drawer -->
    <div id="backdrop" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-30 opacity-0 pointer-events-none transition-opacity duration-300 lg:hidden"></div>

    <!-- Collapsible Sidebar Navigation Panel -->
    <aside id="sidebar" class="fixed top-0 left-0 h-full w-80 z-40 bg-[#070709] border-r border-[#15151a] flex flex-col justify-between transform -translate-x-full lg:transform-none lg:translate-x-0 transition-transform duration-300 ease-in-out font-sans">
        <div>
            <!-- Sidebar Header / Logo -->
            <div class="p-6 border-b border-[#121215] flex items-center space-x-3 select-none">
                <div class="relative flex items-center justify-center w-8 h-8 rounded-lg bg-[#22c55e]/10 border border-[#22c55e]/30">
                    <span class="absolute w-2.5 h-2.5 rounded-full bg-[#22c55e] animate-ping opacity-70"></span>
                    <span class="relative w-1.5 h-1.5 rounded-full bg-[#22c55e]"></span>
                </div>
                <div>
                    <span class="font-bold text-xs tracking-[0.25em] text-white font-display">NEURAL</span>
                    <span class="font-bold text-xs tracking-[0.25em] text-[#22c55e] font-display">ANALYST</span>
                </div>
            </div>

            <!-- Metadata Telemetry Stats Box -->
            <div class="p-5 border-b border-[#121215] font-mono text-[10px] space-y-3.5 text-neutral-400">
                <div class="flex items-center justify-between">
                    <span class="text-neutral-500 uppercase tracking-widest text-[9px]">Pipeline Status</span>
                    <span class="flex items-center space-x-1.5 text-[#22c55e] font-bold">
                        <span class="w-1.5 h-1.5 rounded-full bg-[#22c55e] animate-pulse shadow-[0_0_5px_rgba(34,197,94,0.6)]"></span>
                        <span>ONLINE</span>
                    </span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-neutral-500 uppercase tracking-widest text-[9px]">Matrix Data</span>
                    <span class="text-white truncate max-w-[130px] font-semibold" title="{filename}">{filename}</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-neutral-500 uppercase tracking-widest text-[9px]">Node ID</span>
                    <span class="text-white truncate max-w-[130px]" title="{job_id}">{job_id_short}</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-neutral-500 uppercase tracking-widest text-[9px]">Compiled</span>
                    <span class="text-[#34d399] font-medium">{timestamp}</span>
                </div>
            </div>

            <!-- Table of Contents Area -->
            <div class="p-6 overflow-y-auto max-h-[calc(100vh-280px)]">
                <h4 class="text-[9px] font-semibold text-neutral-500 tracking-[0.2em] uppercase mb-4 select-none">Report Matrix Index</h4>
                <nav class="space-y-1">
                    {toc_html}
                </nav>
            </div>
        </div>

        <!-- Sidebar footer status -->
        <div class="p-6 border-t border-[#121215] font-mono text-[9px] text-neutral-600 select-none">
            SYS.NODE.CONNECT // SECURE
        </div>
    </aside>

    <!-- Floating hamburger for mobile -->
    <button id="mobile-nav-toggle" class="lg:hidden fixed bottom-6 right-6 z-50 p-4 rounded-full bg-[#22c55e] hover:bg-[#39ff14] text-black shadow-[0_0_15px_rgba(34,197,94,0.4)] hover:shadow-[0_0_25px_rgba(34,197,94,0.6)] transition-all duration-300 transform active:scale-95 no-print" aria-label="Toggle Navigation Menu">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path>
        </svg>
    </button>

    <!-- Main Content Pane -->
    <main class="lg:pl-80 relative z-10 transition-all duration-300">
        <div class="max-w-5xl mx-auto px-6 py-10 md:py-16">
            
            <!-- Floating or Inline Top Navigation Bar -->
            <header class="flex items-center justify-between mb-10 pb-6 border-b border-[#15151a] relative">
                <div>
                    <h1 class="text-xl sm:text-2xl font-bold font-display tracking-widest text-white uppercase">EDA Insight Report</h1>
                    <p class="text-xs text-neutral-500 font-mono mt-1">Compiled autonomously by Neural Agent Pipeline</p>
                </div>
                
                <!-- Action Buttons (Export/Print) -->
                <div class="no-print flex items-center space-x-3">
                    <button onclick="window.print()" class="bg-[#22c55e]/10 hover:bg-[#22c55e] text-[#22c55e] hover:text-black font-semibold py-2.5 px-5 rounded-xl border border-[#22c55e]/20 hover:border-transparent shadow-[0_0_15px_rgba(34,197,94,0.05)] transition-all duration-300 hover:scale-[1.03] flex items-center space-x-2 font-mono text-[10px] tracking-wider uppercase">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <span>EXPORT PDF</span>
                    </button>
                </div>
            </header>

            <!-- Main Written Analysis Card -->
            <section class="bg-[#0c0c0e]/90 border border-[#1a1a20] rounded-2xl p-6 md:p-10 shadow-2xl relative overflow-hidden card-glow transition-all duration-300">
                <!-- Corner grid accents -->
                <div class="absolute top-0 left-0 w-4 h-4 border-t border-l border-neutral-700/50"></div>
                <div class="absolute top-0 right-0 w-4 h-4 border-t border-r border-neutral-700/50"></div>
                <div class="absolute bottom-0 left-0 w-4 h-4 border-b border-l border-neutral-700/50"></div>
                <div class="absolute bottom-0 right-0 w-4 h-4 border-b border-r border-neutral-700/50"></div>
                
                <div class="markdown-container relative z-10">
                    {processed_html}
                </div>
            </section>

            <!-- Interactive Visualizations Panel -->
            <section class="mt-16">
                <div class="border-b border-[#15151a] pb-4 mb-8 flex flex-col md:flex-row md:items-center justify-between">
                    <div>
                        <h2 class="text-lg font-bold font-display tracking-widest text-[#22c55e] uppercase">Interactive Visualizations</h2>
                        <p class="text-xs text-neutral-500 font-mono mt-1">Multi-dimensional patterns extracted dynamically</p>
                    </div>
                    <div class="mt-2 md:mt-0 font-mono text-[9px] text-[#34d399] bg-[#34d399]/5 border border-[#34d399]/20 rounded-full px-3 py-1 self-start">
                        PLOTLY DATA STREAM ACTIVE
                    </div>
                </div>

                {charts_html}
            </section>

            <!-- Footer specs -->
            <footer class="mt-20 pt-8 border-t border-[#121215] flex flex-col sm:flex-row items-center justify-between text-xs font-mono text-neutral-600">
                <div>
                    &copy; Autonomous Neural Data Analyzer Engine
                </div>
                <div class="mt-2 sm:mt-0">
                    STATUS: SECURE CONNECTED // SEC_LEVEL_3
                </div>
            </footer>
        </div>
    </main>

    <!-- ScrollReveal & Interactivity Scripts -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            // Intersection Observer for scroll animations (fade in/up)
            const revealObserver = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.classList.remove('opacity-0', 'translate-y-8');
                        entry.target.classList.add('opacity-100', 'translate-y-0');
                        revealObserver.unobserve(entry.target);
                    }}
                }});
            }}, {{ threshold: 0.05, rootMargin: '0px 0px -50px 0px' }});

            // Select headings, paragraphs, lists, tables, and charts to animate on scroll
            const targets = document.querySelectorAll(
                '.markdown-container > p, .markdown-container > h1, .markdown-container > h2, .markdown-container > h3, .markdown-container > table, .markdown-container > ul, .markdown-container > ol, .markdown-container > blockquote, .chart-card-wrap'
            );
            targets.forEach(target => {{
                target.classList.add('opacity-0', 'translate-y-8', 'transition-all', 'duration-700', 'ease-out');
                revealObserver.observe(target);
            }});

            // Intersection Observer for ScrollSpy (TOC highlighting)
            const spyObserver = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        const id = entry.target.getAttribute('id');
                        if (!id) return;
                        
                        document.querySelectorAll('.toc-item').forEach(item => {{
                            item.classList.remove('text-[#22c55e]', 'border-[#22c55e]/50', 'bg-[#22c55e]/5', 'pl-4');
                            item.classList.add('text-neutral-400');
                        }});
                        
                        const activeItem = document.querySelector(`.toc-item[href="#${{id}}"]`);
                        if (activeItem) {{
                            activeItem.classList.add('text-[#22c55e]', 'border-[#22c55e]/50', 'bg-[#22c55e]/5', 'pl-4');
                            activeItem.classList.remove('text-neutral-400');
                        }}
                    }}
                }});
            }}, {{ rootMargin: '-10% 0px -75% 0px' }});

            document.querySelectorAll('h1[id], h2[id], h3[id]').forEach(h => spyObserver.observe(h));

            // Mobile Nav Panel Toggle controls
            const toggleBtn = document.getElementById('mobile-nav-toggle');
            const sidebar = document.getElementById('sidebar');
            const backdrop = document.getElementById('backdrop');
            
            function toggleMobileNav() {{
                const isOpen = sidebar.classList.contains('translate-x-0');
                if (isOpen) {{
                    sidebar.classList.remove('translate-x-0');
                    sidebar.classList.add('-translate-x-full');
                    backdrop.classList.remove('opacity-100');
                    backdrop.classList.add('opacity-0', 'pointer-events-none');
                }} else {{
                    sidebar.classList.remove('-translate-x-full');
                    sidebar.classList.add('translate-x-0');
                    backdrop.classList.remove('opacity-0', 'pointer-events-none');
                    backdrop.classList.add('opacity-100');
                }}
            }}
            
            if (toggleBtn && sidebar && backdrop) {{
                toggleBtn.addEventListener('click', toggleMobileNav);
                backdrop.addEventListener('click', toggleMobileNav);
                
                // Close when a TOC link is clicked on mobile
                document.querySelectorAll('.toc-item').forEach(link => {{
                    link.addEventListener('click', () => {{
                        if (window.innerWidth < 1024) {{
                            toggleMobileNav();
                        }}
                    }});
                }});
            }}
        }});
    </script>
</body>
</html>
    """
    return full_html
