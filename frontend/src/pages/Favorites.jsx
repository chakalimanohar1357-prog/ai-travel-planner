import React, { useEffect, useState } from "react";
import api from "../api/axios";
import DestinationCard from "../components/DestinationCard";

export default function Favorites() {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadFavorites = () => {
    api.get("/trips/favorites").then((res) => setFavorites(res.data.favorites)).finally(() => setLoading(false));
  };

  useEffect(() => { loadFavorites(); }, []);

  const removeFavorite = async (destinationId) => {
    await api.delete(`/trips/favorites/${destinationId}`);
    loadFavorites();
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-display font-bold text-ink-900 mb-2">Saved Favorites</h1>
      <p className="text-ink-500 mb-8">Destinations you've bookmarked for later.</p>

      {loading ? (
        <p className="text-ink-500">Loading...</p>
      ) : favorites.length === 0 ? (
        <div className="card p-10 text-center text-ink-500">No favorites yet. Explore destinations and tap the heart icon to save them here.</div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {favorites.map((d) => (
            <DestinationCard key={d.id} destination={d} isFavorite onFavorite={removeFavorite} />
          ))}
        </div>
      )}
    </div>
  );
}
