# 📸 Photo Manager - AI-Powered Photo Organization

An intelligent photo management tool powered by Claude AI that helps you organize, find duplicates, and manage your local photo collection year by year.

## Features

✅ **Year-based Processing** - Analyze photos one year at a time for faster decisions
✅ **Duplicate Detection** - Find duplicate photos using MD5 file hashing
✅ **Smart Organization** - Automatically organize photos into categorized folders
✅ **Human-Approved Deletions** - All deletions require your explicit approval
✅ **Review Queue** - Persistent queue for managing pending actions
✅ **Metadata Analysis** - View photo metadata (size, dimensions, creation date)

## Requirements

- Node.js 16+
- npm/yarn
- Anthropic API Key
- Mac with Pictures folder

## Installation

```bash
# Clone or create the project
mkdir photo-manager-mcp
cd photo-manager-mcp

# Install dependencies
npm install
```

## Setup

1. **Get your API Key**
   - Visit [console.anthropic.com](https://console.anthropic.com)
   - Create an API key

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

### Run Full Analysis and Review

```bash
npm start
```

This will:
1. Show available years with photos
2. Let you select a year
3. Analyze photos for that year
4. Ask if you want to review pending deletions

### Just Review Existing Queue

```bash
npm run review
```

Select a year and review all pending items.

### Run Both Steps

```bash
npm run analyze
```

## How It Works

1. **Year Selection** - Choose which year to process
2. **Photo Analysis** - AI scans all photos from that year
3. **Duplicate Detection** - Finds identical files using MD5 hashing
4. **Smart Suggestions** - AI suggests which files to remove
5. **Review Queue** - All suggested deletions go to a review queue
6. **Human Approval** - You approve/reject each deletion interactively

## File Structure

```
photo-manager-mcp/
├── server.js           # Main analysis engine
├── review.js           # Review queue processor
├── package.json        # Dependencies
├── .env                # API configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Review Queue Files

Review queues are saved as `.review-queue-YYYY.json` in your Pictures folder:
- One queue per year
- Tracks pending, deleted, and rejected items
- Persists across sessions

## Safety Features

🔒 **Human-First Approach** - Never deletes without approval
🔒 **Review Queue** - All deletions go through review
🔒 **Persistent History** - Tracks all actions
🔒 **Error Handling** - Graceful error management

## Troubleshooting

**No photos found?**
- Ensure photos are in `~/Pictures`
- Check file format (jpg, jpeg, png, gif, webp)

**API errors?**
- Verify your API key in `.env`
- Check internet connection

**Permission errors?**
- Ensure you have read/write access to ~/Pictures

## License

MIT

## Support

For issues or questions, check your terminal output for detailed error messages.