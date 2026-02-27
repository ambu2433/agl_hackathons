import fs from "fs";
import path from "path";
import readline from "readline";
import os from "os";

const photosDir = path.join(os.homedir(), "Pictures");

function createReadlineInterface() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
}

function askQuestion(question) {
  return new Promise((resolve) => {
    const rl = createReadlineInterface();
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}

function askUserConfirmation(question) {
  return new Promise((resolve) => {
    const rl = createReadlineInterface();
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.toLowerCase() === "yes" || answer.toLowerCase() === "y");
    });
  });
}

// Get available review queues
function getAvailableYears() {
  if (!fs.existsSync(photosDir)) {
    return [];
  }

  const files = fs.readdirSync(photosDir);
  const years = new Set();

  files.forEach(file => {
    const match = file.match(/\.review-queue-(\d{4})\.json/);
    if (match) {
      years.add(parseInt(match[1]));
    }
  });

  return Array.from(years).sort((a, b) => b - a);
}

async function reviewQueue(year) {
  const reviewQueueFile = path.join(photosDir, `.review-queue-${year}.json`);
  
  if (!fs.existsSync(reviewQueueFile)) {
    console.log(`✅ No review queue found for year ${year}`);
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
    console.log(`✅ No pending items for year ${year}`);
    return;
  }

  console.log(`\n📋 REVIEW QUEUE (${year}) - ${pendingItems.length} items pending\n`);

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
          console.error(`Error deleting: ${error.message}`);
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

  console.log("\n" + "=".repeat(60));
  console.log("✅ REVIEW COMPLETE!");
  console.log("Summary:", summary);
  console.log("=".repeat(60));
}

async function main() {
  console.log("\n🎬 ==========================================");
  console.log("   📋 Photo Manager - Review Queue");
  console.log("   ==========================================\n");

  const availableYears = getAvailableYears();

  if (availableYears.length === 0) {
    console.log("❌ No review queues found");
    return;
  }

  console.log("📅 Available years with review queues:\n");
  availableYears.forEach((year, index) => {
    console.log(`   ${index + 1}. ${year}`);
  });

  const yearInput = await askQuestion("\n👉 Select year (enter number or year): ");
  
  let selectedYear;
  
  if (!isNaN(yearInput) && yearInput > 0 && yearInput <= availableYears.length) {
    selectedYear = availableYears[yearInput - 1];
  } else if (!isNaN(yearInput) && yearInput.length === 4) {
    selectedYear = parseInt(yearInput);
    if (!availableYears.includes(selectedYear)) {
      console.log(`\n❌ No review queue found for year ${selectedYear}`);
      return;
    }
  } else {
    console.log("\n❌ Invalid input");
    return;
  }

  console.log(`\n✅ Selected Year: ${selectedYear}\n`);
  await reviewQueue(selectedYear);

  const continueWithAnother = await askUserConfirmation("\n👉 Review another year? (yes/no): ");
  if (continueWithAnother) {
    return main();
  }

  console.log("\n✅ Thank you for reviewing! Goodbye 👋\n");
}

main().catch(console.error);