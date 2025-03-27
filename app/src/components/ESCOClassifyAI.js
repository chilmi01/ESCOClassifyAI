import React from "react";

export default function ESCOClassifyAI() {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-4 text-center">ESCOClassifyAI</h1>
      <div className="grid md:grid-cols-2 gap-4 max-w-4xl mx-auto">
        <div className="border p-4 rounded bg-white">
          <h2 className="text-xl font-semibold mb-2">Upload Thesis</h2>
          <input type="file" className="mb-2" />
          <select className="w-full border rounded p-1 mb-2">
            <option>BSc</option>
            <option>MSc</option>
            <option>PhD</option>
          </select>
          <button className="w-full bg-blue-600 text-white py-2 rounded">Analyze</button>
        </div>
        <div className="border p-4 rounded bg-white">
          <h2 className="text-xl font-semibold mb-2">Statistics</h2>
          <p>Total Skills Extracted: <strong>152</strong></p>
          <p>Top STEM Category: <strong>Engineering</strong></p>
          <h3 className="mt-4 font-semibold">Multinomial Result</h3>
          <div className="w-full bg-gray-200 rounded h-4 mt-1">
            <div className="bg-blue-500 h-4 rounded" style={{ width: "65%" }}></div>
          </div>
          <h3 className="mt-4 font-semibold">Top Skills</h3>
          <ul className="list-disc list-inside">
            <li>Feasibility study</li>
            <li>Chromatography</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
