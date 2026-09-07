import React from 'react';
import { Link } from 'react-router-dom';
import { useSiteSettings } from '../context/SiteSettingsContext';
import { BookOpen, Mail, Phone, MapPin, MessageCircle, Instagram, Youtube, Linkedin, Facebook, Twitter, Send } from 'lucide-react';

export const Footer = () => {
  const { settings, navigation, socialLinks, contactInfo } = useSiteSettings();

  const footerNav = navigation.length > 0 ? navigation.filter(i => i.is_enabled && (i.location === 'footer' || i.location === 'both')) : [
    { id: 1, label: 'Home', destination: '/' },
    { id: 2, label: 'About Us', destination: '/about' },
    { id: 3, label: 'All Courses', destination: '/courses' },
    { id: 4, label: 'Subjects', destination: '/subjects' },
    { id: 5, label: 'Announcements', destination: '/announcements' },
    { id: 6, label: 'Contact', destination: '/contact' }
  ];

  const footerSocials = socialLinks.filter(s => s.is_enabled && s.show_in_footer);

  const getSocialIcon = (platform) => {
    const p = platform.toLowerCase();
    if (p.includes('instagram')) return <Instagram size={18} />;
    if (p.includes('youtube')) return <Youtube size={18} />;
    if (p.includes('linkedin')) return <Linkedin size={18} />;
    if (p.includes('facebook')) return <Facebook size={18} />;
    if (p.includes('twitter') || p.includes('x')) return <Twitter size={18} />;
    return <Send size={18} />;
  };

  const whatsappNumber = (contactInfo?.whatsapp || contactInfo?.phone || '+919080385589').replace(/[^0-9]/g, '');
  const displayPhone = contactInfo?.phone || '+91 90803 85589';

  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-grid">
          {/* Brand & Description */}
          <div className="footer-brand">
            <Link to="/" className="brand-logo" style={{ color: '#FFFFFF' }}>
              {settings.logo_url ? (
                <img src={settings.logo_url} alt={settings.site_name} style={{ height: '40px' }} />
              ) : (
                <div style={{ background: 'var(--primary-color)', color: '#fff', padding: '6px 10px', borderRadius: '8px', display: 'flex' }}>
                  <BookOpen size={24} />
                </div>
              )}
              <span>{settings.site_name || 'Annapoorni Academy'}</span>
            </Link>
            <p>{settings.site_description || 'Annapoorni Academy is a premier educational platform providing Vedic Mathematics, Memory Coaching, and Speed Reading with Coach Sindhu Ram.'}</p>
            
            {/* Social Media Icons */}
            <div className="social-icons-wrapper">
              {footerSocials.map((soc) => (
                <a
                  key={soc.id}
                  href={soc.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="social-icon-btn"
                  title={soc.platform}
                >
                  {getSocialIcon(soc.platform)}
                </a>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4>Quick Links</h4>
            <ul className="footer-links">
              {footerNav.map((item) => (
                <li key={item.id}>
                  {item.is_external ? (
                    <a href={item.destination} target="_blank" rel="noopener noreferrer">{item.label}</a>
                  ) : (
                    <Link to={item.destination}>{item.label}</Link>
                  )}
                </li>
              ))}
            </ul>
          </div>

          {/* Educational Content */}
          <div>
            <h4>Coaching Programs</h4>
            <ul className="footer-links">
              <li><Link to="/courses">Vedic Mathematics</Link></li>
              <li><Link to="/courses">Memory Training</Link></li>
              <li><Link to="/courses">Speed Reading</Link></li>
              <li><Link to="/announcements">Competitions & News</Link></li>
              <li><Link to="/about">About Coach Sindhu Ram</Link></li>
            </ul>
          </div>

          {/* Contact Details */}
          <div>
            <h4>Contact Details</h4>
            <ul className="footer-links" style={{ gap: '0.85rem' }}>
              {contactInfo.address && (
                <li style={{ display: 'flex', gap: '0.6rem', color: 'var(--gray-300)', fontSize: '0.9rem' }}>
                  <MapPin size={20} style={{ color: 'var(--accent-color)', flexShrink: 0 }} />
                  <span>{contactInfo.address}</span>
                </li>
              )}
              {contactInfo.email && (
                <li style={{ display: 'flex', gap: '0.6rem', color: 'var(--gray-300)', fontSize: '0.9rem' }}>
                  <Mail size={18} style={{ color: 'var(--accent-color)', flexShrink: 0 }} />
                  <a href={`mailto:${contactInfo.email}`}>{contactInfo.email}</a>
                </li>
              )}
              {displayPhone && (
                <li style={{ display: 'flex', gap: '0.6rem', color: 'var(--gray-300)', fontSize: '0.9rem' }}>
                  <Phone size={18} style={{ color: 'var(--accent-color)', flexShrink: 0 }} />
                  <a href={`tel:${displayPhone.replace(/\s+/g, '')}`}>{displayPhone}</a>
                </li>
              )}
              <li style={{ display: 'flex', gap: '0.6rem', color: 'var(--gray-300)', fontSize: '0.9rem' }}>
                <MessageCircle size={18} style={{ color: '#25D366', flexShrink: 0 }} />
                <a
                  href={`https://wa.me/${whatsappNumber}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: '#25D366', fontWeight: 600 }}
                >
                  WhatsApp Chat
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Footer Bottom */}
        <div className="footer-bottom">
          <div>
            © {new Date().getFullYear()} {settings.site_name || 'Annapoorni Academy'}. All rights reserved.
          </div>
          <div style={{ display: 'flex', gap: '1.5rem' }}>
            <Link to="/about" style={{ color: 'var(--gray-400)' }}>Privacy Policy</Link>
            <Link to="/about" style={{ color: 'var(--gray-400)' }}>Terms of Service</Link>
            <Link to="/admin/login" style={{ color: 'var(--gray-400)', opacity: 0.7 }} title="Admin Control Center">Admin Portal</Link>
          </div>
        </div>
      </div>
    </footer>
  );
};
