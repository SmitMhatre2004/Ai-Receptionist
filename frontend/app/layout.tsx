import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Physiotherapy AI Receptionist",
  description: "AI-powered receptionist for appointment-based clinics.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
