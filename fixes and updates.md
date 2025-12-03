
2025-10-29
- Fixed asset edit/save crash (DetachedInstanceError)
	- `app/gui/dialogs/asset_dialog.py`: always use id or primitive dict; fetch fresh data before editing
	- `app/gui/main_window.py`: pass `asset_id` to dialog instead of ORM object
	- `app/services/asset_service.py`: update flow re-queries asset on same session after commit; avoid `session.refresh()` on detached instances

- UI tweaks
	- `app/gui/ui/admin_screen.ui`: added bold "ADMIN" header and `RECYCLE` button
	- `app/gui/views/admin_screen.py`: wired `recycleBtn` to open Recently Deleted dialog

Next
- Sweep repo for any remaining places that pass ORM Asset instances into UI or services and convert them to ids/dicts
- Add pytest for edit -> save flow after sweep

