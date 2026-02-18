"""Generate Lab 5 datasets: expense_reports.csv, corporate_card.csv, travel_bookings.csv"""
import csv
import random
from datetime import date, timedelta

random.seed(42)

# Shared constants
EMPLOYEES = [
    ("EMP-001", "Ahmed Al-Said", "Finance", "Muscat HQ"),
    ("EMP-002", "Fatima Hassan", "IT", "Muscat HQ"),
    ("EMP-003", "John Smith", "Operations", "Dubai Office"),
    ("EMP-004", "Layla Mahmoud", "HR", "Dubai Office"),
    ("EMP-005", "Noor Al-Busaidi", "Legal", "Muscat HQ"),
    ("EMP-006", "Omar Khalil", "Procurement", "Riyadh Office"),
    ("EMP-007", "Sara Al-Rashdi", "Finance", "London Office"),
    ("EMP-008", "Yusuf Khamis", "IT", "Muscat HQ"),
    ("EMP-009", "Mariam Al-Lawati", "Operations", "Dubai Office"),
    ("EMP-010", "Khalid Nasser", "Audit", "Muscat HQ"),
    ("EMP-011", "Aisha Darwish", "HR", "Riyadh Office"),
    ("EMP-012", "Tariq Salim", "Procurement", "Muscat HQ"),
    ("EMP-013", "Huda Al-Harthi", "Finance", "London Office"),
    ("EMP-014", "Ibrahim Juma", "IT", "Dubai Office"),
    ("EMP-015", "Zainab Al-Hinai", "Legal", "Muscat HQ"),
]

APPROVERS = [
    ("MGR-001", "Saeed Al-Maskari"),
    ("MGR-002", "Rawya Ibrahim"),
    ("MGR-003", "David Wilson"),
    ("MGR-004", "Amina Sulaiman"),
    ("MGR-005", "Hassan Al-Balushi"),
]

EXPENSE_TYPES = ["Meals", "Transportation", "Accommodation", "Office Supplies", "Client Entertainment", "Training", "Miscellaneous"]

