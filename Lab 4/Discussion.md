# Discussion 

<myask>

**I am teaching data visualization using MicroStrategy. This is for an internal audit team. They shared some ideas of use cases. I want your help to suggest some datasets .I don't have to hit every use case, but these help me understand their goals:**

</myask>

<from_client>

Investment Testing  Scenarios 
OIA bench mark - Geographical
If the total investment in north Amirca Exced 40% from OIA intrnationa investment, the systenm send the alarm and should applay for all catograise --- check the % for each one


IRR - types of investment
if the investment type(aggrasive, modrate, greenfield)went below the minum IRR or exced the exit period ; system send alarm 
Aqustion investment
if OIA aquired any new investment; the system should send notification
Deal sizes
system gives notification if investment amount exced >USD 100 M

system gives notification if investment amount < 90 M> 100 M
 sharholder
System should gfive notification if OIA has more than with sames/through same party(sharholder, partener, fund manager, asset management company)
OIA ownership stake
if OIA percentage stake decreas by more than 50% ; system should send notification
Investment Valuation
if the investment value change(increase & decrease) compared to Investment total cost, moer than 30%
Method of the valuation
System should gfive notification if the valuation method for each investment changed compared to the latest valuation method

if any manual modification accured; system should send notifiaction 
Dividendes received
1-System should give notification if OIA received any dividends
2-give comparsion table between dividend declarition date Vs. received date
3- compare dividends amount received from the sam entity for each year
Exit
System should gfive notification if OIA; partialy or fully exit from any investment

if any investment holde it more than 10 years(FGF)
Investment risk
System should gfive notification if OIA; if investment overall risk rating changed from medium to high 
 DD cost - AAC 
