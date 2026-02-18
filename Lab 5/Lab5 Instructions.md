# Lab 5: Building an Expense & Travel Compliance Dashboard in MicroStrategy

## 1. Introduction and Lab Objectives

In Lab 4, you built a multi-chapter Internal Audit Exception Dashboard covering procurement, HR/payroll, and payment risks. You learned to use conditional formatting, text visualizations, visualization-level filters, and derived attributes and metrics.

In this lab, you will apply those same techniques to a different audit domain — **Expense & Travel Compliance**. You will build a 3-chapter Dossier that surfaces red flags in employee expense reports, corporate card transactions, and travel bookings.

This lab reinforces the following skills:

- **Multi-chapter Dossier design** — organizing expense, card, and travel analyses into separate chapters
- **Conditional formatting on Grids** — color-coding rows based on exception severity
- **Visualization-level filters** — isolating flagged records within individual visualizations
- **Derived metrics with `If()`** — counting and summing only records that meet specific conditions
- **Derived attributes** — creating bucketed categories from numeric fields
- **Dataset linking** — connecting corporate card transactions to expense reports via `Employee_ID`

By the end of this lab, you will have a 3-chapter compliance dashboard that an audit team could use to monitor expense policy violations, corporate card misuse, and travel booking exceptions.

## 2. Understanding the Datasets

This lab uses three CSV files representing expense and travel data from a fictional organization.

| File | Rows | Description | Key Fields |
|------|------|-------------|------------|
| `expense_reports.csv` | 80 | Expense reports with approval workflow and policy flags | `Report_ID`, `Employee_Name`, `Expense_Type`, `Amount_USD`, `Is_Split_Transaction`, `Is_Missing_Receipt`, `Is_Weekend_Submission` |
| `corporate_card.csv` | 100 | Corporate card transactions with misuse flags | `Transaction_ID`, `Employee_ID`, `Merchant_Name`, `Amount_USD`, `Is_Personal_Use`, `Is_Duplicate_Charge`, `Is_High_Value_No_Receipt` |
| `travel_bookings.csv` | 60 | Travel bookings with per diem and hotel rate compliance | `Booking_ID`, `Employee_ID`, `Destination`, `Hotel_Rate_Per_Night`, `Policy_Rate_Per_Night`, `Per_Diem_Claimed`, `Standard_Per_Diem`, `Is_Out_Of_Policy`, `Is_Excessive_Per_Diem`, `Is_Duplicate_Claim` |

Each dataset has **embedded red flags** — anomalous records that an internal auditor would want to investigate. Your dashboard will surface these exceptions through KPIs, grids, and charts.

The `corporate_card.csv` dataset shares `Employee_ID` with `expense_reports.csv`, allowing you to link card transactions to the employees who submitted expense reports.

---

## 3. Chapter 1: Expense Report Compliance

### Why This Matters

Expense reports are one of the most common areas for policy violations and fraud in any organization. Employees submit claims for business expenses, and without proper controls, several types of abuse can occur:

1. **Split transactions — are employees circumventing approval thresholds?** Many organizations require additional approval for expenses above a certain amount (e.g., $500). To avoid this scrutiny, employees may split a single expense into two or more smaller claims submitted on consecutive days. Our data contains 8 split transaction pairs (16 flagged records) — cases where the same employee submitted the same expense type on consecutive days with amounts just below the threshold. Each pair should be investigated to determine if a single expense was deliberately broken up.

2. **Missing receipts — where is the documentation?** Receipts are a fundamental internal control. When receipts are missing, the organization cannot verify that the claimed expense actually occurred, or that the amount is accurate. Our data flags 10 expense reports with no receipt attached — each one represents an unverified claim that could be inflated, personal, or entirely fictitious.

3. **Weekend submissions — who is filing expenses outside business hours?** While not inherently fraudulent, expense reports submitted on weekends can indicate that someone is filing claims outside normal oversight, potentially to avoid real-time review by their manager. Our data contains 6 weekend submissions that warrant a closer look at the timing and nature of these claims.

**How to use this dashboard going forward:** This dashboard should be reviewed **bi-weekly** by the audit team. The split transaction KPI is a key indicator — if the count is rising, it may signal that employees have learned the approval threshold and are actively gaming it. The missing receipt percentage should trend toward zero over time as controls improve. The weekend submission count provides context but should be investigated in conjunction with the amounts and expense types involved.

