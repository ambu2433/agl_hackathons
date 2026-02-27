import Groq from "@groq/sdk";
import fs from "fs";
import path from "path";
import crypto from "crypto";
import sharp from "sharp";
import readline from "readline";
import os from "os";
import dotenv from "dotenv";

dotenv.config();

const photosDir = path.join(os.homedir(), "Desktop/walgreens photoes");

// Helper: Create readline interface for user input
function createReadlineInterface() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
}

// Helper: Ask user a question
function askQuestion(question) {
  return new Promise((resolve) => {
    const rl = createReadlineInterface();
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}

// Helper: Ask user for confirmation
function askUserConfirmation(question) {
  return new Promise((resolve) => {
    const rl = createReadlineInterface();
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.toLowerCase() === "yes" || answer.toLowerCase() === "y");
    });
  });
}

// Tool: Get available years
function getAvailableYears() {
  if (!fs.existsSync(photosDir)) {
    console.log(`❌ Pictures directory not found at ${photosDir}`);
    return [];
  }

  const files = fs.readdirSync(photosDir).filter(file => 
    /\.(jpg|jpeg|png|gif|webp)$/i.test(file)
  );

  const years = new Set();
  
  for (const file of files) {
    try {
      const filePath = path.join(photosDir, file);
      const stats = fs.statSync(filePath);
      const year = stats.birthtime.getFullYear();
      years.add(year);
    } catch (error) {
      console.error(`Error reading file ${file}:`, error.message);
    }
  }

  return Array.from(years).sort((a, b) => b - a);
}

// Tool: List photos from a specific year
function listPhotosByYear(year) {
  if (!fs.existsSync(photosDir)) {
    return { error: `Pictures directory not found at ${photosDir}` };
  }

  const files = fs.readdirSync(photosDir).filter(file => 
    /\.(jpg|jpeg|png|gif|webp)$/i.test(file)
  );

  const photosFromYear = [];

  for (const file of files) {
    try {
      const filePath = path.join(photosDir, file);
      const stats = fs.statSync(filePath);
      const fileYear = stats.birthtime.getFullYear();
      
      if (fileYear === year) {
        photosFromYear.push({
          filename: file,
          date: stats.birthtime.toISOString(),
          size: `${(stats.size / 1024 / 1024).toFixed(2)} MB`
        });
      }
    } catch (error) {
      console.error(`Error reading file ${file}:`, error.message);
    }
  }

  return {
    year,
    count: photosFromYear.length,
    photos: photosFromYear.sort((a, b) => new Date(b.date) - new Date(a.date))
  };
}

// Tool: Detect duplicate photos from a specific year
async function detectDuplicatesByYear(year) {
  if (!fs.existsSync(photosDir)) {
    return { error: `Pictures directory not found at ${photosDir}` };
  }

  const files = fs.readdirSync(photosDir).filter(file => 
    /\.(jpg|jpeg|png|gif|webp)$/i.test(file)
  );

  const hashes = {};
  const duplicates = [];
  const yearFiles = [];

  // First, filter files by year
  for (const file of files) {
    try {
      const filePath = path.join(photosDir, file);
      const stats = fs.statSync(filePath);
      const fileYear = stats.birthtime.getFullYear();
      
      if (fileYear === year) {
        yearFiles.push(file);
      }
    } catch (error) {
      console.error(`Error reading file ${file}:`, error.message);
    }
  }

  // Then find duplicates within that year
  for (const file of yearFiles) {
    try {
      const filePath = path.join(photosDir, file);
      const fileBuffer = fs.readFileSync(filePath);
      const hash = crypto.createHash("md5").update(fileBuffer).digest("hex");

      if (hashes[hash]) {
        duplicates.push({
          original: hashes[hash],
          duplicate: file,
          status: "pending_review",
          imageHash: hash.substring(0, 8)
        });
      } else {
        hashes[hash] = file;
      }
    } catch (error) {
      console.error(`Error processing file ${file}:`, error.message);
    }
  }

  return {
    year,
    totalPhotos: yearFiles.length,
    duplicatesFound: duplicates.length,
    duplicates
  };
}

