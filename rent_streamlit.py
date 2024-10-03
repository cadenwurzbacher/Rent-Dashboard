import streamlit as st

# Roommates and rent details
roommates = ["Caden", "Rahul", "John", "Brady"]
total_rent = 3150
parking_fee = 185
internet_fee = 75

# Input fields for variable expenses
electric = st.number_input("Enter electric bill (Rahul pays):", value=0.0)
admin_fee = st.number_input("Enter admin fee:", value=0.0)
water_sewer = st.number_input("Enter water/sewer bill:", value=0.0)
trash = st.number_input("Enter trash bill:", value=0.0)

# Adjustment inputs for each roommate (if they paid extra or not enough)
rahul_paid = st.number_input("Rahul already paid:", value=0.0)
john_paid = st.number_input("John already paid:", value=0.0)
brady_paid = st.number_input("Brady already paid:", value=0.0)
caden_paid = st.number_input("Caden already paid:", value=0.0)

# Calculate total shared expenses
total_shared_expenses = total_rent + internet_fee + electric + admin_fee + water_sewer + trash
per_person_expense = total_shared_expenses / 4

# Calculate individual totals
caden_total = per_person_expense + parking_fee  # Caden pays parking
rahul_total = per_person_expense
john_total = per_person_expense
brady_total = per_person_expense

# Calculate the balance for each person
rahul_balance = rahul_total - rahul_paid
caden_balance = caden_total - caden_paid
john_balance = john_total - john_paid
brady_balance = brady_total - brady_paid

# Display the breakdown for each person
st.write(f"### Monthly Payments Breakdown")
st.write(f"**Caden** owes: ${caden_balance:.2f} (Rent: ${total_rent / 4:.2f}, Parking: ${parking_fee:.2f}, Internet: ${internet_fee / 4:.2f}, Electric: ${electric / 4:.2f}, Admin: ${admin_fee / 4:.2f}, Water/Sewer: ${water_sewer / 4:.2f}, Trash: ${trash / 4:.2f})")
st.write(f"**Rahul** owes: ${rahul_balance:.2f} (Rent: ${total_rent / 4:.2f}, Internet: ${internet_fee / 4:.2f}, Electric: ${electric / 4:.2f}, Admin: ${admin_fee / 4:.2f}, Water/Sewer: ${water_sewer / 4:.2f}, Trash: ${trash / 4:.2f})")
st.write(f"**John** owes: ${john_balance:.2f} (Rent: ${total_rent / 4:.2f}, Internet: ${internet_fee / 4:.2f}, Electric: ${electric / 4:.2f}, Admin: ${admin_fee / 4:.2f}, Water/Sewer: ${water_sewer / 4:.2f}, Trash: ${trash / 4:.2f})")
st.write(f"**Brady** owes: ${brady_balance:.2f} (Rent: ${total_rent / 4:.2f}, Internet: ${internet_fee / 4:.2f}, Electric: ${electric / 4:.2f}, Admin: ${admin_fee / 4:.2f}, Water/Sewer: ${water_sewer / 4:.2f}, Trash: ${trash / 4:.2f})")

# Now calculate transactions to minimize payments

# Store balances and classify them as "owe" or "to be reimbursed"
owed = {
    "Caden": caden_balance,
    "Rahul": rahul_balance,
    "John": john_balance,
    "Brady": brady_balance
}

# Simplify the transactions by paying back the ones owed the most first
def settle_debts(owed):
    # Separate into those who owe money and those who should be reimbursed
    owe_money = {person: amount for person, amount in owed.items() if amount > 0}
    to_be_paid = {person: -amount for person, amount in owed.items() if amount < 0}
    
    transactions = []
    
    # Iterate over a copy of the items in to_be_paid to avoid modifying the dict while iterating
    for person_who_owes, amount_owed in owe_money.items():
        for person_to_pay, amount_to_receive in list(to_be_paid.items()):  # Create a copy here
            if amount_owed == 0:
                break
            # Pay the smaller of the two amounts
            payment_amount = min(amount_owed, amount_to_receive)
            transactions.append((person_who_owes, person_to_pay, payment_amount))
            # Update the balances
            owe_money[person_who_owes] -= payment_amount
            to_be_paid[person_to_pay] -= payment_amount
            # If the person has been fully reimbursed, remove them from to_be_paid
            if to_be_paid[person_to_pay] == 0:
                del to_be_paid[person_to_pay]
    
    return transactions

# Settle the debts and display the transactions
transactions = settle_debts(owed)

# Display the payment instructions
st.write("### Payment Instructions to Minimize Venmo Transactions")
for transaction in transactions:
    payer, payee, amount = transaction
    st.write(f"**{payer}** should pay **{payee}**: ${amount:.2f}")
