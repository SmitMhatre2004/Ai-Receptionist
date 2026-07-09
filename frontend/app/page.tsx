"use client";

import { useEffect, useState } from "react";

type HealthStatus = "checking" | "online" | "offline";

export default function Home() {
  const [status, setStatus] = useState<HealthStatus>("checking");
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

  useEffect(() => {
    fetch(`${apiUrl}/health`)
      .then((res) => (res.ok ? setStatus("online") : setStatus("offline")))
      .catch(() => setStatus("offline"));
  }, [apiUrl]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 px-6 text-center">
      <h1 className="text-2xl font-semibold tracking-tight">
        Physiotherapy AI Receptionist
      </h1>
      <p className="max-w-md text-sm text-slate-500 dark:text-slate-400">
        Project scaffold — this placeholder page will be replaced by the real
        chat and booking UI once the Frontend UI phase lands.
      </p>
      <div className="flex items-center gap-2 rounded-full border border-slate-200 px-4 py-2 text-sm dark:border-slate-800">
        <span
          className={
            "h-2 w-2 rounded-full " +
            (status === "online"
              ? "bg-emerald-500"
              : status === "offline"
                ? "bg-red-500"
                : "bg-amber-400")
          }
        />
        Backend:{" "}
        {status === "checking"
          ? "checking..."
          : status === "online"
            ? "online"
            : "unreachable"}
      </div>
    </main>
  );
}
