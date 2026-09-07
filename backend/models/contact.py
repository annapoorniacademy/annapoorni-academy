from datetime import datetime
from extensions import db

class ContactSetting(db.Model):
    __tablename__ = 'contact_settings'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), default='annapoorniacademy@gmail.com')
    phone = db.Column(db.String(50), default='+91 90803 85589')
    whatsapp = db.Column(db.String(50), default='+919080385589')
    address = db.Column(db.Text, default='Coach Sindhu Ram Academy, Tamil Nadu, India')
    maps_embed_url = db.Column(db.Text, nullable=True)
    working_hours = db.Column(db.String(150), default='Monday - Saturday: 8:30 AM - 6:30 PM')
    contact_form_recipient = db.Column(db.String(120), default='annapoorniacademy@gmail.com')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'phone': self.phone,
            'whatsapp': self.whatsapp or self.phone,
            'address': self.address,
            'maps_embed_url': self.maps_embed_url,
            'working_hours': self.working_hours,
            'contact_form_recipient': self.contact_form_recipient,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
