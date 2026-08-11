import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/axios";
import WeatherWidget from "../components/WeatherWidget";
import { Wallet, Backpack, ShieldCheck, Hotel, Utensils, MapPin, Clock } from "lucide-react";

const SAFETY_TIPS = [
  "Keep digital & physical copies of your ID, passport, and bookings.",
  "Share your itinerary with a trusted friend or family member.",
  "Use registered transport and avoid isolated areas after dark.",
  "Keep local emergency numbers and your embassy contact handy.",
  "Stay hydrated and respect local customs & dress codes.",
];

export default function TripPlanResult() {
  const { id } = useParams();
  const [trip, setTrip] = useState(null);
  const [packingList, setPackingList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get(`/trips/${id}`).then((res) => setTrip(res.data.trip)).finally(() => setLoading(false));
    api.get(`/trips/${id}/packing-list`).then((res) => setPackingList(res.data.packing_list)).catch(() => {});
  }, [id]);

  if (loading) return <p className="text-center py-24 text-ink-500">Loading your itinerary...</p>;
  if (!trip) return <p className="text-center py-24 text-ink-500">Trip not found.</p>;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-display font-bold text-ink-900">Your Trip to {trip.destination_name}</h1>
        <p className="text-ink-500 mt-1">
          {trip.duration_days} days • {trip.travelers} traveler(s) • {trip.transport_mode} • Budget ${trip.budget}
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <h2 className="text-xl font-display font-semibold text-ink-900">Day-Wise Itinerary</h2>
          {trip.itinerary.map((day) => (
            <div key={day.day} className="card p-5">
              <h3 className="font-display font-semibold text-ink-900 mb-3">{day.title}</h3>
              <ul className="space-y-2 mb-4">
                {day.activities.map((act, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-ink-700">
                    <Clock size={14} className="mt-0.5 text-primary-500 shrink-0" />
                    <span>
                      <strong>{act.time}:</strong> {act.activity}
                      {act.duration_hours && ` (~${act.duration_hours}h)`}
                      {act.entry_fee ? ` — $${act.entry_fee} entry` : ""}
                    </span>
                  </li>
                ))}
              </ul>
              <div className="grid sm:grid-cols-3 gap-3 text-xs">
                {day.hotel && (
                  <div className="bg-primary-50 rounded-lg p-2 flex items-start gap-2">
                    <Hotel size={14} className="text-primary-500 mt-0.5" />
                    <div>
                      <p className="font-medium text-ink-900">{day.hotel.name}</p>
                      <p className="text-ink-500">${day.hotel.price_per_night}/night</p>
                    </div>
                  </div>
                )}
                {day.lunch && (
                  <div className="bg-primary-50 rounded-lg p-2 flex items-start gap-2">
                    <Utensils size={14} className="text-primary-500 mt-0.5" />
                    <div>
                      <p className="font-medium text-ink-900">Lunch: {day.lunch.name}</p>
                      <p className="text-ink-500">${day.lunch.avg_cost}/person</p>
                    </div>
                  </div>
                )}
                {day.dinner && (
                  <div className="bg-primary-50 rounded-lg p-2 flex items-start gap-2">
                    <Utensils size={14} className="text-primary-500 mt-0.5" />
                    <div>
                      <p className="font-medium text-ink-900">Dinner: {day.dinner.name}</p>
                      <p className="text-ink-500">${day.dinner.avg_cost}/person</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="space-y-6">
          <div className="card p-5">
            <h3 className="font-display font-semibold text-ink-900 mb-3 flex items-center gap-2">
              <Wallet size={18} className="text-primary-500" /> Estimated Cost
            </h3>
            <p className="text-3xl font-bold text-primary-600 mb-2">${trip.estimated_cost}</p>
            <p className="text-xs text-ink-500">Total estimate for {trip.travelers} traveler(s), all-inclusive.</p>
          </div>

          <WeatherWidget city={trip.destination_name} />

          <div className="card p-5">
            <h3 className="font-display font-semibold text-ink-900 mb-3 flex items-center gap-2">
              <ShieldCheck size={18} className="text-primary-500" /> Safety Tips
            </h3>
            <ul className="space-y-2 text-sm text-ink-700 list-disc list-inside">
              {SAFETY_TIPS.map((tip, i) => <li key={i}>{tip}</li>)}
            </ul>
          </div>

          <div className="card p-5">
            <h3 className="font-display font-semibold text-ink-900 mb-3 flex items-center gap-2">
              <Backpack size={18} className="text-primary-500" /> Packing List
            </h3>
            <p className="text-xs text-ink-500 mb-2 flex items-center gap-1">
              <MapPin size={12} /> Based on your interests: {trip.interests.join(", ")}
            </p>
            <ul className="text-sm text-ink-700 space-y-1 max-h-56 overflow-y-auto pr-1">
              {packingList.map((item, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-primary-500">•</span> {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
