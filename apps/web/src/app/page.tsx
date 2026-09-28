const stages = [
  ["01", "Pre-construction", "Need, approvals, tender and award"],
  ["02", "Construction", "Milestones, quality checks and handover"],
  ["03", "In service", "Inspection, action, work and verification"],
];

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 px-6 py-12 text-slate-100">
      <section className="mx-auto max-w-6xl">
        <p className="text-sm font-semibold tracking-[.2em] text-cyan-300">GUJARAT R&B · DEMO WORKFLOW</p>
        <div className="mt-8 flex flex-col gap-8 md:flex-row md:items-end md:justify-between">
          <div>
            <h1 className="max-w-3xl text-4xl font-semibold tracking-tight md:text-6xl">Bridge lifecycle, with every decision connected.</h1>
            <p className="mt-5 max-w-2xl text-lg text-slate-300">A fictional-data prototype for accountability from project need through verified maintenance closure.</p>
          </div>
          <button className="rounded-lg bg-cyan-300 px-5 py-3 font-semibold text-slate-950">Open demo workspace</button>
        </div>
        <div className="mt-12 grid gap-4 md:grid-cols-3">
          {stages.map(([number, title, description]) => <article key={number} className="rounded-xl border border-slate-700 bg-slate-900 p-6"><p className="text-sm font-bold text-cyan-300">{number}</p><h2 className="mt-8 text-2xl font-semibold">{title}</h2><p className="mt-3 text-slate-300">{description}</p></article>)}
        </div>
        <section className="mt-8 rounded-xl border border-slate-700 bg-slate-900/60 p-6"><h2 className="text-xl font-semibold">Prototype boundary</h2><p className="mt-2 text-slate-300">No live government data, GIS, payments, uploads, or structural-safety automation. Every decision is attributable and auditable.</p></section>
      </section>
    </main>
  );
}
