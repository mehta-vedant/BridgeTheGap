"use client";

import Link from "next/link";
import { useCallback, useEffect, useState, type ChangeEvent } from "react";

const api = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const demoUsers = [
  ["Executive Engineer", "engineer@demo.local", "Moves gates, awards work, and validates finance."],
  ["Bridge Inspector", "inspector@demo.local", "Records condition evidence and safety actions."],
  ["Contractor", "contractor@demo.local", "Submits a controlled bid and rectification evidence."],
  ["Manager", "manager@demo.local", "Has portfolio oversight and configured administration."],
  ["Chief Engineer", "chiefengineer@demo.local", "Reviews the statewide portfolio and configured approvals."],
  ["Superintending Engineer", "superintendent@demo.local", "Provides circle-level tender and review oversight."],
  ["Quality Engineer", "quality@demo.local", "Validates raw test evidence and calculated results."],
  ["Divisional Accountant", "finance@demo.local", "Reviews price-variation and finance controls."],
  ["Auditor / Viewer", "auditor@demo.local", "Reads scope-limited asset history and audit evidence."],
] as const;

type User = { name: string; email: string; role: string };
type PhaseInfo = {
  phase: string;
  phase_label: string;
  basis: string;
  next_phase: string | null;
  next_phase_label: string | null;
  blockers: string[];
};
type ScopeInfo = { roles: string[]; explanation: string; assets_visible?: number; restricted?: boolean; criteria?: string[] };
type Passport = {
  asset: { id: string; asset_code: string; name: string; phase?: string; phase_label?: string; lifecycle_state: string; stored_state_agrees?: boolean | null; service_state: string; condition_?: string; condition_grade: string; district: string; latitude?: number; longitude?: number; bridge?: { class?: string; route?: string; length_m?: number; span_count?: number } };
  phase?: PhaseInfo;
  phase_purpose?: Record<string, string>;
  phase_gates?: Record<string, { available: boolean; open_now: boolean; reason: string }>;
  scope?: ScopeInfo;
  project?: { id: string; title: string; state: string; estimate_amount?: number | null };
  tender?: { id: string; number: string; status: string; tender_form?: string; opening_on?: string | null };
  contract?: { id: string; number: string; state: string; awarded_amount?: number };
  bids?: { id: string; company_id: string; own_bid: boolean; price_amount: number | null; technical_status: string; redacted: boolean; note?: string }[];
  reports: { id: string; type: string; status: string; reference: string; source_class: string }[];
  clearances: { id: string; type: string; status: string; reference?: string; source_class: string }[];
  gates: { id: string; status: string; explanation: string; missing_requirements: string[] }[];
  defects: { id: string; description: string; risk_level: string; status: string; due_on?: string | null }[];
  work_orders: { id: string; defect_id: string; status: string; description: string; company_id?: string }[];
  milestones?: { id: string; name: string; planned_percent: string; actual_percent: string; credit: { passed: boolean; value: { credit_percent?: string }; reasons: string[] } }[];
  defect_liability?: { active?: boolean; available?: boolean; reason?: string; basis?: string; nominal_expiry?: string; open_defects?: number; extended_by_open_defects?: boolean; days_remaining?: number; reasons?: string[] };
  retention?: { available?: boolean; reason?: string; retention_refund_due?: string; note?: string };
  closed_sections?: { phase: string; reason: string }[];
  timeline: { id: string; at: string; event_type: string; reason?: string }[];
};
type Dashboard = {
  metrics: Record<string, number>;
  phases: Record<string, number>;
  phase_order?: string[];
  districts: string[];
  scope?: ScopeInfo;
  register: { id: string; asset_code: string; name: string; phase: string; phase_label: string; phase_basis: string; service_state: string; condition_grade: string | null; district: string }[];
  actions: { id: string; title: string; detail: string; type?: string; asset_id?: string | null }[];
};
type AssetListItem = Passport["asset"];
type RegisterPage = { items: AssetListItem[]; total: number; returned: number; truncated: boolean; register_total: number; department_register_total?: number; scope?: ScopeInfo };
const PHASES: [string, string][] = [
  ["SANCTION_AND_CLEARANCE", "Sanction & Clearance"],
  ["EXECUTION", "Execution"],
  ["POST_COMPLETION", "Post-Completion"],
];

function label(value?: string) { return (value ?? "").replaceAll("_", " ").toLowerCase(); }
function Status({ value }: { value: string }) { const kind = value.includes("FAILED") || value.includes("OPEN") || value.includes("SRI") ? "attention" : value.includes("PASSED") || value.includes("VERIFIED") || value.includes("AWARDED") ? "good" : ""; return <span className={`status ${kind}`}>{label(value)}</span>; }
function Empty({ text }: { text: string }) { return <p className="empty">{text}</p>; }

