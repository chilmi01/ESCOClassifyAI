import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

const data = [
  { skill: "Feasibility study", count: 110 },
  { skill: "Chromatography", count: 95 },
  { skill: "Data modeling", count: 87 },
  { skill: "Scientific writing", count: 80 },
  { skill: "Simulation", count: 75 },
];

export default function SkillChart() {
  return (
    <div className="p-4 bg-white rounded shadow mt-6">
      <h2 className="text-xl font-semibold mb-4">Top Skills Extracted</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="skill" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#3B82F6" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
