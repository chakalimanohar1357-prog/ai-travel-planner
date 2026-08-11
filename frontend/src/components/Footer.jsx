import React from "react";

export default function Footer() {
  return (
    <footer className="bg-ink-900 text-gray-300 mt-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 grid grid-cols-1 md:grid-cols-4 gap-8">
        <div>
          <h3 className="text-white font-display font-bold text-lg mb-2">TravelAI</h3>
          <p className="text-sm text-gray-400">Your smart personal travel assistant, powered by AI.</p>
        </div>
        <div>
          <h4 className="text-white font-semibold mb-2 text-sm">Product</h4>
          <ul className="space-y-1 text-sm text-gray-400">
            <li>Trip Planner</li>
            <li>Destinations</li>
            <li>AI Chatbot</li>
          </ul>
        </div>
        <div>
          <h4 className="text-white font-semibold mb-2 text-sm">Company</h4>
          <ul className="space-y-1 text-sm text-gray-400">
            <li>About</li>
            <li>Careers</li>
            <li>Contact</li>
          </ul>
        </div>
        <div>
          <h4 className="text-white font-semibold mb-2 text-sm">Legal</h4>
          <ul className="space-y-1 text-sm text-gray-400">
            <li>Privacy Policy</li>
            <li>Terms of Service</li>
          </ul>
        </div>
      </div>
      <div className="border-t border-gray-800 text-center text-xs text-gray-500 py-4">
        © {new Date().getFullYear()} TravelAI — Built as a B.Tech final-year project.
      </div>
    </footer>
  );
}
