import type { ActiveWellData } from '../types/domain'

/** Demonstration-only synthetic Active Well data; ready to be replaced by API responses. */
export const activeWellDemoData: ActiveWellData = {
  well: { wellId: 'DEMO-AROH-01', name: 'AROH-01', currentDepth: 2930, formation: 'Tipam Sand', status: 'Drilling', riskLevel: 'elevated', location: 'Demo Pad A', rop: 31.8, updatedAt: '18 sec ago' },
  risk: { wellId: 'DEMO-AROH-01', riskScore: 74, severity: 'elevated', eventType: 'Potential loss zone', riskInterval: '2,960–3,020 m', confidence: 78, evidenceCount: 3 },
  depthTimeline: { currentDepth: 2930, riskStartDepth: 2960, riskEndDepth: 3020, points: [{ depth: 2820, riskScore: 14 }, { depth: 2870, riskScore: 18 }, { depth: 2930, riskScore: 32 }, { depth: 2960, riskScore: 74 }, { depth: 2990, riskScore: 88 }, { depth: 3020, riskScore: 79 }, { depth: 3060, riskScore: 42 }] },
  reasons: [
    { label: 'Formation similarity', detail: 'All supporting synthetic offsets encountered the same mapped Tipam Sand interval.', strength: 'high' },
    { label: 'Depth similarity', detail: 'Historical events cluster within 30–90 m ahead of the current depth.', strength: 'high' },
    { label: 'Historical events', detail: 'Three synthetic offset records show loss-related events in the correlated interval.', strength: 'high' },
    { label: 'Drilling-pattern similarity', detail: 'ROP and torque trend patterns are comparable to the demonstration offset signatures.', strength: 'moderate' },
  ],
  offsetEvidence: [
    { wellId: 'DEMO-OFF-17', depth: 2984, formation: 'Tipam Sand', historicalEvent: 'Partial circulation loss', severity: 'elevated', outcome: 'Losses stabilized after reducing flow and monitoring returns.' },
    { wellId: 'DEMO-OFF-22', depth: 3008, formation: 'Tipam Sand', historicalEvent: 'Loss zone indication', severity: 'critical', outcome: 'Required loss-control material treatment in this synthetic record.' },
    { wellId: 'DEMO-OFF-09', depth: 2972, formation: 'Tipam Sand', historicalEvent: 'Return flow reduction', severity: 'watch', outcome: 'Returns recovered after staged circulation and verification.' },
  ],
  parameters: [
    { label: 'ROP', value: 31.8, unit: 'm/hr', trend: 'rising', detail: 'Above prior 30 min average' },
    { label: 'Torque', value: 22.4, unit: 'kN·m', trend: 'rising', detail: 'Gradual upward trend' },
    { label: 'WOB', value: 14.2, unit: 't', trend: 'stable', detail: 'Within synthetic operating band' },
    { label: 'RPM', value: 81, unit: 'rpm', trend: 'stable', detail: 'Stable over last 15 min' },
    { label: 'Flow rate', value: 2180, unit: 'L/min', trend: 'stable', detail: 'No synthetic variance flagged' },
  ],
  recentEvents: [
    { eventId: 'DEMO-EVT-201', wellId: 'DEMO-AROH-01', timestamp: '09:42 UTC', eventType: 'Risk interval approaching', severity: 'elevated', depth: 2930, formation: 'Tipam Sand', summary: 'Current depth is 30 m before the predicted synthetic risk interval.' },
    { eventId: 'DEMO-EVT-200', wellId: 'DEMO-AROH-01', timestamp: '09:35 UTC', eventType: 'Torque trend update', severity: 'watch', depth: 2918, formation: 'Tipam Sand', summary: 'Torque trend increased relative to the prior demonstration window.' },
    { eventId: 'DEMO-EVT-199', wellId: 'DEMO-AROH-01', timestamp: '09:21 UTC', eventType: 'Formation correlation updated', severity: 'normal', depth: 2891, formation: 'Tipam Sand', summary: 'Synthetic correlation aligned the current interval with three offset records.' },
  ],
  recommendedAction: { title: 'Prepare for a potential loss-related interval', action: 'Verify pit-volume and flow-out monitoring readiness; review the offset outcomes before entering 2,960 m.', rationale: 'This is based on synthetic formation/depth correlation and three synthetic historical offset records. It is not an autonomous drilling instruction.' },
}