// Tool: Add photo to deletion review queue
function addToReviewQueue(filename, reason, year) {
  const reviewQueueFile = path.join(photosDir, `.review-queue-${year}.json`);
  let queue = [];
  
  if (fs.existsSync(reviewQueueFile)) {
    try {
      queue = JSON.parse(fs.readFileSync(reviewQueueFile, "utf8"));
    } catch (error) {
      console.error(`Error reading review queue: ${error.message}`);
      queue = [];
    }
  }

  const item = {
    id: Date.now(),
    filename,
    reason,
    year,
    timestamp: new Date().toISOString(),
    status: "pending",
    humanReviewed: false
  };

  queue.push(item);
  try {
    fs.writeFileSync(reviewQueueFile, JSON.stringify(queue, null, 2));
  } catch (error) {
    console.error(`Error writing review queue: ${error.message}`);
  }

  return `Added to review queue (${year}): ${filename} (Reason: ${reason})`;
}

// Tool: Show review queue for a year
function showReviewQueueByYear(year) {
  const reviewQueueFile = path.join(photosDir, `.review-queue-${year}.json`);
  
  if (!fs.existsSync(reviewQueueFile)) {
    return { 
      year,
      message: "No items in review queue", 
      items: [] 
    };
  }

  try {
    const queue = JSON.parse(fs.readFileSync(reviewQueueFile, "utf8"));
    const pending = queue.filter(q => q.status === "pending");
    
    return {
      year,
      message: `Review queue has ${pending.length} pending items`,
      total: queue.length,
      items: queue
    };
  } catch (error) {
    return {
      year,
      error: `Error reading review queue: ${error.message}`,
      items: []
    };
  }
}

// Tool: Get photo metadata
async function getPhotoMetadata(filename) {
  const filePath = path.join(photosDir, filename);
  
  if (!fs.existsSync(filePath)) {
    return { error: `File not found: ${filename}` };
  }

  try {
    const stats = fs.statSync(filePath);
    const metadata = await sharp(filePath).metadata();

    return {
      filename,
      size: `${(stats.size / 1024 / 1024).toFixed(2)} MB`,
      created: stats.birthtime.toISOString(),
      modified: stats.mtime.toISOString(),
      width: metadata.width,
      height: metadata.height,
      format: metadata.format
    };
  } catch (error) {
    return { error: `Error getting metadata: ${error.message}` };
  }
}

// Tool: Move photo to organized folder
function movePhoto(filename, folderName, year) {
  const sourceDir = photosDir;
  const targetDir = path.join(photosDir, folderName);
  
  if (!fs.existsSync(targetDir)) {
    try {
      fs.mkdirSync(targetDir, { recursive: true });
    } catch (error) {
      return `Error creating folder: ${error.message}`;
    }
  }

  const sourcePath = path.join(sourceDir, filename);
  const targetPath = path.join(targetDir, filename);
  
  if (!fs.existsSync(sourcePath)) {
    return `Error: File not found: ${filename}`;
  }

  try {
    fs.renameSync(sourcePath, targetPath);
    return `✅ Moved ${filename} to ${folderName}`;
  } catch (error) {
    return `Error moving file: ${error.message}`;
  }
}

