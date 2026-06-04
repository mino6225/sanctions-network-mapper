
# Sanctions Network Mapper

A Python tool that maps hidden connections between OFAC-sanctioned entities by 
analyzing shared physical addresses across the U.S. Treasury SDN list. Builds 
an interactive network graph to identify sanctions evasion clusters, shell company 
networks, and high-connectivity hub entities.

Built from scratch as part of an independent technical development program in 
cross-border risk intelligence and Eurasian political economy.

## What It Does
- Loads and processes three OFAC SDN datasets: primary entities, alternate names, 
  and addresses (38,000+ records across 19,015 sanctioned entities)
- Cleans placeholder values and filters to 13,952 real addresses
- Builds a network graph where nodes are sanctioned entities and edges represent 
  shared physical addresses
- Identifies 8,838 address-sharing connections across the sanctions universe
- Ranks entities by network degree (number of connections) to surface hub nodes
- Detects clusters of interconnected sanctioned entities using connected components analysis
- Generates an interactive HTML network visualization of the largest cluster
- Exports top connected nodes to CSV

## Key Findings

**Most connected entity:** MONSOON SHIPPING LTD — 113 connections to other 
sanctioned entities via shared addresses, consistent with Iranian oil sanctions 
evasion infrastructure.

**Five distinct sanctions evasion networks identified:**

| Cluster | Size | Description |
|---|---|---|
| Dark Fleet Shipping Network | 147 entities | Iranian oil sanctions evasion — shell shipping companies sharing offshore registered addresses |
| Belize Shell Factory | 30 entities | Sequential entity IDs, same address — bulk shell company creation pattern |
| OZEAN GROUP (Germany) | 21 entities | Russian real estate money laundering through European GmbH structures |
| China/Offshore Shipping | 18 entities | North Korea-linked sanctions evasion via Pacific maritime network |
| Iranian Shipping Network | 17 entities | IRISL subsidiary structure — Persian-named entities with sequential IDs |

## Tech Stack
Python 3.14 · NetworkX · PyVis · pandas · os

## Data Sources
- OFAC Specially Designated Nationals (SDN) List — U.S. Treasury (public)
- OFAC Alternate Names (ALT) List — U.S. Treasury (public)
- OFAC Addresses (ADD) List — U.S. Treasury (public)

## Output Files
- `sanctions_subgraph.html` — interactive network visualization (open in browser)
- `top_sanctions_nodes.csv` — top 10 most connected sanctioned entities by degree

## How to Run
1. Download SDN.CSV, ALT.CSV, ADD.CSV from ofac.treas.gov
2. Place in the project folder
3. Update the `folder` path in the script
4. Run: `python3 sanctions_network_mapper.py`

## Author
Mia Noll-Jones — International Affairs & Eurasian Risk Intelligence
github.com/mino6225 | Relocating to Washington D.C., July 2026