export default function Workspace() {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [passport, setPassport] = useState<Passport | null>(null);
  const [assets, setAssets] = useState<AssetListItem[]>([]);
  const [registerTotal, setRegisterTotal] = useState(0);
  const [truncated, setTruncated] = useState(false);
  const [page, setPage] = useState("Dashboard");
  const [notice, setNotice] = useState("Choose a demo account. All workflow decisions are enforced by the API.");
  const [busy, setBusy] = useState(false);

  const read = useCallback(async (path: string, accessToken = token) => {
    const response = await fetch(`${api}${path}`, { headers: { Authorization: `Bearer ${accessToken}` } });
    if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail ?? "The service could not complete that request.");
    return response.json();
  }, [token]);

  // A refusal from the API is structured: it carries a machine code, an
  // explanation, remediation steps, and the section of the research record that
  // justifies the rule. Showing the whole thing is the point -- a bare "403
  // Forbidden" tells a demonstrator nothing, and a rule the team cannot explain
  // is a rule the team cannot defend.
  function refusal(error: unknown): string {
    const body = (error as { body?: { error?: { code?: string; message?: string; detail?: string; remediation?: string[]; reference?: string } } })?.body;
    const domain = body?.error;
    if (!domain?.message) return error instanceof Error ? error.message : "The service could not complete that request.";
    return [
      domain.code ? `${domain.code}: ${domain.message}` : domain.message,
      domain.detail,
      domain.remediation?.length ? `Next: ${domain.remediation.join(" ")}` : null,
      domain.reference ? `Source: ${domain.reference}` : null,
    ].filter(Boolean).join("\n");
  }
  const load = useCallback(async (accessToken = token) => {
    if (!accessToken) return;
    try {
      const [nextDashboard, register] = await Promise.all([
        read("/api/mvp/dashboard", accessToken),
        read("/api/mvp/assets", accessToken),
      ]) as [Dashboard, RegisterPage];
      setDashboard(nextDashboard);
      setAssets(register.items ?? []);
      setRegisterTotal(register.register_total ?? register.total ?? 0);
      setTruncated(Boolean(register.truncated));
      const items = register.items ?? [];
      if (items.length) {
        const selectedId = window.localStorage.getItem("btg-active-asset");
        const selected = items.find((item: { id: string }) => item.id === selectedId) ?? items[0];
        window.localStorage.setItem("btg-active-asset", selected.id);
        setPassport(await read(`/api/mvp/assets/${selected.id}/passport`, accessToken));
      }
    } catch (error) { setNotice(error instanceof Error ? error.message : "The API is unavailable."); }
  }, [read, token]);

  // Restore the session once. This intentionally does not depend on `load`,
  // which is re-created whenever the token changes; depending on it would
  // re-sign-in on every render cycle.
  useEffect(() => {
    const saved = window.localStorage.getItem("btg-session");
    if (!saved) return;
    try {
      const session = JSON.parse(saved) as { token: string; user: User };
      setToken(session.token); setUser(session.user); void load(session.token);
    } catch { window.localStorage.removeItem("btg-session"); }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
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
    if (!token) return null; setBusy(true);
    try {
      const response = await fetch(`${api}${path}`, { method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` }, body: JSON.stringify(body) });
      const parsed = await response.json().catch(() => null);
      if (!response.ok) {
        // Surface the whole structured refusal, not just its message.
        const failure = new Error(refusal({ body: parsed })) as Error & { body?: unknown };
        failure.body = parsed;
        throw failure;
      }
      setNotice(success); await load(token); return parsed;
    } catch (error) { setNotice(error instanceof Error ? error.message : "Action failed."); return null; } finally { setBusy(false); }
  }
  async function selectAsset(assetId: string) {
    if (!token) return;
    window.localStorage.setItem("btg-active-asset", assetId);
    try { setPassport(await read(`/api/mvp/assets/${assetId}/passport`)); setPage("Asset passport"); }
    catch (error) { setNotice(refusal({ body: await (error as { response?: Response })?.response?.clone?.().json?.().catch(() => null) })); }
  }
  function signOut() {
    window.localStorage.removeItem("btg-session");
    window.localStorage.removeItem("btg-active-asset");
    setToken(null); setUser(null); setPassport(null); setAssets([]); setDashboard(null);
    setRegisterTotal(0); setTruncated(false); setPage("Dashboard");
  }
  if (!user) return <Login busy={busy} notice={notice} signIn={signIn} />;

  const role = user.role; const gate = passport?.gates[0]; const defect = passport?.defects.find((item) => item.status !== "CLOSED"); const work = passport?.work_orders.find((item) => item.status !== "VERIFIED"); const metrics = dashboard?.metrics ?? {}; const canEngineer = role === "EXECUTIVE_ENGINEER" || role === "MANAGER"; const canQuality = canEngineer || role === "QUALITY_ENGINEER"; const canFinance = canEngineer || role === "FINANCE";
  const navByRole: Record<string, string[]> = {
    MANAGER: ["Dashboard", "Asset registry", "Asset passport", "Pre-construction", "Gates & tender", "Quality control", "Safety & maintenance", "Map & evidence", "Price variation", "Audit trail"],
    EXECUTIVE_ENGINEER: ["Dashboard", "Asset registry", "Asset passport", "Pre-construction", "Gates & tender", "Quality control", "Safety & maintenance", "Map & evidence", "Price variation", "Audit trail"],
    CHIEF_ENGINEER: ["Dashboard", "Asset registry", "Asset passport", "Pre-construction", "Gates & tender", "Price variation", "Audit trail"],
    SUPERINTENDING_ENGINEER: ["Dashboard", "Asset registry", "Asset passport", "Pre-construction", "Gates & tender", "Quality control", "Audit trail"],
    INSPECTOR: ["Dashboard", "Asset registry", "Asset passport", "Safety & maintenance", "Map & evidence", "Audit trail"],
    CONTRACTOR: ["Dashboard", "Asset registry", "Asset passport", "Gates & tender", "Safety & maintenance", "Map & evidence"],
    QUALITY_ENGINEER: ["Dashboard", "Asset registry", "Asset passport", "Quality control", "Audit trail"],
    FINANCE: ["Dashboard", "Asset registry", "Asset passport", "Price variation", "Audit trail"],
    AUDITOR: ["Dashboard", "Asset registry", "Asset passport", "Map & evidence", "Audit trail"],
  };
  const nav = navByRole[role] ?? ["Dashboard", "Asset passport"];
  return <main className="app-shell">
    <aside className="sidebar"><Link href="/" className="brand">Bridge<span>TheGap</span></Link><p className="eyebrow">R&B lifecycle operations</p><nav>{nav.map((item) => <button key={item} className={page === item ? "selected" : ""} onClick={() => setPage(item)}>{item}</button>)}</nav><div className="account"><p>{user.name}</p><small>{label(role)}</small><button onClick={signOut}>Switch role</button></div></aside>
    <section className="workspace">
      <AssetRail
        assets={assets}
        activeId={passport?.asset.id}
        total={registerTotal}
        truncated={truncated}
        scope={dashboard?.scope}
        onSelect={selectAsset}
      />
      <div className="workspace-main">
      <header className="topbar"><div><p className="eyebrow">Gujarat R&amp;B / synthetic demo portfolio</p><h1>{page}</h1></div><Status value={passport?.asset.service_state ?? "loading"} /></header><p className="notice" role="status">{notice}</p>
      {page === "Dashboard" && <><section className="metrics">{[["Registered bridges", metrics.assets], ["Active projects", metrics.active_projects], ["Open defects", metrics.open_defects], ["Blocked gates", metrics.failed_gates], ["Not open to traffic", metrics.restricted_or_closed]].map(([name, value]) => <article key={String(name)}><p>{name}</p><strong>{value ?? "-"}</strong></article>)}</section>{dashboard?.scope && <section className="panel scope-note"><p className="eyebrow">What you can see</p><h2>Your scope is enforced in the query, not in this page</h2><p>{dashboard.scope.explanation}</p><small>Signed in as {label(role)}. Every count above is counted over that scope only.</small></section>}<section className="panel phase-strip"><p className="eyebrow">Portfolio by lifecycle phase</p><div className="phase-row">{PHASES.map(([key, heading]) => <article key={key} className="phase-card"><p>{heading}</p><strong>{dashboard?.phases?.[key] ?? 0}</strong><small>bridges</small></article>)}</div><p className="phase-note">The department&apos;s own phases, not a generic asset taxonomy. Every bridge stays in the register for its whole life; it moves between phases and is never removed.</p></section><section className="split"><article className="panel"><p className="eyebrow">Action required</p><h2>Decisions awaiting an accountable owner</h2>{dashboard?.actions.length ? dashboard.actions.map((item) => <div className="queue" key={item.id}><b>{item.title}</b><p>{item.detail}</p></div>) : <Empty text="No actions are waiting for this seeded scenario." />}</article><AssetSummary passport={passport} /></section></>}
      {page === "Asset registry" && <AssetRegistry assets={assets} activeId={passport?.asset.id} onSelect={selectAsset} />}
      {page === "Asset passport" && <section className="split"><AssetSummary passport={passport} /><article className="panel"><p className="eyebrow">Bridge details</p><h2>Digital asset passport</h2><dl><dt>Route</dt><dd>{passport?.asset.bridge?.route ?? "-"}</dd><dt>Length</dt><dd>{passport?.asset.bridge?.length_m ?? "-"} m</dd><dt>Spans</dt><dd>{passport?.asset.bridge?.span_count ?? "-"}</dd><dt>Project</dt><dd>{passport?.project?.title ?? "-"}</dd></dl></article>{canEngineer && <PassportCreationForm busy={busy} onCreate={async (payload) => { const created = await command("/api/mvp/assets", payload, "Bridge passport, sanction-stage project, draft tender, and audit event created."); if (created && typeof created === "object" && "asset" in created) { const asset = (created as { asset: { id: string } }).asset; window.localStorage.setItem("btg-active-asset", asset.id); setPassport(await read(`/api/mvp/assets/${asset.id}/passport`)); } }} />}</section>}
      {page === "Pre-construction" && <section className="split"><article className="panel"><p className="eyebrow">Survey, feasibility & sanction</p><h2>Reports are records, not checklist text.</h2><p>PFR is used for missing-link projects; FSR/PPR is the feasibility stage; DPR is the sanction-ready technical package. AA and TS record administrative and technical approval.</p><div className="record-list">{passport?.reports.map((report) => <div key={report.id}><Status value={report.status} /><b>{report.type}</b><p>{report.reference}</p><small>{label(report.source_class)}</small></div>)}</div>{canEngineer && passport?.project && !passport.reports.some((report) => report.type === "PFR") && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/projects/${passport.project?.id}/reports`, { report_type: "PFR", reference: "PFR-2026-001: preliminary feasibility and need assessment", source_class: "NATIONAL_REFERENCE" }, "PFR recorded as a research-backed pre-construction report.")}>Record PFR</button>}{canEngineer && passport?.project && !passport.reports.some((report) => report.type === "FSR") && <button className="secondary" disabled={busy} onClick={() => void command(`/api/mvp/projects/${passport.project?.id}/reports`, { report_type: "FSR", reference: "FSR-2026-001: feasibility, options and cost basis", source_class: "NATIONAL_REFERENCE" }, "FSR recorded before commitment of major expenditure.")}>Record FSR</button>}{canEngineer && passport?.project && !passport.reports.some((report) => report.type === "DPR") && <button className="secondary" disabled={busy} onClick={() => void command(`/api/mvp/projects/${passport.project?.id}/reports`, { report_type: "DPR", reference: "DPR-2026-001: design basis, estimate and tender package", source_class: "NATIONAL_REFERENCE" }, "DPR recorded as the sanction-ready package.")}>Record DPR</button>}</article><article className="panel"><p className="eyebrow">Clearance register</p><h2>Known constraints have an owner and status.</h2><p>GAD, ESP, land-use, forest/wildlife and environmental clearance are recorded separately. The exact applicable set remains project-specific.</p><div className="record-list">{passport?.clearances.map((item) => <div key={item.id}><Status value={item.status} /><b>{label(item.type)}</b><p>{item.reference ?? "No reference recorded"}</p></div>)}</div>{canEngineer && passport?.project && !passport.clearances.some((item) => item.type === "GAD") && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/projects/${passport.project?.id}/clearances`, { clearance_type: "GAD", status: "SUBMITTED", reference: "GAD-REF-2026-001", source_class: "GUJARAT_VERIFIED" }, "GAD clearance registered; it remains visible until an accountable approval is recorded.")}>Register GAD clearance</button>}</article></section>}
      {page === "Gates & tender" && <section className="split"><article className="panel"><p className="eyebrow">Sanction &amp; clearance</p><h2>Land-readiness gate</h2>{gate ? <><Status value={gate.status} /><p>{gate.explanation}</p>{gate.missing_requirements.map((item) => <p className="missing" key={item}>{item}</p>)}</> : <Empty text="No gate evaluation recorded." />}{canEngineer && passport?.project && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/projects/${passport.project?.id}/land-readiness`, { possession_percent: 95, handover_reference: "SYN-LAND-MEMO-0142" }, "Land-readiness evidence recorded; the gate has been evaluated against 90% possession plus handover memorandum.")}>Record 95% possession + memo</button>}</article><article className="panel"><p className="eyebrow">Internal controlled tender room</p><h2>{passport?.tender?.number ?? "Tender not available"}</h2><Status value={passport?.tender?.status ?? "DRAFT"} />{passport?.tender?.tender_form && <p>Bidding form <b>{passport.tender.tender_form}</b>. Above the sourced ceiling, B-1 is mandatory.</p>}<p>Department-provisioned contractor access only. This prototype does not integrate with nProcure.</p>{passport?.bids?.length ? <div className="bids">{passport.bids.map((bid) => <div className="bid" key={bid.id}><b>{bid.own_bid ? "Your bid" : "Competing bid"}</b><span>{bid.redacted ? "Price not visible to other bidders" : `${bid.price_amount?.toLocaleString("en-IN")}`}</span><small>{bid.note ?? `Technical status: ${label(bid.technical_status)}`}</small></div>)}</div> : <Empty text="No bids have been submitted." />}{canEngineer && passport?.tender?.status === "DRAFT" && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/tenders/${passport.tender?.id}/publish`, {}, "Tender published after the land-readiness gate passed.")}>Publish tender</button>}{role === "CONTRACTOR" && passport?.tender?.status === "PUBLISHED" && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/tenders/${passport.tender?.id}/bids`, { technical_summary: "Controlled tender-room proposal with a documented execution approach, in-house PWL, and NABL-linked cube testing.", price_amount: 24500000 }, "Bid submitted for your contractor company.")}>Submit controlled bid</button>}{canEngineer && passport?.tender?.status === "PUBLISHED" && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/tenders/${passport.tender?.id}/award`, {}, "Lowest submitted controlled bid selected; contract created and the security deposit and performance bond computed from Gujarat's own percentages.")}>Evaluate and award</button>}</article></section>}
      {page === "Quality control" && <section className="split"><article className="panel"><p className="eyebrow">Execution evidence</p><h2>Raw samples drive the result</h2><p>Demo thresholds are labelled as synthetic configuration, never Gujarat acceptance criteria.</p>{canQuality && passport?.contract ? <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/contracts/${passport.contract?.id}/quality-tests`, { test_type: "Concrete cube strength", specified_value: 30, samples: [32, 31, 33] }, "Raw samples evaluated: calculated quality result recorded in the audit trail.")}>Evaluate quality samples</button> : <Empty text="Award the seeded tender first to create the execution contract." />}</article><article className="panel"><p className="eyebrow">Quality control pattern</p><h2>Evidence -&gt; calculation -&gt; review -&gt; ATR</h2><p>Tests retain raw values. A reviewer cannot silently replace a calculated result; an override must be auditable.</p></article></section>}
      {page === "Safety & maintenance" && <section className="split"><article className="panel"><p className="eyebrow">Post-completion inspection</p><h2>Condition, risk, and service state stay separate</h2><p>Gujarat grades supported: S, SRI, U. Safety restriction is an explicit service decision, not an invented condition grade.</p>{role === "INSPECTOR" && passport && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/assets/${passport.asset.id}/inspections`, { grade: "SRI", notes: "Deck joint drainage observation requires accountable rectification and reinspection.", risk_level: "SAFETY_REVIEW", atr_months: 3 }, "SRI inspection and ATR recorded.")}>Record SRI inspection</button>}</article><article className="panel"><p className="eyebrow">Maintenance maker-checker</p><h2>{defect ? defect.description : "No open defect"}</h2>{defect && <Status value={defect.status} />}{canEngineer && defect && !work && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/defects/${defect.id}/work-orders`, { decision_type: "REPAIR", description: "Repair drainage joint and submit rectification evidence for independent verification.", company_id: "00000000-0000-0000-0000-000000000020" }, "Work order approved and assigned.")}>Approve repair work</button>}{role === "CONTRACTOR" && work?.status === "APPROVED" && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/work-orders/${work.id}/rectification`, { notes: "Joint repaired; drainage path cleared. Evidence reference: SYN-RECT-142." }, "Rectification submitted; it now requires an independent verifier.")}>Submit rectification</button>}{(role === "INSPECTOR" || canEngineer) && work?.status === "VERIFICATION_PENDING" && <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/work-orders/${work.id}/verify`, {}, "Closure independently verified. The contractor could not verify its own work.")}>Independently verify closure</button>}</article></section>}
      {page === "Map & evidence" && <MapEvidence key={passport?.asset.id ?? "empty"} asset={passport?.asset ?? null} role={role} />}
      {page === "Price variation" && <article className="panel wide"><p className="eyebrow">Finance control</p><h2>Preserve the claim, calculation, variance, and policy version.</h2><p>Submitted value is never overwritten by calculated value.</p>{canFinance && passport?.contract ? <button className="primary" disabled={busy} onClick={() => void command(`/api/mvp/contracts/${passport.contract?.id}/price-variation`, { submitted_amount: 1280000, calculated_amount: 1254500 }, "Price-variation claim recorded with its variance and finance-review explanation.")}>Validate demo PV claim</button> : <Empty text="Award the tender first to activate the contract finance timeline." />}</article>}
      {page === "Audit trail" && <article className="panel wide"><p className="eyebrow">Immutable accountability trail</p><h2>Every material transition records actor, time, and reason.</h2><div className="timeline">{passport?.timeline.map((item) => <div key={item.id}><Status value={item.event_type} /><b>{label(item.event_type)}</b><p>{item.reason ?? "Recorded lifecycle decision."}</p><small>{new Date(item.at).toLocaleString()}</small></div>) ?? <Empty text="Loading lifecycle events..." />}</div></article>}
      </div>
    </section>
  </main>;
}

