import json
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_

from ..core.database import get_db
from ..core.models import AuditLog, User

# Module-level globals to allow newly created AuditService instances to
# pick up the current user context without requiring every caller to
# set the user on each AuditService instance.
_GLOBAL_AUDIT_USER_ID = None
_GLOBAL_AUDIT_USERNAME = None

def set_global_audit_user(user_id: int, username: str):
    """Set the global audit user context for new AuditService instances."""
    global _GLOBAL_AUDIT_USER_ID, _GLOBAL_AUDIT_USERNAME
    _GLOBAL_AUDIT_USER_ID = user_id
    _GLOBAL_AUDIT_USERNAME = username


class AuditService:
    def __init__(self):
        # Initialize from module-level globals so newly constructed instances
        # can inherit the currently active UI user context.
        global _GLOBAL_AUDIT_USER_ID, _GLOBAL_AUDIT_USERNAME
        self._current_user_id = _GLOBAL_AUDIT_USER_ID
        self._current_username = _GLOBAL_AUDIT_USERNAME

    def set_current_user(self, user_id: int, username: str):
        """Set the current user for audit logging."""
        self._current_user_id = user_id
        self._current_username = username
        # Also update module-level globals so other AuditService instances
        # created later in the app can observe the same context.
        try:
            set_global_audit_user(user_id, username)
        except Exception:
            pass

    def clear_current_user(self):
        """Clear the current user."""
        self._current_user_id = None
        self._current_username = None

    def log_action(self, action: str, description: str, 
                   table_name: Optional[str] = None, record_id: Optional[str] = None,
                   old_values: Optional[Dict] = None, new_values: Optional[Dict] = None,
                   user_id: Optional[int] = None, username: Optional[str] = None,
                   ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> bool:
        """
        Log an action to the audit log.
        
        Args:
            action: The action performed (CREATE, UPDATE, DELETE, LOGIN, etc.)
            description: Human-readable description of the action
            table_name: Database table affected (optional)
            record_id: ID of the record affected (optional)
            old_values: Dictionary of old values for updates/deletes (optional)
            new_values: Dictionary of new values for creates/updates (optional)
            user_id: ID of user who performed action (uses current user if not set)
            username: Username of user who performed action (uses current user if not set)
            ip_address: IP address of the request (optional)
            user_agent: User agent of the request (optional)
            
        Returns:
            bool: True if logged successfully, False otherwise
        """
        try:
            with get_db() as session:
                # Use provided user info or current user
                log_user_id = user_id or self._current_user_id
                log_username = username or self._current_username
                
                if not log_user_id or not log_username:
                    print("Warning: No user information provided for audit log")
                
                # Convert values to JSON strings with proper date handling
                old_values_json = json.dumps(old_values, default=self._json_serializer) if old_values else None
                new_values_json = json.dumps(new_values, default=self._json_serializer) if new_values else None
                
                # Handle special case for admin user (id=0)
                if log_user_id == 0:
                    # For admin user, store audit log without user_id foreign key
                    audit_log = AuditLog(
                        action=action,
                        table_name=table_name,
                        record_id=str(record_id) if record_id is not None else None,
                        description=description,
                        old_values=old_values_json,
                        new_values=new_values_json,
                        user_id=None,  # Skip foreign key for admin
                        username=log_username or "System Admin",
                        ip_address=ip_address,
                        user_agent=user_agent,
                        timestamp=datetime.utcnow()
                    )
                else:
                    # Normal user audit log
                    audit_log = AuditLog(
                        action=action,
                        table_name=table_name,
                        record_id=str(record_id) if record_id is not None else None,
                        description=description,
                        old_values=old_values_json,
                        new_values=new_values_json,
                        user_id=log_user_id,
                        username=log_username,
                        ip_address=ip_address,
                        user_agent=user_agent,
                        timestamp=datetime.utcnow()
                    )
                
                session.add(audit_log)
                session.commit()
                return True
                
        except Exception as e:
            print(f"Error logging audit action: {e}")
            return False

    def get_audit_logs(self, limit: int = 100, offset: int = 0, 
                       filters: Dict = None) -> List[Dict[str, Any]]:
        """
        Get audit logs with optional filtering.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            filters: Dictionary of filters to apply
                - action: Filter by action type
                - table_name: Filter by table name
                - user_id: Filter by user ID
                - date_from: Filter by start date
                - date_to: Filter by end date
                - search: Search in description
                
        Returns:
            List of audit log dictionaries
        """
        try:
            with get_db() as session:
                query = session.query(AuditLog)
                
                if filters:
                    if filters.get('action'):
                        query = query.filter(AuditLog.action == filters['action'])
                    
                    if filters.get('table_name'):
                        query = query.filter(AuditLog.table_name == filters['table_name'])
                    
                    if filters.get('user_id'):
                        query = query.filter(AuditLog.user_id == filters['user_id'])
                    
                    if filters.get('date_from'):
                        query = query.filter(AuditLog.timestamp >= filters['date_from'])
                    
                    if filters.get('date_to'):
                        query = query.filter(AuditLog.timestamp <= filters['date_to'])
                    
                    if filters.get('search'):
                        search_term = f"%{filters['search']}%"
                        query = query.filter(
                            or_(
                                AuditLog.description.like(search_term),
                                AuditLog.action.like(search_term),
                                AuditLog.username.like(search_term)
                            )
                        )
                
                logs = query.order_by(desc(AuditLog.timestamp))\
                           .offset(offset)\
                           .limit(limit)\
                           .all()
                
                return [self._audit_log_to_dict(log) for log in logs]
                
        except Exception as e:
            print(f"Error getting audit logs: {e}")
            return []

    def get_user_activity(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get audit logs for a specific user."""
        filters = {'user_id': user_id}
        return self.get_audit_logs(limit=limit, filters=filters)

    def get_table_changes(self, table_name: str, record_id: str = None, 
                         limit: int = 50) -> List[Dict[str, Any]]:
        """Get audit logs for changes to a specific table or record."""
        filters = {'table_name': table_name}
        
        try:
            with get_db() as session:
                query = session.query(AuditLog).filter(AuditLog.table_name == table_name)
                
                if record_id:
                    query = query.filter(AuditLog.record_id == str(record_id))
                
                logs = query.order_by(desc(AuditLog.timestamp))\
                           .limit(limit)\
                           .all()
                
                return [self._audit_log_to_dict(log) for log in logs]
                
        except Exception as e:
            print(f"Error getting table changes: {e}")
            return []

    def get_recent_activity(self, hours: int = 24, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent activity within specified hours."""
        from datetime import timedelta
        
        date_from = datetime.utcnow() - timedelta(hours=hours)
        filters = {'date_from': date_from}
        return self.get_audit_logs(limit=limit, filters=filters)

    def get_failed_login_attempts(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get failed login attempts within specified hours."""
        from datetime import timedelta
        
        filters = {
            'action': 'LOGIN_FAILED',
            'date_from': datetime.utcnow() - timedelta(hours=hours)
        }
        return self.get_audit_logs(filters=filters)

    def get_audit_statistics(self) -> Dict[str, Any]:
        """Get audit log statistics."""
        try:
            with get_db() as session:
                from datetime import timedelta
                from sqlalchemy import func
                
                now = datetime.utcnow()
                today = now.replace(hour=0, minute=0, second=0, microsecond=0)
                week_ago = now - timedelta(days=7)
                
                # Total logs
                total_logs = session.query(AuditLog).count()
                
                # Today's activity
                today_logs = session.query(AuditLog).filter(
                    AuditLog.timestamp >= today
                ).count()
                
                # This week's activity
                week_logs = session.query(AuditLog).filter(
                    AuditLog.timestamp >= week_ago
                ).count()
                
                # Failed login attempts today
                failed_logins_today = session.query(AuditLog).filter(
                    and_(
                        AuditLog.action == 'LOGIN_FAILED',
                        AuditLog.timestamp >= today
                    )
                ).count()
                
                # Most active users (this week)
                active_users = session.query(
                    AuditLog.username,
                    func.count(AuditLog.id).label('activity_count')
                ).filter(
                    and_(
                        AuditLog.timestamp >= week_ago,
                        AuditLog.username.isnot(None)
                    )
                ).group_by(AuditLog.username)\
                .order_by(desc('activity_count'))\
                .limit(5).all()
                
                # Most common actions (this week)
                common_actions = session.query(
                    AuditLog.action,
                    func.count(AuditLog.id).label('action_count')
                ).filter(
                    AuditLog.timestamp >= week_ago
                ).group_by(AuditLog.action)\
                .order_by(desc('action_count'))\
                .limit(10).all()
                
                return {
                    'total_logs': total_logs,
                    'today_activity': today_logs,
                    'week_activity': week_logs,
                    'failed_logins_today': failed_logins_today,
                    'most_active_users': [
                        {'username': user[0], 'count': user[1]} 
                        for user in active_users
                    ],
                    'common_actions': [
                        {'action': action[0], 'count': action[1]} 
                        for action in common_actions
                    ]
                }
                
        except Exception as e:
            print(f"Error getting audit statistics: {e}")
            return {
                'total_logs': 0,
                'today_activity': 0,
                'week_activity': 0,
                'failed_logins_today': 0,
                'most_active_users': [],
                'common_actions': []
            }

    def cleanup_old_logs(self, days: int = 90) -> int:
        """
        Clean up audit logs older than specified days.
        
        Args:
            days: Number of days to keep logs
            
        Returns:
            Number of logs deleted
        """
        try:
            with get_db() as session:
                from datetime import timedelta
                
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                
                old_logs = session.query(AuditLog).filter(
                    AuditLog.timestamp < cutoff_date
                ).all()
                
                count = len(old_logs)
                
                for log in old_logs:
                    session.delete(log)
                
                session.commit()
                
                # Log the cleanup action
                self.log_action(
                    action="AUDIT_CLEANUP",
                    description=f"Cleaned up {count} audit logs older than {days} days"
                )
                
                return count
                
        except Exception as e:
            print(f"Error cleaning up audit logs: {e}")
            return 0

    def _audit_log_to_dict(self, audit_log: AuditLog) -> Dict[str, Any]:
        """
        Convert AuditLog object to dictionary format.
        Matches exactly with the AuditLog model structure.
        """
        try:
            result = {
                # Basic identification
                'id': audit_log.id,
                'action': audit_log.action,  # CREATE, UPDATE, DELETE, LOGIN, etc.

                # Table and record information
                'table_name': audit_log.table_name,  # Table affected (if applicable)
                'record_id': audit_log.record_id,    # ID of record affected (if applicable)

                # Action details
                'description': audit_log.description,  # Human-readable description
                'old_values': json.loads(audit_log.old_values) if audit_log.old_values else None,
                'new_values': json.loads(audit_log.new_values) if audit_log.new_values else None,

                # User and session information
                'user_id': audit_log.user_id,     # User who performed the action
                'username': audit_log.username,    # Username (preserved even if user deleted)
                'ip_address': audit_log.ip_address,  # IP address of request
                'user_agent': audit_log.user_agent,  # User agent of request

                # Timing information
                'timestamp': audit_log.timestamp.isoformat() if audit_log.timestamp else None,

                # Additional user information through relationship (defensive)
                'user': None
            }

            # Try to include related user info if it's safe to access. If the relationship is
            # not loaded or the instance is detached this may raise — catch and omit gracefully.
            try:
                u = getattr(audit_log, 'user', None)
                if u is not None:
                    result['user'] = {
                        'id': getattr(u, 'id', None),
                        'name': getattr(u, 'name', None),
                        'email': getattr(u, 'email', None)
                    }
            except Exception:
                result['user'] = None

            return result
        except Exception as e:
            print(f"Error converting audit log to dict: {e}")
            # Return minimal information if there's an error
            return {
                'id': getattr(audit_log, 'id', None),
                'action': getattr(audit_log, 'action', None),
                'description': getattr(audit_log, 'description', None),
                'timestamp': getattr(audit_log, 'timestamp', None).isoformat() if getattr(audit_log, 'timestamp', None) else None
            }

    def _json_serializer(self, obj):
        """JSON serializer for objects not serializable by default json code."""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError(f"Object {obj} is not JSON serializable")

    def log_create(self, table_name: str, record_id: str, values: Dict[str, Any],
                  description: Optional[str] = None) -> bool:
        """Helper method for logging CREATE operations"""
        return self.log_action(
            action="CREATE",
            table_name=table_name,
            record_id=record_id,
            description=description or f"Created new {table_name} record",
            new_values=values
        )

    def log_update(self, table_name: str, record_id: str, 
                  old_values: Dict[str, Any], new_values: Dict[str, Any],
                  description: Optional[str] = None) -> bool:
        """Helper method for logging UPDATE operations"""
        return self.log_action(
            action="UPDATE",
            table_name=table_name,
            record_id=record_id,
            description=description or f"Updated {table_name} record",
            old_values=old_values,
            new_values=new_values
        )

    def log_delete(self, table_name: str, record_id: str, 
                  old_values: Dict[str, Any],
                  description: Optional[str] = None) -> bool:
        """Helper method for logging DELETE operations"""
        return self.log_action(
            action="DELETE",
            table_name=table_name,
            record_id=record_id,
            description=description or f"Deleted {table_name} record",
            old_values=old_values
        )

    def log_login(self, user_id: int, username: str, success: bool,
                 ip_address: Optional[str] = None, 
                 user_agent: Optional[str] = None) -> bool:
        """Helper method for logging login attempts"""
        action = "LOGIN_SUCCESS" if success else "LOGIN_FAILED"
        description = f"User {username} {'logged in successfully' if success else 'failed to log in'}"
        return self.log_action(
            action=action,
            description=description,
            user_id=user_id,
            username=username,
            ip_address=ip_address,
            user_agent=user_agent
        )

    def log_system_event(self, event_type: str, description: str,
                        details: Optional[Dict[str, Any]] = None) -> bool:
        """Helper method for logging system events"""
        return self.log_action(
            action=f"SYSTEM_{event_type.upper()}",
            description=description,
            new_values=details if details else None
        )
