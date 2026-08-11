import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";
import { Calendar, Users, Wallet, Trash2, MapPin } from "lucide-react";

const STATUS_COLORS = {
  planned: "bg-blue-50 text-blue-600",
  ongoing: "bg-yellow-50 text-yellow-600",
  completed: "bg-green-50 text-green-600",
};

export default function Dashboard() {
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadTrips = () => {
    api.get("/trips").then((res) => setTrips(res.data.trips)).finally(() => setLoading(false));
  };

  useEffect(() => { loadTrips(); }, []);

  const updateStatus = async (tripId, status) => {
    await api.patch(`/trips/${tripId}/status`, { status });
    loadTrips();
  };

  const deleteTrip = async (tripId) => {
    if (!window.confirm("Delete this trip permanently?")) return;
    await api.delete(`/trips/${tripId}`);
    loadTrips();
  };

  const totalSpend = trips.reduce((sum, t) => sum + t.estimated_cost, 0);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-display font-bold text-ink-900">My Trips</h1>
          <p className="text-ink-500 mt-1">{trips.length} trip(s) planned • ${totalSpend.toFixed(2)} total estimated spend</p>
        </div>
        <Link to="/plan" className="btn-primary">Plan New Trip</Link>
      </div>

      {loading ? (
        <p className="text-ink-500">Loading your trips...</p>
      ) : trips.length === 0 ? (
        <div className="card p-10 text-center">
          <p className="text-ink-500 mb-4">You haven't planned any trips yet.</p>
          <Link to="/plan" className="btn-primary inline-block">Plan Your First Trip</Link>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 gap-6">
          {trips.map((trip) => (
            <div key={trip.id} className="card p-5">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-display font-semibold text-ink-900 flex items-center gap-1">
                    <MapPin size={16} className="text-primary-500" /> {trip.destination_name}
                  </h3>
                  <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full capitalize inline-block mt-1 ${STATUS_COLORS[trip.status]}`}>
                    {trip.status}
                  </span>
                </div>
                <button onClick={() => deleteTrip(trip.id)} className="text-ink-500 hover:text-red-500">
                  <Trash2 size={16} />
                </button>
              </div>

              <div className="grid grid-cols-3 gap-2 mt-4 text-xs text-ink-500">
                <span className="flex items-center gap-1"><Calendar size={12} /> {trip.duration_days} days</span>
                <span className="flex items-center gap-1"><Users size={12} /> {trip.travelers}</span>
                <span className="flex items-center gap-1"><Wallet size={12} /> ${trip.estimated_cost}</span>
              </div>

              <div className="flex flex-wrap gap-1 mt-3">
                {trip.interests.map((i) => (
                  <span key={i} className="text-[10px] bg-primary-50 text-primary-600 px-2 py-0.5 rounded-full capitalize">{i}</span>
                ))}
              </div>

              <div className="flex items-center justify-between mt-4">
                <select
                  value={trip.status}
                  onChange={(e) => updateStatus(trip.id, e.target.value)}
                  className="text-xs border border-gray-300 rounded-lg px-2 py-1"
                >
                  <option value="planned">Planned</option>
                  <option value="ongoing">Ongoing</option>
                  <option value="completed">Completed</option>
                </select>
                <Link to={`/trips/${trip.id}`} className="text-sm font-medium text-primary-600">View Itinerary →</Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
