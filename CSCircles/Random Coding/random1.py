minimal_withdrawal = 10
withdrawal_percentage = 0.021

def withdrawal_amount(balance):
    if balance < minimal_withdrawal:
        return balance
    else:
        return max(balance * withdrawal_percentage, minimal_withdrawal)

print(withdrawal_amount(1000))
print(withdrawal_amount(600))
print(withdrawal_amount(25))
print(withdrawal_amount(8))