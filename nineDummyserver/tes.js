
const {GoogleGenAI} = require("@google/genai");
const ai = new GoogleGenAI({ apiKey: "AIzaSyCwfg4xDLCh9gHf1wIA2Miy4VAifWuUjdY" });

async function callGemini(prompt) { // last parameters contains info from headerParams
    const requestId = Date.now().toString();
    try {
        
        const response = await ai.models.generateContent({
            model: "gemini-2.5-flash-preview-04-17",
            contents: prompt,
          });
          let output = response.text

        console.log(output)
        console.log("Type ",typeof output)

        let cleaned = output.replace(/^`+json\n|`+$/g, '');

        let parsed;
        try {
        parsed = JSON.parse(cleaned);
        console.log("hello "+parsed.ouptut); // Note the typo: "ouptut"
        } catch (e) {
        console.error('Failed to parse JSON:', e);
        }
        
        return parsed
        
        
    } catch (error) {
        console.error('Error:', error);
        return { message: 'There was an error running this function' };
    }
}

callGemini(`Give me  the top 10 countries with their capital
    Populate the response in json ; {ouptut : [{'country':'capital'}]}
    `)