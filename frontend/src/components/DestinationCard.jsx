import React from "react";
import { useNavigate } from "react-router-dom";
import { MapPin, Star, Heart } from "lucide-react";

export default function DestinationCard({ destination, onFavorite, isFavorite, score }) {
  const navigate = useNavigate();

  return (
    <div className="card overflow-hidden group cursor-pointer" onClick={() => navigate(`/destinations/${destination.id}`)}>
      <div className="relative h-48 overflow-hidden">
        <img
          src={destination.image_url || "https://images.unsplash.com/photo-1488646953014-85cb44e25828"}
          alt={destination.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />
        {onFavorite && (
          <button
            onClick={(e) => { e.stopPropagation(); onFavorite(destination.id); }}
            className="absolute top-3 right-3 bg-white/90 p-2 rounded-full shadow-sm hover:bg-white"
          >
            <Heart size={16} className={isFavorite ? "fill-primary-500 text-primary-500" : "text-ink-700"} />
          </button>
        )}
        {score !== undefined && (
          <span className="absolute bottom-3 left-3 bg-primary-500 text-white text-xs font-semibold px-2 py-1 rounded-full">
            {Math.round(score * 100)}% match
          </span>
        )}
      </div>
      <div className="p-4">
        <div className="flex items-start justify-between">
          <div>
            <h3 className="font-display font-semibold text-ink-900">{destination.name}</h3>
            <p className="text-xs text-ink-500 flex items-center gap-1 mt-0.5">
              <MapPin size={12} /> {destination.country}
            </p>
          </div>
          <div className="flex items-center gap-1 text-xs font-semibold text-ink-700">
            <Star size={13} className="fill-yellow-400 text-yellow-400" />
            {(destination.popularity_score * 5).toFixed(1)}
          </div>
        </div>
        <p className="text-sm text-ink-500 mt-2 line-clamp-2">{destination.description}</p>
        <div className="flex items-center justify-between mt-3">
          <span className="text-xs text-ink-500">From</span>
          <span className="font-semibold text-primary-600">${destination.avg_daily_cost}/day</span>
        </div>
        <div className="flex flex-wrap gap-1 mt-2">
          {(destination.tags || []).slice(0, 3).map((tag) => (
            <span key={tag} className="text-[10px] bg-primary-50 text-primary-600 px-2 py-0.5 rounded-full capitalize">
              {tag}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
