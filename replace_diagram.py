import re

with open('/home/gaspar/IC/spark-ml-big-data/index.html', 'r') as f:
    content = f.read()

# 1. Remove the Mermaid <script> completely
mermaid_script = r"""    <!-- Mermaid.js para Diagramas via CND classico -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            mermaid.initialize({ 
                startOnLoad: false, 
                theme: 'dark',
                flowchart: { htmlLabels: true, curve: 'basis' }
            });
        });
    </script>"""
content = content.replace(mermaid_script, "")

# Remove the run logic in JS
nav_func_mermaid = r"""                // Force mermaid to render if not already rendered
                const activeMermaid = slides[currentSlide].querySelector('.mermaid:not([data-processed="true"])');
                if (activeMermaid) {
                    try {
                        await mermaid.run({ querySelector: '.active .mermaid' });
                    } catch (e) {
                        console.error('Mermaid render error:', e);
                    }
                }"""
content = content.replace(nav_func_mermaid, "")
content = content.replace("async function goToSlide", "function goToSlide")

# 2. Replace the <div class="mermaid"> with pure HTML/CSS diagram
html_diagram = r"""<div style="width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; position: relative;">
                        <!-- Custom CSS -->
                        <style>
                            .arch-box {
                                border: 2px dashed #58a6ff;
                                border-radius: 12px;
                                padding: 30px 20px 20px 20px;
                                background: rgba(88, 166, 255, 0.05);
                                position: relative;
                                width: 100%;
                            }
                            .arch-title {
                                position: absolute;
                                top: -14px;
                                left: 20px;
                                background: var(--bg-main);
                                color: var(--text-main);
                                padding: 0 10px;
                                font-weight: bold;
                                font-size: 16px;
                                font-family: 'JetBrains Mono', monospace;
                            }
                            .node-item {
                                border-radius: 8px;
                                padding: 15px;
                                text-align: center;
                                font-size: 14px;
                                display: flex;
                                flex-direction: column;
                                gap: 8px;
                                align-items: center;
                                justify-content: center;
                                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
                                z-index: 2;
                            }
                            .node-master {
                                background: #f85149;
                                color: #fff;
                                font-weight: 700;
                                width: 200px;
                                margin: 0 auto;
                            }
                            .node-worker {
                                background: #58a6ff;
                                color: #000;
                                font-weight: 700;
                            }
                            .node-storage {
                                background: #3fb950;
                                color: #000;
                                font-weight: 700;
                                width: 100%;
                                margin-top: 20px;
                            }
                            .worker-grid {
                                display: grid;
                                grid-template-columns: repeat(4, 1fr);
                                gap: 15px;
                                margin-top: 40px;
                                position: relative;
                            }
                            /* Connector lines via SVG */
                            .connectors {
                                position: absolute;
                                top: 0; left: 0; width: 100%; height: 100%;
                                pointer-events: none;
                                z-index: 1;
                            }
                        </style>

                        <div class="arch-box">
                            <div class="arch-title">Cluster Spark (64 Cores / 512GB RAM)</div>
                            
                            <!-- Master Node -->
                            <div class="node-item node-master">
                                <i class="fa-solid fa-brain" style="font-size: 24px;"></i>
                                YARN (Master)
                            </div>

                            <!-- Lines from Master to Workers -->
                            <svg class="connectors">
                                <!-- Draw arrows down from Master to Workers (approximated visually) -->
                                <path d="M 50% 70 Q 50% 100, 15% 120" fill="none" stroke="#f85149" stroke-width="2" stroke-dasharray="4"/>
                                <path d="M 50% 70 Q 50% 100, 38% 120" fill="none" stroke="#f85149" stroke-width="2" stroke-dasharray="4"/>
                                <path d="M 50% 70 Q 50% 100, 62% 120" fill="none" stroke="#f85149" stroke-width="2" stroke-dasharray="4"/>
                                <path d="M 50% 70 Q 50% 100, 85% 120" fill="none" stroke="#f85149" stroke-width="2" stroke-dasharray="4"/>
                                
                                <!-- Draw arrows from Workers to HDFS -->
                                <path d="M 15% 210 L 15% 240" fill="none" stroke="#58a6ff" stroke-width="2"/>
                                <path d="M 38% 210 L 38% 240" fill="none" stroke="#58a6ff" stroke-width="2"/>
                                <path d="M 62% 210 L 62% 240" fill="none" stroke="#58a6ff" stroke-width="2"/>
                                <path d="M 85% 210 L 85% 240" fill="none" stroke="#58a6ff" stroke-width="2"/>
                            </svg>

                            <!-- Workers Grid -->
                            <div class="worker-grid">
                                <div class="node-item node-worker">
                                    <i class="fa-solid fa-server" style="font-size: 20px;"></i>
                                    Node 1<br>(8 Cores / 64GB)
                                </div>
                                <div class="node-item node-worker">
                                    <i class="fa-solid fa-server" style="font-size: 20px;"></i>
                                    Node 2<br>(8 Cores / 64GB)
                                </div>
                                <div class="node-item node-worker" style="background: transparent; border: 2px dashed #58a6ff; color: var(--text-main); box-shadow: none;">
                                    <i class="fa-solid fa-ellipsis" style="font-size: 20px;"></i>
                                    Nodes 3-7
                                </div>
                                <div class="node-item node-worker">
                                    <i class="fa-solid fa-server" style="font-size: 20px;"></i>
                                    Node 8<br>(8 Cores / 64GB)
                                </div>
                            </div>

                            <!-- Storage -->
                            <div class="node-item node-storage">
                                <i class="fa-solid fa-database" style="font-size: 24px;"></i>
                                HDFS Storage (Armazenamento Distribuído)
                            </div>
                        </div>
                    </div>"""

# Find the div to replace
mermaid_div_pattern = re.compile(r'<div class="mermaid" style="width: 100%;">.*?</div>', re.DOTALL)
content = mermaid_div_pattern.sub(html_diagram, content)

with open('/home/gaspar/IC/spark-ml-big-data/index.html', 'w') as f:
    f.write(content)

print("Diagram replaced with pure HTML/CSS structure.")
