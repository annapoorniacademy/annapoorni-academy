import React, { useState, useEffect } from 'react';
import API from '../../services/api';
import { UserCheck, Search, Filter, MessageSquare, Mail, Phone, Trash2, CheckCircle2, Clock } from 'lucide-react';

export const EnrollmentsManager = () => {
  const [enrollments, setEnrollments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  const fetchEnrollments = async () => {
    try {
      setLoading(true);
      const params = {};
      if (search) params.search = search;
      if (statusFilter) params.status = statusFilter;

      const res = await API.get('/api/admin/enrollments', { params });
      setEnrollments(res.data);
    } catch (err) {
      console.error('Failed to fetch enrollments', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEnrollments();
  }, [search, statusFilter]);

  const handleStatusChange = async (id, newStatus) => {
    try {
      await API.put(`/api/admin/enrollments/${id}`, { status: newStatus });
      fetchEnrollments();
    } catch (err) {
      alert('Failed to update status.');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this enrollment record?')) return;
    try {
      await API.delete(`/api/admin/enrollments/${id}`);
      fetchEnrollments();
    } catch (err) {
      alert('Failed to delete enrollment.');
    }
  };

  const getStatusBadgeStyle = (status) => {
    switch (status) {
      case 'new':
        return { background: '#FEF3C7', color: '#92400E' };
      case 'contacted':
        return { background: '#E0F2FE', color: '#075985' };
      case 'interested':
        return { background: '#F3E8FF', color: '#6B21A8' };
      case 'enrolled':
        return { background: '#D1FAE5', color: '#065F46' };
      case 'closed':
        return { background: '#F1F5F9', color: '#475569' };
      default:
        return { background: '#F1F5F9', color: '#475569' };
    }
  };

  return (
    <div className="admin-page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>Student Course Enrollments</h1>
          <p style={{ color: 'var(--gray-600)', fontSize: '0.95rem' }}>
            Manage student batch registrations, learning modes, and enrollment statuses.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <div className="search-box" style={{ position: 'relative' }}>
            <Search size={18} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--gray-400)' }} />
            <input
              type="text"
              className="form-control"
              placeholder="Search student, email, course..."
              style={{ paddingLeft: '2.5rem', width: '260px' }}
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
          </div>

          <select
            className="form-control"
            style={{ width: '170px' }}
            value={statusFilter}
            onChange={e => setStatusFilter(e.target.value)}
          >
            <option value="">All Statuses</option>
            <option value="new">🆕 New</option>
            <option value="contacted">📞 Contacted</option>
            <option value="interested">⭐ Interested</option>
            <option value="enrolled">✅ Enrolled</option>
            <option value="closed">📁 Closed</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div style={{ padding: '4rem', textAlign: 'center', color: 'var(--gray-500)' }}>Loading enrollment records...</div>
      ) : enrollments.length === 0 ? (
        <div className="glass-card" style={{ padding: '4rem', textAlign: 'center' }}>
          <UserCheck size={48} style={{ color: 'var(--gray-400)', margin: '0 auto 1rem' }} />
          <h3>No Course Enrollments Found</h3>
          <p style={{ color: 'var(--gray-500)', marginTop: '0.5rem' }}>
            When students click "Enroll Now" on course pages, their registration details will appear here.
          </p>
        </div>
      ) : (
        <div className="glass-card" style={{ overflow: 'hidden' }}>
          <table className="admin-table" style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: 'var(--gray-100)', textAlign: 'left', fontSize: '0.85rem', textTransform: 'uppercase', color: 'var(--gray-600)' }}>
                <th style={{ padding: '1rem 1.25rem' }}>Date</th>
                <th style={{ padding: '1rem 1.25rem' }}>Student Details</th>
                <th style={{ padding: '1rem 1.25rem' }}>Course Requested</th>
                <th style={{ padding: '1rem 1.25rem' }}>Mode</th>
                <th style={{ padding: '1rem 1.25rem' }}>Status</th>
                <th style={{ padding: '1rem 1.25rem', textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {enrollments.map((item) => (
                <tr key={item.id} style={{ borderBottom: '1px solid var(--gray-200)' }}>
                  <td style={{ padding: '1rem 1.25rem', fontSize: '0.85rem', color: 'var(--gray-500)', whiteSpace: 'nowrap' }}>
                    {new Date(item.created_at).toLocaleDateString()} <br />
                    <span style={{ fontSize: '0.75rem' }}>{new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                  </td>

                  <td style={{ padding: '1rem 1.25rem' }}>
                    <div style={{ fontWeight: 700, fontSize: '1rem' }}>{item.student_name}</div>
                    <div style={{ display: 'flex', gap: '12px', marginTop: '4px', fontSize: '0.85rem', flexWrap: 'wrap' }}>
                      <a
                        href={`https://wa.me/${item.phone.replace(/[^0-9]/g, '')}?text=${encodeURIComponent(`Hi ${item.student_name}, thank you for inquiring about ${item.course_title} at Annapoorni Academy!`)}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{ color: '#059669', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '4px' }}
                      >
                        <Phone size={14} /> {item.phone}
                      </a>
                      <a
                        href={`mailto:${item.email}`}
                        style={{ color: 'var(--primary-color)', display: 'flex', alignItems: 'center', gap: '4px' }}
                      >
                        <Mail size={14} /> {item.email}
                      </a>
                    </div>
                    {item.message && (
                      <p style={{ fontSize: '0.8rem', color: 'var(--gray-600)', marginTop: '4px', fontStyle: 'italic' }}>
                        "{item.message}"
                      </p>
                    )}
                  </td>

                  <td style={{ padding: '1rem 1.25rem', fontWeight: 600 }}>
                    {item.course_title}
                  </td>

                  <td style={{ padding: '1rem 1.25rem' }}>
                    <span style={{
                      background: item.preferred_mode?.includes('Zoom') ? '#DBEAFE' : '#D1FAE5',
                      color: item.preferred_mode?.includes('Zoom') ? '#1E40AF' : '#065F46',
                      fontSize: '0.8rem',
                      fontWeight: 700,
                      padding: '4px 10px',
                      borderRadius: '12px'
                    }}>
                      {item.preferred_mode}
                    </span>
                  </td>

                  <td style={{ padding: '1rem 1.25rem' }}>
                    <select
                      value={item.status}
                      onChange={e => handleStatusChange(item.id, e.target.value)}
                      style={{
                        padding: '6px 10px',
                        borderRadius: '6px',
                        fontSize: '0.85rem',
                        fontWeight: 700,
                        border: '1px solid var(--gray-300)',
                        ...getStatusBadgeStyle(item.status)
                      }}
                    >
                      <option value="new">🆕 New</option>
                      <option value="contacted">📞 Contacted</option>
                      <option value="interested">⭐ Interested</option>
                      <option value="enrolled">✅ Enrolled</option>
                      <option value="closed">📁 Closed</option>
                    </select>
                  </td>

                  <td style={{ padding: '1rem 1.25rem', textAlign: 'right' }}>
                    <button
                      onClick={() => handleDelete(item.id)}
                      className="btn btn-outline btn-sm"
                      style={{ color: 'var(--error-color)', borderColor: 'var(--gray-300)' }}
                      title="Delete Record"
                    >
                      <Trash2 size={16} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
