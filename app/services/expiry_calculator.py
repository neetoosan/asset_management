"""
End of Useful Life Calculator using Dec 31 Depreciation Logic

Every Dec 31 is a universal depreciation point where useful_life decreases by 1.
The remaining useful life = original_useful_life - (number of Dec 31s since acquisition)
"""

from datetime import datetime, date, timedelta
from typing import Union


class ExpiryCalculator:
    """Calculate asset end of useful life dates using Dec 31 depreciation cycles"""
    
    @staticmethod
    def count_dec31_since_acquisition(acquisition_date: Union[date, datetime], evaluation_date: Union[date, datetime] = None) -> int:
        """
        Count how many Dec 31 dates have passed between acquisition and evaluation.
        
        Args:
            acquisition_date: Date asset was acquired
            evaluation_date: Date to evaluate from (default: today)
        
        Returns:
            Number of Dec 31 dates (inclusive) between acquisition and evaluation
        
        Example:
            Acquired: 2023-12-30, Evaluation: 2025-06-15
            Dec 31s: 2023-12-31, 2024-12-31 → count = 2
        """
        if evaluation_date is None:
            evaluation_date = datetime.now().date()
        
        # Convert to date objects if datetime provided
        if isinstance(acquisition_date, datetime):
            acquisition_date = acquisition_date.date()
        if isinstance(evaluation_date, datetime):
            evaluation_date = evaluation_date.date()
        
        # Count Dec 31s from acquisition year through evaluation year
        count = 0
        start_year = acquisition_date.year
        end_year = evaluation_date.year
        
        for year in range(start_year, end_year + 1):
            dec31 = date(year, 12, 31)
            # Dec 31 must be >= acquisition_date and <= evaluation_date
            if acquisition_date <= dec31 <= evaluation_date:
                count += 1
        
        return count
    
    @staticmethod
    def calculate_remaining_useful_life(original_useful_life: float, acquisition_date: Union[date, datetime], 
                                       evaluation_date: Union[date, datetime] = None) -> float:
        """
        Calculate remaining useful life after accounting for Dec 31 depreciations.
        
        Formula: L_r = max(0, L_0 - D)
        where D = number of Dec 31s since acquisition
        
        Args:
            original_useful_life: Original useful life in years (can be fractional)
            acquisition_date: Date asset was acquired
            evaluation_date: Date to evaluate from (default: today)
        
        Returns:
            Remaining useful life (minimum 0)
        
        Example:
            Original: 5.5 years, Acquired: 2023-12-30, Evaluated: 2025-06-15
            D = 2 Dec 31s → Remaining = 5.5 - 2 = 3.5 years
        """
        dec31_count = ExpiryCalculator.count_dec31_since_acquisition(acquisition_date, evaluation_date)
        remaining = max(0, original_useful_life - dec31_count)
        return remaining
    
    @staticmethod
    def calculate_expiry_date(acquisition_date: Union[date, datetime], original_useful_life: float, 
                            evaluation_date: Union[date, datetime] = None) -> date:
        """
        Calculate end of useful life date using Dec 31 depreciation logic.
        
        Steps:
        1. Count Dec 31s since acquisition (D)
        2. Calculate remaining life: L_r = max(0, L_0 - D)
        3. Expiry = evaluation_date + L_r years
        
        Args:
            acquisition_date: Date asset was acquired
            original_useful_life: Original useful life in years (can be fractional)
            evaluation_date: Date to evaluate from (default: today)
        
        Returns:
            Calculated expiry date
        
        Example:
            Acquired: 2025-11-11, Useful life: 4 years, Eval: 2025-11-12
            D = 0 (no Dec 31 yet passed)
            Remaining = 4 - 0 = 4 years
            Expiry = 2025-11-12 + 4 years = 2029-11-12
            (but then Dec 31 2025 hits → Remaining = 3, Expiry = 2028-12-31)
        """
        if evaluation_date is None:
            evaluation_date = datetime.now().date()
        
        # Convert to date if datetime provided
        if isinstance(evaluation_date, datetime):
            evaluation_date = evaluation_date.date()
        if isinstance(acquisition_date, datetime):
            acquisition_date = acquisition_date.date()
        
        # Calculate remaining useful life
        remaining_life = ExpiryCalculator.calculate_remaining_useful_life(
            original_useful_life, acquisition_date, evaluation_date
        )
        
        # If no remaining life, expiry is today
        if remaining_life <= 0:
            return evaluation_date
        
        # Add remaining years to evaluation date
        # Convert fractional years to days (1 year = 365.25 days for accuracy)
        days_to_add = int(remaining_life * 365.25)
        expiry_date = evaluation_date + timedelta(days=days_to_add)
        
        return expiry_date
    
    @staticmethod
    def calculate_expiry_date_aligned_to_year_end(acquisition_date: Union[date, datetime], original_useful_life: float,
                                                   evaluation_date: Union[date, datetime] = None) -> date:
        """
        Calculate expiry date aligned to Dec 31 (accounting standard).
        
        Instead of expiry = evaluation_date + L_r years,
        use expiry = Dec 31 of (current_year + floor(L_r))
        
        Args:
            acquisition_date: Date asset was acquired
            original_useful_life: Original useful life in years
            evaluation_date: Date to evaluate from (default: today)
        
        Returns:
            Expiry date (always Dec 31)
        
        Example:
            Acquired: 2025-11-11, Useful life: 4, Evaluated: 2025-11-12
            D = 0, Remaining = 4
            Expiry = Dec 31 of (2025 + 4) = 2029-12-31
        """
        if evaluation_date is None:
            evaluation_date = datetime.now().date()
        
        if isinstance(evaluation_date, datetime):
            evaluation_date = evaluation_date.date()
        if isinstance(acquisition_date, datetime):
            acquisition_date = acquisition_date.date()
        
        # Calculate remaining useful life
        remaining_life = ExpiryCalculator.calculate_remaining_useful_life(
            original_useful_life, acquisition_date, evaluation_date
        )
        
        if remaining_life <= 0:
            return date(evaluation_date.year, 12, 31)
        
        # Expiry = Dec 31 of (current_year + floor(remaining_life))
        expiry_year = evaluation_date.year + int(remaining_life)
        expiry_date = date(expiry_year, 12, 31)
        
        return expiry_date


