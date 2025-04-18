const fetch = require("node-fetch");

async function run() {
  // Fetch API
  let response = await fetch(
    "https://product.aiqod.com/genai_chatbot/chatbot/chat",
    {
      method: "POST",

      headers: { Origin: "Go-agile", "Content-Type": "application/json" },
      body: JSON.stringify({
        input: {
          prompt: "Please provide the pricing details",
          userId: "660f798f211a9401f8a6cd58",
          orgId: "660f798f211a9401f8a6cd47",
          subscriberId: "660f798f211a9401f8a6cd46",
          mode: "online",
          collN: "Chat Genie",
          supervisor: "admin",
          permission: "sub",
          module: "document",
        },
      }),
    }
  );

  console.log(await response.json());
  //   response = JSON.parse(JSON.stringify(response));
  //   console.log(response)
}

run();
