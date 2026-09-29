import type { Metadata } from "next";
import type { ReactNode } from "react";
import { SiteShell } from "@/components/ui";
import "./globals.css";
import "./bill-font.css";

export const metadata: Metadata = {
  title: {
    default: "Fabin Gurung — Engineering Research Hub",
    template: "%s · Fabin Gurung Research Hub",
  },
  description:
    "A static engineering research portal containing independently governed AEC/Structural and Hydropower research modules.",
  robots: {
    index: false,
    follow: false,
    nocache: true,
  },
};

export const dynamic = "force-static";

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <SiteShell>{children}</SiteShell>
      </body>
    </html>
  );
}
