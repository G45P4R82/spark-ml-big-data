import re

with open('/home/gaspar/IC/spark-ml-big-data/index.html', 'r') as f:
    content = f.read()

# Replace the module script
old_script = r"""    <!-- Mermaid.js para Diagramas -->
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ 
            startOnLoad: true, 
            theme: 'dark',
            flowchart: { htmlLabels: true, curve: 'basis' }
        });
    </script>"""

new_script = r"""    <!-- Mermaid.js para Diagramas via CND classico -->
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

content = content.replace(old_script, new_script)

# Add dynamic rendering in goToSlide
nav_func_old = r"""            function goToSlide(index) {
                slides[currentSlide].classList.remove('active');
                currentSlide = index;
                slides[currentSlide].classList.add('active');
                
                // Força os gráficos a renderizarem corretamente se o slide os contiver
                window.dispatchEvent(new Event('resize')); 
            }"""

nav_func_new = r"""            async function goToSlide(index) {
                slides[currentSlide].classList.remove('active');
                currentSlide = index;
                slides[currentSlide].classList.add('active');
                
                // Force mermaid to render if not already rendered
                const activeMermaid = slides[currentSlide].querySelector('.mermaid:not([data-processed="true"])');
                if (activeMermaid) {
                    try {
                        await mermaid.run({ querySelector: '.active .mermaid' });
                    } catch (e) {
                        console.error('Mermaid render error:', e);
                    }
                }

                // Força os gráficos a renderizarem corretamente se o slide os contiver
                window.dispatchEvent(new Event('resize')); 
            }"""

content = content.replace(nav_func_old, nav_func_new)

with open('/home/gaspar/IC/spark-ml-big-data/index.html', 'w') as f:
    f.write(content)

print("HTML patched for dynamic Mermaid rendering.")