function Login({ busy, notice, signIn }: { busy: boolean; notice: string; signIn: (email: string) => Promise<void> }) { return <main className="login"><header><Link href="/">Bridge<span>TheGap</span></Link><small>Secure fictional demo</small></header><section><p className="eyebrow">Role-based lifecycle workspace</p><h1>Enter from the point where you hold accountability.</h1><p>Each account uses the same seeded password. The backend—not hidden UI controls—enforces authority.</p><div className="login-grid">{demoUsers.map(([name, email, description]) => <button key={email} disabled={busy} onClick={() => void signIn(email)}><b>{name}</b><span>{description}</span><small>{email}</small></button>)}</div><p className="notice">{notice}</p></section></main>; }
function AssetSummary({ passport }: { passport: Passport | null }) { return <article className="panel"><p className="eyebrow">Permanent asset identity</p><h2>{passport?.asset.name ?? "Loading bridge passport"}</h2><p>{passport?.asset.asset_code} / {passport?.asset.bridge?.route} / {passport?.asset.district}</p><div className="passport-meta"><span><b>Lifecycle</b><Status value={passport?.asset.lifecycle_state ?? "-"} /></span><span><b>Condition</b><Status value={passport?.asset.condition_grade ?? "-"} /></span></div></article>; }
function AssetRail({ assets, activeId, total, truncated, scope, onSelect }: { assets: AssetListItem[]; activeId?: string; total: number; truncated: boolean; scope?: ScopeInfo; onSelect: (id: string) => Promise<void> }) {
  const [query, setQuery] = useState("");
  const term = query.trim().toLowerCase();
  const visible = assets.filter((asset) => !term || `${asset.asset_code} ${asset.name} ${asset.district ?? ""}`.toLowerCase().includes(term));
  // Group by the DERIVED phase, not the stored label. A stored label can
  // disagree with the records behind it; the derived value cannot, so grouping
  // on the stored one would put a bridge in "Post-Completion" on the strength of
  // a column rather than on the fact that it was built.
  const groups = PHASES.map(([key, heading]) => ({ key, heading, rows: visible.filter((asset) => (asset.phase ?? asset.lifecycle_state) === key) }));
  const other = visible.filter((asset) => !PHASES.some(([key]) => key === (asset.phase ?? asset.lifecycle_state)));
  return <nav className="asset-rail" aria-label="Bridge register">
    <div className="rail-head">
      <p className="eyebrow">Register</p>
      <h2>All bridges</h2>
      <strong>{total} assets</strong>
      <input aria-label="Search the bridge register" placeholder="Search code, name, district" value={query} onChange={(event) => setQuery(event.target.value)} />
      {truncated && <p className="rail-warn">Showing {assets.length} of {total}. Narrow the search to reach the rest.</p>}
      {scope?.restricted && <details className="rail-scope" open>
        <summary>Scoped to your role — {scope.explanation}</summary>
        <ul>{scope.criteria?.map((item) => <li key={item}>{item}</li>)}</ul>
      </details>}
    </div>
    <div className="rail-list">
      {groups.map((group) => group.rows.length ? <section key={group.key}>
        <p className="rail-phase">{group.heading} <b>{group.rows.length}</b></p>
        {group.rows.map((asset) => <button key={asset.id} className={asset.id === activeId ? "rail-item active" : "rail-item"} onClick={() => void onSelect(asset.id)}>
          <b>{asset.name}</b>
          <small>{asset.asset_code}</small>
          <small>{asset.district}{asset.service_state !== "OPEN" ? ` · ${label(asset.service_state)}` : ""}</small>
        </button>)}
      </section> : null)}
      {other.length ? <section><p className="rail-phase">Other <b>{other.length}</b></p>{other.map((asset) => <button key={asset.id} className={asset.id === activeId ? "rail-item active" : "rail-item"} onClick={() => void onSelect(asset.id)}><b>{asset.name}</b><small>{asset.asset_code}</small></button>)}</section> : null}
      {!visible.length && <div className="empty">
        <p>{term ? "No bridge matches that search." : "No bridge is currently in your scope."}</p>
        {!term && scope?.criteria?.length ? <ul className="scope-criteria">{scope.criteria.map((item) => <li key={item}>{item}</li>)}</ul> : null}
      </div>}
    </div>
  </nav>;
}