# ============================================================
# Dataset 1: expense_reports.csv (~80 rows)
# ============================================================
def generate_expense_reports():
    rows = []
    report_id = 1

    def random_weekday(month_range=(1, 6)):
        """Return a random weekday date."""
        while True:
            d = date(2025, random.randint(*month_range), random.randint(1, 28))
            if d.weekday() < 5:
                return d

    def random_weekend(month_range=(1, 6)):
        """Return a random weekend date."""
        while True:
            d = date(2025, random.randint(*month_range), random.randint(1, 28))
            if d.weekday() >= 5:
                return d

    # We'll track which ones are split transactions
    split_groups = []  # list of (employee_idx, expense_type, base_date)
    # Create 8 split transaction groups (each will produce 2 rows = 16 rows from splits)
    split_employee_indices = random.sample(range(len(EMPLOYEES)), 8)
    for emp_idx in split_employee_indices:
        exp_type = random.choice(["Meals", "Client Entertainment", "Training"])
        base_date = random_weekday()
        split_groups.append((emp_idx, exp_type, base_date))

    # Missing receipt indices (we'll flag ~10 rows)
    missing_receipt_ids = set()
    # Weekend submission indices (~6 rows)
    weekend_submission_ids = set()

    # Generate split transaction rows first (8 groups x 2 rows = 16 rows)
    for emp_idx, exp_type, base_date in split_groups:
        emp_id, emp_name, dept, loc = EMPLOYEES[emp_idx]
        approver_id, approver_name = random.choice(APPROVERS)
        # Split: two submissions on consecutive days, each just under $500 policy threshold
        for offset in range(2):
            rid = f"EXP-{report_id:03d}"
            amount = round(random.uniform(420, 499), 2)
            sub_date = base_date + timedelta(days=offset)
            approval_date = sub_date + timedelta(days=random.randint(1, 3))
            rows.append({
                "Report_ID": rid,
                "Employee_ID": emp_id,
                "Employee_Name": emp_name,
                "Department": dept,
                "Location": loc,
                "Submission_Date": sub_date.isoformat(),
                "Approval_Date": approval_date.isoformat(),
                "Approver_Name": approver_name,
                "Expense_Type": exp_type,
                "Amount_USD": amount,
                "Receipt_Attached": "Y",
                "Is_Split_Transaction": "Y",
                "Is_Missing_Receipt": "N",
                "Is_Weekend_Submission": "N",  # split txns are on weekdays
            })
            report_id += 1

    # Generate remaining normal rows to reach ~80 total
    target_total = 80
    normal_count = target_total - len(rows)

    # Decide which normal rows get missing receipts (~10) and weekend submissions (~6)
    normal_indices = list(range(normal_count))
    missing_receipt_normals = set(random.sample(normal_indices, 10))
    # Weekend: we'll force submission dates to be weekends
    remaining_for_weekend = [i for i in normal_indices if i not in missing_receipt_normals]
    weekend_normals = set(random.sample(remaining_for_weekend, min(6, len(remaining_for_weekend))))

    for i in range(normal_count):
        emp_id, emp_name, dept, loc = random.choice(EMPLOYEES)
        approver_id, approver_name = random.choice(APPROVERS)
        exp_type = random.choice(EXPENSE_TYPES)
        amount = round(random.uniform(50, 3000), 2)

        if i in weekend_normals:
            sub_date = random_weekend()
            is_weekend = "Y"
        else:
            sub_date = random_weekday()
            is_weekend = "N"

        is_missing = "Y" if i in missing_receipt_normals else "N"
        receipt = "N" if is_missing == "Y" else "Y"

        approval_date = sub_date + timedelta(days=random.randint(1, 5))

        rid = f"EXP-{report_id:03d}"
        rows.append({
            "Report_ID": rid,
            "Employee_ID": emp_id,
            "Employee_Name": emp_name,
            "Department": dept,
            "Location": loc,
            "Submission_Date": sub_date.isoformat(),
            "Approval_Date": approval_date.isoformat(),
            "Approver_Name": approver_name,
            "Expense_Type": exp_type,
            "Amount_USD": amount,
            "Receipt_Attached": receipt,
            "Is_Split_Transaction": "N",
            "Is_Missing_Receipt": is_missing,
            "Is_Weekend_Submission": is_weekend,
        })
        report_id += 1

    # Sort by Report_ID
    rows.sort(key=lambda r: r["Report_ID"])

    headers = ["Report_ID", "Employee_ID", "Employee_Name", "Department", "Location",
               "Submission_Date", "Approval_Date", "Approver_Name", "Expense_Type",
               "Amount_USD", "Receipt_Attached", "Is_Split_Transaction",
               "Is_Missing_Receipt", "Is_Weekend_Submission"]

    with open("Lab 5/datasets/expense_reports.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(rows)

    print(f"expense_reports.csv: {len(rows)} rows")
    print(f"  Split transactions: {sum(1 for r in rows if r['Is_Split_Transaction'] == 'Y')}")
    print(f"  Missing receipts: {sum(1 for r in rows if r['Is_Missing_Receipt'] == 'Y')}")
    print(f"  Weekend submissions: {sum(1 for r in rows if r['Is_Weekend_Submission'] == 'Y')}")


# ============================================================
# Dataset 2: corporate_card.csv (~100 rows)
# ============================================================
def generate_corporate_card():
    MERCHANT_CATEGORIES = ["Travel", "Dining", "Office Supplies", "Fuel", "Technology", "Professional Services", "Subscriptions"]
    MERCHANTS = [
        ("Gulf Air", "Travel"), ("Emirates Airlines", "Travel"),
        ("Al Bustan Restaurant", "Dining"), ("The Chedi Muscat", "Dining"),
        ("Carrefour", "Office Supplies"), ("Lulu Hypermarket", "Office Supplies"),
        ("Shell Oman", "Fuel"), ("ADNOC", "Fuel"),
        ("Amazon Business", "Technology"), ("Microsoft Store", "Technology"),
        ("McKinsey Oman", "Professional Services"), ("Deloitte", "Professional Services"),
        ("Netflix", "Subscriptions"), ("Spotify", "Subscriptions"),
    ]

    rows = []
    txn_id = 1

    # Personal use flagged rows (~7)
    personal_merchants = [("Netflix", "Subscriptions"), ("Spotify", "Subscriptions"),
                          ("Lulu Hypermarket", "Office Supplies")]

    # Duplicate charge pairs (~4 pairs = 8 flagged rows)
    dup_pairs = []
    for _ in range(4):
        emp = random.choice(EMPLOYEES)
        merchant, cat = random.choice([m for m in MERCHANTS if m[1] in ("Travel", "Dining", "Technology")])
        amount = round(random.uniform(200, 2000), 2)
        txn_date = date(2025, random.randint(1, 6), random.randint(1, 28))
        dup_pairs.append((emp, merchant, cat, amount, txn_date))

    # Generate duplicate pairs first
    for emp, merchant, cat, amount, txn_date in dup_pairs:
        emp_id, emp_name, dept, loc = emp
        for copy in range(2):
            tid = f"TXN-{txn_id:04d}"
            rows.append({
                "Transaction_ID": tid,
                "Employee_ID": emp_id,
                "Employee_Name": emp_name,
                "Department": dept,
                "Transaction_Date": txn_date.isoformat(),
                "Merchant_Name": merchant,
                "Merchant_Category": cat,
                "Amount_USD": amount,
                "Receipt_Provided": "Y",
                "Is_Personal_Use": "N",
                "Is_Duplicate_Charge": "Y",
                "Is_High_Value_No_Receipt": "N",
            })
            txn_id += 1

    # Generate personal use rows (~7)
    for _ in range(7):
        emp_id, emp_name, dept, loc = random.choice(EMPLOYEES)
        merchant, cat = random.choice(personal_merchants)
        amount = round(random.uniform(10, 150), 2)
        txn_date = date(2025, random.randint(1, 6), random.randint(1, 28))
        tid = f"TXN-{txn_id:04d}"
        rows.append({
            "Transaction_ID": tid,
            "Employee_ID": emp_id,
            "Employee_Name": emp_name,
            "Department": dept,
            "Transaction_Date": txn_date.isoformat(),
            "Merchant_Name": merchant,
            "Merchant_Category": cat,
            "Amount_USD": amount,
            "Receipt_Provided": "Y",
            "Is_Personal_Use": "Y",
            "Is_Duplicate_Charge": "N",
            "Is_High_Value_No_Receipt": "N",
        })
        txn_id += 1

    # Generate high-value no-receipt rows (~6)
    for _ in range(6):
        emp_id, emp_name, dept, loc = random.choice(EMPLOYEES)
        merchant, cat = random.choice([m for m in MERCHANTS if m[1] in ("Travel", "Professional Services", "Technology")])
        amount = round(random.uniform(1500, 5000), 2)
        txn_date = date(2025, random.randint(1, 6), random.randint(1, 28))
        tid = f"TXN-{txn_id:04d}"
        rows.append({
            "Transaction_ID": tid,
            "Employee_ID": emp_id,
            "Employee_Name": emp_name,
            "Department": dept,
            "Transaction_Date": txn_date.isoformat(),
            "Merchant_Name": merchant,
            "Merchant_Category": cat,
            "Amount_USD": amount,
            "Receipt_Provided": "N",
            "Is_Personal_Use": "N",
            "Is_Duplicate_Charge": "N",
            "Is_High_Value_No_Receipt": "Y",
        })
        txn_id += 1

    # Fill remaining normal rows to reach ~100
    target_total = 100
    remaining = target_total - len(rows)
    for _ in range(remaining):
        emp_id, emp_name, dept, loc = random.choice(EMPLOYEES)
        merchant, cat = random.choice(MERCHANTS)
        amount = round(random.uniform(20, 3000), 2)
        txn_date = date(2025, random.randint(1, 6), random.randint(1, 28))
        tid = f"TXN-{txn_id:04d}"
        rows.append({
            "Transaction_ID": tid,
            "Employee_ID": emp_id,
            "Employee_Name": emp_name,
            "Department": dept,
            "Transaction_Date": txn_date.isoformat(),
            "Merchant_Name": merchant,
            "Merchant_Category": cat,
            "Amount_USD": amount,
            "Receipt_Provided": "Y",
            "Is_Personal_Use": "N",
            "Is_Duplicate_Charge": "N",
            "Is_High_Value_No_Receipt": "N",
        })
        txn_id += 1

    rows.sort(key=lambda r: r["Transaction_ID"])

    headers = ["Transaction_ID", "Employee_ID", "Employee_Name", "Department",
               "Transaction_Date", "Merchant_Name", "Merchant_Category", "Amount_USD",
               "Receipt_Provided", "Is_Personal_Use", "Is_Duplicate_Charge",
               "Is_High_Value_No_Receipt"]

    with open("Lab 5/datasets/corporate_card.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(rows)

    print(f"\ncorporate_card.csv: {len(rows)} rows")
    print(f"  Personal use: {sum(1 for r in rows if r['Is_Personal_Use'] == 'Y')}")
    print(f"  Duplicate charges: {sum(1 for r in rows if r['Is_Duplicate_Charge'] == 'Y')}")
    print(f"  High-value no receipt: {sum(1 for r in rows if r['Is_High_Value_No_Receipt'] == 'Y')}")


# ============================================================
# Dataset 3: travel_bookings.csv (~60 rows)
# ============================================================
def generate_travel_bookings():
    DESTINATIONS = ["Dubai", "Riyadh", "London", "Muscat", "Doha", "Bahrain", "Abu Dhabi", "Cairo"]
    HOTEL_NAMES = ["Hilton", "Marriott", "Sheraton", "Holiday Inn", "Radisson", "InterContinental", "Crowne Plaza"]

    # Policy rates by destination
    POLICY_RATES = {
        "Dubai": 250, "Riyadh": 200, "London": 300, "Muscat": 180,
        "Doha": 220, "Bahrain": 190, "Abu Dhabi": 240, "Cairo": 150,
    }
    STANDARD_PER_DIEM = {
        "Dubai": 120, "Riyadh": 100, "London": 150, "Muscat": 90,
        "Doha": 110, "Bahrain": 95, "Abu Dhabi": 115, "Cairo": 80,
    }

    rows = []
    booking_id = 1

    # Out-of-policy hotel rates (~8)
    out_of_policy_indices = set()
    # Excessive per diem (~6)
    excessive_per_diem_indices = set()
    # Duplicate reimbursement claims (~3 pairs = 6 rows)
    dup_claim_groups = []

    # Generate duplicate claim pairs first (3 pairs)
    for _ in range(3):
        emp = random.choice(EMPLOYEES)
        dest = random.choice(DESTINATIONS)
        hotel = random.choice(HOTEL_NAMES)
        nights = random.randint(2, 5)
        travel_date = date(2025, random.randint(1, 6), random.randint(1, 28))
        return_date = travel_date + timedelta(days=nights)
        hotel_rate = POLICY_RATES[dest] - random.randint(0, 30)  # within policy
        per_diem_claimed = STANDARD_PER_DIEM[dest]
        dup_claim_groups.append((emp, dest, hotel, nights, travel_date, return_date, hotel_rate, per_diem_claimed))

    for emp, dest, hotel, nights, travel_date, return_date, hotel_rate, per_diem_claimed in dup_claim_groups:
        emp_id, emp_name, dept, loc = emp
        total_hotel = hotel_rate * nights
        total_per_diem = per_diem_claimed * nights
        for _ in range(2):
            bid = f"TRV-{booking_id:03d}"
            rows.append({
                "Booking_ID": bid,
                "Employee_ID": emp_id,
                "Employee_Name": emp_name,
                "Department": dept,
                "Destination": dest,
                "Travel_Date": travel_date.isoformat(),
                "Return_Date": return_date.isoformat(),
                "Nights": nights,
                "Hotel_Name": hotel,
                "Hotel_Rate_Per_Night": hotel_rate,
                "Total_Hotel_Cost": total_hotel,
                "Policy_Rate_Per_Night": POLICY_RATES[dest],
                "Per_Diem_Claimed": per_diem_claimed,
                "Standard_Per_Diem": STANDARD_PER_DIEM[dest],
                "Total_Per_Diem": total_per_diem,
                "Is_Out_Of_Policy": "N",
                "Is_Excessive_Per_Diem": "N",
                "Is_Duplicate_Claim": "Y",
            })
            booking_id += 1

    # Now generate the rest to reach ~60
    target = 60
    remaining = target - len(rows)

    # Decide which of the remaining rows are out-of-policy (~8) and excessive per diem (~6)
    remaining_indices = list(range(remaining))
    oop_indices = set(random.sample(remaining_indices, 8))
    non_oop = [i for i in remaining_indices if i not in oop_indices]
    epd_indices = set(random.sample(non_oop, 6))

    for i in range(remaining):
        emp_id, emp_name, dept, loc = random.choice(EMPLOYEES)
        dest = random.choice(DESTINATIONS)
        hotel = random.choice(HOTEL_NAMES)
        nights = random.randint(1, 7)
        travel_date = date(2025, random.randint(1, 6), random.randint(1, 28))
        return_date = travel_date + timedelta(days=nights)

        policy_rate = POLICY_RATES[dest]
        std_per_diem = STANDARD_PER_DIEM[dest]

        if i in oop_indices:
            # Out of policy: hotel rate 20-60% above policy
            hotel_rate = round(policy_rate * random.uniform(1.20, 1.60))
            is_oop = "Y"
        else:
            hotel_rate = policy_rate - random.randint(0, 40)
            is_oop = "N"

        if i in epd_indices:
            # Excessive per diem: 30-80% above standard
            per_diem_claimed = round(std_per_diem * random.uniform(1.30, 1.80))
            is_epd = "Y"
        else:
            per_diem_claimed = std_per_diem
            is_epd = "N"

        total_hotel = hotel_rate * nights
        total_per_diem = per_diem_claimed * nights

        bid = f"TRV-{booking_id:03d}"
        rows.append({
            "Booking_ID": bid,
            "Employee_ID": emp_id,
            "Employee_Name": emp_name,
            "Department": dept,
            "Destination": dest,
            "Travel_Date": travel_date.isoformat(),
            "Return_Date": return_date.isoformat(),
            "Nights": nights,
            "Hotel_Name": hotel,
            "Hotel_Rate_Per_Night": hotel_rate,
            "Total_Hotel_Cost": total_hotel,
            "Policy_Rate_Per_Night": POLICY_RATES[dest],
            "Per_Diem_Claimed": per_diem_claimed,
            "Standard_Per_Diem": STANDARD_PER_DIEM[dest],
            "Total_Per_Diem": total_per_diem,
            "Is_Out_Of_Policy": is_oop,
            "Is_Excessive_Per_Diem": is_epd,
            "Is_Duplicate_Claim": "N",
        })
        booking_id += 1

    rows.sort(key=lambda r: r["Booking_ID"])

    headers = ["Booking_ID", "Employee_ID", "Employee_Name", "Department", "Destination",
               "Travel_Date", "Return_Date", "Nights", "Hotel_Name", "Hotel_Rate_Per_Night",
               "Total_Hotel_Cost", "Policy_Rate_Per_Night", "Per_Diem_Claimed",
               "Standard_Per_Diem", "Total_Per_Diem", "Is_Out_Of_Policy",
               "Is_Excessive_Per_Diem", "Is_Duplicate_Claim"]

    with open("Lab 5/datasets/travel_bookings.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(rows)

    print(f"\ntravel_bookings.csv: {len(rows)} rows")
    print(f"  Out-of-policy hotel: {sum(1 for r in rows if r['Is_Out_Of_Policy'] == 'Y')}")
    print(f"  Excessive per diem: {sum(1 for r in rows if r['Is_Excessive_Per_Diem'] == 'Y')}")
    print(f"  Duplicate claims: {sum(1 for r in rows if r['Is_Duplicate_Claim'] == 'Y')}")


if __name__ == "__main__":
    generate_expense_reports()
    generate_corporate_card()
    generate_travel_bookings()
    print("\nAll datasets generated successfully.")
