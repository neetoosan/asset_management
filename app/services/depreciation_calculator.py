"""
Depreciation Calculator with First-Year Proration

Implements the correct depreciation logic:
1. Depreciation calculated every year on December 31st
2. First-year depreciation is prorated based on purchase month
3. After first year, full yearly depreciation is applied
4. Stop when net book value == residual value OR useful life completed
"""

from datetime import date, datetime
from typing import Dict, Union


class DepreciationCalculator:
    """Calculate depreciation with first-year proration and residual value checks"""
    
    @staticmethod
    def calculate_yearly_depreciation(cost: float, residual_value: float, useful_life: int) -> float:
        """
        Calculate yearly depreciation amount using straight-line method.
        
        Args:
            cost: Total asset cost
            residual_value: Salvage/residual value at end of life
            useful_life: Useful life in years
            
        Returns:
            Yearly depreciation amount
        """
        if useful_life <= 0:
            return 0.0
        
        depreciable_amount = cost - residual_value
        yearly_depreciation = depreciable_amount / useful_life
        
        return yearly_depreciation
    
    @staticmethod
    def calculate_monthly_depreciation(cost: float, residual_value: float, useful_life: int) -> float:
        """
        Calculate monthly depreciation amount.
        
        Args:
            cost: Total asset cost
            residual_value: Salvage/residual value at end of life
            useful_life: Useful life in years
            
        Returns:
            Monthly depreciation amount
        """
        yearly_depreciation = DepreciationCalculator.calculate_yearly_depreciation(
            cost, residual_value, useful_life
        )
        monthly_depreciation = yearly_depreciation / 12.0
        
        return monthly_depreciation
    
    @staticmethod
    def calculate_months_used_in_first_year(purchase_date: Union[date, datetime, str]) -> int:
        """
        Calculate number of months used before year end (including purchase month).
        
        Formula: months_used = 12 - purchase_month + 1
        
        Args:
            purchase_date: Date asset was purchased (date object or ISO string)
            
        Returns:
            Number of months from purchase to end of year (1-12)
            
        Example:
            Purchase in October (month 10): 12 - 10 + 1 = 3 months
            Purchase in January (month 1): 12 - 1 + 1 = 12 months
            Purchase in December (month 12): 12 - 12 + 1 = 1 month
        """
        # Convert to date object if string
        if isinstance(purchase_date, str):
            purchase_date = datetime.fromisoformat(purchase_date.split('T')[0]).date()
        elif isinstance(purchase_date, datetime):
            purchase_date = purchase_date.date()
        
        purchase_month = purchase_date.month
        months_used = 12 - purchase_month + 1
        
        return months_used
    
    @staticmethod
    def calculate_first_year_depreciation(
        cost: float, 
        residual_value: float, 
        useful_life: int, 
        purchase_date: Union[date, datetime, str]
    ) -> float:
        """
        Calculate prorated first-year depreciation based on purchase month.
        
        Args:
            cost: Total asset cost
            residual_value: Salvage/residual value at end of life
            useful_life: Useful life in years
            purchase_date: Date asset was purchased
            
        Returns:
            First year depreciation amount (prorated)
            
        Example:
            Cost: 500,000
            Residual: 50,000
            Useful life: 5 years
            Purchase: October 15 (month 10)
            
            Yearly depreciation: (500,000 - 50,000) / 5 = 90,000
            Monthly depreciation: 90,000 / 12 = 7,500
            Months used: 12 - 10 + 1 = 3
            First year: 7,500 * 3 = 22,500
        """
        monthly_depreciation = DepreciationCalculator.calculate_monthly_depreciation(
            cost, residual_value, useful_life
        )
        
        months_used = DepreciationCalculator.calculate_months_used_in_first_year(purchase_date)
        
        first_year_depreciation = monthly_depreciation * months_used
        
        return first_year_depreciation
    
    @staticmethod
    def calculate_depreciation_for_year(
        cost: float,
        residual_value: float,
        useful_life: int,
        purchase_date: Union[date, datetime, str],
        depreciation_years_applied: int,
        current_net_book_value: float
    ) -> Dict[str, float]:
        """
        Calculate depreciation for a specific year, accounting for first-year proration.
        
        Args:
            cost: Total asset cost
            residual_value: Salvage/residual value
            useful_life: Useful life in years
            purchase_date: Date asset was purchased
            depreciation_years_applied: Number of Dec 31 depreciations already applied
            current_net_book_value: Current net book value
            
        Returns:
            Dictionary with:
                - depreciation_to_apply: Amount to depreciate this year
                - new_accumulated_depreciation: Total accumulated after this year
                - new_net_book_value: NBV after this year
                - should_continue: Whether depreciation should continue
                - reason: Reason if stopped
        """
        # Check if useful life is completed (check this FIRST)
        if depreciation_years_applied >= useful_life:
            return {
                'depreciation_to_apply': 0.0,
                'new_accumulated_depreciation': cost - current_net_book_value,
                'new_net_book_value': current_net_book_value,
                'should_continue': False,
                'reason': 'Useful life completed'
            }
        
        # Check if already fully depreciated
        if current_net_book_value <= residual_value:
            return {
                'depreciation_to_apply': 0.0,
                'new_accumulated_depreciation': cost - current_net_book_value,
                'new_net_book_value': current_net_book_value,
                'should_continue': False,
                'reason': 'Net book value has reached residual value'
            }
        
        # Determine if this is first year or subsequent year
        is_first_year = (depreciation_years_applied == 0)
        
        if is_first_year:
            # First year: prorated depreciation
            depreciation_amount = DepreciationCalculator.calculate_first_year_depreciation(
                cost, residual_value, useful_life, purchase_date
            )
        else:
            # Subsequent years: full yearly depreciation
            depreciation_amount = DepreciationCalculator.calculate_yearly_depreciation(
                cost, residual_value, useful_life
            )
        
        # Calculate new values
        current_accumulated = cost - current_net_book_value
        new_accumulated = current_accumulated + depreciation_amount
        new_net_book_value = cost - new_accumulated
        
        # Don't let net book value go below residual value
        if new_net_book_value < residual_value:
            # Adjust depreciation to bring NBV exactly to residual value
            depreciation_amount = current_net_book_value - residual_value
            new_accumulated = cost - residual_value
            new_net_book_value = residual_value
        
        return {
            'depreciation_to_apply': depreciation_amount,
            'new_accumulated_depreciation': new_accumulated,
            'new_net_book_value': new_net_book_value,
            'should_continue': new_net_book_value > residual_value and (depreciation_years_applied + 1) < useful_life,
            'reason': None
        }


