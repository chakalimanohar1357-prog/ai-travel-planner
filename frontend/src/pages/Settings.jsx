import React, { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import api from "../api/axios";
import { ArrowLeftRight } from "lucide-react";

export default function Settings() {
    const { user } = useAuth();

    // --- Profile state ---
    const [name, setName] = useState(user?.name || "");
    const [email, setEmail] = useState(user?.email || "");
    const [currentPassword, setCurrentPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [profileMsg, setProfileMsg] = useState("");
    const [profileSaving, setProfileSaving] = useState(false);

    // --- Preferences state ---
    const [theme, setTheme] = useState(
        localStorage.getItem("pref_theme") || "light"
    );
    const [notifications, setNotifications] = useState(
        localStorage.getItem("pref_notifications") !== "false"
    );
    const [prefsMsg, setPrefsMsg] = useState("");

    // --- Currency converter state ---
    const [rates, setRates] = useState(null);
    const [ratesLoading, setRatesLoading] = useState(true);
    const [ratesMock, setRatesMock] = useState(false);
    const [amount, setAmount] = useState(100);
    const [fromCurrency, setFromCurrency] = useState("USD");
    const [toCurrency, setToCurrency] = useState("INR");

    const currencies = ["USD", "EUR", "GBP", "INR", "JPY", "AUD", "CAD", "SGD", "AED"];

    useEffect(() => {
        api.get("/currency/rates")
            .then((res) => {
                setRates(res.data.rates);
                setRatesMock(res.data.mock);
            })
            .catch(() => setRates(null))
            .finally(() => setRatesLoading(false));
    }, []);

    const convertedAmount = () => {
        if (!rates || !rates[fromCurrency] || !rates[toCurrency]) return null;
        // rates are USD -> currency, so first normalize the input amount to USD, then to target
        const amountInUsd = amount / rates[fromCurrency];
        const converted = amountInUsd * rates[toCurrency];
        return converted.toFixed(2);
    };

    const swapCurrencies = () => {
        setFromCurrency(toCurrency);
        setToCurrency(fromCurrency);
    };

    const handleProfileSave = async (e) => {
        e.preventDefault();
        setProfileSaving(true);
        setProfileMsg("");
        try {
            // TODO: replace with your real backend call, e.g.:
            // await api.put("/users/me", { name, email, currentPassword, newPassword });
            await new Promise((res) => setTimeout(res, 600)); // placeholder delay
            setProfileMsg("Profile updated successfully.");
            setCurrentPassword("");
            setNewPassword("");
        } catch (err) {
            setProfileMsg("Could not update profile. Please try again.");
        } finally {
            setProfileSaving(false);
        }
    };

    const handlePrefsSave = (e) => {
        e.preventDefault();
        localStorage.setItem("pref_theme", theme);
        localStorage.setItem("pref_notifications", notifications);
        setPrefsMsg("Preferences saved.");
        setTimeout(() => setPrefsMsg(""), 2000);
    };

    return (
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <h1 className="text-2xl font-bold text-ink-900 mb-8">Settings</h1>

            {/* Profile section */}
            <section className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-8">
                <h2 className="text-lg font-semibold text-ink-900 mb-4">Profile</h2>
                <form onSubmit={handleProfileSave} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-ink-700 mb-1">Name</label>
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            className="w-full border rounded-lg p-2"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-ink-700 mb-1">Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full border rounded-lg p-2"
                        />
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-ink-700 mb-1">
                                Current password
                            </label>
                            <input
                                type="password"
                                value={currentPassword}
                                onChange={(e) => setCurrentPassword(e.target.value)}
                                className="w-full border rounded-lg p-2"
                                placeholder="Leave blank to keep unchanged"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-ink-700 mb-1">
                                New password
                            </label>
                            <input
                                type="password"
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                                className="w-full border rounded-lg p-2"
                                placeholder="Leave blank to keep unchanged"
                            />
                        </div>
                    </div>

                    <button type="submit" className="btn-primary text-sm" disabled={profileSaving}>
                        {profileSaving ? "Saving..." : "Save profile"}
                    </button>

                    {profileMsg && <p className="text-sm text-primary-600 mt-2">{profileMsg}</p>}
                </form>
            </section>

            {/* Currency Converter section */}
            <section className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-8">
                <h2 className="text-lg font-semibold text-ink-900 mb-4">Currency Converter</h2>

                {ratesLoading ? (
                    <p className="text-sm text-ink-500">Loading exchange rates...</p>
                ) : !rates ? (
                    <p className="text-sm text-red-600">Could not load exchange rates. Please try again later.</p>
                ) : (
                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-ink-700 mb-1">Amount</label>
                            <input
                                type="number"
                                min="0"
                                value={amount}
                                onChange={(e) => setAmount(Number(e.target.value))}
                                className="w-full border rounded-lg p-2"
                            />
                        </div>

                        <div className="flex items-end gap-2">
                            <div className="flex-1">
                                <label className="block text-sm font-medium text-ink-700 mb-1">From</label>
                                <select
                                    value={fromCurrency}
                                    onChange={(e) => setFromCurrency(e.target.value)}
                                    className="w-full border rounded-lg p-2"
                                >
                                    {currencies.map((c) => (
                                        <option key={c} value={c}>{c}</option>
                                    ))}
                                </select>
                            </div>

                            <button
                                type="button"
                                onClick={swapCurrencies}
                                className="mb-1 p-2 rounded-lg border border-gray-300 hover:border-primary-500 hover:text-primary-600 text-ink-700"
                                title="Swap currencies"
                            >
                                <ArrowLeftRight size={16} />
                            </button>

                            <div className="flex-1">
                                <label className="block text-sm font-medium text-ink-700 mb-1">To</label>
                                <select
                                    value={toCurrency}
                                    onChange={(e) => setToCurrency(e.target.value)}
                                    className="w-full border rounded-lg p-2"
                                >
                                    {currencies.map((c) => (
                                        <option key={c} value={c}>{c}</option>
                                    ))}
                                </select>
                            </div>
                        </div>

                        <div className="bg-primary-50 rounded-lg p-4 text-center">
                            <p className="text-xs text-ink-500 mb-1">
                                {amount} {fromCurrency} =
                            </p>
                            <p className="text-2xl font-bold text-primary-600">
                                {convertedAmount() ?? "--"} {toCurrency}
                            </p>
                        </div>

                        {ratesMock && (
                            <p className="text-xs text-ink-500">
                                *Sample rates shown — add EXCHANGE_RATE_API_KEY in the backend .env for live rates.
                            </p>
                        )}
                    </div>
                )}
            </section>

            {/* Preferences section */}
            <section className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                <h2 className="text-lg font-semibold text-ink-900 mb-4">Preferences</h2>
                <form onSubmit={handlePrefsSave} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-ink-700 mb-1">Theme</label>
                        <select
                            value={theme}
                            onChange={(e) => setTheme(e.target.value)}
                            className="w-full border rounded-lg p-2"
                        >
                            <option value="light">Light</option>
                            <option value="dark">Dark</option>
                        </select>
                    </div>

                    <div className="flex items-center gap-2">
                        <input
                            type="checkbox"
                            id="notifications"
                            checked={notifications}
                            onChange={(e) => setNotifications(e.target.checked)}
                        />
                        <label htmlFor="notifications" className="text-sm text-ink-700">
                            Email me trip reminders and offers
                        </label>
                    </div>

                    <button type="submit" className="btn-primary text-sm">
                        Save preferences
                    </button>

                    {prefsMsg && <p className="text-sm text-primary-600 mt-2">{prefsMsg}</p>}
                </form>
            </section>
        </div>
    );
}