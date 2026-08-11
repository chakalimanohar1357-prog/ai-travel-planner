import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import DestinationCard from "../components/DestinationCard";

const INTERESTS = ["adventure", "beaches", "nature", "history", "shopping", "nightlife", "wildlife"];
const TRANSPORT = ["flight", "train", "bus", "car", "cruise"];
const ACCOMMODATION = ["budget", "mid-range", "luxury"];

export default function PlanTrip() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({
    budget: 1000,
    duration_days: 5,
    travelers: 2,
    interests: [],
    transport_mode: "flight",
    accommodation_pref: "mid-range",
  });
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const toggleInterest = (interest) => {
    setForm((f) => ({
      ...f,
      interests: f.interests.includes(interest)
        ? f.interests.filter((i) => i !== interest)
        : [...f.interests, interest],
    }));
  };

  const getRecommendations = async () => {
    setError("");
    if (form.interests.length === 0) {
      setError("Please select at least one interest.");
      return;
    }
    setLoading(true);
    try {
      const res = await api.post("/recommendations/destinations", form);
      setRecommendations(res.data.recommendations);
      setStep(2);
    } catch (err) {
      setError(err.response?.data?.error || "Could not fetch recommendations");
    } finally {
      setLoading(false);
    }
  };

  const selectDestination = async (destinationId) => {
    setLoading(true);
    setError("");
    try {
      const res = await api.post("/trips/plan", { ...form, destination_id: destinationId });
      navigate(`/trips/${res.data.trip.id}`);
    } catch (err) {
      setError(err.response?.data?.error || "Could not generate itinerary");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-display font-bold text-ink-900 mb-2">Plan Your Trip</h1>
      <p className="text-ink-500 mb-8">Tell us your preferences and let AI recommend the perfect destination & itinerary.</p>

      {error && <div className="bg-red-50 text-red-600 text-sm p-3 rounded-lg mb-6">{error}</div>}

      {step === 1 && (
        <div className="card p-6 md:p-8 space-y-6">
          <div className="grid md:grid-cols-3 gap-4">
            <div>
              <label className="text-sm font-medium text-ink-700">Total Budget (USD)</label>
              <input type="number" min="50" className="input-field mt-1"
                value={form.budget}
                onChange={(e) => setForm({ ...form, budget: Number(e.target.value) })} />
            </div>
            <div>
              <label className="text-sm font-medium text-ink-700">Trip Duration (days)</label>
              <input type="number" min="1" max="30" className="input-field mt-1"
                value={form.duration_days}
                onChange={(e) => setForm({ ...form, duration_days: Number(e.target.value) })} />
            </div>
            <div>
              <label className="text-sm font-medium text-ink-700">Number of Travelers</label>
              <input type="number" min="1" max="20" className="input-field mt-1"
                value={form.travelers}
                onChange={(e) => setForm({ ...form, travelers: Number(e.target.value) })} />
            </div>
          </div>

          <div>
            <label className="text-sm font-medium text-ink-700 mb-2 block">Interests</label>
            <div className="flex flex-wrap gap-2">
              {INTERESTS.map((interest) => (
                <button
                  key={interest}
                  type="button"
                  onClick={() => toggleInterest(interest)}
                  className={`text-sm px-4 py-2 rounded-full capitalize border transition-colors ${
                    form.interests.includes(interest)
                      ? "bg-primary-500 text-white border-primary-500"
                      : "border-gray-300 text-ink-700 hover:border-primary-400"
                  }`}
                >
                  {interest}
                </button>
              ))}
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium text-ink-700 mb-2 block">Transportation Mode</label>
              <div className="flex flex-wrap gap-2">
                {TRANSPORT.map((t) => (
                  <button key={t} type="button" onClick={() => setForm({ ...form, transport_mode: t })}
                    className={`text-sm px-3 py-1.5 rounded-lg capitalize border ${
                      form.transport_mode === t ? "bg-primary-500 text-white border-primary-500" : "border-gray-300 text-ink-700"
                    }`}>
                    {t}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label className="text-sm font-medium text-ink-700 mb-2 block">Accommodation Preference</label>
              <div className="flex flex-wrap gap-2">
                {ACCOMMODATION.map((a) => (
                  <button key={a} type="button" onClick={() => setForm({ ...form, accommodation_pref: a })}
                    className={`text-sm px-3 py-1.5 rounded-lg capitalize border ${
                      form.accommodation_pref === a ? "bg-primary-500 text-white border-primary-500" : "border-gray-300 text-ink-700"
                    }`}>
                    {a}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <button onClick={getRecommendations} disabled={loading} className="btn-primary w-full md:w-auto">
            {loading ? "Finding destinations..." : "Get AI Recommendations"}
          </button>
        </div>
      )}

      {step === 2 && (
        <div>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-display font-semibold text-ink-900">Recommended for you</h2>
            <button onClick={() => setStep(1)} className="text-sm text-primary-600 font-medium">Edit preferences</button>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {recommendations.map((r) => (
              <div key={r.destination.id} onClick={() => !loading && selectDestination(r.destination.id)}>
                <DestinationCard destination={r.destination} score={r.final_score} />
              </div>
            ))}
          </div>
          {loading && <p className="text-center text-ink-500 mt-6">Generating your itinerary...</p>}
        </div>
      )}
    </div>
  );
}