# Example usage
if __name__ == "__main__":
    # Example from requirements
    acq = date(2025, 11, 11)
    useful_life = 4
    today = date(2025, 11, 12)
    
    dec31s = ExpiryCalculator.count_dec31_since_acquisition(acq, today)
    remaining = ExpiryCalculator.calculate_remaining_useful_life(useful_life, acq, today)
    expiry = ExpiryCalculator.calculate_expiry_date(acq, useful_life, today)
    
    print(f"Acquired: {acq}")
    print(f"Original useful life: {useful_life} years")
    print(f"Evaluation date: {today}")
    print(f"Dec 31s passed: {dec31s}")
    print(f"Remaining useful life: {remaining} years")
    print(f"Expiry date: {expiry}")
    print()
    
    # After Dec 31, 2025
    after_year_end = date(2026, 1, 1)
    dec31s_after = ExpiryCalculator.count_dec31_since_acquisition(acq, after_year_end)
    remaining_after = ExpiryCalculator.calculate_remaining_useful_life(useful_life, acq, after_year_end)
    expiry_after = ExpiryCalculator.calculate_expiry_date(acq, useful_life, after_year_end)
    
    print(f"After Dec 31, 2025:")
    print(f"Evaluation date: {after_year_end}")
    print(f"Dec 31s passed: {dec31s_after}")
    print(f"Remaining useful life: {remaining_after} years")
    print(f"Expiry date: {expiry_after}")
