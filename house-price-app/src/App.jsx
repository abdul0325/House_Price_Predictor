import { useState } from "react";
import axios from "axios";

export default function App() {
  const [form, setForm] = useState({
    SquareFeet: "",
    Bedrooms: "",
    Bathrooms: "",
    Neighborhood: "Neighborhood1",
    YearBuilt: ""
  });
  const [price, setPrice] = useState(null);
  const [loading, setLoading] = useState(false);

  const neighborhoods = [
    "Rural",
    "Suburb",
    "Urban"
  ];

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Input validation
    for (let key of ["SquareFeet", "Bedrooms", "Bathrooms", "YearBuilt"]) {
      if (!form[key] || Number(form[key]) <= 0) {
        alert(`Please enter a valid positive value for ${key}`);
        return;
      }
    }

    setLoading(true);
    setPrice(null);
    try {
      const response = await axios.post("http://127.0.0.1:8000/predict", form);
      setPrice(response.data.predicted_price);
    } catch (err) {
      console.error(err);
      alert("Error predicting price. Make sure FastAPI is running!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl p-6 max-w-md w-full">
        <h1 className="text-3xl font-bold mb-6 text-center text-purple-600">
          House Price Predictor
        </h1>

        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <input
            name="SquareFeet"
            type="number"
            placeholder="Square Feet"
            value={form.SquareFeet}
            onChange={handleChange}
            className="border p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400"
          />
          <input
            name="Bedrooms"
            type="number"
            placeholder="Bedrooms"
            value={form.Bedrooms}
            onChange={handleChange}
            className="border p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400"
          />
          <input
            name="Bathrooms"
            type="number"
            placeholder="Bathrooms"
            value={form.Bathrooms}
            onChange={handleChange}
            className="border p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400"
          />
          <input
            name="YearBuilt"
            type="number"
            placeholder="Year Built"
            value={form.YearBuilt}
            onChange={handleChange}
            className="border p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400"
          />
          <select
            name="Neighborhood"
            value={form.Neighborhood}
            onChange={handleChange}
            className="border p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400"
          >
            {neighborhoods.map((n) => (
              <option key={n} value={n}>
                {n}
              </option>
            ))}
          </select>

          <button
            type="submit"
            className="bg-purple-600 text-white p-3 rounded-lg font-semibold hover:bg-purple-700 transition-colors mt-2 flex items-center justify-center"
            disabled={loading}
          >
            {loading ? (
              <svg
                className="animate-spin h-5 w-5 mr-2 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 00-8 8z"
                ></path>
              </svg>
            ) : null}
            {loading ? "Predicting..." : "Predict Price"}
          </button>
        </form>

        {price && (
          <div className="mt-6 bg-purple-50 p-4 rounded-xl text-center">
            <h2 className="text-xl font-bold text-purple-700">
              🏡 Predicted Price
            </h2>
            <p className="text-2xl mt-2 font-semibold text-purple-900">
              ${price.toFixed(2)}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