### Importing `expense_reports.csv`

1. Create a **New Dossier** in MicroStrategy. In the Dataset panel, click **New Data** and select **File from Disk**.

2. Choose the `expense_reports.csv` file and click **Prepare Data** (not Finish).

### Classifying Attributes and Metrics

3. In the Data Editor, verify that MicroStrategy has correctly classified your columns. You will need to make the following adjustments:

   - **Convert to Metric** (right-click > Convert to Metric):
     - `Amount_USD`

   - **Verify as Attribute** (these should already be attributes):
     - `Report_ID`, `Employee_ID`, `Employee_Name`, `Department`, `Location`
     - `Submission_Date`, `Approval_Date`, `Approver_Name`
     - `Expense_Type`, `Receipt_Attached`
     - `Is_Split_Transaction`, `Is_Missing_Receipt`, `Is_Weekend_Submission`

4. Click **Finish** to complete the import.

### Renaming the Chapter

5. At the bottom of the Dossier, you will see a tab labeled **Page 1**. Double-click the tab name and rename it to **Expense Report Compliance**.

### Adding a Text Visualization

6. From the visualization gallery, add a **Text** visualization at the top of the page. Type the following description:

   > **Expense Report Compliance Dashboard**
   >
   > This chapter highlights expense report exceptions including split transactions that circumvent approval thresholds, missing receipt violations, and weekend submissions that may bypass oversight.

   Format the text with bold for the title. This provides context for anyone viewing the dashboard.

### KPI 1: Total Reports

7. Add a **KPI** visualization. Drag `Row Count - expense_reports.csv` into it. Rename this metric to `Total Reports`.

### KPI 2: Split Transaction Count

8. We need to create a derived metric that counts only the expense reports flagged as split transactions. Open the **Formula Editor** (click the **+** next to Metrics) and create a new metric with the formula:

   ```
   Sum(IF(([Is Split Transaction]@ID="Y"), 1, 0)){~+}
   ```

   Name this metric `Split Transaction Count`. Validate and save.

9. Add a second **KPI** visualization and drag `Split Transaction Count` into it.

### KPI 3: Missing Receipt Percentage

10. Create another derived metric. In the Formula Editor, enter:

    ```
    Sum(IF(([Is Missing Receipt]@ID="Y"), 1, 0)){~+}/Count([Report ID]){~+}
    ```

    Name this metric `Missing Receipt Pct`. Validate and save.

11. Add a third **KPI** visualization and drag `Missing Receipt Pct` into it. Format the number to show one decimal place and add a `%` suffix if desired.

12. Arrange the three KPI cards in a row at the top of the page (below the text visualization).

### Grid: Expense Report Details

13. Add a **Grid** visualization below the KPI cards. Drag the following fields into the grid:
    - `Report_ID`
    - `Employee_Name`
    - `Department`
    - `Submission_Date`
    - `Expense_Type`
    - `Amount_USD`
    - `Receipt_Attached`
    - `Is_Split_Transaction`
    - `Is_Missing_Receipt`

14. Name this visualization `Expense Report Details`.

### Conditional Formatting: Split Transactions (Red)

15. Select the Grid visualization. Right-click the `Is_Split_Transaction` column and select **Thresholds**.

16. Click **New Threshold** and configure:
    - **Based on:** `Is_Split_Transaction`
    - **Condition:** Equals `Y`
    - **Formatting:** Set the **background color** to **Red** and the **font color** to **White**

17. Click **Apply**. Rows where the expense report is flagged as a split transaction will now be highlighted in red.

### Conditional Formatting: Missing Receipts (Orange)

18. Add a second conditional formatting rule:
    - Right-click the `Is_Missing_Receipt` column and select **Thresholds**
    - Click **New Threshold**
    - **Based on:** `Is_Missing_Receipt`
    - **Condition:** Equals `Y`
    - **Formatting:** Set the **background color** to **Orange**

19. Click **Apply**. Rows with missing receipts will now be highlighted in orange, while split transactions remain in red.

### Horizontal Bar Chart: Reports by Expense Type

20. Add a **Horizontal Bar Chart** visualization. Drag `Expense Type` to the vertical axis and `Total Reports` (Row Count) to the horizontal axis.

21. Name this visualization `Reports by Expense Type`. This chart shows which expense categories have the most submissions.

