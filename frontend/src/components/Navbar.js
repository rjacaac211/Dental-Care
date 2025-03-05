import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="bg-gray-900 text-white py-4 px-6 flex justify-between items-center">
      <h1 className="text-xl font-bold">Dental Care PH</h1>
      <div className="space-x-4">
        <Link
          to="/"
          className="px-3 py-2 rounded-md transition-colors duration-200 hover:bg-gray-700">
            Home
        </Link>
        <Link
          to="/about"
          className="px-3 py-2 rounded-md transition-colors duration-200 hover:bg-gray-700">
            About
          </Link>
        <Link
          to="/products"
          className="px-3 py-2 rounded-md transition-colors duration-200 hover:bg-gray-700">
            Products
          </Link>
        <Link
          to="/contact"
          className="px-3 py-2 rounded-md transition-colors duration-200 hover:bg-gray-700">
            Contact
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