// Main agent function
async function runPhotoManagerAgent(selectedYear) {
  const client = new Groq({
    apiKey: process.env.GROQ_API_KEY
  });

  const tools = [
    {
      type: "function",
      function: {
        name: "list_photos_by_year",
        description: "List all photos from a specific year",
        parameters: {
          type: "object",
          properties: {
            year: { type: "integer", description: "Year to filter photos" }
          },
          required: ["year"]
        }
      }
    },
    {
      type: "function",
      function: {
        name: "detect_duplicates_by_year",
        description: "Find duplicate photos from a specific year based on file hash",
        parameters: {
          type: "object",
          properties: {
            year: { type: "integer", description: "Year to find duplicates from" }
          },
          required: ["year"]
        }
      }
    },
    {
      type: "function",
      function: {
        name: "add_to_review_queue",
        description: "Add a photo to the deletion/action review queue for human approval",
        parameters: {
          type: "object",
          properties: {
            filename: { type: "string", description: "Name of the file to review" },
            reason: { type: "string", description: "Reason for the suggested action (e.g., 'Duplicate of X', 'Blurry image', 'Poor quality')" },
            year: { type: "integer", description: "Year of the photo" }
          },
          required: ["filename", "reason", "year"]
        }
      }
    },
    {
      type: "function",
      function: {
        name: "show_review_queue_by_year",
        description: "Show all photos pending human review for a specific year",
        parameters: {
          type: "object",
          properties: {
            year: { type: "integer", description: "Year to show review queue for" }
          },
          required: ["year"]
        }
      }
    },
    {
      type: "function",
      function: {
        name: "get_photo_metadata",
        description: "Get detailed information about a photo",
        parameters: {
          type: "object",
          properties: {
            filename: { type: "string", description: "Name of the photo file" }
          },
          required: ["filename"]
        }
      }
    },
    {
      type: "function",
      function: {
        name: "move_photo",
        description: "Move a photo to a specific folder for organization",
        parameters: {
          type: "object",
          properties: {
            filename: { type: "string", description: "Name of the file to move" },
            folderName: { type: "string", description: "Target folder name (e.g., 'Favorites', 'Archive', 'Blurry')" },
            year: { type: "integer", description: "Year of the photo" }
          },
          required: ["filename", "folderName", "year"]
        }
      }
    }
  ];

  const messages = [
    {
      role: "user",
      content: `Please analyze my photos folder in ~/Pictures for YEAR ${selectedYear} ONLY.
      
      Your tasks:
      1. List all photos from ${selectedYear}
      2. Detect duplicate photos from ${selectedYear}
      3. For any duplicates or questionable images, ADD THEM TO REVIEW QUEUE instead of deleting
      4. Organize photos into folders if they seem to belong together
      5. Show me the final review queue for ${selectedYear}
      
      IMPORTANT: 
      - Only analyze photos from ${selectedYear}
      - Never delete photos directly. Always add them to the review queue first for human approval.
      - Focus on finding obvious duplicates
      
      After organizing, show me a summary of what you found and what's in the review queue for ${selectedYear}.`
    }
  ];

  console.log("🖼️ Photo Manager Agent Started");
  console.log(`📅 Processing Year: ${selectedYear}`);
  console.log("📌 NOTE: Photos will NOT be deleted without your approval\n");

  let response = await client.chat.completions.create({
    model: "mixtral-8x7b-32768",
    max_tokens: 4096,
    tools,
    messages
  });

  let stepCount = 0;
  const maxSteps = 30;

  while (response.choices[0].finish_reason === "tool_calls" && stepCount < maxSteps) {
    stepCount++;
    const toolUseBlock = response.choices[0].message.tool_calls[0];
    
    if (!toolUseBlock) break;

    const { function: { name, arguments: inputStr }, id } = toolUseBlock;
    const input = JSON.parse(inputStr);
    let result;

    console.log(`\n[Step ${stepCount}] 🔧 Tool: ${name}`);
    if (input.filename) console.log(`   File: ${input.filename}`);
    if (input.reason) console.log(`   Reason: ${input.reason}`);
    if (input.year) console.log(`   Year: ${input.year}`);

    try {
      switch (name) {
        case "list_photos_by_year":
          result = listPhotosByYear(input.year);
          break;
        case "detect_duplicates_by_year":
          result = await detectDuplicatesByYear(input.year);
          break;
        case "add_to_review_queue":
          result = addToReviewQueue(input.filename, input.reason, input.year);
          break;
        case "show_review_queue_by_year":
          result = showReviewQueueByYear(input.year);
          break;
        case "get_photo_metadata":
          result = await getPhotoMetadata(input.filename);
          break;
        case "move_photo":
          result = movePhoto(input.filename, input.folderName, input.year);
          break;
        default:
          result = "Unknown tool";
      }
    } catch (error) {
      result = `Error: ${error.message}`;
    }

    messages.push({
      role: "assistant",
      content: "",
      tool_calls: [toolUseBlock]
    });

    messages.push({
      role: "tool",
      tool_call_id: id,
      content: JSON.stringify(result)
    });

    response = await client.chat.completions.create({
      model: "mixtral-8x7b-32768",
      max_tokens: 4096,
      tools,
      messages
    });
  }

  const finalResponse = response.choices[0].message.content;
  if (finalResponse) {
    console.log("\n" + "=".repeat(70));
    console.log(`✅ ANALYSIS COMPLETE FOR ${selectedYear}\n`);
    console.log(finalResponse);
    console.log("=".repeat(70));
  }

  return selectedYear;
}