function AssetRegistry({ assets, activeId, onSelect }: { assets: AssetListItem[]; activeId?: string; onSelect: (id: string) => Promise<void> }) {
  const [query, setQuery] = useState("");
  const [service, setService] = useState("ALL");
  const visible = assets.filter((asset) => (service === "ALL" || asset.service_state === service) && (asset.asset_code + " " + asset.name + " " + asset.district).toLowerCase().includes(query.toLowerCase()));
  return <article className="panel wide registry"><div className="registry-heading"><div><p className="eyebrow">Portfolio register</p><h2>All bridge assets</h2><p>Create a passport once; select it whenever you need its lifecycle detail. No bridge is replaced or hidden when a new one is created.</p></div><strong>{assets.length} assets</strong></div><div className="registry-filters"><label>Search<input placeholder="Code, bridge name, district" value={query} onChange={(event) => setQuery(event.target.value)} /></label><label>Service state<select value={service} onChange={(event) => setService(event.target.value)}><option value="ALL">All states</option><option value="OPEN">Open</option><option value="RESTRICTED">Restricted</option><option value="CLOSED">Closed</option></select></label></div>{visible.length ? <div className="registry-table"><div className="registry-row registry-head"><span>Asset</span><span>Location</span><span>Lifecycle</span><span>Service</span><span /></div>{visible.map((asset) => <div className="registry-row" key={asset.id}><div><b>{asset.name}</b><small>{asset.asset_code} · {asset.bridge?.class?.replaceAll("_", " ").toLowerCase()}</small></div><span>{asset.district}<small>{asset.bridge?.route ?? "Route not recorded"}</small></span><Status value={asset.phase ?? asset.lifecycle_state} /><Status value={asset.service_state} /><button className={asset.id === activeId ? "secondary" : "primary"} onClick={() => void onSelect(asset.id)}>{asset.id === activeId ? "Viewing" : "Open passport"}</button></div>)}</div> : <Empty text="No bridge matches the selected search and filter." />}</article>;
}

