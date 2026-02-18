# Hands-On MicroStrategy Training

A progressive, lab-based training course for building interactive dashboards and analytics dossiers in **MicroStrategy Workstation**. Each lab introduces new concepts while reinforcing skills from previous exercises, taking you from your first visualization to multi-chapter audit dashboards.

## Prerequisites

- **MicroStrategy Workstation** installed locally (desktop application) or access via the MicroStrategy web interface
- No prior MicroStrategy experience required — Lab 1 starts from scratch
- Basic familiarity with spreadsheet data (rows, columns, data types) is helpful

## Course Outline

### Lab 1 — Building Your First Analytics Dossier

| | |
|---|---|
| **Domain** | Barcelona Airbnb market analysis |
| **Dataset** | `Barcelona Airbnb Data.xlsx` (single file) |
| **What You Build** | A single-page dossier with map visualizations, charts, and KPIs |

**Skills introduced:** MicroStrategy Workstation setup, importing data from disk, classifying attributes and metrics, building map visualizations (latitude/longitude), KPI cards, bar charts, filtering, and basic formatting.

---

### Lab 2 — Gold Historical Data Analysis

| | |
|---|---|
| **Domain** | Gold price performance |
| **Dataset** | `gold_historical_data.csv` (single file) |
| **What You Build** | A self-directed performance dashboard |

**Skills introduced:** Working with time-series data, line charts, self-directed dashboard design. This lab is intentionally less prescriptive — you apply what you learned in Lab 1 with minimal hand-holding.

---

### Lab 3 — Multi-Dataset Pizza Analytics Dashboard

| | |
|---|---|
| **Domain** | Pizza restaurant operations |
| **Datasets** | `pizzas.csv`, `pizza_types.csv`, `orders.csv`, `order_details.csv` |
| **What You Build** | A comprehensive analytics dashboard combining four related datasets |

**Skills introduced:** Importing multiple datasets, data wrangling (duplicate columns, find-and-replace), multi-form attributes, dataset linking via shared keys, derived metrics with the Formula Editor, ranking, and filtering.

---

### Lab 4 — Internal Audit Exception Dashboard

| | |
|---|---|
| **Domain** | Internal audit — procurement, HR/payroll, and payment exceptions |
| **Datasets** | `procurement_audit.csv`, `hr_employees.csv`, `hr_payroll.csv`, `payment_transactions.csv` |
| **What You Build** | A 3-chapter dossier surfacing audit red flags with color-coded grids |

**Skills introduced:** Multi-chapter dossier design, conditional formatting on grids (color-coding rows by severity), text visualizations, visualization-level filters, derived attributes (bucketing numeric fields), conditional derived metrics with `If()`.

---

### Lab 5 — Expense & Travel Compliance Dashboard

| | |
|---|---|
| **Domain** | Expense reports, corporate card monitoring, and travel compliance |
| **Datasets** | `expense_reports.csv`, `corporate_card.csv`, `travel_bookings.csv` |
| **What You Build** | A 3-chapter compliance dashboard identifying policy violations and fraud risks |

**Skills introduced:** Multi-level conditional formatting (red/orange/yellow), OR-condition visualization filters, dataset linking across chapters, derived metrics with arithmetic (`(Claimed - Standard) * Nights`), derived attributes with `Case()` for rate variance bucketing.

---

## Repository Structure

```
Lab 1/
  Lab 1 Instructions.MD        # Step-by-step walkthrough
  Lab 1 Instructions.pdf        # PDF version
  Barcelona Airbnb Data.xlsx    # Dataset
  Airbnb Dashboard.mstr         # Completed dossier (MicroStrategy export)
  images/                       # Screenshots referenced by instructions

Lab 2/
  README.md                     # Brief instructions
  gold_historical_data.csv      # Dataset

Lab 3/
  Lab3 instructions.md          # Step-by-step walkthrough
  datasets/                     # 4 CSV files
  images/                       # Screenshots

Lab 4/
  Lab4 Instructions.md          # Step-by-step walkthrough
  Lab4 Instructions.pdf         # PDF version
  Data Dictionary.md            # Column-level documentation for all datasets
  Internal Audit Reports.mstr   # Completed dossier (MicroStrategy export)
  datasets/                     # 4 CSV files
  images/                       # Screenshots

Lab 5/
  Lab5 Instructions.md          # Step-by-step walkthrough
  Data Dictionary.md            # Column-level documentation for all datasets
  datasets/                     # 3 CSV files
```

## How to Use This Course

1. **Work through the labs in order.** Each lab builds on skills from the previous one. Lab 1 covers setup and fundamentals; Lab 5 assumes comfort with everything before it.

2. **Follow the instructions alongside MicroStrategy Workstation.** Open the Markdown (or PDF) instructions and work through each numbered step. The instructions include exact field names, formula syntax, and formatting details.

3. **Datasets are ready to use.** All CSV and Excel files can be imported directly into MicroStrategy — no data preparation is needed outside the tool.

4. **`.mstr` files are reference solutions.** Where provided, these are exported MicroStrategy dossiers showing the completed dashboard. You can import them to see the finished product, but the learning value comes from building it yourself.

## Skills Progression

| Skill | Lab 1 | Lab 2 | Lab 3 | Lab 4 | Lab 5 |
|-------|:-----:|:-----:|:-----:|:-----:|:-----:|
| Import data from disk | x | x | x | x | x |
| Classify attributes & metrics | x | x | x | x | x |
| KPI cards | x | | x | x | x |
| Bar & horizontal bar charts | x | | x | x | x |
| Map visualizations | x | | | | |
| Line charts | | x | x | x | |
| Multiple datasets | | | x | x | x |
| Dataset linking | | | x | x | x |
| Data wrangling | | | x | | |
| Multi-form attributes | | | x | | |
| Derived metrics (`If()`) | | | x | x | x |
| Multi-chapter dossiers | | | | x | x |
| Conditional formatting | | | | x | x |
| Text visualizations | | | | x | x |
| Visualization-level filters | | | | x | x |
| Derived attributes (`Case()`) | | | | x | x |
