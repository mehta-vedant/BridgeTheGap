"use client";

import { useEffect, useState } from "react";

type Summary = { projects: number; bridges: number; attention_required: number; active_work_orders: number };
const apiUrl = process.env.NEXT_PUBLIC_API_URL;

export default function Home() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (!apiUrl) return;
    fetch(`${apiUrl}/api/dashboard/summary`)
      .then((response) => response.ok ? response.json() : Promise.reject())
      .then(setSummary)
      .catch(() => setError(true));
  }, []);

  const stats = summary ? [
    ["Active projects", String(summary.projects).padStart(2, "0")],
    ["Assets in service", String(summary.bridges).padStart(2, "0")],
    ["Action required", String(summary.attention_required).padStart(2, "0")],
    ["Active work orders", String(summary.active_work_orders).padStart(2, "0")],
  ] : [["Active projects", "--"], ["Assets in service", "--"], ["Action required", "--"], ["Active work orders", "--"]];

  return <main className="min-h-screen bg-slate-950 text-slate-100"><header className="border-b border-slate-800 px-6 py-5"><div className="mx-auto flex max-w-7xl items-center justify-between"><div><p className="text-xs font-bold tracking-[.2em] text-cyan-300">GUJARAT R&B · DEMO</p><h1 className="mt-1 text-xl font-semibold">BridgeTheGap</h1></div><span className="rounded-full border border-cyan-400/40 px-3 py-1 text-xs text-cyan-200">Fictional demo data</span></div></header><section className="mx-auto max-w-7xl px-6 py-10"><h2 className="text-3xl font-semibold">Lifecycle command centre</h2><p className="mt-2 text-slate-400">Connected project, bridge, inspection, and maintenance decisions.</p>{error && <p className="mt-5 rounded-lg bg-amber-400/10 p-3 text-sm text-amber-100">The live API is unavailable. Showing dashboard shell only.</p>}<div className="mt-8 grid gap-4 md:grid-cols-4">{stats.map(([label, value]) => <article key={label} className="rounded-xl border border-slate-800 bg-slate-900 p-5"><p className="text-sm text-slate-400">{label}</p><p className="mt-3 text-3xl font-semibold">{value}</p></article>)}</div><div className="mt-8 grid gap-6 lg:grid-cols-[1.4fr_.8fr]"><section className="rounded-xl border border-slate-800 bg-slate-900 p-6"><div className="flex justify-between"><div><h3 className="font-semibold">Mahi River Bridge Rehabilitation</h3><p className="mt-2 text-sm text-slate-400">PRJ-001 · Vadodara Division · Estimate ₹1.25 Cr</p></div><span className="h-fit rounded-full bg-amber-400/15 px-3 py-1 text-xs text-amber-200">Tender open</span></div><ol className="mt-8 space-y-3">{["Need identified", "Administrative approval", "Technical sanction", "Tender open", "Awarded", "Construction", "Handover", "In service"].map((stage, index) => <li key={stage} className={`flex items-center gap-3 rounded-lg p-3 ${index <= 3 ? "bg-cyan-300/10 text-cyan-100" : "text-slate-500"}`}><span className={`flex h-7 w-7 items-center justify-center rounded-full text-xs ${index <= 3 ? "bg-cyan-300 text-slate-950" : "bg-slate-800"}`}>{index + 1}</span>{stage}</li>)}</ol></section><aside className="space-y-6"><section className="rounded-xl border border-slate-800 bg-slate-900 p-6"><h3 className="font-semibold">Bid evaluation</h3><div className="mt-5 space-y-3 text-sm"><Row label="Saffron Infrastructure" value="₹1.185 Cr"/><Row label="Narmada Works" value="₹1.210 Cr"/></div><button className="mt-6 w-full rounded-lg border border-cyan-400/50 px-4 py-2 text-sm font-semibold text-cyan-200">Record award decision</button></section><section className="rounded-xl border border-slate-800 bg-slate-900 p-6"><h3 className="font-semibold">Bridge attention queue</h3><p className="mt-3 rounded-lg bg-amber-400/10 p-3 text-sm text-amber-100">GJ-RB-042: inspection finding awaits engineering disposition.</p></section></aside></div></section></main>;
}

function Row({ label, value }: { label: string; value: string }) { return <div className="flex justify-between rounded-lg bg-slate-800 p-3"><span>{label}</span><span className="font-semibold text-cyan-200">{value}</span></div>; }