// Helper function to process review queue for a year
async function processReviewQueue(year) {
  const reviewQueueFile = path.join(photosDir, `.review-queue-${year}.json`);
  
  if (!fs.existsSync(reviewQueueFile)) {
    console.log("✅ No items in review queue for this year");
    return;
  }

  let queue = [];
  try {
    queue = JSON.parse(fs.readFileSync(reviewQueueFile, "utf8"));
  } catch (error) {
    console.error(`Error reading review queue: ${error.message}`);
    return;
  }

  const pendingItems = queue.filter(q => q.status === "pending");

  if (pendingItems.length === 0) {
    console.log("✅ No pending items in review queue");
    return;
  }

  console.log(`\n📋 REVIEW QUEUE (${year}) - ${pendingItems.length} items pending approval\n`);

  for (let i = 0; i < pendingItems.length; i++) {
    const item = pendingItems[i];
    console.log(`\n[${i + 1}/${pendingItems.length}]`);
    console.log(`📄 File: ${item.filename}`);
    console.log(`💭 Reason: ${item.reason}`);
    console.log(`📅 Added: ${new Date(item.timestamp).toLocaleString()}`);
    
    const approved = await askUserConfirmation("Delete this file? (yes/no): ");
    
    if (approved) {
      const filePath = path.join(photosDir, item.filename);
      if (fs.existsSync(filePath)) {
        try {
          fs.unlinkSync(filePath);
          item.status = "deleted";
          console.log("✅ Deleted!");
        } catch (error) {
          console.error(`Error deleting file: ${error.message}`);
          item.status = "delete_failed";
        }
      }
    } else {
      item.status = "rejected";
      console.log("👍 Kept the file");
    }
    
    item.humanReviewed = true;
  }

  try {
    fs.writeFileSync(reviewQueueFile, JSON.stringify(queue, null, 2));
  } catch (error) {
    console.error(`Error writing review queue: ${error.message}`);
  }
  
  const summary = queue.reduce((acc, item) => {
    acc[item.status] = (acc[item.status] || 0) + 1;
    return acc;
  }, {});

  console.log("\n" + "=".repeat(70));
  console.log("✅ REVIEW COMPLETE!");
  console.log("Summary:", summary);
  console.log("=".repeat(70));
}

// Main entry point
async function main() {
  console.log("\n🎬 ==========================================");
  console.log("   📸 Photo Manager - Year-Based Processing");
  console.log("   ==========================================\n");

  // Get available years
  const availableYears = getAvailableYears();

  if (availableYears.length === 0) {
    console.log("❌ No photos found in ~/Pictures");
    return;
  }

  console.log("📅 Available years:\n");
  availableYears.forEach((year, index) => {
    console.log(`   ${index + 1}. ${year}`);
  });

  const yearInput = await askQuestion("\n👉 Enter year number or year itself (e.g., '1' or '2024'): ");
  
  let selectedYear;
  
  if (!isNaN(yearInput) && yearInput > 0 && yearInput <= availableYears.length) {
    selectedYear = availableYears[yearInput - 1];
  } else if (!isNaN(yearInput) && yearInput.length === 4) {
    selectedYear = parseInt(yearInput);
    if (!availableYears.includes(selectedYear)) {
      console.log(`\n❌ Year ${selectedYear} not found in your photos`);
      return;
    }
  } else {
    console.log("\n❌ Invalid input");
    return;
  }

  console.log(`\n✅ Selected Year: ${selectedYear}\n`);

  // Run agent for the selected year
  try {
    await runPhotoManagerAgent(selectedYear);
    
    const continueReview = await askUserConfirmation("\n👉 Proceed to review queue? (yes/no): ");
    if (continueReview) {
      await processReviewQueue(selectedYear);
    }

    const continueWithAnother = await askUserConfirmation("\n👉 Process another year? (yes/no): ");
    if (continueWithAnother) {
      return main();
    }
    
    console.log("\n✅ Thank you for using Photo Manager! Goodbye 👋\n");
  } catch (error) {
    console.error("❌ Error:", error.message);
  }
}

main().catch(console.error);