# Test the calculator with the example provided
if __name__ == "__main__":
    # INPUTS from example
    cost = 500000
    residual_value = 50000
    useful_life = 5
    purchase_date = "2025-10-15"   # October 15th
    
    # Calculate first year depreciation
    first_year_dep = DepreciationCalculator.calculate_first_year_depreciation(
        cost, residual_value, useful_life, purchase_date
    )
    
    print(f"Cost: ₦{cost:,.2f}")
    print(f"Residual Value: ₦{residual_value:,.2f}")
    print(f"Useful Life: {useful_life} years")
    print(f"Purchase Date: {purchase_date}")
    print(f"\nFirst Year Depreciation: ₦{first_year_dep:,.2f}")
    
    # Show breakdown
    yearly_dep = DepreciationCalculator.calculate_yearly_depreciation(cost, residual_value, useful_life)
    monthly_dep = DepreciationCalculator.calculate_monthly_depreciation(cost, residual_value, useful_life)
    months_used = DepreciationCalculator.calculate_months_used_in_first_year(purchase_date)
    
    print(f"\nBreakdown:")
    print(f"  Yearly depreciation: ₦{yearly_dep:,.2f}")
    print(f"  Monthly depreciation: ₦{monthly_dep:,.2f}")
    print(f"  Months used in first year: {months_used}")
    print(f"  First year depreciation: ₦{monthly_dep:,.2f} × {months_used} = ₦{first_year_dep:,.2f}")
    
    # Simulate depreciation over 5 years
    print(f"\n{'='*80}")
    print(f"DEPRECIATION SCHEDULE")
    print(f"{'='*80}")
    
    current_nbv = cost
    accumulated = 0.0
    years_applied = 0
    
    print(f"{'Year':<6} {'Depreciation':>15} {'Accumulated':>15} {'Net Book Value':>18}")
    print(f"{'-'*60}")
    print(f"{'Start':<6} {'-':>15} ₦{accumulated:>13,.2f} ₦{current_nbv:>16,.2f}")
    
    for year in range(1, useful_life + 2):  # +2 to show it stops
        result = DepreciationCalculator.calculate_depreciation_for_year(
            cost, residual_value, useful_life, purchase_date, years_applied, current_nbv
        )
        
        if result['depreciation_to_apply'] > 0:
            print(f"{year:<6} ₦{result['depreciation_to_apply']:>13,.2f} ₦{result['new_accumulated_depreciation']:>13,.2f} ₦{result['new_net_book_value']:>16,.2f}")
            accumulated = result['new_accumulated_depreciation']
            current_nbv = result['new_net_book_value']
            years_applied += 1
        else:
            print(f"{year:<6} {'STOPPED':>15} ₦{accumulated:>13,.2f} ₦{current_nbv:>16,.2f}")
            print(f"       Reason: {result['reason']}")
            break
