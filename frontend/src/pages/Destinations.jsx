import React, { useEffect, useState } from "react";
import api from "../api/axios";
import DestinationCard from "../components/DestinationCard";
import { Search } from "lucide-react";

export default function Destinations() {
  const [destinations, setDestinations] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/destinations")
      .then((res) => setDestinations(res.data.destinations))
      .finally(() => setLoading(false));
  }, []);

  const filtered = destinations.filter((d) =>
    (d.name + d.country + d.tags.join(" ")).toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-display font-bold text-ink-900 mb-2">Explore Destinations</h1>
      <p className="text-ink-500 mb-6">Browse curated destinations across the globe.</p>

      <div className="relative max-w-md mb-8">
        <Search size={16} className="absolute left-3 top-3 text-ink-500" />
        <input
          className="input-field pl-9"
          placeholder="Search by name, country, or interest..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>

      {loading ? (
        <p className="text-ink-500">Loading destinations...</p>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((d) => <DestinationCard key={d.id} destination={d} />)}
        </div>
      )}
    </div>
  );
}
