"use client";

import Link from "next/link";
import { useCallback, useState } from "react";

type Summary = { projects: number; bridges: number; attention_required: number; active_work_orders: number };
type Bridge = { id: string; code: string; name: string; service_status: string; maintenance_status: string; next_inspection: string };
type WorkOrder = { id: string; description: string; contractor: string; status: string };
type User = { name: string; email: string; role: string };

const api = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const demos = [
  ["Project manager", "manager@demo.local"],
  ["Executive engineer", "engineer@demo.local"],
  ["Bridge inspector", "inspector@demo.local"],
  ["Contractor", "contractor@demo.local"],
] as const;

function readableStatus(value: string) {
  return value.toLowerCase().replaceAll("_", " ");
}

export default function Workspace() {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [bridge, setBridge] = useState<Bridge | null>(null);
  const [workOrders, setWorkOrders] = useState<WorkOrder[]>([]);
  const [message, setMessage] = useState("Choose a demo role to enter the workspace.");
  const [busy, setBusy] = useState(false);

  const request = useCallback(async (path: string, init: RequestInit = {}) => {
    const response = await fetch(`${api}${path}`, {
      ...init,
      headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}), ...init.headers },
    });
    if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail ?? "Request could not be completed");
    return response.json();
  }, [token]);

  const load = useCallback(async (accessToken = token) => {
    if (!accessToken) return;
    try {
      const read = async (path: string) => {
        const response = await fetch(`${api}${path}`, { headers: { Authorization: `Bearer ${accessToken}` } });
        if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail ?? "Request could not be completed");
        return response.json();
      };
      const [nextSummary, bridges] = await Promise.all([read("/api/dashboard/summary"), read("/api/bridges")]);
      const mahi = bridges.find((item: Bridge) => item.id === "BRG-001") ?? bridges[0] ?? null;
      setSummary(nextSummary);
      setBridge(mahi);
      if (mahi) setWorkOrders(await read(`/api/bridges/${mahi.id}/work-orders`));
      setMessage("Live lifecycle data loaded from the API.");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "The API is unavailable.");
    }
  }, [token]);

  async function signIn(email: string) {
    setBusy(true);
    try {
      const result = await fetch(`${api}/api/auth/login`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, password: "DemoPass123" }) });
      if (!result.ok) throw new Error("Demo sign-in failed. Confirm the Render deployment has DATABASE_URL and JWT_SECRET.");
      const body = await result.json();
      setToken(body.access_token);
      setUser(body.user);
      setMessage(`Signed in as ${body.user.name}. Permissions are checked by the API.`);
      await load(body.access_token);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Demo sign-in failed."); }
    finally { setBusy(false); }
  }

  async function act(path: string, init: RequestInit, success: string) {
    setBusy(true);
    try { await request(path, init); setMessage(success); await load(); }
    catch (error) { setMessage(error instanceof Error ? error.message : "Action could not be completed."); }
    finally { setBusy(false); }
  }

  const firstWork = workOrders.find((item) => item.status !== "VERIFIED");
  const role = user?.role;
  const cards = [["Active projects", summary?.projects], ["Bridge assets", summary?.bridges], ["Disposition required", summary?.attention_required], ["Active work orders", summary?.active_work_orders]];

  if (!user) return <main className="min-h-screen bg-[#f6f5ef] px-6 py-8 text-[#183127]"><header className="mx-auto flex max-w-6xl items-center justify-between"><Link href="/" className="text-sm font-semibold">← BridgeTheGap</Link><span className="text-xs font-bold tracking-[.15em] text-[#66806a]">SECURE DEMO WORKSPACE</span></header><section className="mx-auto mt-20 max-w-3xl text-center"><p className="text-xs font-bold tracking-[.18em] text-[#66806a]">ROLE-BASED PROTOTYPE</p><h1 className="mt-5 text-5xl font-semibold tracking-[-.06em]">Enter the lifecycle from the right point of view.</h1><p className="mx-auto mt-5 max-w-xl text-lg text-[#536057]">Use one of four seeded roles. The API, rather than the browser, decides what each role can change.</p><div className="mt-10 grid gap-3 sm:grid-cols-2">{demos.map(([label, email]) => <button key={email} disabled={busy} onClick={() => void signIn(email)} className="rounded-2xl border border-[#cdd6cb] bg-white p-5 text-left transition hover:-translate-y-0.5 hover:border-[#527657] disabled:opacity-50"><p className="font-semibold">{label}</p><p className="mt-1 text-sm text-[#68756b]">{email}</p><p className="mt-4 text-xs font-bold tracking-[.12em] text-[#527657]">ENTER AS THIS ROLE →</p></button>)}</div><p className="mt-6 text-sm text-[#68756b]">{message}</p></section></main>;

  return <main className="min-h-screen bg-[#07111f] p-6 text-slate-100 md:p-10"><header className="mx-auto flex max-w-7xl items-center justify-between border-b border-slate-800 pb-6"><div><Link href="/" className="text-sm text-cyan-200">← Landing page</Link><h1 className="mt-3 text-3xl font-semibold">Lifecycle command centre</h1><p className="mt-1 text-sm text-slate-400">{user.name} · {readableStatus(user.role)}</p></div><button onClick={() => { setToken(null); setUser(null); setSummary(null); }} className="rounded-full border border-slate-700 px-4 py-2 text-xs font-bold tracking-[.12em] hover:border-cyan-300">SWITCH ROLE</button></header><p className="mx-auto mt-6 max-w-7xl rounded-lg bg-slate-900 p-4 text-sm text-slate-300">{message}</p><section className="mx-auto mt-6 grid max-w-7xl gap-4 md:grid-cols-4">{cards.map(([label, value]) => <article key={String(label)} className="rounded-xl border border-slate-800 bg-slate-900 p-5"><p className="text-sm text-slate-400">{label}</p><p className="mt-3 text-3xl font-semibold text-cyan-200">{value ?? "—"}</p></article>)}</section><section className="mx-auto mt-6 grid max-w-7xl gap-6 lg:grid-cols-2"><article className="rounded-xl border border-slate-800 bg-slate-900 p-6"><p className="text-xs font-bold tracking-[.14em] text-cyan-200">BRIDGE PASSPORT</p><h2 className="mt-2 text-xl font-semibold">{bridge?.name ?? "Loading asset…"}</h2><p className="mt-2 text-slate-400">{bridge?.code} · {bridge ? readableStatus(bridge.service_status) : ""} · next inspection {bridge?.next_inspection}</p><div className="mt-6 rounded-lg bg-slate-800 p-4"><p className="text-xs font-bold tracking-[.12em] text-slate-400">MAINTENANCE STATE</p><p className="mt-2 text-lg font-semibold text-amber-200">{bridge ? readableStatus(bridge.maintenance_status) : "—"}</p></div><div className="mt-5 flex flex-wrap gap-3">{role === "INSPECTOR" && <button disabled={busy || !bridge} onClick={() => bridge && void act(`/api/bridges/${bridge.id}/inspections`, { method: "POST" }, "Inspection recorded; it now requires an accountable disposition.")} className="rounded-full bg-cyan-300 px-4 py-2 text-xs font-bold text-slate-950 disabled:opacity-50">RECORD INSPECTION</button>}{role === "EXECUTIVE_ENGINEER" && bridge?.maintenance_status === "ACTION_REQUIRED" && <button disabled={busy} onClick={() => void act(`/api/bridges/${bridge.id}/work-orders`, { method: "POST", body: JSON.stringify({ description: "Repair deck drainage joint", contractor: "Saffron Infrastructure" }) }, "Work order approved and assigned to the contractor.")} className="rounded-full bg-cyan-300 px-4 py-2 text-xs font-bold text-slate-950 disabled:opacity-50">APPROVE DEMO WORK</button>}{role === "CONTRACTOR" && firstWork?.status === "APPROVED" && <button disabled={busy} onClick={() => void act(`/api/work-orders/${firstWork.id}/complete`, { method: "POST" }, "Work marked complete and awaiting independent verification.")} className="rounded-full bg-cyan-300 px-4 py-2 text-xs font-bold text-slate-950 disabled:opacity-50">MARK WORK COMPLETE</button>}{(role === "EXECUTIVE_ENGINEER" || role === "INSPECTOR") && firstWork?.status === "VERIFICATION_PENDING" && <button disabled={busy} onClick={() => void act(`/api/work-orders/${firstWork.id}/verify`, { method: "POST" }, "Work independently verified; maintenance state is clear.")} className="rounded-full bg-cyan-300 px-4 py-2 text-xs font-bold text-slate-950 disabled:opacity-50">VERIFY COMPLETION</button>}</div></article><article className="rounded-xl border border-slate-800 bg-slate-900 p-6"><p className="text-xs font-bold tracking-[.14em] text-cyan-200">ACCOUNTABILITY QUEUE</p><h2 className="mt-2 text-xl font-semibold">Work cannot close itself.</h2><div className="mt-5 space-y-3">{workOrders.length === 0 ? <p className="rounded-lg bg-slate-800 p-4 text-sm text-slate-400">No maintenance work has been raised for this bridge.</p> : workOrders.map((work) => <div key={work.id} className="rounded-lg bg-slate-800 p-4"><p className="font-semibold">{work.description}</p><p className="mt-1 text-sm text-slate-400">{work.contractor} · {readableStatus(work.status)}</p></div>)}</div><div className="mt-5 rounded-lg bg-amber-300/10 p-4 text-sm text-amber-100">This is fictional demo data. It records accountable decisions; it does not automate structural safety decisions or claim official Gujarat compliance.</div></article></section></main>;
}
