import ReviewSection from "../components/ReviewSection";
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/axios";
import MapView from "../components/MapView";
import WeatherWidget from "../components/WeatherWidget";
import { Star, MapPin, Utensils, Building2, Ticket, ExternalLink } from "lucide-react";

const FALLBACK_IMAGE = "https://images.unsplash.com/photo-1488646953014-85cb44e25828";

function mapLink(lat, lng) {
  if (!lat || !lng) return null;
  return `https://maps.google.com/?q=${lat},${lng}`;
}

export default function DestinationDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [destination, setDestination] = useState(null);
  const [attractions, setAttractions] = useState([]);
  const [hotels, setHotels] = useState([]);
  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {
    api.get(`/destinations/${id}`).then((res) => setDestination(res.data.destination));
    api.get(`/recommendations/destinations/${id}/attractions`).then((res) => setAttractions(res.data.attractions));
    api.get(`/recommendations/destinations/${id}/hotels`).then((res) => setHotels(res.data.hotels));
    api.get(`/recommendations/destinations/${id}/restaurants`).then((res) => setRestaurants(res.data.restaurants));
  }, [id]);

  if (!destination) return <p className="text-center py-24 text-ink-500">Loading destination...</p>;

  return (
    <div>
      <div className="h-72 md:h-96 relative">
        <img src={destination.image_url} alt={destination.name} className="w-full h-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
        <div className="absolute bottom-6 left-4 sm:left-6 lg:left-8 text-white">
          <h1 className="text-3xl md:text-4xl font-display font-bold">{destination.name}</h1>
          <p className="flex items-center gap-1 text-sm"><MapPin size={14} /> {destination.country}</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 grid lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          <div>
            <h2 className="text-xl font-display font-semibold text-ink-900 mb-2">About</h2>
            <p className="text-ink-500">{destination.description}</p>
            <div className="flex gap-2 mt-3 flex-wrap">
              {destination.tags.map((t) => (
                <span key={t} className="text-xs bg-primary-50 text-primary-600 px-3 py-1 rounded-full capitalize">{t}</span>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-xl font-display font-semibold text-ink-900 mb-3 flex items-center gap-2">
              <Ticket size={18} /> Top Attractions
            </h2>
            <div className="grid sm:grid-cols-2 gap-3">
              {attractions.map((a) => (
                <div key={a.id} className="card overflow-hidden">
                  <img
                    src={a.image_url || FALLBACK_IMAGE}
                    alt={a.name}
                    className="w-full h-32 object-cover"
                  />
                  <div className="p-4">
                    <p className="font-medium text-ink-900 text-sm">{a.name}</p>
                    <p className="text-xs text-ink-500 capitalize">{a.category} • {a.est_duration_hours}h</p>
                    {a.address && (
                      <p className="text-xs text-ink-500 flex items-center gap-1 mt-1">
                        <MapPin size={11} /> {a.address}
                      </p>
                    )}
                    <div className="flex justify-between items-center mt-2 text-xs">
                      <span className="text-primary-600 font-semibold">${a.entry_fee}</span>
                      <span className="flex items-center gap-1"><Star size={12} className="fill-yellow-400 text-yellow-400" /> {a.rating}</span>
                    </div>
                    {mapLink(a.latitude, a.longitude) && (
                      <a
                        href={mapLink(a.latitude, a.longitude)}
                        target="_blank"
                        rel="noreferrer"
                        className="text-xs text-primary-600 font-medium flex items-center gap-1 mt-2 hover:underline"
                      >
                        View on map <ExternalLink size={11} />
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-xl font-display font-semibold text-ink-900 mb-3 flex items-center gap-2">
              <Building2 size={18} /> Hotels
            </h2>
            <div className="grid sm:grid-cols-3 gap-3">
              {hotels.map((h) => (
                <div key={h.id} className="card overflow-hidden">
                  <img
                    src={h.image_url || FALLBACK_IMAGE}
                    alt={h.name}
                    className="w-full h-28 object-cover"
                  />
                  <div className="p-4">
                    <p className="font-medium text-ink-900 text-sm">{h.name}</p>
                    <p className="text-xs text-ink-500 capitalize">{h.category}</p>
                    {h.address && (
                      <p className="text-xs text-ink-500 flex items-center gap-1 mt-1">
                        <MapPin size={11} /> {h.address}
                      </p>
                    )}
                    <div className="flex justify-between items-center mt-2 text-xs">
                      <span className="text-primary-600 font-semibold">${h.price_per_night}/night</span>
                      <span className="flex items-center gap-1"><Star size={12} className="fill-yellow-400 text-yellow-400" /> {h.rating}</span>
                    </div>
                    {mapLink(h.latitude, h.longitude) && (
                      <a
                        href={mapLink(h.latitude, h.longitude)}
                        target="_blank"
                        rel="noreferrer"
                        className="text-xs text-primary-600 font-medium flex items-center gap-1 mt-2 hover:underline"
                      >
                        View on map <ExternalLink size={11} />
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-xl font-display font-semibold text-ink-900 mb-3 flex items-center gap-2">
              <Utensils size={18} /> Restaurants
            </h2>
            <div className="grid sm:grid-cols-3 gap-3">
              {restaurants.map((r) => (
                <div key={r.id} className="card overflow-hidden">
                  <img
                    src={r.image_url || FALLBACK_IMAGE}
                    alt={r.name}
                    className="w-full h-28 object-cover"
                  />
                  <div className="p-4">
                    <p className="font-medium text-ink-900 text-sm">{r.name}</p>
                    <p className="text-xs text-ink-500">{r.cuisine}</p>
                    {r.address && (
                      <p className="text-xs text-ink-500 flex items-center gap-1 mt-1">
                        <MapPin size={11} /> {r.address}
                      </p>
                    )}
                    <div className="flex justify-between items-center mt-2 text-xs">
                      <span className="text-primary-600 font-semibold">${r.avg_cost}/person</span>
                      <span className="flex items-center gap-1"><Star size={12} className="fill-yellow-400 text-yellow-400" /> {r.rating}</span>
                    </div>
                    {mapLink(r.latitude, r.longitude) && (
                      <a
                        href={mapLink(r.latitude, r.longitude)}
                        target="_blank"
                        rel="noreferrer"
                        className="text-xs text-primary-600 font-medium flex items-center gap-1 mt-2 hover:underline"
                      >
                        View on map <ExternalLink size={11} />
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <ReviewSection destinationId={id} />
        </div>

        <div className="space-y-6">
          <MapView latitude={destination.latitude} longitude={destination.longitude} name={destination.name} />
          <WeatherWidget city={destination.name} />
          <button onClick={() => navigate("/plan")} className="btn-primary w-full">Plan a trip here</button>
        </div>
      </div>
    </div>
  );
}