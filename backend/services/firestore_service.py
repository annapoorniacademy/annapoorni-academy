"""
Firestore Service for Annapoorni Academy V2.0
Provides native document collection mapping and data operations for Google Cloud Firestore.
"""

import os
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Lazy Firestore client initialization
_firestore_client = None

def get_firestore_client():
    """
    Get or initialize Google Cloud Firestore client.
    Returns None if google-cloud-firestore is not installed or not configured.
    """
    global _firestore_client
    if _firestore_client is not None:
        return _firestore_client

    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT') or os.environ.get('FIRESTORE_PROJECT_ID')
    try:
        from google.cloud import firestore
        if project_id:
            _firestore_client = firestore.Client(project=project_id)
        else:
            _firestore_client = firestore.Client()
        logger.info(f"Initialized Firestore client for project: {project_id or 'default'}")
        return _firestore_client
    except Exception as e:
        logger.warning(f"Firestore client initialization skipped: {e}")
        return None

def is_firestore_enabled():
    """Check if Firestore mode is active and available."""
    db_type = os.environ.get('DB_TYPE', '').lower()
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT') or os.environ.get('FIRESTORE_PROJECT_ID')
    if db_type == 'firestore' or (db_type == 'auto' and project_id):
        client = get_firestore_client()
        return client is not None
    return False

class FirestoreRepository:
    """Generic repository for Firestore document operations."""

    def __init__(self, collection_name):
        self.collection_name = collection_name

    def _col(self):
        client = get_firestore_client()
        if not client:
            raise RuntimeError("Firestore is not available.")
        return client.collection(self.collection_name)

    def get_by_id(self, doc_id):
        doc_ref = self._col().document(str(doc_id))
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc_id
            return data
        return None

    def get_all(self, filter_published=False, order_by=None, descending=False, limit=None):
        query = self._col()
        if filter_published:
            query = query.where('status', '==', 'published')
        if order_by:
            from google.cloud import firestore
            direction = firestore.Query.DESCENDING if descending else firestore.Query.ASCENDING
            query = query.order_by(order_by, direction=direction)
        if limit:
            query = query.limit(limit)

        docs = query.stream()
        results = []
        for doc in docs:
            d = doc.to_dict()
            d['id'] = int(doc.id) if doc.id.isdigit() else doc.id
            results.append(d)
        return results

    def create(self, doc_id, data):
        data['created_at'] = data.get('created_at') or datetime.utcnow().isoformat()
        data['updated_at'] = datetime.utcnow().isoformat()
        doc_ref = self._col().document(str(doc_id))
        doc_ref.set(data)
        data['id'] = doc_id
        return data

    def update(self, doc_id, data):
        data['updated_at'] = datetime.utcnow().isoformat()
        doc_ref = self._col().document(str(doc_id))
        doc_ref.update(data)
        return self.get_by_id(doc_id)

    def delete(self, doc_id):
        self._col().document(str(doc_id)).delete()
        return True

    def count(self):
        docs = self._col().stream()
        return sum(1 for _ in docs)

# Preset collection helpers
courses_col = FirestoreRepository('courses')
subjects_col = FirestoreRepository('subjects')
lessons_col = FirestoreRepository('lessons')
quizzes_col = FirestoreRepository('quizzes')
announcements_col = FirestoreRepository('announcements')
inquiries_col = FirestoreRepository('inquiries')
enrollments_col = FirestoreRepository('enrollments')
settings_col = FirestoreRepository('settings')
media_col = FirestoreRepository('media')
admins_col = FirestoreRepository('admins')
