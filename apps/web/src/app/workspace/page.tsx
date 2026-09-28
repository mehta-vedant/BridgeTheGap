"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";

const api = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const demoUsers = [
  ["Executive Engineer", "engineer@demo.local", "Moves gates, awards work, and validates finance."],
  ["Bridge Inspector", "inspector@demo.local", "Records condition evidence and safety actions."],
  ["Contractor", "contractor@demo.local", "Submits a controlled bid and rectification evidence."],
  ["Manager", "manager@demo.local", "Has portfolio oversight and configured administration."],
] as const;

type User = { name: string; email: string; role: string };
type Passport = {
  asset: { id: string; asset_code: string; name: string; lifecycle_state: string; service_state: string; condition_grade: string; district: string; bridge?: { route?: string; length_m?: number; span_count?: number } };
  project?: { id: string; title: string; state: string };
  tender?: { id: string; number: string; status: string };
  contract?: { id: string; number: string; state: string };
  gates: { id: string; status: string; explanation: string; missing_requirements: string[] }[];
  defects: { id: string; description: string; risk_level: string; status: string }[];
  work_orders: { id: string; defect_id: string; status: string; description: string }[];
  timeline: { id: string; at: string; event_type: string; reason?: string }[];
};
type Dashboard = { metrics: Record<string, number>; actions: { id: string; title: string; detail: string }[] };

function label(value?: string) { return (value ?? "").replaceAll("_", " ").toLowerCase(); }
function Status({ value }: { value: string }) { const kind = value.includes("FAILED") || value.includes("OPEN") || value.includes("SRI") ? "attention" : value.includes("PASSED") || value.includes("VERIFIED") || value.includes("AWARDED") ? "good" : ""; return <span className={`status ${kind}`}>{label(value)}</span>; }
function Empty({ text }: { text: string }) { return <p className="empty">{text}</p>; }

