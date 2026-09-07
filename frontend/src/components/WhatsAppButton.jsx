import React, { useState } from 'react';
import { useSiteSettings } from '../context/SiteSettingsContext';
import { MessageCircle, X } from 'lucide-react';

export const WhatsAppButton = () => {
  const { contactInfo } = useSiteSettings();
  const [showTooltip, setShowTooltip] = useState(false);

  // Extract phone/whatsapp number from centralized context
  const rawNumber = contactInfo?.whatsapp || contactInfo?.phone || '+919080385589';
  const cleanNumber = rawNumber.replace(/[^0-9]/g, '');
  const message = encodeURIComponent('Hello Coach Sindhu Ram, I would like to inquire about coaching programs at Annapoorni Academy.');
  const whatsappUrl = `https://wa.me/${cleanNumber}?text=${message}`;

  return (
    <div
      style={{
        position: 'fixed',
        bottom: '24px',
        right: '24px',
        zIndex: 999,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-end',
        gap: '8px'
      }}
    >
      {showTooltip && (
        <div
          style={{
            background: '#FFFFFF',
            color: '#0F172A',
            padding: '10px 14px',
            borderRadius: '12px',
            boxShadow: '0 10px 25px -5px rgba(0,0,0,0.15)',
            fontSize: '0.85rem',
            fontWeight: 600,
            maxWidth: '220px',
            border: '1px solid #E2E8F0',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '8px',
            animation: 'fadeIn 0.2s ease-out'
          }}
        >
          <span>Chat with Coach Sindhu Ram on WhatsApp</span>
          <button
            onClick={(e) => {
              e.stopPropagation();
              setShowTooltip(false);
            }}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              color: '#94A3B8',
              padding: 0
            }}
            aria-label="Close tooltip"
          >
            <X size={14} />
          </button>
        </div>
      )}

      <a
        href={whatsappUrl}
        target="_blank"
        rel="noopener noreferrer"
        onMouseEnter={() => setShowTooltip(true)}
        aria-label="Chat on WhatsApp with Annapoorni Academy"
        style={{
          width: '56px',
          height: '56px',
          borderRadius: '50%',
          backgroundColor: '#25D366',
          color: '#FFFFFF',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 8px 20px rgba(37, 211, 102, 0.4)',
          transition: 'all 0.3s ease',
          textDecoration: 'none'
        }}
        className="whatsapp-floating-btn"
      >
        <MessageCircle size={30} fill="#FFFFFF" color="#25D366" />
      </a>
    </div>
  );
};
