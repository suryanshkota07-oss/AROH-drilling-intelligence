import { ActiveWellEvents } from '../components/activeWell/ActiveWellEvents'
import { DepthRiskTimeline } from '../components/activeWell/DepthRiskTimeline'
import { DrillingParameters } from '../components/activeWell/DrillingParameters'
import { OffsetEvidence } from '../components/activeWell/OffsetEvidence'
import { RecommendedAction } from '../components/activeWell/RecommendedAction'
import { RiskAheadPanel } from '../components/activeWell/RiskAheadPanel'
import { WellHeader } from '../components/activeWell/WellHeader'
import { WhyThisRisk } from '../components/activeWell/WhyThisRisk'
import { activeWellDemoData } from '../data/activeWellDemo'

export function ActiveWellPage() { const data = activeWellDemoData; return <div className="active-well-page"><WellHeader well={data.well} /><RiskAheadPanel risk={data.risk} well={data.well} /><section className="active-well-page__timeline-grid"><DepthRiskTimeline timeline={data.depthTimeline} /><RecommendedAction recommendation={data.recommendedAction} /></section><section className="active-well-page__evidence-grid"><WhyThisRisk reasons={data.reasons} /><OffsetEvidence evidence={data.offsetEvidence} /></section><DrillingParameters parameters={data.parameters} /><ActiveWellEvents events={data.recentEvents} /></div> }
