import React from "react";

export default function MapView({ latitude, longitude, name }) {
  if (!latitude || !longitude) return null;

  const src = `https://maps.google.com/maps?q=${latitude},${longitude}&z=10&output=embed`;

  return (
    <div className="card overflow-hidden">
      <iframe
        title={`Map of ${name}`}
        src={src}
        width="100%"
        height="280"
        style={{ border: 0 }}
        loading="lazy"
        referrerPolicy="no-referrer-when-downgrade"
      />
    </div>
  );
}
