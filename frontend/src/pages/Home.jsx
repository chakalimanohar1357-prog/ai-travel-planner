import React from "react";
import { Link } from "react-router-dom";
import { Sparkles, MapPinned, Wallet, CalendarCheck, ShieldCheck, Backpack } from "lucide-react";

const FEATURES = [
  { icon: Sparkles, title: "AI-Personalized Plans", desc: "Content-based & collaborative filtering match destinations to your interests." },
  { icon: CalendarCheck, title: "Day-Wise Itineraries", desc: "Auto-generated schedules with attractions, hotels, and restaurants." },
  { icon: Wallet, title: "Budget Estimation", desc: "Transparent cost breakdown across transport, stay, food & activities." },
  { icon: MapPinned, title: "Interactive Maps", desc: "Explore destinations and optimize routes visually." },
  { icon: Backpack, title: "Smart Packing Lists", desc: "Weather- and activity-aware packing suggestions." },
  { icon: ShieldCheck, title: "Safety Tips", desc: "AI chatbot answers travel questions & shares safety guidance." },
];

export default function Home() {
  return (
    <div>
      <section className="relative bg-gradient-to-br from-primary-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 grid md:grid-cols-2 gap-10 items-center">
          <div>
            <span className="inline-block bg-primary-100 text-primary-600 text-xs font-semibold px-3 py-1 rounded-full mb-4">
              AI-Powered Travel Assistant
            </span>
            <h1 className="text-4xl md:text-5xl font-display font-bold text-ink-900 leading-tight">
              Plan your perfect trip <span className="text-primary-500">with AI</span>
            </h1>
            <p className="text-ink-500 mt-4 text-lg">
              Tell us your interests, budget, and travel style — our AI recommendation engine builds
              a personalized day-wise itinerary, estimates your costs, and keeps you weather-ready.
            </p>
            <div className="flex gap-3 mt-8">
              <Link to="/plan" className="btn-primary">Plan My Trip</Link>
              <Link to="/destinations" className="btn-outline">Explore Destinations</Link>
            </div>
          </div>
          <div className="relative">
            <img
              src="https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=800&q=80"
              alt="Travel"
              className="rounded-xl2 shadow-card-hover w-full h-96 object-cover"
            />
          </div>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-2xl font-display font-bold text-center text-ink-900 mb-2">Everything you need for stress-free travel</h2>
        <p className="text-center text-ink-500 mb-10">From discovery to departure — powered by AI</p>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {FEATURES.map((f) => (
            <div key={f.title} className="card p-6">
              <div className="bg-primary-50 text-primary-500 w-11 h-11 rounded-xl flex items-center justify-center mb-4">
                <f.icon size={22} />
              </div>
              <h3 className="font-display font-semibold text-ink-900 mb-1">{f.title}</h3>
              <p className="text-sm text-ink-500">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-ink-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
          <h2 className="text-3xl font-display font-bold mb-3">Ready to start planning?</h2>
          <p className="text-gray-400 mb-8">Join now and let AI craft your next adventure.</p>
          <Link to="/register" className="btn-primary inline-block">Get Started Free</Link>
        </div>
      </section>
    </div>
  );
}