### Bar Chart: Top Submitters by Amount

22. Add a **Bar Chart** visualization. Drag `Employee_Name` to the horizontal axis and `Amount_USD` to the vertical axis.

23. Sort descending by `Amount_USD` to see which employees submit the highest total expense amounts. Name this visualization `Top Submitters by Amount`.

24. Your completed Expense Report Compliance chapter should include KPIs at top, the conditional-formatted grid in the middle, and two charts at the bottom.

---

## 4. Chapter 2: Corporate Card Monitoring

### Why This Matters

Corporate cards give employees direct spending authority, which creates unique risks that differ from the traditional expense report process. Unlike expense reports — where employees request reimbursement after the fact — corporate cards allow spending first and questions later. This makes monitoring essential.

This dashboard targets three specific risks:

1. **Personal use — is someone using a company card for personal expenses?** Corporate card policies universally prohibit personal purchases, yet it remains one of the most common policy violations. Our data flags 7 transactions at merchants typically associated with personal spending (streaming services, personal shopping). Each flagged transaction requires the cardholder to provide a business justification or repay the organization.

2. **Duplicate charges — are we being billed twice for the same transaction?** Duplicate charges can result from merchant processing errors, but they can also be a sign of intentional fraud — submitting the same charge twice and pocketing the second reimbursement. Our data contains 4 duplicate charge pairs (8 flagged records) where the same employee, merchant, and amount appear on the same date. Each pair should be investigated to determine if it was a legitimate error or intentional double-billing.

3. **High-value transactions without receipts — where is the documentation?** When high-value card transactions lack receipts, the organization cannot verify that the goods or services were actually received, or that the amount is accurate. Our data flags 6 transactions over the policy threshold that have no receipt attached. These represent the highest financial exposure and should be prioritized for follow-up.

**How to use this dashboard going forward:** This dashboard should be reviewed **monthly**, ideally within the first week after the card billing cycle closes. The personal use count should be a zero-tolerance metric — any non-zero value triggers immediate cardholder notification. The duplicate charge pairs should be reconciled with the card issuer. The unreceipted high-value transactions should be escalated to department managers for documentation or repayment.

### Adding a New Chapter

1. At the bottom of the Dossier, click the **+** icon (or right-click the existing chapter tab) to add a new chapter. Name it **Corporate Card Monitoring**.

### Importing `corporate_card.csv`

2. In the Dataset panel, click **New Data** and import the `corporate_card.csv` file. Click **Prepare Data**.

3. In the Data Editor, verify the column classifications:

   - **Convert to Metric** (right-click > Convert to Metric):
     - `Amount_USD`

   - **Verify as Attribute** (these should already be attributes):
     - `Transaction_ID`, `Employee_ID`, `Employee_Name`, `Department`
     - `Transaction_Date`, `Merchant_Name`, `Merchant_Category`
     - `Receipt_Provided`
     - `Is_Personal_Use`, `Is_Duplicate_Charge`, `Is_High_Value_No_Receipt`

4. Click **Finish** to complete the import.

### Linking Datasets by Employee_ID

5. In the Dataset panel, right-click `Employee_ID` (under `expense_reports.csv`) and select **Link to Other Dataset...**

6. Link it to `Employee_ID` in `corporate_card.csv`. Click **Show Attribute Forms** to verify the mapping shows `Employee_ID (ID)` linked to `Employee_ID (ID)`. Click **OK**.

7. You should now see link icons next to the `Employee_ID` fields in both datasets, confirming the datasets are connected.

### KPI 1: Total Transactions

8. Rename `Row Count - corporate_card.csv` to `Total Transactions`. Add it as a **KPI** visualization.

### KPI 2: Personal Use Count

9. Create a derived metric with the formula:

   ```
   Sum(IF(([Is Personal Use]@ID="Y"), 1, 0)){~+}
   ```

   Name it `Personal Use Count`. Add it as a **KPI** visualization.

### KPI 3: Duplicate Charge Count

10. Create a derived metric:

    ```
    Sum(IF(([Is Duplicate Charge]@ID="Y"), 1, 0)){~+}
    ```

    Name it `Duplicate Charge Count`. Add it as a **KPI** visualization.

### KPI 4: Total Unreceipted Amount

