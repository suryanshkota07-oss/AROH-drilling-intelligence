import { Activity, Database, ShieldAlert, TowerControl } from 'lucide-react'
import { ActiveWellSummary } from '../components/dashboard/ActiveWellSummary'
import { ActiveWellsTable } from '../components/dashboard/ActiveWellsTable'
import { RecentEvents } from '../components/dashboard/RecentEvents'
import { RiskOverview } from '../components/dashboard/RiskOverview'
import { SummaryCard } from '../components/dashboard/SummaryCard'
import { commandCenterDemoData } from '../data/commandCenterDemo'

export function CommandCenterPage() {
  const { activeWells, recentEvents, risks, systemHealth } = commandCenterDemoData
  const highRiskWells = risks.filter(({ severity }) => severity === 'elevated' || severity === 'critical').length
  return <div className="command-center"><section className="page-intro"><div><p className="eyebrow">LIVE OVERVIEW</p><h2>Drilling operations at a glance</h2><p>Situation, risk, and supporting context for the demonstration fleet.</p></div><span className="last-updated">Telemetry refresh: synthetic stream</span></section><section className="summary-grid" aria-label="Operational summary"><SummaryCard label="Total active wells" value={String(activeWells.length)} detail="Across 3 demonstration pads" icon={TowerControl} tone="normal" /><SummaryCard label="High-risk wells" value={String(highRiskWells)} detail="Elevated or critical risk state" icon={ShieldAlert} tone="critical" /><SummaryCard label="Active alerts" value={String(risks.length)} detail="Require engineer review" icon={Activity} tone="elevated" /><SummaryCard label="Data / system health" value={systemHealth.telemetry} detail={`${systemHealth.connectedSources}/${systemHealth.totalSources} sources · ${systemHealth.dataFreshness}`} icon={Database} tone="normal" /></section><section className="command-center__primary-grid"><ActiveWellSummary well={activeWells[0]} /><RiskOverview risks={risks} wells={activeWells} /></section><section className="command-center__secondary-grid"><ActiveWellsTable wells={activeWells} /><RecentEvents events={recentEvents} /></section></div>
}
