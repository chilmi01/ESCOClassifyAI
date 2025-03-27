import axios from "axios";

// This is a mock template assuming the ESCOSkillExtractor is hosted locally or on a server.
const API_BASE_URL = "http://localhost:5000/api"; // Adjust based on your actual deployment

/**
 * Send text to the ESCOSkillExtractor backend and retrieve extracted skills.
 * @param {string} title - The title of the document
 * @param {string} abstract - The abstract or body text
 * @returns {Promise<object>} Extracted skills and occupations
 */
export async function extractSkills(title, abstract) {
  try {
    const response = await axios.post(`${API_BASE_URL}/extract`, {
      title,
      abstract
    });
    return response.data;
  } catch (error) {
    console.error("Skill extraction failed:", error);
    return { success: false, error: error.message };
  }
}
