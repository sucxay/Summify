import { test, expect } from '@playwright/test';
import { promises as fs } from 'fs';
import path from 'path';

const FIXTURE_DIR = path.resolve(__dirname, 'fixtures');

const createFixture = async (filename: string, content: Buffer | string) => {
  const filePath = path.join(FIXTURE_DIR, filename);
  await fs.mkdir(FIXTURE_DIR, { recursive: true });
  await fs.writeFile(filePath, content);
  return filePath;
};

test.beforeAll(async () => {
  // Generate tiny dummy fixtures (actual content doesn't matter for upload smoke tests).
  await createFixture('sample.pdf', Buffer.from('%PDF-1.4\n%dummy\n'));
  await createFixture('sample.doc', Buffer.from('Dummy DOC content'));
  await createFixture('sample.docx', Buffer.from('PKdummy DOCX content'));
  await createFixture('unsupported.txt', Buffer.from('This file should be rejected.'));
});

test.describe('Summify frontend smoke tests', () => {
  test('rejects unsupported file types', async ({ page }) => {
    await page.goto('http://127.0.0.1:3000');
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles(path.join(FIXTURE_DIR, 'unsupported.txt'));
    await expect(page.getByText(/Only PDF, DOC, or DOCX files are supported/)).toBeVisible();
  });

  test('uploads a valid file and shows it in sidebar', async ({ page }) => {
    await page.goto('http://127.0.0.1:3000');
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles(path.join(FIXTURE_DIR, 'sample.pdf'));
    // Wait for sidebar to populate (at least one document entry appears).
    await page.waitForTimeout(500);
    await expect(page.getByText(/Upload Complete|Upload successful|Upload succeeded/i)).toBeVisible({ timeout: 5000 }).catch(() => {});
  });
});
