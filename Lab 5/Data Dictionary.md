# Lab 5 Data Dictionary

This document describes each column across the three datasets used in Lab 5, including its meaning, data type, and how it should be classified in MicroStrategy.

---

## 1. `expense_reports.csv` (80 rows)

Expense reports with approval workflow and policy violation flags. Used in **Chapter 1: Expense Report Compliance**.

| Column | Description | Data Type | MicroStrategy |
|--------|-------------|-----------|---------------|
| `Report_ID` | Unique identifier for each expense report (e.g., EXP-001) | Text | Attribute |
| `Employee_ID` | Employee identifier, links to `corporate_card.csv` | Text | Attribute |
| `Employee_Name` | Employee's full name | Text | Attribute |
| `Department` | Department the employee belongs to (Finance, IT, Operations, HR, Legal, Procurement, Audit) | Text | Attribute |
| `Location` | Office location (Muscat HQ, Dubai Office, Riyadh Office, London Office) | Text | Attribute |
| `Submission_Date` | Date the expense report was submitted | Date | Attribute |
| `Approval_Date` | Date the expense report was approved | Date | Attribute |
| `Approver_Name` | Name of the manager who approved the expense report | Text | Attribute |
| `Expense_Type` | Category of expense (Meals, Transportation, Accommodation, Office Supplies, Client Entertainment, Training, Miscellaneous) | Text | Attribute |
| `Amount_USD` | Dollar amount of the expense claim | Numeric | Metric |
| `Receipt_Attached` | Whether a receipt was provided (Y/N) | Text | Attribute |
| `Is_Split_Transaction` | Flag indicating a potential split transaction — same employee, same expense type, consecutive days, amounts just below the approval threshold (Y/N) | Text | Attribute |
| `Is_Missing_Receipt` | Flag indicating no receipt was attached to the expense report (Y/N) | Text | Attribute |
| `Is_Weekend_Submission` | Flag indicating the expense report was submitted on a Saturday or Sunday (Y/N) | Text | Attribute |

**Red flag columns:** `Is_Split_Transaction` (Y), `Is_Missing_Receipt` (Y), `Is_Weekend_Submission` (Y).

---

## 2. `corporate_card.csv` (100 rows)

Corporate card transactions with misuse and policy violation flags. Used in **Chapter 2: Corporate Card Monitoring**. Linked to `expense_reports.csv` via `Employee_ID`.

| Column | Description | Data Type | MicroStrategy |
|--------|-------------|-----------|---------------|
| `Transaction_ID` | Unique identifier for each card transaction (e.g., TXN-0001) | Text | Attribute |
| `Employee_ID` | Employee identifier, links to `expense_reports.csv` | Text | Attribute |
| `Employee_Name` | Employee's full name (denormalized for convenience) | Text | Attribute |
| `Department` | Department the employee belongs to | Text | Attribute |
| `Transaction_Date` | Date the card transaction occurred | Date | Attribute |
| `Merchant_Name` | Name of the merchant where the purchase was made | Text | Attribute |
| `Merchant_Category` | Category of the merchant (Travel, Dining, Office Supplies, Fuel, Technology, Professional Services, Subscriptions) | Text | Attribute |
| `Amount_USD` | Dollar amount of the card transaction | Numeric | Metric |
| `Receipt_Provided` | Whether a receipt was provided for the transaction (Y/N) | Text | Attribute |
| `Is_Personal_Use` | Flag indicating the transaction appears to be for personal use based on merchant type (Y/N) | Text | Attribute |
| `Is_Duplicate_Charge` | Flag indicating a duplicate charge — same employee, merchant, amount, and date appearing twice (Y/N) | Text | Attribute |
| `Is_High_Value_No_Receipt` | Flag indicating a high-value transaction (above policy threshold) with no receipt attached (Y/N) | Text | Attribute |

**Red flag columns:** `Is_Personal_Use` (Y), `Is_Duplicate_Charge` (Y), `Is_High_Value_No_Receipt` (Y).

---

## 3. `travel_bookings.csv` (60 rows)

Travel bookings with hotel rate compliance and per diem claims. Used in **Chapter 3: Travel & Per Diem Review**.

| Column | Description | Data Type | MicroStrategy |
|--------|-------------|-----------|---------------|
| `Booking_ID` | Unique identifier for each travel booking (e.g., TRV-001) | Text | Attribute |
| `Employee_ID` | Employee identifier | Text | Attribute |
| `Employee_Name` | Employee's full name | Text | Attribute |
| `Department` | Department the employee belongs to | Text | Attribute |
| `Destination` | Travel destination city (Dubai, Riyadh, London, Muscat, Doha, Bahrain, Abu Dhabi, Cairo) | Text | Attribute |
| `Travel_Date` | Date of departure | Date | Attribute |
| `Return_Date` | Date of return | Date | Attribute |
| `Nights` | Number of hotel nights | Numeric | Metric |
| `Hotel_Name` | Name of the hotel booked | Text | Attribute |
| `Hotel_Rate_Per_Night` | Actual nightly hotel rate charged | Numeric | Metric |
| `Total_Hotel_Cost` | Total hotel cost (Hotel_Rate_Per_Night x Nights) | Numeric | Metric |
| `Policy_Rate_Per_Night` | Maximum allowed nightly hotel rate for the destination per organizational policy | Numeric | Metric |
| `Per_Diem_Claimed` | Daily per diem amount claimed by the employee | Numeric | Metric |
| `Standard_Per_Diem` | Standard daily per diem rate for the destination per organizational policy | Numeric | Metric |
| `Total_Per_Diem` | Total per diem claimed (Per_Diem_Claimed x Nights) | Numeric | Metric |
| `Is_Out_Of_Policy` | Flag indicating hotel rate exceeds the destination policy rate by 20% or more (Y/N) | Text | Attribute |
| `Is_Excessive_Per_Diem` | Flag indicating per diem claimed exceeds the standard rate by 30% or more (Y/N) | Text | Attribute |
| `Is_Duplicate_Claim` | Flag indicating a duplicate reimbursement claim — same employee, destination, and travel dates appearing twice (Y/N) | Text | Attribute |

**Red flag columns:** `Is_Out_Of_Policy` (Y), `Is_Excessive_Per_Diem` (Y), `Is_Duplicate_Claim` (Y).

---

## Dataset Relationships

```
expense_reports.csv ──── Employee_ID ────── corporate_card.csv
```

The `travel_bookings.csv` dataset is used independently (no linking required).