System should give notification if OIA; if the actual DD cost exceed the approved budget 
Maker-checker
System to show a list of individuals who creat, review and approve transactions
Financial Anaylsis
- Debt to equity ration
- Liquidity rations
- EBITDA
- Profitability ratios
- Earning quality
- Capital erosion
Related party
To check system ability to identify related party( Board membership and employee declarition list)
Manual modification
if any manual modification accured; system should send notifiaction 
Business support testing cenarios 
procurement 
1-Creation of Purchase requesition and approval by the same person
2- Delay in approval of Purchase requestion above the standard time
3- Competivite bidding where they do single or slective vendor
4- open approved purchase order for long time
5- type of expenses  that goes through direct invoice
6- Multiple vendors sharing the same address or phone number
7- changes in supplier account details
8- same person creating PR is creating PO
9- Same user/vendor 
Finance - Payment 
1- Dublicate payment for the same invoice provided by the vendor
2- Total Purchase order amount paid exceeded puchase order amount
3-  payment that are due for long time
4- payment overriddes
5- Backdated or forward-dated entries
HR
1- Bogus employees
2- Payroll changes month on month comparison
3- Banck account changes of emplyees without proper approval
4-  Identify resigned staff with Active status
5- Payroll Weekend Processing (transaction process on weekend or holidays



<from_client>

<ideas_shared_by_AI>

Here’s a structured set of **synthetic / example datasets** you can build or adapt for your MicroStrategy course, tailored to the internal‑audit use cases you shared. You don’t need to cover every scenario, but these datasets will let you:

- Demonstrate **threshold‑based alerts** (dashboard alerts, exception flags).
- Show **trend and comparison charts**.
- Practice **dimensions vs. metrics** (region, sector, period, risk, etc.).

------

## 1. Investment portfolio dataset

**Purpose:** cover IRR, deal size, geography, valuation, ownership stake, exit, risk rating, AAQ, etc.

**Table name:** `INV_Investment_Portfolio`

**Sample fields:**

- `Investment_ID` (unique)
- `Investment_Name`
- `Investment_Type` (`Aggressive`, `Moderate`, `Greenfield`, `Private_Equity`, etc.)
- `Geography` (`North_America`, `Europe`, `Asia`, `Middle_East`, `Africa`, `Latin_America`)
- `Currency` (`USD`, `EUR`, `OMR`, etc.)
- `Deal_Size_USD` (e.g., 120.5, 85.0, 250.0)
- `Cost_Basis_USD` (initial investment cost)
- `Current_Value_USD`
- `Valuation_Change_Pct` = `((Current_Value – Cost_Basis) / Cost_Basis) * 100`
- `Valuation_Method` (`DCF`, `Comparables`, `NAV`, `Book_Value`, …)
- `Prev_Valuation_Method` (last valuation method)
- `OIA_Ownership_Stake_Pct` (e.g., 65%, 40%, 15%)
- `Prev_Ownership_Stake_Pct`
- `IRR_Current` (e.g., 12.5%)
- `Min_Allowed_IRR` (e.g., 8.0%)
- `Exit_Period_Years` (e.g., 5, 7, 12)
- `Current_Holding_Period_Years` (e.g., 3, 6, 11)
- `Overall_Risk_Rating` (`Low`, `Medium`, `High`)
- `Prev_Risk_Rating`
- `Deal_Status` (`Active`, `Partially_Exit`, `Fully_Exit`, `Closed`)
- `Investment_Date`
- `Exit_Date` (nullable)
- `Is_Acquired_New` (`Y`/`N`)
- `Is_Manual_Modification` (`Y`/`N`)
- `Is_DD_Cost_Over_Budget` (`Y`/`N`)
- `DD_Cost_Approved_Budget_USD`
- `DD_Cost_Actual_USD`
- `Maker_User_ID`, `Checker_User_ID`, `Approver_User_ID`

**How you’ll use it in MicroStrategy:**

- Create **threshold‑based alerts**:
  - `% change from cost > 30%` → Valuation alert.
  - `OIA stake decrease > 50%` → ownership stake alert.
  - `IRR < Min_Allowed_IRR` → underperformance alert.
- Build **geographic‑ and type‑based dashboards**:
  - `Sum(Deal_Size) by Geography` to flag when North America > 40% of total portfolio.
- Use **cascading filters** for:
  - `Investment_Type`, `Geography`, `Risk_Rating`, `Deal_Status`.

------

## 2. Dividends and exit notifications dataset

**Purpose:** dividends received, timing, comparisons, and exit notifications.

**Table name:** `DIV_Dividends`

**Fields:**

- `Dividend_ID`
- `Investment_ID`
- `Dividend_Declaration_Date`
- `Dividend_Payment_Date`
- `Days_Diff` = `Payment_Date – Declaration_Date`
- `Dividend_Amount_USD`
- `Currency`
- `Is_OIA_Receiving` (`Y`/`N`)

**Table name:** `EXIT_Investments`

**Fields:**

- `Exit_ID`
- `Investment_ID`
- `Exit_Type` (`Partial`, `Full`)
- `Exit_Date`
- `Proceeds_USD`
- `FGF_Holding_Period_Years` (e.g., 11, 15, 12)

**How you’ll use it in MicroStrategy:**

- Build a **dividend timeline** comparing `Declaration` vs `Payment` dates.
- Create a **year‑over‑year dividend table** for each entity.
- Flag investments held > 10 years (FGF) using `FGF_Holding_Period_Years > 10`.

------

## 3. Financial analysis dataset (for ratios)

**Purpose:** ratios like debt‑to‑equity, liquidity, EBITDA, profitability, etc.

**Table name:** `FIN_Financial_Statements`

**Fields:**

- `Year`, `Quarter`
- `Entity` (e.g., `Investment_ID` or `Subsidiary_Name`)
- `Total_Assets`
- `Total_Liabilities`
- `Shareholders_Equity`
- `Revenue`
- `EBITDA`
- `Net_Income`
- `Operating_Cash_Flow`
- `Current_Assets`
- `Current_Liabilities`
- `Capital_Erosion_Flag` (`Y`/`N`)

**Computed metrics (in MicroStrategy or DW):**

- `Debt_to_Equity = Total_Liabilities / Shareholders_Equity`
- `Current_Ratio = Current_Assets / Current_Liabilities`
- `EBITDA_Margin = EBITDA / Revenue`
- `Profitability_Ratio = Net_Income / Revenue`

**How you’ll use it in MicroStrategy:**

- Show **ratios over time** with line charts.
- Add **threshold coloring** (e.g., red if debt‑to‑equity exceeds policy limit).

------

## 4. Procurement audit dataset

**Purpose:** procurement red‑flag scenarios (duplicated approvals, single‑vendor, long‑open POs, etc.).

**Table name:** `PROC_Purchase_Requests`

**Fields:**

- `PR_ID`
- `PR_Creator_User_ID`
- `PR_Creation_Date`
- `PR_Approver_User_ID`
- `PR_Approval_Date`
- `PR_Approval_Duration_Days`
- `Standard_Approval_Threshold_Days` (e.g., 3)
- `Vendor_ID`
- `Vendor_Name`
- `Vendor_Address`, `Vendor_Phone`
- `Account_No`
- `Expense_Type` (`Consulting`, `Travel`, `IT`, `Equipment`, `Services`, etc.)
- `Is_Direct_Invoice` (`Y`/`N`)
- `Is_Competitive_Bidding` (`Open`, `Selective`, `Single_Source`)
- `Is_Delayed` (`Y`/`N`)

**Table name:** `PROC_Purchase_Orders`

**Fields:**

- `PO_ID`
- `PR_ID`
- `PO_Creator_User_ID`
- `PO_Creation_Date`
- `PO_Status` (`Open`, `Closed`, `Partially_Received`)
- `PO_Open_Duration_Days`
- `Total_PO_Amount_USD`
- `Vendor_ID`
- `Is_Long_Open` (`Y`/`N` if open > policy days)

**Table name:** `PROC_Vendors`

**Fields:**

- `Vendor_ID`
- `Vendor_Name`
- `Address`
- `Phone`
- `Bank_Account`
- `Updated_By_User`
- `Update_Date`

**How you’ll use it in MicroStrategy:**

- Flag **creator‑and‑approver same person**.
- Flag **same vendor multiple times with same address/phone**.
- Show **open POs longer than standard**.
- Detect **direct‑invoice expense types** vs policy.

------

## 5. Finance – payments dataset

**Purpose:** payment‑related audit tests (duplicate payments, over‑payment, long‑outstanding, etc.).

**Table name:** `PAY_Payments`

**Fields:**

- `Payment_ID`
- `Vendor_ID`
- `Invoice_ID`
- `Invoice_Amount_USD`
- `PO_ID` (nullable)
- `Payment_Amount_USD`
- `Payment_Date`
- `Due_Date`
- `Days_Overdue`
- `Is_Overdue` (`Y`/`N`)
- `Is_Duplicate_Payment` (`Y`/`N`)
- `Is_PO_Overpayment` (`Y`/`N`)
- `Is_Backdated` (`Y`/`N`)
- `Is_Forward_Dated` (`Y`/`N`)
- `Override_Flag` (`Y`/`N`)
- `Override_Reason`

**How you’ll use it in MicroStrategy:**

- Duplicate‑payment detection (e.g., same vendor + same invoice + same amount).
- Flag **payments exceeding PO amount**.
- Visualize **overdue payments** by age bucket.

------

## 6. HR / payroll dataset

**Purpose:** bogus employees, payroll changes, bank‑account changes, weekend processing, etc.

**Table name:** `HR_Employees`

**Fields:**

- `Employee_ID`
- `Full_Name`
- `Branch_Location`
- `Department`
- `Status` (`Active`, `Resigned`, `Terminated`)
- `Resignation_Date` (nullable)
- `Bank_Account_Number`
- `Bank_Account_Last_Changed_Date`
- `Bank_Account_Last_Changed_By_User`
- `Is_Active_But_Resigned` (`Y`/`N`)

**Table name:** `HR_Payroll_Transactions`

**Fields:**

- `Payroll_ID`
- `Employee_ID`
- `Payroll_Month`
- `Gross_Pay`
- `Previous_Month_Gross_Pay`
- `Pay_Change_Pct`
- `Payroll_Process_Date`
- `Is_Weekend_Holiday` (`Y`/`N`)
- `Is_Payroll_Change_Unusual` (`Y`/`N` if change > threshold)

**How you’ll use it in MicroStrategy:**

- Detect **resigned employees with active status**.
- Flag **unusual payroll changes** month‑on‑month.
- Identify **payroll processed on weekends/holidays**.
- Show **bank‑account change patterns** without approval trail.

------

## 7. Related‑party and manual‑modification dataset

**Purpose:** related‑party identification and manual‑modifications.

**Table name:** `REL_Related_Parties`

**Fields:**

- `Person_ID`
- `Person_Name`
- `Role` (`Board_Member`, `Employee`, `Vendor`, `Investor`, etc.)
- `Entity_ID` (e.g., `Investment_ID`, `Vendor_ID`, `Subsidiary_ID`)
- `Related_Entity_Type` (`Investment`, `Vendor`, `Subsidiary`, `Fund`)
- `Is_Direct_Related_Party` (`Y`/`N`)

**Table name:** `AUDIT_Manual_Modifications`

**Fields:**

- `Mod_ID`
- `Table_Name`
- `Row_ID`
- `Field_Name`
- `Old_Value`
- `New_Value`
- `Modified_By_User`
- `Modification_Date`
- `Is_System_Audit_Alert` (`Y`/`N`)

**How you’ll use it in MicroStrategy:**

- Show **related‑party links** in a network‑style or cross‑tab view.
- List all **manual modifications** with timestamps and users.

------

## 8. Maker‑checker / transaction lines dataset

**Purpose:** show who created, reviewed, approved each transaction.

**Table name:** `TXN_Transactions`

**Fields:**

- `Transaction_ID`
- `Transaction_Type` (`Investment`, `Payment`, `PR`, `PO`, etc.)
- `Amount_USD`
- `Creation_Date`
- `Creation_User`
- `Review_Date`
- `Review_User`
- `Approval_Date`
- `Approval_User`
- `Status` (`Draft`, `Reviewed`, `Approved`, `Rejected`)

**How you’ll use it in MicroStrategy:**

- Build a **maker‑checker dashboard** showing segregation of duties.
- Flag **self‑approval** or missing reviewers.

------

## How to turn this into MicroStrategy labs

For each module, design a **short lab**:

- **Lab 1 – Investment dashboards:**
  Create a dashboard with:
  - Map/chart of investments by **geography**.
  - Bar chart of **investment types** with IRR vs minimum.
  - KPIs for **deal size > 100M** and **40% North America threshold**.
- **Lab 2 – Threshold alerts (valuations, risk, ownership):**
  Use **conditional formatting**, **metric‑level alerts**, and **filters** to flag:
  - `Valuation change > 30%`.
  - `Risk rating change from Medium to High`.
  - `Ownership stake decrease > 50%`.
- **Lab 3 – Procurement & payments:**
  Build a **procurement risk dashboard** highlighting:
  - Duplicate approvals, long‑open POs, single‑vendor scenarios.
  - Payment‑related alerts (duplicates, over‑payments, overdue).
- **Lab 4 – HR / Payroll:**
  Show **bogus employees**, **active‑but‑resigned**, and **weekend payroll** entries.
- **Lab 5 – Related‑party & manual mods:**
  Demonstrate how to **trace related parties** and **list all manual adjustments**.

If you tell me which areas you want to emphasize (e.g., “focus on investments + procurement”), a next step can be to sketch **exact MicroStrategy attributes / metrics** for one or two of these datasets.

</ideas_shared_by_AI>

<my_response_to_AI>

I like concepts for Labs 3, 4, and 5

</my_response_to_AI>

<followup_by_ai>

Here’s how you can structure **Labs 3, 4, and 5** around MicroStrategy, using the concepts you liked, with clear learning objectives and sample visualizations for each.

------

## Lab 3: Procurement & Payment Audit Dashboard

**Learning goal:** Use MicroStrategy to detect red‑flags in procurement and payments (duplicate approvals, single‑vendor, long‑open POs, overdue payments, over‑payments).

## 1. Data & modeling

- Use the `PROC_Purchase_Requests`, `PROC_Purchase_Orders`, and `PAY_Payments` tables you defined earlier.
- Create **attributes**:
  - `PR_Creator`, `PR_Approver`, `Vendor`, `Payment_Date`, `Due_Date`, `PO_Status`.
- Create **metrics**:
  - `PR_Count`, `PO_Amount_Total`, `Days_Overdue`, `PO_Open_Duration_Days`, `Duplicate_Payment_Count`.

## 2. Key exercises for learners

- **Duplicate creator/approver:**
  - Create a **filter** where `PR_Creator = PR_Approver` and show counts of such PRs.
- **Single‑vendor / long‑open POs:**
  - Build a **bar chart** of `PO_Count by Vendor` and a **table** of POs with `PO_Open_Duration_Days > 30`.
- **Competitive bidding check:**
  - Use a **pie chart / table** of `Is_Competitive_Bidding` (`Open` vs `Selective` vs `Single_Source`) to show concentration.
- **Payment‑related alerts:**
  - Show KPIs for:
    - `Count of Is_Duplicate_Payment = Y`.
    - `Sum(Payment_Amount) where Days_Overdue > 0`.
    - `Count of Is_PO_Overpayment = Y`.

## 3. Final deliverable (MicroStrategy dossier)

- A **single dossier** with:
  - **Procurement tab:**
    - KPIs for long‑open POs, single‑vendor concentration, and PR approval‑time issues.
  - **Payments tab:**
    - KPIs for duplicate payments, overdue payments, and over‑payments.
  - Use **conditional formatting** to highlight values above thresholds (e.g., red if overdue > 60 days).

------

## Lab 4: HR / Payroll Audit Dashboard

**Learning goal:** Use MicroStrategy to spot payroll anomalies, bogus employees, and control issues (weekend‑processing, account‑change risks).

## 1. Data & modeling

- Use the `HR_Employees` and `HR_Payroll_Transactions` tables.
- Create **attributes**:
  - `Employee_ID`, `Department`, `Status`, `Payroll_Month`, `Is_Weekend_Holiday`.
- Create **metrics**:
  - `Gross_Pay`, `Pay_Change_Pct`, `Transaction_Count`, `Active_But_Resigned_Count`.

## 2. Key exercises for learners

- **Bogus / ghost employees:**
  - Create a **filter** where `Status = Active` and `Resignation_Date is not null`, then show a list of employees.
- **Resigned employees still active:**
  - Build a **table** of `Employee_ID`, `Name`, `Resignation_Date`, `Status`, and flag those with `Is_Active_But_Resigned = Y`.
- **Unusual payroll changes:**
  - Create a **line chart** of `Gross_Pay by Month` per employee, with a **conditional color** when `Pay_Change_Pct > 20%`.
- **Weekend and holiday payroll:**
  - Show a **count of Transactions** where `Is_Weekend_Holiday = Y` and drill down to employee list.
- **Bank‑account changes:**
  - Create a **table** of `Employee_ID`, `Bank_Account_Last_Change_Date`, and `Bank_Account_Last_Changed_By_User` to spot frequent changes.

## 3. Final deliverable (MicroStrategy dossier)

- An **HR / Payroll dossier** with:
  - **Employees tab:**
    - KPIs for “active but resigned” and a table of suspicious employees.
  - **Payroll tab:**
    - Graphs of payroll trends, highlighting outliers, and a list of weekend‑processed transactions.
  - Use **cross‑filtering** (e.g., click a department to see its payroll anomalies).

------

## Lab 5: Related‑Party & Manual‑Modification Dashboard

**Learning goal:** Use MicroStrategy to trace related‑party relationships and monitor manual data changes as audit trails.

## 1. Data & modeling

- Use the `REL_Related_Parties` and `AUDIT_Manual_Modifications` tables.
- Create **attributes**:
  - `Person_ID`, `Person_Name`, `Role`, `Entity_ID`, `Related_Entity_Type`, `Row_ID`, `Table_Name`, `Modified_By_User`.
- Create **metrics**:
  - `Related_Party_Count`, `Manual_Mod_Count`.

## 2. Key exercises for learners

- **Related‑party identification:**
  - Build a **cross‑tab** of `Person_Name` vs `Related_Entity_Type` (e.g., “investments”, “vendors”, “subsidiaries”).
  - Create a **table** of all relationships where `Is_Direct_Related_Party = Y`.
- **Manual modifications overview:**
  - Show a **bar chart** of `Manual_Mod_Count by Table_Name` to highlight tables with many changes.
  - Create a **table** of all manual modifications with:
    - `Table_Name`, `Row_ID`, `Field_Name`, `Old_Value`, `New_Value`, `Modified_By_User`, `Modification_Date`.
  - Use **conditional formatting** to highlight high‑risk tables (e.g., investment valuations, ownership stakes).
- **Drill‑through to explanations:**
  - Set up a **drill map** so learners can click a modification row and “see” a mock “audit note” or description field.

## 3. Final deliverable (MicroStrategy dossier)

- A **Governance & Controls dossier** with:
  - **Related‑Parties tab:**
    - Network‑style or cross‑tab view of people and entities, colored by relationship type.
  - **Manual Modifications tab:**
    - KPIs for total modifications and a detailed log table.
  - Use **filters** such as `Role = Board_Member` or `Table_Name = INV_Investment_Portfolio` to simulate focused audit tests.

</followup_by_ai>