# Lab 4 Data Dictionary

This document describes each column across the four datasets used in Lab 4, including its meaning, data type, and how it should be classified in MicroStrategy.

---

## 1. `procurement_audit.csv` (75 rows)

Purchase requests with approval workflow and vendor details. Used in **Chapter 1: Procurement Audit**.

| Column | Description | Data Type | MicroStrategy |
|--------|-------------|-----------|---------------|
| `PR_ID` | Unique identifier for each purchase request (e.g., PR-001) | Text | Attribute |
| `PR_Date` | Date the purchase request was created | Date | Attribute |
| `PR_Creator` | Name of the employee who created the purchase request | Text | Attribute |
| `PR_Approver` | Name of the employee who approved the purchase request | Text | Attribute |
| `Vendor_Name` | Name of the vendor supplying the goods or services | Text | Attribute |
| `Vendor_City` | City where the vendor is located | Text | Attribute |
| `PR_Amount_USD` | Dollar amount of the purchase request | Numeric | Metric |
| `Expense_Category` | Type of expense (IT, Consulting, Travel, Equipment, Services, Office Supplies) | Text | Attribute |
| `Bidding_Type` | How the vendor was selected (Competitive, Selective, Single_Source) | Text | Attribute |
| `Approval_Days` | Number of days it took to approve the request | Numeric | Metric |
| `Standard_Max_Days` | Maximum allowed approval days per policy (varies by expense category) | Numeric | Metric |
| `PO_Status` | Current status of the purchase order (Closed, Open, Partially_Received) | Text | Attribute |
| `PO_Open_Days` | Number of days the purchase order has been open (0 if closed) | Numeric | Metric |
| `Is_Same_Creator_Approver` | Flag indicating the creator and approver are the same person (Y/N) | Text | Attribute |

**Red flag columns:** `Is_Same_Creator_Approver`, `Bidding_Type` (Single_Source), `Approval_Days` vs `Standard_Max_Days`, `PO_Open_Days` with `PO_Status` = Open.

---

## 2. `hr_employees.csv` (50 rows)

Employee master data including status and bank account details. Used in **Chapter 2: HR & Payroll Audit**. Linked to `hr_payroll.csv` via `Employee_ID`.

| Column | Description | Data Type | MicroStrategy |
|--------|-------------|-----------|---------------|
| `Employee_ID` | Unique identifier for each employee (e.g., EMP-001) | Text | Attribute |
| `Full_Name` | Employee's full name | Text | Attribute |
| `Department` | Department the employee belongs to (Finance, IT, Operations, HR, Legal, Audit, Procurement) | Text | Attribute |
| `Branch_Location` | Office location (Muscat HQ, Dubai Office, Riyadh Office, London Office) | Text | Attribute |
| `Status` | Current employment status (Active, Resigned, Terminated) | Text | Attribute |
| `Hire_Date` | Date the employee was hired | Date | Attribute |
| `Resignation_Date` | Date the employee resigned (blank if still employed or terminated) | Date | Attribute |
| `Bank_Account_Last_Changed` | Date the employee's bank account was last updated (blank if never changed) | Date | Attribute |
| `Bank_Change_Approved` | Whether the bank account change was approved (Y, N, or blank) | Text | Attribute |
| `Is_Ghost_Employee` | Flag indicating a ghost employee: Status = Active but Resignation_Date is filled (Y/N) | Text | Attribute |

**Red flag columns:** `Is_Ghost_Employee` (Y), `Bank_Account_Last_Changed` (recent dates) with `Bank_Change_Approved` (N).

---

## 3. `hr_payroll.csv` (200 rows)

Monthly payroll records for 50 employees across 4 months (Jan--Apr 2025). Used in **Chapter 2: HR & Payroll Audit**. Linked to `hr_employees.csv` via `Employee_ID`.

| Column | Description | Data Type | MicroStrategy |
|--------|-------------|-----------|---------------|
| `Payroll_ID` | Unique identifier for each payroll record (e.g., PAY-0001) | Text | Attribute |
| `Employee_ID` | Employee identifier, links to `hr_employees.csv` | Text | Attribute |
| `Employee_Name` | Employee's full name (denormalized for convenience) | Text | Attribute |
| `Department` | Department the employee belongs to | Text | Attribute |
| `Pay_Month` | Month of the payroll period (e.g., 2025-01) | Text | Attribute |
| `Process_Date` | Date the payroll was actually processed | Date | Attribute |
| `Day_of_Week` | Day name when payroll was processed (Monday--Sunday) | Text | Attribute |
| `Gross_Pay` | Total pay before deductions | Numeric | Metric |
| `Deductions` | Total deductions (taxes, benefits, etc.) | Numeric | Metric |
| `Net_Pay` | Take-home pay after deductions (Gross_Pay minus Deductions) | Numeric | Metric |
| `Previous_Gross_Pay` | Gross pay from the prior month (blank for the first month) | Numeric | Metric |
| `Pay_Change_Pct` | Percentage change in gross pay from the prior month (blank for the first month) | Numeric | Metric |
| `Is_Weekend` | Flag indicating payroll was processed on a Saturday or Sunday (Y/N) | Text | Attribute |
| `Is_Unusual_Change` | Flag indicating the pay change exceeded 20% month-over-month (Y/N, blank for first month) | Text | Attribute |

**Red flag columns:** `Is_Weekend` (Y), `Is_Unusual_Change` (Y).

---

## 4. `payment_transactions.csv` (80 rows)

Invoice payments with exception flags for duplicates, overpayments, and overdue balances. Used in **Chapter 3: Payment Exceptions**.

| Column | Description | Data Type | MicroStrategy |
|--------|-------------|-----------|---------------|
| `Payment_ID` | Unique identifier for each payment (e.g., PMT-001) | Text | Attribute |
| `Invoice_ID` | Invoice number being paid (duplicate payments share the same Invoice_ID) | Text | Attribute |
| `Vendor_Name` | Name of the vendor receiving payment | Text | Attribute |
| `Payment_Date` | Date the payment was made | Date | Attribute |
| `Due_Date` | Date the payment was due | Date | Attribute |
| `PO_Amount` | Original purchase order amount | Numeric | Metric |
| `Payment_Amount` | Actual amount paid (may exceed PO_Amount for overpayments) | Numeric | Metric |
| `Days_Overdue` | Number of days past the due date (0 if paid on time or early) | Numeric | Metric |
| `Aging_Bucket` | Categorized overdue range (Current, 1-30 Days, 31-60 Days, 61-90 Days, Over 90 Days) | Text | Attribute |
| `Is_Duplicate` | Flag indicating a duplicate payment for the same invoice (Y/N) | Text | Attribute |
| `Is_Overpayment` | Flag indicating Payment_Amount exceeds PO_Amount (Y/N) | Text | Attribute |
| `Is_Overdue` | Flag indicating payment is more than 30 days past due (Y/N) | Text | Attribute |

**Red flag columns:** `Is_Duplicate` (Y), `Is_Overpayment` (Y), `Is_Overdue` (Y), `Aging_Bucket` (31-60, 61-90, Over 90).

---

## Dataset Relationships

```
hr_employees.csv ──── Employee_ID ────── hr_payroll.csv
```

The `procurement_audit.csv` and `payment_transactions.csv` datasets are used independently (no linking required).