export default function Workspace() {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [passport, setPassport] = useState<Passport | null>(null);
  const [page, setPage] = useState("Dashboard");
  const [notice, setNotice] = useState("Choose a demo account. All workflow decisions are enforced by the API.");
  const [busy, setBusy] = useState(false);

  const read = useCallback(async (path: string, accessToken = token) => {
    const response = await fetch(`${api}${path}`, { headers: { Authorization: `Bearer ${accessToken}` } });
    if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail ?? "The service could not complete that request.");
    return response.json();
  }, [token]);
  const load = useCallback(async (accessToken = token) => {
    if (!accessToken) return;
    try {
      const [nextDashboard, assets] = await Promise.all([read("/api/mvp/dashboard", accessToken), read("/api/mvp/assets", accessToken)]);
      setDashboard(nextDashboard);
      if (assets.items?.[0]) setPassport(await read(`/api/mvp/assets/${assets.items[0].id}/passport`, accessToken));
    } catch (error) { setNotice(error instanceof Error ? error.message : "The API is unavailable."); }
  }, [read, token]);
  useEffect(() => {
    const saved = window.localStorage.getItem("btg-session");
    if (!saved) return;
    try {
      const session = JSON.parse(saved) as { token: string; user: User };
      queueMicrotask(() => { setToken(session.token); setUser(session.user); void load(session.token); });
    } catch { window.localStorage.removeItem("btg-session"); }
  }, [load]);
  async function signIn(email: string) {
    setBusy(true);
    try {
      const response = await fetch(`${api}/api/auth/login`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, password: "DemoPass123" }) });
      if (!response.ok) throw new Error("Sign-in failed. Start the API, then try again.");
      const result = await response.json(); setToken(result.access_token); setUser(result.user);
      window.localStorage.setItem("btg-session", JSON.stringify({ token: result.access_token, user: result.user }));
      setNotice(`Signed in as ${result.user.name}. Your authority is checked server-side.`); await load(result.access_token);
    } catch (error) { setNotice(error instanceof Error ? error.message : "Sign-in failed."); } finally { setBusy(false); }
  }
  async function command(path: string, body: unknown, success: string) {
    if (!token) return; setBusy(true);
    try {
      const response = await fetch(`${api}${path}`, { method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` }, body: JSON.stringify(body) });
      if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail ?? "The workflow transition was rejected.");
      setNotice(success); await load(token);
    } catch (error) { setNotice(error instanceof Error ? error.message : "Action failed."); } finally { setBusy(false); }
  }
  function signOut() { window.localStorage.removeItem("btg-session"); setToken(null); setUser(null); setPassport(null); setDashboard(null); setPage("Dashboard"); }
  if (!user) return <Login busy={busy} notice={notice} signIn={signIn} />;

  const role = user.role; const gate = passport?.gates[0]; const defect = passport?.defects.find((item) => item.status !== "CLOSED"); const work = passport?.work_orders.find((item) => item.status !== "VERIFIED"); const metrics = dashboard?.metrics ?? {}; const canEngineer = role === "EXECUTIVE_ENGINEER" || role === "MANAGER";
  const nav = ["Dashboard", "Asset passport", "Gates & tender", "Quality control", "Safety & maintenance", "Price variation", "Audit trail"];
  return <main className="app-shell">
    <aside className="sidebar"><Link href="/" className="brand">Bridge<span>TheGap</span></Link><p className="eyebrow">R&B lifecycle operations</p><nav>{nav.map((item) => <button key={item} className={page === item ? "selected" : ""} onClick={() => setPage(item)}>{item}</button>)}</nav><div className="account"><p>{user.name}</p><small>{label(role)}</small><button onClick={signOut}>Switch role</button></div></aside>
    <section className="workspace"><header className="topbar"><div><p className="eyebrow">Gujarat R&B / fictional demo data</p><h1>{page}</h1></div><Status value={passport?.asset.service_state ?? "loading"} /></header><p className="notice" role="status">{notice}</p>
      {page === "Dashboard" && <><section className="metrics">{[["Registered assets", metrics.assets], ["Active projects", metrics.active_projects], ["Open defects", metrics.open_defects], ["Blocked gates", metrics.failed_gates]].map(([name, value]) => <article key={String(name)}><p>{name}</p><strong>{value ?? "-"}</strong></article>)}</section><section className="split"><article className="panel"><p className="eyebrow">Action required</p><h2>Decisions awaiting an accountable owner</h2>{dashboard?.actions.length ? dashboard.actions.map((item) => <div className="queue" key={item.id}><b>{item.title}</b><p>{item.detail}</p></div>) : <Empty text="No actions are waiting for this seeded scenario." />}</article><AssetSummary passport={passport} /></section></>}
      {page === "Asset passport" && <section className="split"><AssetSummary passport={passport} /><article className="panel"><p className="eyebrow">Bridge details</p><h2>Digital asset passport</h2><dl><dt>Route</dt><dd>{passport?.asset.bridge?.route ?? "-"}</dd><dt>Length</dt><dd>{passport?.asset.bridge?.length_m ?? "-"} m</dd><dt>Spans</dt><dd>{passport?.asset.bridge?.span_count ?? "-"}</dd><dt>Project</dt><dd>{passport?.project?.title ?? "-"}</dd></dl></article></section>}
      {page === "Gates & tender" && <section className="split"><article className="panel"><p className="eyebrow">Sanction & clearance</p><h2>Land-readiness gate</h2>{gate ? <><Status value={gate.status} /><p>{gate.explanation}</p>{gate.missing_requirements.map((item) => <p className="missing" key={item}>{item}</p>)}</> : <Empty text="No gate evaluation recorded." />}{canEngineer && passport?.project && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/projects/${passport.project?.id}/land-readiness`, { possession_percent: 95, handover_reference: "SYN-LAND-MEMO-0142" }, "Land-readiness evidence recorded; the configured gate has been evaluated.")}>Record 95% possession + memo</button>}</article><article className="panel"><p className="eyebrow">Internal controlled tender room</p><h2>{passport?.tender?.number ?? "Tender not available"}</h2><Status value={passport?.tender?.status ?? "DRAFT"} /><p>Department-provisioned contractor access only. This prototype does not integrate with nProcure.</p>{canEngineer && passport?.tender?.status === "DRAFT" && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/tenders/${passport.tender?.id}/publish`, {}, "Tender published after its evidence gate passed.")}>Publish tender</button>}{role === "CONTRACTOR" && passport?.tender?.status === "PUBLISHED" && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/tenders/${passport.tender?.id}/bids`, { technical_summary: "Controlled tender-room proposal with a documented execution approach.", price_amount: 24500000 }, "Bid submitted for your contractor company.")}>Submit controlled bid</button>}{canEngineer && passport?.tender?.status === "PUBLISHED" && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/tenders/${passport.tender?.id}/award`, {}, "Lowest submitted controlled bid selected; contract created.")}>Evaluate and award</button>}</article></section>}
      {page === "Quality control" && <section className="split"><article className="panel"><p className="eyebrow">Execution evidence</p><h2>Raw samples drive the result</h2><p>Demo thresholds are labelled as synthetic configuration, never Gujarat acceptance criteria.</p>{canEngineer && passport?.contract ? <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/contracts/${passport.contract?.id}/quality-tests`, { test_type: "Concrete cube strength", specified_value: 30, samples: [32, 31, 33] }, "Raw samples evaluated: calculated quality result recorded in the audit trail.")}>Evaluate quality samples</button> : <Empty text="Award the seeded tender first to create the execution contract." />}</article><article className="panel"><p className="eyebrow">Quality control pattern</p><h2>Evidence -&gt; calculation -&gt; review -&gt; ATR</h2><p>Tests retain raw values. A reviewer cannot silently replace a calculated result; an override must be auditable.</p></article></section>}
      {page === "Safety & maintenance" && <section className="split"><article className="panel"><p className="eyebrow">Post-completion inspection</p><h2>Condition, risk, and service state stay separate</h2><p>Gujarat grades supported: S, SRI, U. Safety restriction is an explicit service decision, not an invented condition grade.</p>{role === "INSPECTOR" && passport && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/assets/${passport.asset.id}/inspections`, { grade: "SRI", notes: "Deck joint drainage observation requires accountable rectification and reinspection.", risk_level: "SAFETY_REVIEW", atr_months: 3 }, "SRI inspection and ATR recorded.")}>Record SRI inspection</button>}</article><article className="panel"><p className="eyebrow">Maintenance maker-checker</p><h2>{defect ? defect.description : "No open defect"}</h2>{defect && <Status value={defect.status} />}{canEngineer && defect && !work && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/defects/${defect.id}/work-orders`, { decision_type: "REPAIR", description: "Repair drainage joint and submit rectification evidence for independent verification.", company_id: "COMP-20" }, "Work order approved and assigned.")}>Approve repair work</button>}{role === "CONTRACTOR" && work?.status === "APPROVED" && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/work-orders/${work.id}/rectification`, { notes: "Joint repaired; drainage path cleared. Evidence reference: SYN-RECT-142." }, "Rectification submitted; it now requires an independent verifier.")}>Submit rectification</button>}{(role === "INSPECTOR" || canEngineer) && work?.status === "VERIFICATION_PENDING" && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/work-orders/${work.id}/verify`, {}, "Closure independently verified. The contractor could not verify its own work.")}>Independently verify closure</button>}</article></section>}
      {page === "Price variation" && <article className="panel wide"><p className="eyebrow">Finance control</p><h2>Preserve the claim, calculation, variance, and policy version.</h2><p>Submitted value is never overwritten by calculated value.</p>{canEngineer && passport?.contract ? <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/contracts/${passport.contract?.id}/price-variation`, { submitted_amount: 1280000, calculated_amount: 1254500 }, "Price-variation claim recorded with its variance and finance-review explanation.")}>Validate demo PV claim</button> : <Empty text="Award the tender first to activate the contract finance timeline." />}</article>}
      {page === "Audit trail" && <article className="panel wide"><p className="eyebrow">Immutable accountability trail</p><h2>Every material transition records actor, time, and reason.</h2><div className="timeline">{passport?.timeline.map((item) => <div key={item.id}><Status value={item.event_type} /><b>{label(item.event_type)}</b><p>{item.reason ?? "Recorded lifecycle decision."}</p><small>{new Date(item.at).toLocaleString()}</small></div>) ?? <Empty text="Loading lifecycle events..." />}</div></article>}
    </section>
  </main>;
}

function Login({ busy, notice, signIn }: { busy: boolean; notice: string; signIn: (email: string) => Promise<void> }) { return <main className="login"><header><Link href="/">Bridge<span>TheGap</span></Link><small>Secure fictional demo</small></header><section><p className="eyebrow">Role-based lifecycle workspace</p><h1>Enter from the point where you hold accountability.</h1><p>Each account uses the same seeded password. The backend—not hidden UI controls—enforces authority.</p><div className="login-grid">{demoUsers.map(([name, email, description]) => <button key={email} disabled={busy} onClick={() => void signIn(email)}><b>{name}</b><span>{description}</span><small>{email}</small></button>)}</div><p className="notice">{notice}</p></section></main>; }
function AssetSummary({ passport }: { passport: Passport | null }) { return <article className="panel"><p className="eyebrow">Permanent asset identity</p><h2>{passport?.asset.name ?? "Loading bridge passport"}</h2><p>{passport?.asset.asset_code} / {passport?.asset.bridge?.route} / {passport?.asset.district}</p><div className="passport-meta"><span><b>Lifecycle</b><Status value={passport?.asset.lifecycle_state ?? "-"} /></span><span><b>Condition</b><Status value={passport?.asset.condition_grade ?? "-"} /></span></div></article>; }