type PassportInput = {
  asset_code: string; canonical_name: string; district: string; bridge_class: string; route_name: string;
  chainage_km: number; length_m: number; span_count: number; project_title: string; project_type: string; estimate_amount: number; latitude: number; longitude: number;
};
function PassportCreationForm({ busy, onCreate }: { busy: boolean; onCreate: (payload: PassportInput) => Promise<void> }) {
  const [form, setForm] = useState<PassportInput>({ asset_code: "", canonical_name: "", district: "Vadodara", bridge_class: "MINOR_BRIDGE", route_name: "", chainage_km: 0, length_m: 0, span_count: 1, project_title: "", project_type: "NEW_CONSTRUCTION", estimate_amount: 0, latitude: 0, longitude: 0 });
  function set(name: keyof PassportInput, value: string) {
    const numeric = ["chainage_km", "length_m", "span_count", "estimate_amount", "latitude", "longitude"].includes(name);
    setForm((current) => ({ ...current, [name]: numeric ? Number(value) : value }) as PassportInput);
  }
  return <article className="panel passport-form"><p className="eyebrow">Executive Engineer action</p><h2>Initiate a bridge project</h2><p>A passport is permanent from project initiation. The new project begins at Sanction & Clearance; it cannot publish its tender until gate evidence passes.</p><form onSubmit={(event) => { event.preventDefault(); void onCreate(form); }}>
    <label>Asset code <small>Optional — generated by system when blank</small><input pattern="[A-Z0-9-]{6,64}" placeholder="BRG-GJ-VAD-2026-A1B2C3" value={form.asset_code} onChange={(event) => set("asset_code", event.target.value.toUpperCase())} /></label>
    <label>Bridge name<input required minLength={5} placeholder="Orsang River Bridge" value={form.canonical_name} onChange={(event) => set("canonical_name", event.target.value)} /></label>
    <label>District<input required value={form.district} onChange={(event) => set("district", event.target.value)} /></label>
    <label>Bridge class<select value={form.bridge_class} onChange={(event) => set("bridge_class", event.target.value)}><option value="MAJOR_BRIDGE">Major bridge</option><option value="MINOR_BRIDGE">Minor bridge</option><option value="ROB">Road over bridge</option><option value="RUB">Road under bridge</option><option value="CULVERT">Culvert</option></select></label>
    <label>Route<input required minLength={3} placeholder="Dabhoi - Bodeli Road" value={form.route_name} onChange={(event) => set("route_name", event.target.value)} /></label>
    <label>Latitude<input required min="-90" max="90" step="0.000001" type="number" value={form.latitude || ""} onChange={(event) => set("latitude", event.target.value)} /></label>
    <label>Longitude<input required min="-180" max="180" step="0.000001" type="number" value={form.longitude || ""} onChange={(event) => set("longitude", event.target.value)} /></label>
    <label>Chainage (km)<input required min="0" step="0.001" type="number" value={form.chainage_km || ""} onChange={(event) => set("chainage_km", event.target.value)} /></label>
    <label>Length (m)<input required min="0.01" step="0.01" type="number" value={form.length_m || ""} onChange={(event) => set("length_m", event.target.value)} /></label>
    <label>Number of spans<input required min="1" max="100" type="number" value={form.span_count} onChange={(event) => set("span_count", event.target.value)} /></label>
    <label>Project title<input required minLength={5} placeholder="Orsang River Bridge Renewal" value={form.project_title} onChange={(event) => set("project_title", event.target.value)} /></label>
    <label>Project type<select value={form.project_type} onChange={(event) => set("project_type", event.target.value)}><option value="NEW_CONSTRUCTION">New construction</option><option value="REHABILITATION">Rehabilitation</option><option value="REPLACEMENT">Replacement</option></select></label>
    <label>Estimate (INR)<input required min="1" step="0.01" type="number" value={form.estimate_amount || ""} onChange={(event) => set("estimate_amount", event.target.value)} /></label>
    <button className="primary" disabled={busy}>Create passport and project</button>
  </form></article>;
}