11. Create a derived metric:

    ```
    Sum(IF(([Is High Value No Receipt]@ID="Y"), [Amount USD], 0)){~+}
    ```

    Name it `Total Unreceipted Amount`. Add it as a **KPI** visualization. Format as currency.

12. Arrange the four KPI cards in a row at the top of the chapter.

### Grid: Flagged Transactions

13. Add a **Grid** visualization with the following fields:
    - `Transaction_ID`
    - `Employee_Name`
    - `Department`
    - `Transaction_Date`
    - `Merchant_Name`
    - `Merchant_Category`
    - `Amount_USD`
    - `Receipt_Provided`
    - `Is_Personal_Use`
    - `Is_Duplicate_Charge`
    - `Is_High_Value_No_Receipt`

14. Name this visualization `Flagged Card Transactions`.

### Applying a Visualization-Level Filter

15. We only want to show flagged transactions in this grid. Click on the Grid, then click the three dots on the top right corner and select **Edit Filter**.

16. Add filter qualifications to show only records where `Is_Personal_Use = Y` **OR** `Is_Duplicate_Charge = Y` **OR** `Is_High_Value_No_Receipt = Y`.

    > **Tip:** You may create a derived attribute: `Has_Any_Flag = If(Is_Personal_Use = "Y" OR Is_Duplicate_Charge = "Y" OR Is_High_Value_No_Receipt = "Y", "Y", "N")` and filter on `Has_Any_Flag = Y`.

### Conditional Formatting on Flagged Transactions Grid

17. Add conditional formatting rules to this grid:
    - **Rule 1:** Where `Is_Personal_Use = Y` → Background color **Red**, font color **White**
    - **Rule 2:** Where `Is_Duplicate_Charge = Y` → Background color **Orange**
    - **Rule 3:** Where `Is_High_Value_No_Receipt = Y` → Background color **Yellow**

18. Click **Apply**. Each type of exception will now have a distinct color in the grid.

### Bar Chart: Spend by Merchant Category

19. Add a **Bar Chart** visualization. Drag `Merchant_Category` to the horizontal axis and `Amount_USD` to the vertical axis.

20. Name this visualization `Spend by Merchant Category`. This chart shows how corporate card spending is distributed across categories.

### Horizontal Bar Chart: Flagged Transactions by Department

21. Add a **Horizontal Bar Chart** visualization. To show only flagged transactions in this chart, we will use a derived metric.

22. Create a derived metric:

    ```
    Sum(IF(([Is Personal Use]@ID="Y" OR [Is Duplicate Charge]@ID="Y" OR [Is High Value No Receipt]@ID="Y"), 1, 0)){~+}
    ```

    Name it `Flagged Transaction Count`.

23. Drag `Department` to the vertical axis and `Flagged Transaction Count` to the horizontal axis.

24. Name this visualization `Flagged Transactions by Department`. This chart highlights which departments have the most card policy violations.

25. Your completed Corporate Card Monitoring chapter should include 4 KPIs at top, the filtered and color-coded grid in the middle, and two charts at the bottom.

---

## 5. Chapter 3: Travel & Per Diem Review

### Why This Matters

Travel is a significant expense category for most organizations, and it introduces compliance risks that go beyond simple expense reports. Hotel bookings, per diem claims, and reimbursement requests each have their own policy limits — and each can be manipulated.

This dashboard monitors three categories of travel exceptions:

1. **Out-of-policy hotel rates — are employees booking above the approved rate?** Organizations typically set maximum hotel rates by destination to control costs. When an employee books a hotel that exceeds the policy rate, it increases travel costs unnecessarily. Our data flags 8 bookings where the hotel rate exceeds the destination-specific policy rate by 20% or more. Each case should be reviewed to determine if there was a legitimate reason (e.g., no availability at lower rates) or if the employee is consistently choosing premium accommodations.

2. **Excessive per diem claims — is someone inflating their daily allowance?** Per diem rates are set by destination and are meant to cover meals and incidental expenses at a reasonable level. When claimed per diem exceeds the standard rate by 30% or more, it suggests the employee is either inflating claims or spending beyond the expected level. Our data contains 6 bookings with excessive per diem claims — each one represents potential overpayment that should be verified against actual receipts.

