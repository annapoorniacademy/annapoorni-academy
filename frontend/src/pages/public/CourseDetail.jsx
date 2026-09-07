import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import API from '../../services/api';
import { useSiteSettings } from '../../context/SiteSettingsContext';
import { BookOpen, Clock, BarChart, CheckCircle2, UserCheck, Calendar, Sparkles, Send, MessageSquare, MessageCircle } from 'lucide-react';
import { EnrollmentModal } from '../../components/EnrollmentModal';

export const CourseDetail = () => {
  const { id } = useParams();
  const { contactInfo } = useSiteSettings();
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const rawWhatsapp = contactInfo?.whatsapp || contactInfo?.phone || '+919080385589';
  const whatsappNum = rawWhatsapp.replace(/[^0-9]/g, '');
  const displayPhone = contactInfo?.phone || '+91 90803 85589';

  useEffect(() => {
    const fetchDetail = async () => {
      try {
        const res = await API.get(`/api/courses/${id}`);
        setCourse(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchDetail();
  }, [id]);

  if (loading) return <div className="container" style={{ padding: '5rem 0', textAlign: 'center' }}>Loading Course Details...</div>;
  if (!course) return <div className="container" style={{ padding: '5rem 0', textAlign: 'center', color: 'var(--error-color)' }}>Course not found.</div>;

  const whatsappInquiryUrl = `https://wa.me/${whatsappNum}?text=${encodeURIComponent(`Hi Coach Sindhu Ram, I would like details regarding the "${course.title}" program.`)}`;

  return (
    <div>
      {/* Course Header Banner */}
      <section style={{ background: 'linear-gradient(135deg, var(--primary-color) 0%, #1E3A8A 100%)', color: '#FFFFFF', padding: '4.5rem 0' }}>
        <div className="container responsive-grid-2-1" style={{ alignItems: 'center' }}>
          <div>
            <div style={{ display: 'flex', gap: '10px', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap' }}>
              <span style={{ background: 'var(--accent-color)', color: '#0F172A', fontWeight: 800, fontSize: '0.85rem', padding: '4px 12px', borderRadius: '20px', textTransform: 'uppercase' }}>
                {course.category || 'General'}
              </span>
              <span style={{ background: '#059669', color: '#FFFFFF', fontWeight: 700, fontSize: '0.85rem', padding: '4px 12px', borderRadius: '20px' }}>
                📹 Live Zoom & 🏫 Offline Classes
              </span>
            </div>

            <h1 style={{ fontSize: '2.5rem', color: '#FFFFFF', marginBottom: '1rem', fontWeight: 800 }}>
              {course.title}
            </h1>
            <p style={{ fontSize: '1.1rem', opacity: 0.9, lineHeight: 1.6, marginBottom: '2rem', maxWidth: '750px' }}>
              {course.description}
            </p>

            <div style={{ display: 'flex', gap: '2rem', fontSize: '0.95rem', marginBottom: '2.5rem', flexWrap: 'wrap' }}>
              <div><BarChart size={16} /> Skill Level: <strong>{course.difficulty || 'All Levels'}</strong></div>
              <div><Clock size={16} /> Duration: <strong>{course.duration || '4 Weeks'}</strong></div>
              <div><UserCheck size={16} /> Coach: <strong>Sindhu Ram</strong></div>
            </div>

            <button
              onClick={() => setIsModalOpen(true)}
              className="btn btn-accent btn-lg"
              style={{ fontSize: '1.1rem', fontWeight: 800, padding: '1rem 2.25rem', boxShadow: '0 10px 25px rgba(245, 158, 11, 0.4)' }}
            >
              <Sparkles size={20} /> Enroll Now & Get Batch Details
            </button>
          </div>

          <div>
            <div className="glass-card" style={{ padding: '1.5rem', background: '#FFFFFF', borderRadius: '20px', color: 'var(--text-color)' }}>
              <img
                src={course.thumbnail_url || 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600&auto=format&fit=crop&q=80'}
                alt={course.title}
                style={{ borderRadius: '12px', width: '100%', height: '200px', objectFit: 'cover', marginBottom: '1.25rem' }}
              />

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginBottom: '1.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.9rem' }}>
                  <CheckCircle2 size={18} style={{ color: 'var(--secondary-color)' }} />
                  <span>Direct Coaching by Coach Sindhu Ram</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.9rem' }}>
                  <CheckCircle2 size={18} style={{ color: 'var(--secondary-color)' }} />
                  <span>Interactive Live Q&A & Assessments</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.9rem' }}>
                  <CheckCircle2 size={18} style={{ color: 'var(--secondary-color)' }} />
                  <span>National Competition Practice Drills</span>
                </div>
              </div>

              <button
                onClick={() => setIsModalOpen(true)}
                className="btn btn-primary"
                style={{ width: '100%', fontSize: '1rem', fontWeight: 700, justifyContent: 'center' }}
              >
                Enroll Now <Send size={16} />
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Course Highlights & Syllabus Structure */}
      <section className="container" style={{ padding: '4rem 1.5rem' }}>
        <div className="responsive-grid-2-1">
          <div>
            <h2 style={{ fontSize: '1.75rem', marginBottom: '1.5rem' }}>Course Syllabus & Training Highlights</h2>

            {course.modules && course.modules.length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                {course.modules.map((mod) => (
                  <div key={mod.id} className="glass-card" style={{ padding: '1.75rem' }}>
                    <h3 style={{ fontSize: '1.3rem', color: 'var(--primary-color)', marginBottom: '0.5rem' }}>
                      {mod.title}
                    </h3>
                    {mod.description && <p style={{ color: 'var(--gray-600)', marginBottom: '1rem', fontSize: '0.95rem' }}>{mod.description}</p>}

                    {mod.lessons && mod.lessons.length > 0 && (
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem', marginTop: '1rem' }}>
                        {mod.lessons.map((les) => (
                          <div
                            key={les.id}
                            style={{
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'space-between',
                              padding: '0.85rem 1rem',
                              background: 'var(--gray-50)',
                              borderRadius: '8px',
                              border: '1px solid var(--gray-200)'
                            }}
                          >
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                              <CheckCircle2 size={18} style={{ color: 'var(--secondary-color)', flexShrink: 0 }} />
                              <span style={{ fontWeight: 600, fontSize: '0.95rem' }}>{les.title}</span>
                            </div>
                            <span style={{ fontSize: '0.8rem', color: 'var(--gray-500)' }}>{les.duration || 'Live Session'}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="glass-card" style={{ padding: '2rem' }}>
                <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>Live Batch Curriculum Overview</h3>
                <p style={{ color: 'var(--gray-600)', lineHeight: 1.6 }}>
                  This program features structured live interactive sessions, speed calculation drills, mnemonic strategies, and direct personalized guidance from Coach Sindhu Ram.
                </p>
              </div>
            )}
          </div>

          <div>
            <div className="glass-card" style={{ padding: '2rem', position: 'sticky', top: '100px' }}>
              <h3 style={{ fontSize: '1.3rem', marginBottom: '1rem' }}>Have Questions About Batches?</h3>
              <p style={{ fontSize: '0.9rem', color: 'var(--gray-600)', lineHeight: 1.6, marginBottom: '1.5rem' }}>
                Click below to submit your details. Our team will send the full batch schedule and fee structure to your WhatsApp and Email.
              </p>

              <button
                onClick={() => setIsModalOpen(true)}
                className="btn btn-primary"
                style={{ width: '100%', marginBottom: '1rem', fontWeight: 700, justifyContent: 'center' }}
              >
                Enroll Now <Send size={16} />
              </button>

              <a
                href={whatsappInquiryUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-outline"
                style={{ width: '100%', textAlign: 'center', justifyContent: 'center', display: 'flex', alignItems: 'center', gap: '8px' }}
              >
                <MessageCircle size={18} color="#25D366" /> Chat on WhatsApp
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Registration Modal */}
      <EnrollmentModal
        course={course}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </div>
  );
};
