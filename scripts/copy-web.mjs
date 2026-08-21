// Copies the runtime HTML files (source of truth = repo root) into www/,
// which is Capacitor's webDir. The data/ folder is build-time only
// (the vocab decks are already inlined into each HTML), so it is NOT copied.
import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const www = join(root, 'www');
mkdirSync(www, { recursive: true });

const files = [
  'index.html',
  'VocabMatch.html',
  'ChineseMatch.html',
  'KoreanMatch.html',
  'GermanMatch.html',
];

for (const f of files) {
  copyFileSync(join(root, f), join(www, f));
  console.log('copied', f, '-> www/');
}
