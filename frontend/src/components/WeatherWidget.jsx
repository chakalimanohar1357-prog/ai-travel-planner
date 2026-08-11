import React, { useEffect, useState } from "react";
import { CloudSun, Droplets } from "lucide-react";
import api from "../api/axios";

export default function WeatherWidget({ city }) {
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!city) return;
    setLoading(true);
    api
      .get("/external/weather", { params: { city } })
      .then((res) => setWeather(res.data))
      .catch(() => setWeather(null))
      .finally(() => setLoading(false));
  }, [city]);

  if (loading) return <div className="card p-4 text-sm text-ink-500">Loading weather...</div>;
  if (!weather) return null;

  return (
    <div className="card p-4">
      <div className="flex items-center justify-between mb-3">
        <h4 className="font-display font-semibold text-sm text-ink-900">Weather in {weather.city}</h4>
        <CloudSun size={20} className="text-primary-500" />
      </div>
      <div className="flex items-center gap-4">
        <span className="text-3xl font-bold text-ink-900">{Math.round(weather.temperature_c)}°C</span>
        <div>
          <p className="text-sm text-ink-700 capitalize">{weather.condition}</p>
          <p className="text-xs text-ink-500 flex items-center gap-1">
            <Droplets size={12} /> {weather.humidity}% humidity
          </p>
        </div>
      </div>
      {weather.forecast && (
        <div className="grid grid-cols-3 gap-2 mt-4">
          {weather.forecast.map((f) => (
            <div key={f.day} className="bg-primary-50 rounded-lg p-2 text-center">
              <p className="text-[10px] text-ink-500">{f.day}</p>
              <p className="text-sm font-semibold text-ink-900">{f.temp_c}°C</p>
              <p className="text-[10px] text-ink-500">{f.condition}</p>
            </div>
          ))}
        </div>
      )}
      {weather.mock && <p className="text-[10px] text-ink-500 mt-2">*Sample data — add OPENWEATHER_API_KEY for live forecasts.</p>}
    </div>
  );
}
