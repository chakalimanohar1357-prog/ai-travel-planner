import React, { useEffect, useState } from "react";
import api from "../api/axios";
import { Users, MapPin, Briefcase, Hotel, Utensils, Trash2, Plus } from "lucide-react";

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [destinations, setDestinations] = useState([]);
  const [tab, setTab] = useState("overview");
  const [newDest, setNewDest] = useState({ name: "", country: "", description: "", tags: "", avg_daily_cost: 50 });

  const loadAll = () => {
    api.get("/admin/stats").then((res) => setStats(res.data));
    api.get("/admin/users").then((res) => setUsers(res.data.users));
    api.get("/destinations").then((res) => setDestinations(res.data.destinations));
  };

  useEffect(() => { loadAll(); }, []);

  const deleteUser = async (id) => {
    if (!window.confirm("Delete this user?")) return;
    await api.delete(`/admin/users/${id}`);
    loadAll();
  };

  const deleteDestination = async (id) => {
    if (!window.confirm("Delete this destination?")) return;
    await api.delete(`/admin/destinations/${id}`);
    loadAll();
  };

  const createDestination = async (e) => {
    e.preventDefault();
    await api.post("/admin/destinations", {
      ...newDest,
      tags: newDest.tags.split(",").map((t) => t.trim()).filter(Boolean),
      avg_daily_cost: Number(newDest.avg_daily_cost),
    });
    setNewDest({ name: "", country: "", description: "", tags: "", avg_daily_cost: 50 });
    loadAll();
  };

  const statCards = stats && [
    { label: "Users", value: stats.total_users, icon: Users },
    { label: "Destinations", value: stats.total_destinations, icon: MapPin },
    { label: "Trips Planned", value: stats.total_trips, icon: Briefcase },
    { label: "Hotels", value: stats.total_hotels, icon: Hotel },
    { label: "Restaurants", value: stats.total_restaurants, icon: Utensils },
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-display font-bold text-ink-900 mb-2">Admin Dashboard</h1>
      <p className="text-ink-500 mb-8">Manage destinations, hotels, restaurants, and users.</p>

      <div className="flex gap-2 mb-8 border-b border-gray-200">
        {["overview", "destinations", "users"].map((t) => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-4 py-2 text-sm font-medium capitalize border-b-2 ${tab === t ? "border-primary-500 text-primary-600" : "border-transparent text-ink-500"}`}>
            {t}
          </button>
        ))}
      </div>

      {tab === "overview" && stats && (
        <div className="grid sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {statCards.map((s) => (
            <div key={s.label} className="card p-5 text-center">
              <s.icon className="mx-auto text-primary-500 mb-2" size={22} />
              <p className="text-2xl font-bold text-ink-900">{s.value}</p>
              <p className="text-xs text-ink-500">{s.label}</p>
            </div>
          ))}
        </div>
      )}

      {tab === "destinations" && (
        <div className="space-y-8">
          <form onSubmit={createDestination} className="card p-5 grid sm:grid-cols-2 gap-3">
            <input required placeholder="Name" className="input-field" value={newDest.name}
              onChange={(e) => setNewDest({ ...newDest, name: e.target.value })} />
            <input required placeholder="Country" className="input-field" value={newDest.country}
              onChange={(e) => setNewDest({ ...newDest, country: e.target.value })} />
            <input placeholder="Tags (comma separated)" className="input-field sm:col-span-2" value={newDest.tags}
              onChange={(e) => setNewDest({ ...newDest, tags: e.target.value })} />
            <textarea placeholder="Description" className="input-field sm:col-span-2" value={newDest.description}
              onChange={(e) => setNewDest({ ...newDest, description: e.target.value })} />
            <input type="number" placeholder="Avg daily cost" className="input-field" value={newDest.avg_daily_cost}
              onChange={(e) => setNewDest({ ...newDest, avg_daily_cost: e.target.value })} />
            <button type="submit" className="btn-primary flex items-center justify-center gap-2 sm:col-span-2">
              <Plus size={16} /> Add Destination
            </button>
          </form>

          <div className="grid sm:grid-cols-2 gap-3">
            {destinations.map((d) => (
              <div key={d.id} className="card p-4 flex items-center justify-between">
                <div>
                  <p className="font-medium text-ink-900 text-sm">{d.name}, {d.country}</p>
                  <p className="text-xs text-ink-500">${d.avg_daily_cost}/day</p>
                </div>
                <button onClick={() => deleteDestination(d.id)} className="text-ink-500 hover:text-red-500">
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {tab === "users" && (
        <div className="card divide-y divide-gray-100">
          {users.map((u) => (
            <div key={u.id} className="flex items-center justify-between p-4">
              <div>
                <p className="font-medium text-ink-900 text-sm">{u.name}</p>
                <p className="text-xs text-ink-500">{u.email} • {u.role}</p>
              </div>
              {u.role !== "admin" && (
                <button onClick={() => deleteUser(u.id)} className="text-ink-500 hover:text-red-500">
                  <Trash2 size={16} />
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
