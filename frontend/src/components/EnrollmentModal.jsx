import React, { useState } from 'react';
import { X, CheckCircle2, Send, Video, MapPin, Sparkles, MessageCircle } from 'lucide-react';
import API from '../services/api';
import { useSiteSettings } from '../context/SiteSettingsContext';

export const EnrollmentModal = ({ course, isOpen, onClose, onSuccess }) => {
  const { contactInfo } = useSiteSettings();
  const [formData, setFormData] = useState({
    student_name: '',
    email: '',
    phone: '',
    preferred_mode: 'Live Online via Zoom',
    message: ''
  });

  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen || !course) return null;

  const rawWhatsapp = contactInfo?.whatsapp || contactInfo?.phone || '+919080385589';
  const whatsappNum = rawWhatsapp.replace(/[^0-9]/g, '');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.student_name.trim() || !formData.email.trim() || !formData.phone.trim()) {
      setError('Please fill in your name, email, and phone number.');
      return;
    }

    try {
      setLoading(true);
      setError('');
      await API.post(`/api/courses/${course.id}/enroll`, formData);
      setSubmitted(true);
      if (onSuccess) onSuccess();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to submit registration. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleModalClose = () => {
    setSubmitted(false);
    setError('');
    setFormData({
      student_name: '',
      email: '',
      phone: '',
      preferred_mode: 'Live Online via Zoom',
      message: ''
    });
    onClose();
  };

  return (
    <div className="modal-backdrop" style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(15, 23, 42, 0.75)',
      backdropFilter: 'blur(6px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 9999,
      padding: '1rem',
      overflowY: 'auto'
    }}>
      <div className="glass-card" style={{
        background: '#FFFFFF',
        maxWidth: '540px',
        width: '100%',
        maxHeight: 'calc(100vh - 2rem)',
        display: 'flex',
        flexDirection: 'column',
        borderRadius: '20px',
        overflow: 'hidden',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        position: 'relative',
        margin: 'auto'
      }}>
        {/* Header */}
        <div style={{
          background: 'linear-gradient(135deg, var(--primary-color) 0%, #1E40AF 100%)',
          color: '#FFFFFF',
          padding: '1.5rem 1.75rem',
          flexShrink: 0,
          position: 'relative'
        }}>
          <button
            onClick={handleModalClose}
            style={{
              position: 'absolute',
              top: '16px',
              right: '16px',
              background: 'rgba(255, 255, 255, 0.15)',
              border: 'none',
              color: '#FFFFFF',
              width: '32px',
              height: '32px',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer'
            }}
            aria-label="Close modal"
          >
            <X size={18} />
          </button>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
            <Sparkles size={18} style={{ color: 'var(--accent-color)' }} />
            <span style={{ fontSize: '0.8rem', fontWeight: 800, letterSpacing: '0.08em', textTransform: 'uppercase', color: 'var(--accent-color)' }}>
              Enrollment Request
            </span>
          </div>
          <h3 style={{ fontSize: '1.3rem', fontWeight: 700, color: '#FFFFFF', lineHeight: 1.3 }}>{course.title}</h3>
          <p style={{ fontSize: '0.85rem', opacity: 0.9, marginTop: '4px' }}>
            Join Coach Sindhu Ram's upcoming batch (Zoom / Offline)
          </p>
        </div>

        {/* Scrollable Form Body */}
        <div style={{ padding: '1.5rem 1.75rem', overflowY: 'auto', flex: 1 }}>
          {submitted ? (
            <div style={{ textAlign: 'center', padding: '1rem 0' }}>
              <div style={{
                width: '64px',
                height: '64px',
                borderRadius: '50%',
                background: '#D1FAE5',
                color: '#059669',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 1.25rem'
              }}>
                <CheckCircle2 size={36} />
              </div>
              <h3 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: '0.5rem' }}>Registration Submitted!</h3>
              <p style={{ color: 'var(--gray-600)', fontSize: '0.95rem', lineHeight: 1.6, marginBottom: '1.5rem' }}>
                Thank you <strong>{formData.student_name}</strong>! Your registration has been safely recorded in the system. A confirmation email has been dispatched to <strong>{formData.email}</strong>, and our team will get in touch with you shortly.
              </p>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                <a
                  href={`https://wa.me/${whatsappNum}?text=${encodeURIComponent(`Hi Coach Sindhu Ram, I just submitted an enrollment request for "${course.title}" (${formData.preferred_mode}). My name is ${formData.student_name}.`)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-primary"
                  style={{ width: '100%', background: '#25D366', borderColor: '#25D366', justifyContent: 'center' }}
                >
                  <MessageCircle size={18} /> Connect on WhatsApp
                </a>
                
                <button className="btn btn-outline" onClick={handleModalClose} style={{ width: '100%', justifyContent: 'center' }}>
                  Close Window
                </button>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit}>
              {error && (
                <div style={{ background: '#FEE2E2', color: '#991B1B', padding: '0.75rem 1rem', borderRadius: '8px', marginBottom: '1.25rem', fontSize: '0.875rem', fontWeight: 600 }}>
                  ⚠️ {error}
                </div>
              )}

              <div className="form-group" style={{ marginBottom: '1.25rem' }}>
                <label className="form-label" style={{ fontWeight: 600 }}>Student Full Name *</label>
                <input
                  type="text"
                  required
                  className="form-control"
                  placeholder="e.g. Priya Sharma"
                  value={formData.student_name}
                  onChange={e => setFormData({ ...formData, student_name: e.target.value })}
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1.25rem' }}>
                <div className="form-group">
                  <label className="form-label" style={{ fontWeight: 600 }}>Phone / WhatsApp *</label>
                  <input
                    type="tel"
                    required
                    className="form-control"
                    placeholder="+91 98765 43210"
                    value={formData.phone}
                    onChange={e => setFormData({ ...formData, phone: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label" style={{ fontWeight: 600 }}>Email Address *</label>
                  <input
                    type="email"
                    required
                    className="form-control"
                    placeholder="student@example.com"
                    value={formData.email}
                    onChange={e => setFormData({ ...formData, email: e.target.value })}
                  />
                </div>
              </div>

              <div className="form-group" style={{ marginBottom: '1.25rem' }}>
                <label className="form-label" style={{ fontWeight: 600 }}>Preferred Batch Mode *</label>
                <select
                  className="form-control"
                  value={formData.preferred_mode}
                  onChange={e => setFormData({ ...formData, preferred_mode: e.target.value })}
                >
                  <option value="Live Online via Zoom">📹 Live Online via Zoom</option>
                  <option value="In-Person Offline Classroom">🏫 In-Person Offline Classroom</option>
                  <option value="Hybrid / Weekend Batch">🔄 Hybrid / Weekend Batch</option>
                </select>
              </div>

              <div className="form-group" style={{ marginBottom: '1.5rem' }}>
                <label className="form-label" style={{ fontWeight: 600 }}>Message / Notes (Optional)</label>
                <textarea
                  rows="3"
                  className="form-control"
                  placeholder="e.g. Inquiring for standard 8 student, evening batch preference..."
                  value={formData.message}
                  onChange={e => setFormData({ ...formData, message: e.target.value })}
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary btn-lg"
                style={{ width: '100%', fontSize: '1rem', fontWeight: 700, justifyContent: 'center' }}
              >
                {loading ? 'Submitting Registration...' : <>Enroll Now & Get Details <Send size={18} /></>}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};
