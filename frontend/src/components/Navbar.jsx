import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useSiteSettings } from '../context/SiteSettingsContext';
import { Menu, X, BookOpen, Instagram, Youtube, Linkedin, Facebook, Twitter, Send, ArrowRight } from 'lucide-react';

export const Navbar = () => {
  const { settings, navigation, socialLinks } = useSiteSettings();
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  const getSocialIcon = (platform) => {
    const p = platform.toLowerCase();
    if (p.includes('instagram')) return <Instagram size={18} />;
    if (p.includes('youtube')) return <Youtube size={18} />;
    if (p.includes('linkedin')) return <Linkedin size={18} />;
    if (p.includes('facebook')) return <Facebook size={18} />;
    if (p.includes('twitter') || p.includes('x')) return <Twitter size={18} />;
    return <Send size={18} />;
  };

  const headerNav = navigation.length > 0 ? navigation.filter(i => i.is_enabled && (i.location === 'header' || i.location === 'both')) : [
    { id: 1, label: 'Home', destination: '/' },
    { id: 2, label: 'About', destination: '/about' },
    { id: 3, label: 'Courses', destination: '/courses' },
    { id: 4, label: 'Subjects', destination: '/subjects' },
    { id: 5, label: 'Announcements', destination: '/announcements' },
    { id: 6, label: 'Contact', destination: '/contact' }
  ];

  const headerSocials = socialLinks.filter(s => s.is_enabled && s.show_in_header);

  return (
    <header className="header-navbar">
      <div className="container header-container">
        <Link to="/" className="brand-logo">
          {settings.logo_url ? (
            <img src={settings.logo_url} alt={settings.site_name} />
          ) : (
            <div style={{ background: 'var(--primary-color)', color: '#fff', padding: '6px 10px', borderRadius: '8px', display: 'flex' }}>
              <BookOpen size={24} />
            </div>
          )}
          <span>{settings.site_name || 'Annapoorni Academy'}</span>
        </Link>

        {/* Desktop Navigation */}
        <ul className={`nav-links ${mobileOpen ? 'mobile-open' : ''}`}>
          {headerNav.map((item) => {
            const isActive = location.pathname === item.destination;
            return (
              <li key={item.id}>
                {item.is_external ? (
                  <a href={item.destination} target="_blank" rel="noopener noreferrer" className="nav-link">
                    {item.label}
                  </a>
                ) : (
                  <Link
                    to={item.destination}
                    className={`nav-link ${isActive ? 'active' : ''}`}
                    onClick={() => setMobileOpen(false)}
                  >
                    {item.label}
                  </Link>
                )}
              </li>
            );
          })}
          {mobileOpen && (
            <li style={{ marginTop: '0.5rem' }}>
              <Link
                to="/contact"
                className="btn btn-primary btn-sm"
                onClick={() => setMobileOpen(false)}
                style={{ width: '100%', justifyContent: 'center' }}
              >
                Enquire Now
              </Link>
            </li>
          )}
        </ul>

        {/* Header Social Icons & Actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div className="header-social-group" style={{ display: 'flex', gap: '0.5rem' }}>
            {headerSocials.map((soc) => (
              <a
                key={soc.id}
                href={soc.url}
                target="_blank"
                rel="noopener noreferrer"
                className="social-icon-btn"
                title={soc.platform}
                style={{ width: '34px', height: '34px', color: 'var(--text-color)' }}
              >
                {getSocialIcon(soc.platform)}
              </a>
            ))}
          </div>

          <Link
            to="/contact"
            className="btn btn-primary btn-sm header-cta-btn"
            style={{ padding: '0.45rem 0.9rem', fontSize: '0.85rem' }}
          >
            Enquire Now <ArrowRight size={14} />
          </Link>

          {/* Mobile Menu Toggle */}
          <button
            className="mobile-menu-btn"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Toggle navigation menu"
          >
            {mobileOpen ? <X size={26} /> : <Menu size={26} />}
          </button>
        </div>
      </div>
    </header>
  );
};
