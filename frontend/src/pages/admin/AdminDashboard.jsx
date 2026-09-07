import React, { useState, useEffect } from 'react';
import API from '../../services/api';
import { 
  BookOpen, Layers, FileText, HelpCircle, Bell, Image as ImageIcon, MessageSquare, UserCheck, Download, Plus, Sparkles, ExternalLink 
} from 'lucide-react';
import { Link } from 'react-router-dom';

export const AdminDashboard = () => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);

  const fetchDashboard = async () => {
    try {
      const res = await API.get('/api/admin/dashboard');
      setSummary(res.data);
    } catch (err) {
      console.error('Error fetching admin dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  const handleExportBackup = async () => {
    try {
      setExporting(true);
      const res = await API.get('/api/admin/backup/export', { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `annapoorni_academy_backup_${new Date().toISOString().slice(0,10)}.json`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      alert('Failed to export backup: ' + (err.message || 'Error'));
    } finally {
      setExporting(false);
    }
  };

  if (loading) return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading Admin Control Dashboard...</div>;

  const metrics = summary?.metrics || {};

  return (
    <div>
      {/* Metric Cards Row */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon-box" style={{ background: '#EFF6FF', color: '#1E3A8A' }}>
            <BookOpen size={24} />
          </div>
          <div className="metric-info">
            <h3>{metrics.total_courses || 0}</h3>
            <p>Total Courses ({metrics.published_courses || 0} Published)</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon-box" style={{ background: '#CCFBF1', color: '#0D9488' }}>
            <Layers size={24} />
          </div>
          <div className="metric-info">
            <h3>{metrics.active_subjects || metrics.total_subjects || 0}</h3>
            <p>Active Flagship Subjects</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon-box" style={{ background: '#FEF3C7', color: '#D97706' }}>
            <UserCheck size={24} />
          </div>
          <div className="metric-info">
            <h3>{metrics.total_enrollments || 0}</h3>
            <p>Enrollment Requests ({metrics.new_enrollments || 0} New)</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon-box" style={{ background: '#DCFCE7', color: '#16A34A' }}>
            <MessageSquare size={24} />
          </div>
          <div className="metric-info">
            <h3>{metrics.total_inquiries || 0}</h3>
            <p>Contact Inquiries ({metrics.new_inquiries || 0} New)</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon-box" style={{ background: '#E0E7FF', color: '#4338CA' }}>
            <FileText size={24} />
          </div>
          <div className="metric-info">
            <h3>{metrics.total_lessons || 0}</h3>
            <p>Structured Lessons</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon-box" style={{ background: '#FCE7F3', color: '#BE185D' }}>
            <HelpCircle size={24} />
          </div>
          <div className="metric-info">
            <h3>{metrics.total_quizzes || 0}</h3>
            <p>Quizzes ({metrics.total_quiz_attempts || 0} Attempts)</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon-box" style={{ background: '#FEE2E2', color: '#B91C1C' }}>
            <Bell size={24} />
          </div>
          <div className="metric-info">
            <h3>{metrics.total_announcements || 0}</h3>
            <p>Announcements</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon-box" style={{ background: '#F3E8FF', color: '#6B21A8' }}>
            <ImageIcon size={24} />
          </div>
          <div className="metric-info">
            <h3>{metrics.total_media || 0}</h3>
            <p>Media Library Assets</p>
          </div>
        </div>
      </div>

      {/* Quick Action Shortcuts */}
      <div style={{ display: 'flex', gap: '0.85rem', marginBottom: '2rem', flexWrap: 'wrap', alignItems: 'center' }}>
        <Link to="/admin/enrollments" className="btn btn-primary btn-sm">
          <UserCheck size={16} /> Manage Enrollments {metrics.new_enrollments > 0 && `(${metrics.new_enrollments} New)`}
        </Link>
        <Link to="/admin/contact" className="btn btn-outline btn-sm">
          <MessageSquare size={16} /> View Inquiries {metrics.new_inquiries > 0 && `(${metrics.new_inquiries} New)`}
        </Link>
        <Link to="/admin/courses" className="btn btn-outline btn-sm">
          <Plus size={16} /> Manage Courses
        </Link>
        <Link to="/admin/homepage" className="btn btn-outline btn-sm">
          <Sparkles size={16} /> Edit Homepage
        </Link>
        <button
          onClick={handleExportBackup}
          className="btn btn-outline btn-sm"
          style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '6px' }}
          disabled={exporting}
        >
          <Download size={16} /> {exporting ? 'Exporting...' : 'Export JSON Backup'}
        </button>
      </div>

      {/* Tables Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.75rem', marginBottom: '2rem' }}>
        {/* Recent Enrollments */}
        <div className="table-card">
          <div className="table-header">
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Recent Student Enrollments</h3>
            <Link to="/admin/enrollments" style={{ fontSize: '0.85rem', fontWeight: 600 }}>View All</Link>
          </div>
          <table className="data-table">
            <thead>
              <tr>
                <th>Student</th>
                <th>Course</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {summary?.recent_enrollments && summary.recent_enrollments.length > 0 ? (
                summary.recent_enrollments.map(e => (
                  <tr key={e.id}>
                    <td style={{ fontWeight: 600 }}>{e.student_name}</td>
                    <td style={{ fontSize: '0.85rem' }}>{e.course_title}</td>
                    <td>
                      <span className={`badge ${e.status === 'new' ? 'badge-primary' : 'badge-success'}`}>
                        {e.status}
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr><td colSpan="3" style={{ textAlign: 'center', color: '#94A3B8' }}>No enrollment requests yet</td></tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Recent Contact Inquiries */}
        <div className="table-card">
          <div className="table-header">
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Recent Contact Inquiries</h3>
            <Link to="/admin/contact" style={{ fontSize: '0.85rem', fontWeight: 600 }}>View All</Link>
          </div>
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Subject</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {summary?.recent_inquiries && summary.recent_inquiries.length > 0 ? (
                summary.recent_inquiries.map(i => (
                  <tr key={i.id}>
                    <td style={{ fontWeight: 600 }}>{i.name}</td>
                    <td style={{ fontSize: '0.85rem' }}>{i.subject}</td>
                    <td>
                      <span className={`badge ${i.status === 'new' ? 'badge-warning' : 'badge-secondary'}`}>
                        {i.status}
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr><td colSpan="3" style={{ textAlign: 'center', color: '#94A3B8' }}>No inquiries yet</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
