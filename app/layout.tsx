import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Atlas - AI-Powered Research Workspace",
  description: "Transform your search query into a user-controlled mini-app workspace",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
