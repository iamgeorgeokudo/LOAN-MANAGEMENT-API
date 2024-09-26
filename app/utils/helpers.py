def calculate_total_repayment(principal, interest_rate, term):
    """
    Calculate the total repayment for a loan.
    """
    interest = principal * (interest_rate / 100) * (term / 12)
    return principal + interest

def calculate_monthly_repayment(principal, interest_rate, term):
    """
    Calculate the monthly repayment for a loan.
    """
    total_repayment = calculate_total_repayment(principal, interest_rate, term)
    return total_repayment / term