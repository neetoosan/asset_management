import sys
from pathlib import Path
from uuid import uuid4

# add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.asset_service import AssetService
from app.core.database import init_db

# Initialize a local SQLite database for tests to avoid needing the
# project's production/remote database. This ensures tests can run
# in isolation on CI or local machines.
init_db("sqlite:///./tests/test_db.sqlite")


def test_create_high_value_asset_and_fields():
    """Create a high-value asset and verify model/serial/location are persisted.

    This test creates an asset with a unique asset_id, asserts the create
    call succeeds, fetches the created asset and checks that the
    `model_number`, `serial_number` and `location` fields are present and
    match what was supplied. The created asset is deleted at the end.
    """
    svc = AssetService()

    unique_id = f"TEST-{uuid4()}"
    payload = {
        "asset_id": unique_id,
        "description": "Test asset for high-value create",
        "name": "Test Asset",
        "category_id": None,
        "subcategory_id": None,
        "acquisition_date": None,
        "supplier": "UnitTest Supplier",
        "quantity": 1,
        "unit_cost": 20000.00,
        "total_cost": 20000.00,
        "useful_life": 5,
        "depreciation_method": "STRAIGHT_LINE",
        "accumulated_depreciation": 0.0,
        "net_book_value": 20000.0,
        "location": "UNIT_TEST_LOCATION",
        "model_number": "MODEL-UT-123",
        "serial_number": "SN-UT-456",
        "custodian": "unittest",
        "remarks": "cleanup-after-test",
        "status": "Available",
        "department": "Testing",
    }

    # Create asset
    res = svc.create_asset(payload)
    assert res.get("success") is True, f"Create failed: {res}"

    created = res.get("asset")
    assert created is not None, "No asset returned from create_asset"

    # Verify fields are present and match
    assert created.get("asset_id") == unique_id
    assert created.get("model_number") == payload["model_number"]
    assert created.get("serial_number") == payload["serial_number"]
    assert created.get("location") == payload["location"]

    # Fetch again via service getter
    fetched = svc.get_asset_by_asset_id(unique_id)
    assert fetched is not None, "get_asset_by_asset_id returned None"
    assert fetched.get("model_number") == payload["model_number"]
    assert fetched.get("serial_number") == payload["serial_number"]
    assert fetched.get("location") == payload["location"]

    # Cleanup: delete the created asset using the numeric id
    try:
        created_id = created.get("id")
        if created_id:
            svc.delete_asset(created_id, reason="test cleanup")
    except Exception:
        # Non-fatal cleanup failure
        pass


if __name__ == "__main__":
    test_create_high_value_asset_and_fields()
