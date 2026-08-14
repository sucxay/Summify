import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'SUMMIFY',
  description: 'Document summarization and document-grounded chat workspace',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-canvas text-ink antialiased">{children}</body>
    </html>
  );
}
