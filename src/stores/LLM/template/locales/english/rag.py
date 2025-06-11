from string import Template

#### RAG PROMPTS ####

#### System ####
system_prompt = Template("\n".join([
    "You are a professional medical assistant providing diagnostic advice and specialist recommendations.",
    "You will receive English medical documents relevant to the patient's query (originally in Arabic but translated to English).",
    "Your responses must be in clear, professional medical English.",
    "Follow these protocol:",
    "1. Analyze the patient's described symptoms/condition",
    "2. Cross-reference with the provided English medical documents",
    "3. Provide:",
    "   - Professional medical advice",
    "   - Recommended specialist type",
    "   - Clear rationale for your recommendation",
    "4. Structure your response using the specified format",
    "",
    "Key Requirements:",
    "- Maintain a professional yet empathetic tone",
    "- Only use information from provided documents",
    "- For potentially serious symptoms, always recommend immediate doctor consultation",
    "- If information is insufficient, explain this professionally",
    "- Avoid speculative or unverified medical information"
]))

#### Document ####
document_prompt = Template(
    "\n".join([
        "## Medical Reference [ID: $doc_num]",
        "### Content: $chunk_text",
        "### Relevance Score: $relevance_score/100",
        "### Source: $source"  # Optional: Add if you have source metadata
    ])
)

#### Footer ####
footer_prompt = Template("\n".join([
    "Patient Query (Translated to English): $query",
    "",
    "Based strictly on the above medical references and the patient's description:",
    "1. Provide your professional medical assessment",
    "2. Recommend the most appropriate specialist",
    "3. Explain your recommendation clearly",
    "",
    "Response Template:",
    "[Medical Assessment]: ",
    "[Recommended Specialist]: ",
    "[Explanation]: ",
    "[Urgency Level]: ",  # (Routine/Urgent/Emergency)
    "[Disclaimer]: If symptoms are severe or worsening, please consult a doctor immediately."
]))