3. **Duplicate reimbursement claims — is someone getting paid twice for the same trip?** This is one of the most costly travel fraud schemes. An employee submits a travel claim through the normal process, and then submits the same trip again — sometimes through a different system or to a different approver. Our data contains 3 duplicate claim pairs (6 flagged records) where the same employee, destination, and travel dates appear in two separate bookings. Each pair represents a potential double payment.

**How to use this dashboard going forward:** This dashboard should be reviewed **monthly** after travel expenses are processed. The out-of-policy hotel count is a key metric — a rising trend may indicate that policy rates need to be updated, or that employees are not being held accountable for booking within policy. The excess per diem metric should be tracked by department to identify patterns. The duplicate claim count is a zero-tolerance metric — any value above zero requires immediate investigation and recovery of the duplicate payment.

### Adding a New Chapter

1. Click the **+** icon at the bottom of the Dossier to add a third chapter. Name it **Travel & Per Diem Review**.

### Importing `travel_bookings.csv`

2. Click **New Data** and import `travel_bookings.csv`. Click **Prepare Data**.

3. Convert the following columns to **Metrics** if they are not already detected as such:
   - `Nights`
   - `Hotel_Rate_Per_Night`
   - `Total_Hotel_Cost`
   - `Policy_Rate_Per_Night`
   - `Per_Diem_Claimed`
   - `Standard_Per_Diem`
   - `Total_Per_Diem`

4. Verify that `Is_Out_Of_Policy`, `Is_Excessive_Per_Diem`, and `Is_Duplicate_Claim` remain as **Attributes**. Click **Finish**.

### KPI 1: Total Bookings

5. Rename `Row Count - travel_bookings.csv` to `Total Bookings`. Add it as a **KPI** visualization.

### KPI 2: Out-of-Policy Count

6. Create a derived metric with the formula:

   ```
   Sum(IF(([Is Out Of Policy]@ID="Y"), 1, 0)){~+}
   ```

   Name it `Out of Policy Count`. Add it as a **KPI** visualization.

### KPI 3: Total Excess Per Diem

7. Create a derived metric that sums the difference between claimed and standard per diem, but only for bookings flagged as excessive:

   ```
   Sum(IF(([Is Excessive Per Diem]@ID="Y"), ([Total Per Diem]-[Standard Per Diem]*[Nights]), 0)){~+}
   ```

   Name it `Total Excess Per Diem`. Add it as a **KPI** visualization. Format as currency.

### Grid: Travel Exception Details

8. Add a **Grid** visualization with the following fields:
   - `Booking_ID`
   - `Employee_Name`
   - `Department`
   - `Destination`
   - `Travel_Date`
   - `Nights`
   - `Hotel_Rate_Per_Night`
   - `Policy_Rate_Per_Night`
   - `Per_Diem_Claimed`
   - `Standard_Per_Diem`
   - `Is_Out_Of_Policy`
   - `Is_Excessive_Per_Diem`
   - `Is_Duplicate_Claim`

9. Name this visualization `Travel Exception Details`.

### Applying a Visualization-Level Filter

10. Apply a **visualization-level filter** to show only flagged records: `Is_Out_Of_Policy = Y` OR `Is_Excessive_Per_Diem = Y` OR `Is_Duplicate_Claim = Y`.

    > **Tip:** You may create a derived attribute: `Has_Travel_Flag = If(Is_Out_Of_Policy = "Y" OR Is_Excessive_Per_Diem = "Y" OR Is_Duplicate_Claim = "Y", "Y", "N")` and filter on `Has_Travel_Flag = Y`.

### Conditional Formatting: Travel Exceptions

11. Add conditional formatting rules to this grid:
    - **Rule 1:** Where `Is_Duplicate_Claim = Y` → Background color **Red**, font color **White**
    - **Rule 2:** Where `Is_Out_Of_Policy = Y` → Background color **Orange**
    - **Rule 3:** Where `Is_Excessive_Per_Diem = Y` → Background color **Yellow**

12. Click **Apply**. Each type of travel exception will now have a distinct color — red for the most severe (duplicate claims), orange for out-of-policy hotels, and yellow for excessive per diem.

### Derived Attribute: Rate Variance Category

