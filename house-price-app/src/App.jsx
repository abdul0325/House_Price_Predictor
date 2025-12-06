import { useState } from "react";
import axios from "axios";

export default function App() {
  const [form, setForm] = useState({
    SquareFeet: "",
    Bedrooms: "",
    Bathrooms: "",
    Neighborhood: "Neighborhood1",
    YearBuilt: "",
  });
  const [price, setPrice] = useState(null);
  const [loading, setLoading] = useState(false);

  const neighborhoods = ["Rural", "Suburb", "Urban"];

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
      alert("Error predicting price. Make sure Backend API is running!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#ECE5D8] flex items-center justify-center px-4 py-10">
      <div className="bg-[#F7F3ED] rounded-xl shadow-lg p-6 sm:p-8 w-full max-w-md md:max-w-lg border border-[#D6C7B2]">
        <h1 className="text-xl sm:text-2xl font-semibold mb-6 text-center text-[#5C3A21]">
          House Price Estimator
        </h1>

        <form
          onSubmit={handleSubmit}
          className="grid grid-cols-1 sm:grid-cols-2 gap-4"
        >
          {/* Square Feet */}
          <div className="flex flex-col gap-1 sm:col-span-2">
            <label className="text-sm font-medium text-[#5C3A21]">
              Square Feet
            </label>
            <input
              name="SquareFeet"
              type="number"
              placeholder="Enter total area"
              value={form.SquareFeet}
              onChange={handleChange}
              className="border border-[#CBB8A0] p-3 rounded-md bg-[#FBF9F6] focus:outline-none focus:ring-1 focus:ring-[#8B5E3C]"
            />
          </div>

          {/* Bedrooms */}
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-[#5C3A21]">
              Bedrooms
            </label>
            <input
              name="Bedrooms"
              type="number"
              placeholder="e.g. 3"
              value={form.Bedrooms}
              onChange={handleChange}
              className="border border-[#CBB8A0] p-3 rounded-md bg-[#FBF9F6] focus:outline-none focus:ring-1 focus:ring-[#8B5E3C]"
            />
          </div>

          {/* Bathrooms */}
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-[#5C3A21]">
              Bathrooms
            </label>
            <input
              name="Bathrooms"
              type="number"
              placeholder="e.g. 2"
              value={form.Bathrooms}
              onChange={handleChange}
              className="border border-[#CBB8A0] p-3 rounded-md bg-[#FBF9F6] focus:outline-none focus:ring-1 focus:ring-[#8B5E3C]"
            />
          </div>

          {/* Year Built */}
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-[#5C3A21]">
              Year Built
            </label>
            <input
              name="YearBuilt"
              type="number"
              placeholder="e.g. 2018"
              value={form.YearBuilt}
              onChange={handleChange}
              className="border border-[#CBB8A0] p-3 rounded-md bg-[#FBF9F6] focus:outline-none focus:ring-1 focus:ring-[#8B5E3C]"
            />
          </div>

          {/* Neighborhood */}
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-[#5C3A21]">
              Neighborhood
            </label>
            <select
              name="Neighborhood"
              value={form.Neighborhood}
              onChange={handleChange}
              className="border border-[#CBB8A0] p-3 rounded-md bg-[#FBF9F6] focus:outline-none focus:ring-1 focus:ring-[#8B5E3C]"
            >
              {neighborhoods.map((n) => (
                <option key={n} value={n}>
                  {n}
                </option>
              ))}
            </select>
          </div>

          {/* Submit Button */}
          <div className="sm:col-span-2">
            <button
              type="submit"
              disabled={loading}
              className="w-full mt-2 bg-[#8B5E3C] text-white p-3 rounded-md font-medium hover:bg-[#6F4528] transition flex items-center justify-center"
            >
              {loading ? (
                <>
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
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 00-8 8z"
                    />
                  </svg>
                  Estimating...
                </>
              ) : (
                "Estimate Price"
              )}
            </button>
          </div>
        </form>

        {price && (
          <div className="mt-6 bg-[#EFE6D8] p-4 rounded-lg text-center border border-[#D6C7B2]">
            <h2 className="text-base sm:text-lg font-semibold text-[#5C3A21]">
              Estimated Property Value
            </h2>
            <p className="text-xl sm:text-2xl mt-2 font-bold text-[#3E2615]">
              ${price.toFixed(2)}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