function MapEvidence({ asset, role }: { asset: Passport["asset"] | null; role: string }) {
  const storageKey = asset ? `btg-local-evidence-${asset.id}` : "btg-local-evidence";
  const [photos, setPhotos] = useState<{ type: string; name: string; data: string; at: string }[]>(() => {
    if (typeof window === "undefined") return [];
    try { return JSON.parse(window.localStorage.getItem(storageKey) ?? "[]"); } catch { return []; }
  });
  function addPhoto(event: ChangeEvent<HTMLInputElement>, type: string) {
    const file = event.target.files?.[0];
    if (!file || !asset) return;
    const reader = new FileReader();
    reader.onload = () => {
      const next = [...photos.filter((item) => item.type !== type), { type, name: file.name, data: String(reader.result), at: new Date().toISOString() }];
      setPhotos(next); window.localStorage.setItem(storageKey, JSON.stringify(next));
    };
    reader.readAsDataURL(file); event.target.value = "";
  }
  const lat = asset?.latitude; const lng = asset?.longitude;
  const mapUrl = lat !== undefined && lng !== undefined ? `https://www.openstreetmap.org/export/embed.html?bbox=${lng - 0.02}%2C${lat - 0.015}%2C${lng + 0.02}%2C${lat + 0.015}&layer=mapnik&marker=${lat}%2C${lng}` : null;
  const mayAdd = (type: string) => type === "BEFORE" ? role === "INSPECTOR" : role === "CONTRACTOR";
  return <section className="split map-evidence"><article className="panel map-panel"><p className="eyebrow">Asset location</p><h2>{asset?.name ?? "Select an asset"}</h2>{mapUrl ? <><iframe title="OpenStreetMap asset location" src={mapUrl} loading="lazy" /><p>{lat?.toFixed(6)}, {lng?.toFixed(6)}. Location is user-entered demo data and must be verified before production use.</p></> : <Empty text="No latitude/longitude is recorded for this bridge yet. Add verified coordinates when creating its passport." />}</article><article className="panel"><p className="eyebrow">Field evidence pack</p><h2>Before / after rectification</h2><p>Local-demo only: before evidence is added by the Inspector; after evidence is added by the Contractor. All roles shown here can view available evidence.</p><div className="evidence-grid">{["BEFORE", "AFTER"].map((type) => { const photo = photos.find((item) => item.type === type); return <label className="photo-slot" key={type}>{photo ? <img src={photo.data} alt={`${type.toLowerCase()} evidence: ${photo.name}`} /> : <span>{type} PHOTO</span>}{mayAdd(type) ? <input accept="image/*" type="file" onChange={(event) => addPhoto(event, type)} /> : <small>{photo ? `${photo.name} • ${new Date(photo.at).toLocaleString()}` : `Only the ${type === "BEFORE" ? "Inspector" : "Contractor"} can add this evidence.`}</small>}<small>{photo && mayAdd(type) ? `${photo.name} • ${new Date(photo.at).toLocaleString()}` : null}</small></label>; })}</div></article></section>;
}
