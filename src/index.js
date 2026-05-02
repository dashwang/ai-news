#!/usr/bin/env node
/**
 * AI News Publisher - OpenClaw Skill Entry Point
 * Run: openclaw skill run ai-news-publisher [--publish]
 */

import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import process from 'process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const skillDir = dirname(__dirname); // skills/ai-news-publisher

// Add skill's node_modules to path if needed
const pkg = await import('../package.json');

// Re-export main functionality
const { main } = await import('./fetch_news.js');
await main();
