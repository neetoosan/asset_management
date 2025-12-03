"""
Year-End Accounting Service

Handles year-end depreciation updates on December 31st.
- Reduces useful_life by 1 year
- Recalculates expiry_date based on new remaining useful life
- Updates accumulated_depreciation
- Records audit trail
"""

from datetime import datetime, timedelta, date
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from app.core.models import Asset
from app.core.database import get_db_session
from app.services.audit_service import AuditService
from app.services.expiry_calculator import ExpiryCalculator
from app.services.depreciation_calculator import DepreciationCalculator


class YearEndService:
    """Service to handle year-end accounting for assets"""
    
    def __init__(self):
        self.audit_service = AuditService()
    
    def is_year_end(self, target_date: datetime = None) -> bool:
        """Check if today is December 31st or a specified date is Dec 31"""
        check_date = target_date or datetime.utcnow()
        return check_date.month == 12 and check_date.day == 31
    
    def process_year_end_depreciation(self, session: Session = None) -> Dict[str, Any]:
        """
        Process year-end depreciation for all active assets.
        
        On December 31st, for each asset:
        1. Reduce useful_life by 1 year
        2. Recalculate expiry_date based on new remaining useful life
        3. Apply annual depreciation to accumulated_depreciation
        4. Update net_book_value
        5. Record audit trail
        
        Returns:
            Dictionary with processing results
        """
        if not self.is_year_end():
            return {
                "success": False,
                "message": "Year-end processing only runs on December 31st",
                "processed_count": 0
            }
        
        close_session = False
        if session is None:
            session = get_db_session()
            close_session = True
        
        try:
            # Get all active assets
            assets = session.query(Asset).filter(
                Asset.status.in_(['Available', 'In Use', 'Under Maintenance'])
            ).all()
            
            processed_count = 0
            updated_assets = []
            
            today = datetime.utcnow().date()
            
            for asset in assets:
                try:
                    old_values = {
                        'useful_life': asset.useful_life,
                        'expiry_date': asset.expiry_date.isoformat() if asset.expiry_date else None,
                        'accumulated_depreciation': asset.accumulated_depreciation,
                        'net_book_value': asset.net_book_value,
                        'depreciation_years_applied': asset.depreciation_years_applied if hasattr(asset, 'depreciation_years_applied') else 0
                    }
                    
                    # Skip if missing required data
                    if not asset.acquisition_date or not asset.useful_life or not asset.total_cost:
                        continue
                    
                    # Ensure salvage_value exists (default to 10% if not set)
                    if not hasattr(asset, 'salvage_value') or asset.salvage_value is None:
                        asset.salvage_value = asset.total_cost * 0.10
                    
                    # Ensure depreciation_years_applied exists
                    if not hasattr(asset, 'depreciation_years_applied') or asset.depreciation_years_applied is None:
                        asset.depreciation_years_applied = 0
                    
                    # Calculate depreciation using the new prorated logic
                    depreciation_result = DepreciationCalculator.calculate_depreciation_for_year(
                        cost=asset.total_cost,
                        residual_value=asset.salvage_value,
                        useful_life=asset.useful_life,
                        purchase_date=asset.acquisition_date,
                        depreciation_years_applied=asset.depreciation_years_applied,
                        current_net_book_value=asset.net_book_value
                    )
                    
                    # Only apply depreciation if should_continue is True or depreciation_to_apply > 0
                    if depreciation_result['depreciation_to_apply'] > 0:
                        # Apply the calculated depreciation
                        asset.accumulated_depreciation = depreciation_result['new_accumulated_depreciation']
                        asset.net_book_value = depreciation_result['new_net_book_value']
                        asset.depreciation_years_applied += 1
                        
                        # Recalculate expiry date based on remaining useful life - aligned to Dec 31
                        if asset.acquisition_date and asset.useful_life:
                            new_expiry = ExpiryCalculator.calculate_expiry_date_aligned_to_year_end(
                                asset.acquisition_date, 
                                asset.useful_life,
                                today
                            )
                            asset.expiry_date = new_expiry
                    else:
                        # Depreciation stopped - log the reason
                        print(f"Asset {asset.asset_id}: Depreciation stopped - {depreciation_result['reason']}")
                    
                    new_values = {
                        'useful_life': asset.useful_life,
                        'expiry_date': asset.expiry_date.isoformat() if asset.expiry_date else None,
                        'accumulated_depreciation': asset.accumulated_depreciation,
                        'net_book_value': asset.net_book_value,
                        'depreciation_years_applied': asset.depreciation_years_applied
                    }
                    
                    # 5. Record audit trail
                    self.audit_service.log_action(
                        action='YEAR_END_DEPRECIATION',
                        table_name='assets',
                        record_id=str(asset.id),
                        description=f'Year-end depreciation update for asset {asset.asset_id} (Year {asset.depreciation_years_applied})',
                        old_values=str(old_values),
                        new_values=str(new_values)
                    )
                    
                    depreciation_applied = depreciation_result['depreciation_to_apply'] if depreciation_result['depreciation_to_apply'] > 0 else 0
                    
                    updated_assets.append({
                        'asset_id': asset.asset_id,
                        'asset_name': asset.name,
                        'old_useful_life': old_values['useful_life'],
                        'new_useful_life': asset.useful_life,
                        'old_expiry_date': old_values['expiry_date'],
                        'new_expiry_date': new_values['expiry_date'],
                        'depreciation_applied': depreciation_applied,
                        'depreciation_years_applied': asset.depreciation_years_applied,
                        'is_first_year': asset.depreciation_years_applied == 1,
                        'stopped': depreciation_result['depreciation_to_apply'] == 0,
                        'stop_reason': depreciation_result.get('reason')
                    })
                    
                    processed_count += 1
                    
                except Exception as e:
                    print(f"Error processing asset {asset.asset_id}: {e}")
                    continue
            
            # Commit changes
            session.commit()
            
            return {
                "success": True,
                "message": f"Year-end depreciation processed for {processed_count} assets",
                "processed_count": processed_count,
                "updated_assets": updated_assets
            }
        
        except Exception as e:
            session.rollback()
            return {
                "success": False,
                "message": f"Error processing year-end depreciation: {str(e)}",
                "processed_count": 0,
                "error": str(e)
            }
        
        finally:
            if close_session:
                session.close()
    
    def calculate_new_expiry_date(self, acquisition_date, remaining_useful_life: int) -> datetime:
        """
        Calculate new expiry date based on acquisition date and remaining useful life
        
        Args:
            acquisition_date: Original acquisition date of the asset
            remaining_useful_life: Years of useful life remaining
            
        Returns:
            New expiry date (acquisition_date + remaining_useful_life years)
        """
        if not acquisition_date or remaining_useful_life <= 0:
            return datetime.utcnow().date()
        
        return acquisition_date + timedelta(days=remaining_useful_life * 365)
    
    def get_asset_year_end_summary(self, session: Session = None) -> Dict[str, Any]:
        """
        Get summary of assets that will be affected by year-end processing
        
        Returns:
            Summary with asset counts, total depreciation to be applied, etc.
        """
        close_session = False
        if session is None:
            session = get_db_session()
            close_session = True
        
        try:
            # Get all active assets
            assets = session.query(Asset).filter(
                Asset.status.in_(['Available', 'In Use', 'Under Maintenance'])
            ).all()
            
            total_assets = len(assets)
            assets_with_useful_life = sum(1 for a in assets if a.useful_life and a.useful_life > 0)
            total_depreciation_to_apply = 0.0
            
            for asset in assets:
                if hasattr(asset, 'depreciation_percentage') and asset.depreciation_percentage and asset.total_cost:
                    annual_depreciation = asset.total_cost * (asset.depreciation_percentage / 100.0)
                    total_depreciation_to_apply += annual_depreciation
            
            return {
                "total_active_assets": total_assets,
                "assets_with_useful_life": assets_with_useful_life,
                "total_depreciation_to_apply": total_depreciation_to_apply,
                "processing_date": datetime.utcnow().date().isoformat(),
                "ready_to_process": self.is_year_end()
            }
        
        finally:
            if close_session:
                session.close()
    
    def manually_trigger_year_end(self, session: Session = None) -> Dict[str, Any]:
        """
        Manually trigger year-end processing (for testing or administrative purposes)
        
        Returns:
            Processing results
        """
        return self.process_year_end_depreciation(session)
