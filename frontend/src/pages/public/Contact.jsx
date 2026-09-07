import React, { useState } from 'react';
import { useSiteSettings } from '../../context/SiteSettingsContext';
import { Mail, Phone, MapPin, Clock, Send, CheckCircle2, MessageCircle } from 'lucide-react';
import API from '../../services/api';

export const Contact = () => {
  const { contactInfo, socialLinks } = useSiteSettings();
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    mode: 'Live Online via Zoom',
    subject: '',
    message: ''
  });
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  const whatsappNum = (contactInfo?.whatsapp || contactInfo?.phone || '+919080385589').replace(/[^0-9]/g, '');
  const displayPhone = contactInfo?.phone || '+91 90803 85589';
  const displayEmail = contactInfo?.email || 'annapoorniacademy@gmail.com';

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name.trim() || !formData.email.trim() || !formData.phone.trim() || !formData.message.trim()) {
      setError('Please provide your name, phone number, email address, and message.');
      return;
    }

    try {
      setLoading(true);
      setError('');
      await API.post('/api/contact/inquiry', formData);
      setSubmitted(true);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to submit inquiry. Please try again or reach out on WhatsApp.');
    } finally {
      setLoading(false);
    }
  };

  const contactSocials = socialLinks.filter(s => s.is_enabled && s.show_in_contact);

  return (
    <div>
      <section style={{ background: 'var(--primary-color)', color: '#FFFFFF', padding: '4rem 0', textAlign: 'center' }}>
        <div className="container" style={{ maxWidth: '750px' }}>
          <h1 style={{ fontSize: '2.5rem', color: '#FFFFFF', marginBottom: '1rem' }}>Contact Annapoorni Academy</h1>
          <p style={{ fontSize: '1.15rem', opacity: 0.9 }}>
            Have questions about Vedic Maths, Memory Coaching, or Speed Reading? Connect directly with Coach Sindhu Ram.
          </p>
        </div>
      </section>

      <section className="container" style={{ padding: '4rem 1.5rem' }}>
        <div className="responsive-grid-1-1">
          {/* Contact Details Column */}
          <div>
            <h2 style={{ fontSize: '1.75rem', marginBottom: '1.5rem' }}>Get in Touch</h2>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginBottom: '2.5rem' }}>
              {contactInfo.address && (
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
                  <div style={{ width: '44px', height: '44px', borderRadius: '10px', background: 'rgba(30, 58, 138, 0.08)', color: 'var(--primary-color)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                    <MapPin size={22} />
                  </div>
                  <div>
                    <h4 style={{ fontSize: '1rem', fontWeight: 700 }}>Campus Address</h4>
                    <p style={{ color: 'var(--gray-600)', fontSize: '0.95rem', marginTop: '0.2rem' }}>{contactInfo.address}</p>
                  </div>
                </div>
              )}

              <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
                <div style={{ width: '44px', height: '44px', borderRadius: '10px', background: 'rgba(30, 58, 138, 0.08)', color: 'var(--primary-color)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                  <Mail size={22} />
                </div>
                <div>
                  <h4 style={{ fontSize: '1rem', fontWeight: 700 }}>Email Inquiries</h4>
                  <a href={`mailto:${displayEmail}`} style={{ color: 'var(--primary-color)', fontWeight: 600, fontSize: '0.95rem', display: 'inline-block', marginTop: '0.2rem' }}>
                    {displayEmail}
                  </a>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
                <div style={{ width: '44px', height: '44px', borderRadius: '10px', background: 'rgba(30, 58, 138, 0.08)', color: 'var(--primary-color)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                  <Phone size={22} />
                </div>
                <div>
                  <h4 style={{ fontSize: '1rem', fontWeight: 700 }}>Phone / WhatsApp</h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', marginTop: '0.2rem' }}>
                    <a
                      href={`tel:${displayPhone.replace(/\s+/g, '')}`}
                      style={{ color: 'var(--text-color)', fontWeight: 600, fontSize: '0.95rem' }}
                    >
                      📞 {displayPhone}
                    </a>
                    <a
                      href={`https://wa.me/${whatsappNum}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{ color: '#25D366', fontWeight: 700, fontSize: '0.95rem' }}
                      title="Click to chat on WhatsApp"
                    >
                      💬 Chat Directly on WhatsApp
                    </a>
                  </div>
                </div>
              </div>

              {contactInfo.working_hours && (
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
                  <div style={{ width: '44px', height: '44px', borderRadius: '10px', background: 'rgba(30, 58, 138, 0.08)', color: 'var(--primary-color)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                    <Clock size={22} />
                  </div>
                  <div>
                    <h4 style={{ fontSize: '1rem', fontWeight: 700 }}>Working Hours</h4>
                    <p style={{ color: 'var(--gray-600)', fontSize: '0.95rem', marginTop: '0.2rem' }}>{contactInfo.working_hours}</p>
                  </div>
                </div>
              )}
            </div>

            {/* Official Social Links */}
            {contactSocials.length > 0 && (
              <div style={{ marginBottom: '2rem' }}>
                <h4 style={{ fontSize: '1.1rem', marginBottom: '1rem' }}>Connect on Official Channels</h4>
                <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
                  {contactSocials.map(soc => (
                    <a
                      key={soc.id}
                      href={soc.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn btn-outline btn-sm"
                    >
                      {soc.platform}
                    </a>
                  ))}
                </div>
              </div>
            )}

            {/* Google Maps Location Section */}
            <div className="glass-card" style={{ padding: '1.5rem', borderRadius: '16px', background: '#FFFFFF' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '1rem' }}>
                <MapPin size={22} style={{ color: 'var(--primary-color)' }} />
                <div>
                  <h4 style={{ fontSize: '1.05rem', fontWeight: 700, margin: 0 }}>Campus & Class Location</h4>
                  <p style={{ fontSize: '0.85rem', color: 'var(--gray-500)', margin: 0 }}>Annapoorni Academy — Coach Sindhu Ram</p>
                </div>
              </div>

              <div style={{ borderRadius: '12px', overflow: 'hidden', height: '220px', background: 'var(--gray-100)', marginBottom: '1rem' }}>
                <iframe
                  title="Annapoorni Academy Google Maps"
                  src={contactInfo.maps_embed_url || "https://maps.google.com/maps?q=Annapoorni%20Academy%20Coach%20Sindhu%20Ram&t=&z=15&ie=UTF8&iwloc=&output=embed"}
                  width="100%"
                  height="100%"
                  style={{ border: 0 }}
                  allowFullScreen=""
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                />
              </div>

              <a
                href={contactInfo.maps_embed_url || "https://maps.google.com/maps?q=Annapoorni%20Academy%20Coach%20Sindhu%20Ram"}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-outline"
                style={{ width: '100%', textAlign: 'center', justifyContent: 'center', gap: '8px', fontSize: '0.9rem', fontWeight: 700 }}
              >
                📍 Open Location in Google Maps
              </a>
            </div>
          </div>

          {/* Contact Form Box */}
          <div className="glass-card" style={{ padding: '2.5rem' }}>
            {submitted ? (
              <div style={{ textAlign: 'center', padding: '2rem 1rem' }}>
                <CheckCircle2 size={56} style={{ color: 'var(--success-color)', margin: '0 auto 1rem' }} />
                <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Inquiry Received!</h3>
                <p style={{ color: 'var(--gray-600)', marginBottom: '1.5rem', lineHeight: 1.6 }}>
                  Thank you <strong>{formData.name}</strong>! Your inquiry has been safely recorded in our system. A confirmation copy has been sent to your email (<strong>{formData.email}</strong>), and our team will get back to you shortly.
                </p>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  <a
                    href={`https://wa.me/${whatsappNum}?text=${encodeURIComponent(`Hi Coach Sindhu Ram, I just submitted an inquiry on the website regarding ${formData.subject}. My name is ${formData.name}.`)}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn-primary"
                    style={{ background: '#25D366', borderColor: '#25D366', width: '100%', justifyContent: 'center' }}
                  >
                    <MessageCircle size={18} /> Connect Directly on WhatsApp
                  </a>
                  <button
                    onClick={() => {
                      setSubmitted(false);
                      setFormData({ name: '', phone: '', email: '', mode: 'Live Online via Zoom', subject: '', message: '' });
                    }}
                    className="btn btn-outline"
                    style={{ width: '100%', justifyContent: 'center' }}
                  >
                    Submit Another Inquiry
                  </button>
                </div>
              </div>
            ) : (
              <form onSubmit={handleSubmit}>
                <h3 style={{ fontSize: '1.4rem', marginBottom: '1.5rem' }}>Send Us a Message</h3>

                {error && (
                  <div style={{ background: '#FEE2E2', color: '#991B1B', padding: '0.75rem 1rem', borderRadius: '8px', marginBottom: '1.25rem', fontSize: '0.875rem' }}>
                    ⚠️ {error}
                  </div>
                )}

                <div className="form-group">
                  <label className="form-label">Full Name *</label>
                  <input
                    type="text"
                    required
                    className="form-control"
                    placeholder="e.g. Anand Kumar"
                    value={formData.name}
                    onChange={e => setFormData({ ...formData, name: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Phone / WhatsApp Number *</label>
                  <input
                    type="tel"
                    required
                    className="form-control"
                    placeholder="e.g. +91 98765 43210"
                    value={formData.phone}
                    onChange={e => setFormData({ ...formData, phone: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Email Address *</label>
                  <input
                    type="email"
                    required
                    className="form-control"
                    placeholder="e.g. anand@example.com"
                    value={formData.email}
                    onChange={e => setFormData({ ...formData, email: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Preferred Learning Mode</label>
                  <select
                    className="form-control"
                    value={formData.mode}
                    onChange={e => setFormData({ ...formData, mode: e.target.value })}
                  >
                    <option value="Live Online via Zoom">📹 Live Online via Zoom</option>
                    <option value="In-Person Offline Classes">🏫 In-Person Offline Classroom</option>
                    <option value="Hybrid / Weekend Batch">🔄 Hybrid / Weekend Batch</option>
                    <option value="General Inquiry">💬 General Inquiry</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Subject / Program *</label>
                  <input
                    type="text"
                    required
                    className="form-control"
                    placeholder="e.g. Vedic Maths Zoom Batch Schedule"
                    value={formData.subject}
                    onChange={e => setFormData({ ...formData, subject: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Message *</label>
                  <textarea
                    required
                    rows="4"
                    className="form-control"
                    placeholder="Please let us know your child's grade, learning goals, or any questions..."
                    value={formData.message}
                    onChange={e => setFormData({ ...formData, message: e.target.value })}
                  />
                </div>

                <button
                  type="submit"
                  className="btn btn-primary btn-lg"
                  style={{ width: '100%', marginTop: '1rem', justifyContent: 'center' }}
                  disabled={loading}
                >
                  {loading ? 'Submitting Inquiry...' : <><Send size={18} /> Send Inquiry</>}
                </button>
              </form>
            )}
          </div>
        </div>
      </section>
    </div>
  );
};
