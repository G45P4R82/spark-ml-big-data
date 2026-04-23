import urllib.request
import json

diagram = """
flowchart TD
    classDef master fill:#f85149,stroke:#30363d,stroke-width:2px,color:#fff,rx:8px,ry:8px
    classDef worker fill:#58a6ff,stroke:#30363d,stroke-width:2px,color:#000,rx:8px,ry:8px,font-weight:bold
    classDef storage fill:#3fb950,stroke:#30363d,stroke-width:2px,color:#000,rx:8px,ry:8px,font-weight:bold
    classDef cluster fill:#161b22,stroke:#58a6ff,stroke-width:2px,stroke-dasharray: 5 5,color:#e6edf3

    subgraph Cluster ["Cluster Spark (64 Cores / 512GB RAM)"]
        direction TD
        M["YARN (Master)"]:::master
        
        W1["Node 1<br/>(8 Cores, 64GB)"]:::worker
        W2["Node 2<br/>(8 Cores, 64GB)"]:::worker
        W3["Nodes 3-7"]:::worker
        W8["Node 8<br/>(8 Cores, 64GB)"]:::worker
        
        HDFS[("HDFS Storage<br/>(Armazenamento)")]:::storage

        M ==> W1
        M ==> W2
        M ==> W3
        M ==> W8

        W1 -.-> HDFS
        W2 -.-> HDFS
        W3 -.-> HDFS
        W8 -.-> HDFS
    end
    class Cluster cluster
"""

url = "https://kroki.io/mermaid/svg"
data = json.dumps({"diagram_source": diagram}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla'})
try:
    with urllib.request.urlopen(req) as response:
        with open('cluster.svg', 'w') as f:
            f.write(response.read().decode('utf-8'))
    print("SVG gerado")
except Exception as e:
    print(e.read().decode())
