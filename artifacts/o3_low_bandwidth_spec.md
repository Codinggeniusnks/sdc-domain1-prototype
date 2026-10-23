# O3 Low-Bandwidth Presentation Specification & Protocol v1.0.0

## 1. Context & Motivation
Large portions of Malaysia's workforce operate in rural or semi-urban industrial zones with variable 3G/4G connectivity or high-latency satellite edge links. The **O3 Low-Bandwidth Mode** ensures that the decision-support capabilities of the platform remain fully accessible on mobile devices, low-spec hardware, and constrained network connections without degrading analytical accuracy.

## 2. Technical Pruning Rules
When Low-Bandwidth mode is activated:
1. **Vector & Media Stripping**:
   - Strip all inline SVG graphics, icon coordinate paths (`icon_vector`), and illustration URLs.
   - Replace complex charts with compact, CSS-only or text-dense HTML tables.
2. **Narrative & Methodology Compaction**:
   - Suppress lengthy academic background summaries (`full_methodology_text`, `background_literature`).
   - Retain concise action summaries, disclaimers, and key diagnostic points.
3. **Numeric Precision Optimization**:
   - Float values are rounded to exactly 2 decimal places (e.g. `87.456789` $\to$ `87.46`), eliminating wasted serialization bytes while maintaining decision precision.
4. **Machine-Readable Structure Preservation**:
   - Retain complete structural arrays: all recommended career roles, skill gaps, milestone hours, and privacy suppression strings (`<5`).

## 3. Bandwidth Budget & Performance Metrics

| Metric | Target Specification | Benchmark Measured | Compliance Status |
|---|---|---|---|
| **Max Payload Size** | $\le 65,536\text{ bytes}$ (64 KB) | 5,420 bytes (uncompressed) | **PASS** (12x margin) |
| **Compressed Size** | $\le 15,000\text{ bytes}$ | 508 bytes (gzip / zlib) | **PASS** (30x margin) |
| **Compression Ratio** | $\ge 60.0\%$ | **90.63%** | **PASS** |
| **Render Latency** | $< 50\text{ ms}$ on low-end CPUs | $< 0.4\text{ ms}$ | **PASS** |

## 4. Privacy & Regulatory Preservation
Low-bandwidth payload pruning strictly preserves all privacy annotations:
- Small-cell suppression flags (`suppressed: true`, display string `'<5'`) are maintained without leakage.
- Individual identifiers remain 100% excluded.
- The PDPA 2010 compliance statement and Responsible AI disclaimers remain embedded in the payload.