13. In the Formula Editor, create a new **attribute** to bucket hotel rate overages:

    ```
    Case(([Hotel Rate Per Night]-[Policy Rate Per Night])<=0, "Within Policy",
         ([Hotel Rate Per Night]-[Policy Rate Per Night])<=50, "1-50 Over",
         ([Hotel Rate Per Night]-[Policy Rate Per Night])<=100, "51-100 Over",
         "Over 100 Above Policy")
    ```

    Name it `Rate_Variance_Category`. This derived attribute categorizes the degree of hotel rate overage, making it easier to prioritize which bookings need immediate attention.

14. You can drag `Rate_Variance_Category` into the grid or use it in a separate chart to analyze the distribution of overages.

### Bar Chart: Bookings by Destination

15. Add a **Bar Chart** visualization. Drag `Destination` to the horizontal axis and `Total Bookings` (Row Count) to the vertical axis.

16. Name this visualization `Bookings by Destination`. This chart shows travel volume by city.

### Horizontal Bar Chart: Excess Per Diem by Department

17. Add a **Horizontal Bar Chart** visualization. Create a derived metric to calculate excess per diem amount per record:

    ```
    Sum(IF(([Is Excessive Per Diem]@ID="Y"), ([Per Diem Claimed]-[Standard Per Diem])*[Nights], 0)){~+}
    ```

    Name it `Excess Per Diem Amount`.

18. Drag `Department` to the vertical axis and `Excess Per Diem Amount` to the horizontal axis.

19. Name this visualization `Excess Per Diem by Department`. This chart highlights which departments have the most per diem overages.

20. Your completed Travel & Per Diem Review chapter should include KPIs at top, the filtered and color-coded grid in the middle, and two charts at the bottom.

---

## 6. Final Review and Save

### Reviewing All Three Chapters

1. Navigate through your three chapters by clicking the tabs at the bottom of the Dossier:
   - **Expense Report Compliance** — KPIs, expense report detail grid with conditional formatting, expense type chart, top submitters chart
   - **Corporate Card Monitoring** — KPIs, flagged card transaction grid with conditional formatting, merchant category chart, flagged transactions by department chart
   - **Travel & Per Diem Review** — KPIs, travel exception grid with conditional formatting, bookings by destination chart, excess per diem by department chart

2. Verify that conditional formatting is applied correctly in each chapter:
   - Chapter 1: Red rows for split transactions, orange for missing receipts
   - Chapter 2: Red rows for personal use, orange for duplicate charges, yellow for high-value no receipt
   - Chapter 3: Red rows for duplicate claims, orange for out-of-policy hotels, yellow for excessive per diem

3. Save the Dossier with a meaningful name such as `Expense Travel Compliance Dashboard`.

### Conclusion

In this lab, you built a comprehensive 3-chapter Expense & Travel Compliance Dashboard. You reinforced and extended the skills learned in Lab 4:

- **Designed multi-chapter Dossiers** to organize expense, card, and travel analyses into logical sections
- **Applied conditional formatting** with multiple severity levels (red, orange, yellow) to Grid visualizations
- **Created visualization-level filters** with OR conditions to isolate flagged records
- **Built derived metrics** using `If()` for conditional counting, summing, and percentage calculations
- **Created derived attributes** using `Case()` to bucket numeric ranges into categories
- **Linked datasets** via `Employee_ID` to connect corporate card transactions to expense report data

These techniques directly apply to real-world compliance monitoring, where dashboards must surface policy violations, quantify financial exposure, and enable investigation workflows.

---

## 7. Summary of New Concepts

| Concept | Where Used | Description |
|---------|-----------|-------------|
| Multi-chapter Dossier | All 3 chapters | Organizing expense, card, and travel analyses into separate named chapters |
| Conditional formatting (multi-level) | Ch 1, 2, 3 | Using red, orange, and yellow to indicate exception severity |
| Text visualization | Ch 1 | Adding descriptive context to a dashboard page |
| Visualization-level filters (OR conditions) | Ch 2, 3 | Filtering data within a single visualization using multiple OR conditions |
| Dataset linking | Ch 2 | Connecting `corporate_card.csv` to `expense_reports.csv` via `Employee_ID` |
| Derived attributes (bucketing) | Ch 3 | Creating `Rate_Variance_Category` from numeric hotel rate overages using `Case()` |
| Conditional derived metrics | Ch 1, 2, 3 | Using `If()` to count, sum, or calculate percentages for matching records |
| Derived metric with arithmetic | Ch 3 | Computing excess per diem as `(Claimed - Standard) * Nights` within an `If()` |
