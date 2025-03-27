export async function mockUpload(file) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        success: true,
        timestamp: new Date().toLocaleTimeString(),
        skills: [
          "Feasibility study",
          "Chromatography",
          "Scientific writing",
          "Data modeling",
          "Simulation"
        ],
        totalSkills: 152,
        topCategory: "Engineering"
      });
    }, 1500);
  });
}
